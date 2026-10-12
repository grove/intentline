"""Operator-only sample probes; never authenticate an environment or run a model."""

import errno
import os
import socket
import stat


def visible_canary(path, expected):
    """Read an operator-created nonsecret positive sentinel, preserving no contents."""
    if (not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_NONBLOCK")
            or not isinstance(expected, bytes) or len(expected) > 256):
        return False
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        try:
            info = os.fstat(fd)
            return (stat.S_ISREG(info.st_mode) and info.st_nlink == 1
                    and info.st_size == len(expected) and os.read(fd, 257) == expected)
        finally:
            os.close(fd)
    except OSError:
        return False


def forbidden_canary(path):
    """Try to open a nonsecret private sentinel; missing/wrong paths are unresolved."""
    if not hasattr(os, "O_NONBLOCK"):
        return False
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
        os.close(fd)
    except OSError as error:
        return error.errno in (errno.EACCES, errno.EPERM)
    return False


def network_canary(ip, port):
    """Probe one authorized operator-owned TCP endpoint; timeout/refusal is unresolved."""
    if type(port) is not int or not 1 <= port <= 65535:
        return False
    try:
        socket.inet_pton(socket.AF_INET, ip)
    except (OSError, TypeError, ValueError):
        return False
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.settimeout(1)
            connection.connect((ip, port))
    except OSError as error:
        return error.errno in (errno.EACCES, errno.EPERM)
    except (TypeError, ValueError):
        return False
    return False


def connected_app_canary(dispatch):
    """Use a real host tool-dispatch callback, without fetching any real app data."""
    if not callable(dispatch):
        return False
    try:
        dispatch({"resource": "intentline-access-06-nonsecret-sentinel", "read_only": True})
    except PermissionError:
        return True
    except Exception:
        return False
    return False


def summary(positive, forbidden, network, connected_app):
    """Sample denials plus host evidence are necessary; this code never qualifies a host."""
    values = [positive, *forbidden, network, connected_app]
    return {"sample_probes_passed": bool(forbidden) and all(value is True for value in values),
            "host_qualified": False,
            "scope": "operator-canary-samples-only"}
