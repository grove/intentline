"""Descriptor-relative, no-follow POSIX storage; unsupported hosts fail closed."""
import contextlib
import os
from pathlib import Path
import stat
import uuid

from .errors import IntentlineError

MAX_FILE = 2 * 1024 * 1024


def absolute(path):
    raw = os.fspath(path)
    if (not raw or any(ord(c) < 32 for c in raw) or '\\' in raw
            or '//' in raw or any(p in ('.', '..') for p in raw.split('/'))):
        raise IntentlineError('Ambiguous, Windows-style, or traversing path')
    return Path(os.path.abspath(raw))


def capability():
    if os.name != 'posix' or not hasattr(os, 'O_NOFOLLOW') or os.open not in os.supports_dir_fd:
        raise IntentlineError('Secure descriptor-relative filesystem capability unavailable on this host', 3)


class Directory:
    def __init__(self, path, create=False):
        capability()
        self.path = absolute(path)
        fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
        try:
            for part in self.path.parts[1:]:
                if create:
                    try:
                        os.mkdir(part, 0o700, dir_fd=fd)
                    except FileExistsError:
                        pass
                new = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                os.close(fd)
                fd = new
            self.fd = fd
            self.identity = os.fstat(fd)
        except OSError as exc:
            os.close(fd)
            raise IntentlineError(f'Unsafe or unavailable directory: {self.path}: {exc}', 3) from exc

    def __enter__(self):
        return self

    def __exit__(self, *args):
        os.close(self.fd)

    def check(self):
        with Directory(self.path) as now:
            if (now.identity.st_dev, now.identity.st_ino) != (self.identity.st_dev, self.identity.st_ino):
                raise IntentlineError('Directory identity changed during operation', 3)

    @staticmethod
    def name(name):
        if not name or name in ('.', '..') or '/' in name or '\\' in name or '\x00' in name:
            raise IntentlineError('Unsafe record filename', 3)

    def read(self, name, limit=MAX_FILE):
        self.name(name)
        try:
            fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=self.fd)
        except FileNotFoundError:
            raise
        except OSError as exc:
            raise IntentlineError(f'Unsafe file: {name}', 3) from exc
        try:
            before = os.fstat(fd)
            if not stat.S_ISREG(before.st_mode) or before.st_size > limit:
                raise IntentlineError(f'Not a bounded regular file: {name}')
            chunks = []
            remaining = limit + 1
            while remaining:
                chunk = os.read(fd, min(65536, remaining))
                if not chunk:
                    break
                chunks.append(chunk)
                remaining -= len(chunk)
            data = b''.join(chunks)
            after = os.fstat(fd)
            current = os.stat(name, dir_fd=self.fd, follow_symlinks=False)
            identity = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
            if len(data) > limit or identity(before) != identity(after) or identity(after) != identity(current):
                raise IntentlineError('File changed during capture', 3)
            self.check()
            return data, {'device': before.st_dev, 'inode': before.st_ino}
        finally:
            os.close(fd)

    def write(self, name, data, replace=False):
        self.name(name)
        self.check()
        temp = '.stage-' + uuid.uuid4().hex
        fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=self.fd)
        try:
            with os.fdopen(fd, 'wb') as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            self.check()
            if replace:
                # Locking coordinates Intentline writers; hostile owner edits are outside this boundary.
                os.replace(temp, name, src_dir_fd=self.fd, dst_dir_fd=self.fd)
            else:
                os.link(temp, name, src_dir_fd=self.fd, dst_dir_fd=self.fd, follow_symlinks=False)
            os.fsync(self.fd)
        finally:
            with contextlib.suppress(FileNotFoundError):
                os.unlink(temp, dir_fd=self.fd)

    @contextlib.contextmanager
    def lock(self):
        try:
            fd = os.open('.writer.lock', os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=self.fd)
        except FileExistsError as exc:
            raise IntentlineError('Conflicting writer or interrupted operation; inspect .writer.lock before recovery', 3) from exc
        try:
            os.write(fd, str(os.getpid()).encode())
            os.fsync(fd)
            yield
            self.check()
        finally:
            os.close(fd)
            os.unlink('.writer.lock', dir_fd=self.fd)


def read_file(path):
    path = absolute(path)
    with Directory(path.parent) as parent:
        return parent.read(path.name)


def text(data):
    if b'\0' in data:
        raise IntentlineError('NUL/binary input is unsupported')
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise IntentlineError('Input must be exact UTF-8') from exc
