# Windows storage feasibility, 2026-10-12

Verdict for 0.3: NO-GO for secure record storage. This is a qualification decision,
not a claim that a safe Win32 backend is impossible. The existing explicit exit-3
refusal remains. CLI dispatch now checks capability before parsing record paths,
so every record command refuses without creating files, even for device/ADS/UNC,
traversal or other ambiguous Windows inputs. Help and installation remain supported.

The POSIX backend uses descriptor-relative no-follow operations on every parent,
regular bounded reads with identity rechecks, owner-only output, cooperative
exclusive locks, synced sibling stages and create-vs-replace atomic publication.
No equivalent complete Win32 adapter, private ACL gate, relative-handle parent
walk, lock/publication recovery or attack corpus is implemented or independently
qualified. Path.resolve/is_symlink and default ACLs cannot stand in for those gates.

Win32 APIs can provide useful primitives: CreateFileW supports directory handles
with FILE_FLAG_BACKUP_SEMANTICS and opening a reparse point with
FILE_FLAG_OPEN_REPARSE_POINT; a default security descriptor is not an explicit
owner-only boundary. See Microsoft's [CreateFileW specification](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
and [file security rights](https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights).
These flags alone do not establish safe traversal of all parents.

The committed actual-Windows feasibility test opens an ordinary temporary file
through two native handles, compares volume/file-index identity, checks its reparse
tag and opens a directory handle. It uses ctypes, no dependencies or inference.
[Handle information](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getfileinformationbyhandle)
is a narrow identity observation, not atomic publication, ACL or junction security.
Windows naming/namespace hazards include reserved devices, trailing dots/spaces,
ADS, UNC/device namespaces and case collisions; see [Microsoft's naming rules](https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file).

On macOS/Linux the native API probe is explicitly skipped; the blanket capability
refusal regression runs everywhere. Exact-head Windows CI provides the actual
probe/refusal observations, reported separately in the 0.3 handoff/scorecard.
No privileged junction mutation, ACL adversary, concurrent native writer or Win32
interrupted-publication test is claimed. The smallest next step toward support
is a separately scoped handle-relative backend with private ACL enforcement and
real Windows swap/junction/interrupt controls. Unsupported capability is safer
than an unqualified prototype and is an allowed PR-06 outcome in the 0.3 plan.
