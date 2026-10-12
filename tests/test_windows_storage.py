"""Real Windows feasibility observations; no secure backend is qualified."""
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest

from intentline.cli import main


class WindowsStorage(unittest.TestCase):
    def test_unavailable_capability_refuses_every_record_command_before_io(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);work=str(root/'work');out=str(root/'out')
            commands=[['prepare','--source','C:\\CON','--root',str(root),'--out',out],
                      ['propose','--work',work,'--draft','C:\\draft.json'],
                      ['review','--work',work],['approval-request','--work',work],
                      ['check','--work',work],['status','--work',work],['render','--work',work],
                      ['audit-record','--work',work,'--report','C:\\audit.json'],
                      ['adopt','--work',work,'--expected-contract-sha256','0'*64,'--approval-file','C:\\approval.json'],
                      ['amend-source','--work',work,'--amendment','C:\\amendment.md','--root',str(root),'--out',out,'--expected-contract-sha256','0'*64],
                      ['reconcile','--work',work,'--draft','C:\\draft.json','--continuity','C:\\mapping.json'],
                      ['export','--work',work,'--format','proofline-native','--out',out],
                      ['inspect-native','--bundle',out]]
            with patch('os.name','nt'):
                for command in commands:
                    stdout=io.StringIO()
                    with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(io.StringIO()):
                        self.assertEqual(main(command+['--json']),3,command)
                    self.assertEqual(json.loads(stdout.getvalue())['error']['code'],3)
            self.assertEqual(list(root.iterdir()),[])

    @unittest.skipUnless(os.name=='nt','Actual Win32 handle/API feasibility probe runs on Windows CI')
    def test_real_win32_regular_handles_identity_and_reparse_tag(self):
        import ctypes
        from ctypes import wintypes
        kernel=ctypes.WinDLL('kernel32',use_last_error=True)
        create=kernel.CreateFileW;create.argtypes=[wintypes.LPCWSTR,wintypes.DWORD,wintypes.DWORD,wintypes.LPVOID,wintypes.DWORD,wintypes.DWORD,wintypes.HANDLE];create.restype=wintypes.HANDLE
        class Information(ctypes.Structure):
            _fields_=[('attributes',wintypes.DWORD),('created',wintypes.FILETIME),('accessed',wintypes.FILETIME),('written',wintypes.FILETIME),('volume',wintypes.DWORD),('size_high',wintypes.DWORD),('size_low',wintypes.DWORD),('links',wintypes.DWORD),('index_high',wintypes.DWORD),('index_low',wintypes.DWORD)]
        class Tag(ctypes.Structure):
            _fields_=[('attributes',wintypes.DWORD),('reparse_tag',wintypes.DWORD)]
        info=kernel.GetFileInformationByHandle;info.argtypes=[wintypes.HANDLE,ctypes.POINTER(Information)];info.restype=wintypes.BOOL
        tag=kernel.GetFileInformationByHandleEx;tag.argtypes=[wintypes.HANDLE,ctypes.c_int,wintypes.LPVOID,wintypes.DWORD];tag.restype=wintypes.BOOL
        close=kernel.CloseHandle;close.argtypes=[wintypes.HANDLE];close.restype=wintypes.BOOL
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'probe.txt';path.write_bytes(b'Authored ordinary handle observation, not secure storage\n')
            handles=[]
            try:
                for _ in range(2):
                    handle=create(str(path),0x80,7,None,3,0x00200000,None)
                    if handle==ctypes.c_void_p(-1).value:raise ctypes.WinError(ctypes.get_last_error())
                    handles.append(handle)
                records=[]
                for handle in handles:
                    record=Information()
                    if not info(handle,ctypes.byref(record)):raise ctypes.WinError(ctypes.get_last_error())
                    attributes=Tag()
                    if not tag(handle,9,ctypes.byref(attributes),ctypes.sizeof(attributes)):raise ctypes.WinError(ctypes.get_last_error())
                    self.assertFalse(attributes.attributes & 0x400)
                    records.append((record.volume,record.index_high,record.index_low))
                self.assertEqual(records[0],records[1])
                directory_handle=create(directory,0x80,7,None,3,0x02000000|0x00200000,None)
                if directory_handle==ctypes.c_void_p(-1).value:raise ctypes.WinError(ctypes.get_last_error())
                handles.append(directory_handle)
            finally:
                for handle in handles:close(handle)
