"""
ENHANCED SECURE DELETE  with Improved Path Detection
"""

import os
import shutil
import secrets
import logging
import platform
import tempfile
import threading
import time
from pathlib import Path
from typing import Callable, Optional, Tuple, List

LOG = logging.getLogger("secure_delete")
LOG.addHandler(logging.NullHandler())

class ShredError(RuntimeError):
    pass

class OperationInterrupted(Exception):
    pass

class AdvancedShredder:
    PATTERNS = {
        "simple_random": lambda size: os.urandom(size),
        "us_dod_5220": [
            lambda size: b'\x00' * size,
            lambda size: b'\xFF' * size,
            lambda size: os.urandom(size)
        ],
        "gutmann": [
            lambda size: b'\x00' * size,
            lambda size: b'\xFF' * size,
            lambda size: b'\xAA' * size,
            lambda size: b'\x55' * size,
            lambda size: b'\x92' * size,
            lambda size: b'\x49' * size,
            lambda size: os.urandom(size)
        ],
        "rcmp_tssit_opsii": [
            lambda size: b'\x00' * size,
            lambda size: b'\xFF' * size,
            lambda size: b'\x96' * size,
            lambda size: os.urandom(size)
        ]
    }
    
    @staticmethod
    def get_wipe_method(name: str, passes: int) -> List[callable]:
        safe_passes = min(passes, 7)
        
        if name == "gutmann":
            return AdvancedShredder.PATTERNS["gutmann"][:safe_passes]
        elif name == "us_dod":
            return AdvancedShredder.PATTERNS["us_dod_5220"][:safe_passes]
        elif name == "rcmp":
            return AdvancedShredder.PATTERNS["rcmp_tssit_opsii"][:safe_passes]
        else:
            return [AdvancedShredder.PATTERNS["simple_random"]] * safe_passes

def _secure_rename(path: Path, iterations: int = 3) -> Path:
    current_path = path
    for i in range(iterations):
        rand_name = "~" + secrets.token_hex(16) + ".tmp"
        new_path = current_path.parent / rand_name
        try:
            os.replace(current_path, new_path)
            current_path = new_path
        except OSError as e:
            if i == 0:
                raise ShredError(f"Failed to rename file: {e}")
            break
    return current_path

def _obscure_timestamps(file: Path):
    try:
        import time
        import random
        
        now = time.time()
        random_time = now - random.uniform(0, 157680000)
        os.utime(file, (random_time, random_time))
        
        if platform.system() == "Windows":
            import ctypes
            from ctypes import wintypes
            
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.CreateFileW(
                str(file), 0x100, 0, None, 3, 0x80, None
            )
            if handle != -1:
                filetime = wintypes.FILETIME()
                time_val = int((random_time + 11644473600) * 10000000)
                filetime.dwLowDateTime = time_val & 0xFFFFFFFF
                filetime.dwHighDateTime = time_val >> 32
                kernel32.SetFileTime(handle, ctypes.byref(filetime), None, None)
                kernel32.CloseHandle(handle)
                
    except Exception as e:
        LOG.warning(f"Could not obscure timestamps: {e}")

def _secure_overwrite_advanced(
    file: Path,
    method: str = "simple_random",
    passes: int = 3,
    bufsize: int = 1 << 16,
    progress: Optional[Callable[[int, int, str], None]] = None,
    stop_event: Optional[threading.Event] = None,
) -> None:
    """Advanced overwrite with safe progress updates"""
    try:
        size = file.stat().st_size
    except OSError as e:
        raise ShredError(f"Cannot access file: {e}")
    
    patterns = AdvancedShredder.get_wipe_method(method, passes)
    
    # Adjust buffer size for performance
    if size > 100 * 1024 * 1024:
        bufsize = 1 << 20
    elif size > 10 * 1024 * 1024:
        bufsize = 1 << 18
    
    try:
        with file.open("r+b", buffering=0) as fh:
            for pass_num, pattern_fn in enumerate(patterns, 1):
                # Check for interruption
                if stop_event and stop_event.is_set():
                    raise OperationInterrupted("Operation cancelled by user")
                    
                fh.seek(0)
                written = 0
                
                # Update progress at start of pass
                if progress:
                    if not progress(pass_num, len(patterns), f"Starting pass {pass_num}/{len(patterns)}"):
                        raise OperationInterrupted("Operation cancelled by user")
                
                while written < size:
                    if stop_event and stop_event.is_set():
                        raise OperationInterrupted("Operation cancelled by user")
                        
                    chunk_size = min(bufsize, size - written)
                    data = pattern_fn(chunk_size)
                    fh.write(data)
                    written += chunk_size
                    
                    # Update progress periodically (but not too often)
                    if progress and written % (50 * bufsize) == 0:
                        if not progress(pass_num, len(patterns), f"Pass {pass_num}/{len(patterns)} - {written}/{size} bytes"):
                            raise OperationInterrupted("Operation cancelled by user")
                
                # Force sync to disk
                fh.flush()
                os.fsync(fh.fileno())
                
                # Final progress update for this pass
                if progress:
                    if not progress(pass_num, len(patterns), f"Pass {pass_num}/{len(patterns)} completed"):
                        raise OperationInterrupted("Operation cancelled by user")
                        
    except PermissionError as e:
        raise ShredError(f"Permission denied: {e}")
    except OSError as e:
        raise ShredError(f"File access error: {e}")

def shred_file(
    path: str | os.PathLike,
    *,
    passes: int = 3,
    method: str = "simple_random",
    keep_bytes: bool = False,
    keep_root: Optional[str | os.PathLike] = None,
    obscure_metadata: bool = True,
    progress: Optional[Callable[[int, int, str], None]] = None,
    stop_event: Optional[threading.Event] = None,
) -> Tuple[bool, str]:
    """Enhanced shred_file with better error handling and path detection"""
    path = Path(path)
    
    try:
        if not path.exists():
            raise ShredError("Target does not exist")

        # Convert to absolute path for better system path detection
        abs_path = path.absolute()
        
        # Improved system path detection
        if _is_sensitive_system_path(abs_path):
            raise ShredError(f"Refusing to shred sensitive system path: {abs_path}")

        if path.is_symlink():
            raise ShredError("Refusing to shred symbolic link")

        if path.stat().st_nlink > 1:
            raise ShredError("Refusing to shred hard-linked file")

        # SSD detection
        if _looks_like_ssd(path):
            LOG.warning("SSD detected - physical overwrite not guaranteed")

        # Secure operations
        scrambled = _secure_rename(path, 3 if obscure_metadata else 1)
        
        if obscure_metadata:
            _obscure_timestamps(scrambled)
        
        _secure_overwrite_advanced(scrambled, method, passes, 1 << 16, progress, stop_event)

        if keep_bytes:
            if not keep_root:
                raise ShredError("keep_root must be set when keep_bytes=True")
            
            keep_root = Path(keep_root).expanduser().absolute()
            dst = keep_root / scrambled.name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(scrambled), str(dst))
            return True, f"Shredded and preserved at {dst}"
        else:
            scrambled.unlink()
            return True, "Completely shredded and deleted"
            
    except OperationInterrupted as exc:
        try:
            if 'scrambled' in locals() and scrambled.exists():
                scrambled.unlink()
        except:
            pass
        return False, str(exc)
    except Exception as exc:
        LOG.exception("Shredding failed: %s", exc)
        return False, f"Shred error: {exc}"

def shred_directory(
    directory: str | os.PathLike,
    *,
    passes: int = 3,
    method: str = "simple_random",
    keep_bytes: bool = False,
    keep_root: Optional[str | os.PathLike] = None,
    obscure_metadata: bool = True,
    progress: Optional[Callable[[int, int, str], None]] = None,
    stop_event: Optional[threading.Event] = None,
) -> Tuple[bool, str]:
    """Enhanced shred_directory with better path handling"""
    directory = Path(directory)
    
    try:
        if not directory.is_dir():
            raise ShredError("Target is not a directory")

        # Convert to absolute path
        abs_directory = directory.absolute()
        
        # Improved system path detection
        if _is_sensitive_system_path(abs_directory):
            raise ShredError(f"Refusing to shred sensitive system directory: {abs_directory}")

        if keep_bytes and keep_root and _is_subdir(Path(keep_root).absolute(), abs_directory):
            raise ShredError("keep_root cannot be inside target directory")

        # Get files with better error handling
        files = []
        try:
            for p in directory.rglob("*"):
                if p.is_file() and not p.is_symlink():
                    # Check if file is in sensitive location
                    if not _is_sensitive_system_path(p.absolute()):
                        files.append(p)
        except PermissionError as e:
            raise ShredError(f"Permission denied accessing directory: {e}")
        
        if not files:
            return False, "No accessible files found in directory"
            
        total_passes = len(files) * passes
        completed = 0

        for file_path in files:
            if stop_event and stop_event.is_set():
                raise OperationInterrupted("Operation cancelled by user")

            def file_progress(cur_pass, total_passes, status):
                nonlocal completed
                if stop_event and stop_event.is_set():
                    return False
                overall_progress = completed + cur_pass
                if progress:
                    return progress(overall_progress, total_passes, f"Processing {file_path.name}")
                return True

            ok, msg = shred_file(
                file_path,
                passes=passes,
                method=method,
                keep_bytes=keep_bytes,
                keep_root=keep_root,
                obscure_metadata=obscure_metadata,
                progress=file_progress,
                stop_event=stop_event,
            )
            
            if not ok:
                if "cancelled" in msg.lower() or "interrupted" in msg.lower():
                    raise OperationInterrupted(msg)
                raise ShredError(f"Failed on {file_path}: {msg}")
                
            completed += passes

        if not keep_bytes and not (stop_event and stop_event.is_set()):
            shutil.rmtree(directory)
            
        return True, f"Directory shredded: {len(files)} files processed"
        
    except OperationInterrupted as exc:
        return False, str(exc)
    except Exception as exc:
        LOG.exception("Directory shredding failed: %s", exc)
        return False, f"Directory shred error: {exc}"

def _is_sensitive_system_path(path: Path) -> bool:
    """Improved system path detection - only blocks critical system paths"""
    try:
        path_str = str(path).lower()
        abs_path = path.absolute()
        abs_path_str = str(abs_path).lower()
        
        # Critical Windows system paths
        if platform.system() == "Windows":
            sensitive_paths = [
                "c:\\windows\\",
                "c:\\program files\\",
                "c:\\programdata\\",
                "c:\\system32\\",
                "c:\\$",
                "c:\\pagefile.sys",
                "c:\\hiberfil.sys",
                "c:\\swapfile.sys",
            ]
            
            for sensitive in sensitive_paths:
                if abs_path_str.startswith(sensitive):
                    return True
                    
            # Block root of system drives
            if abs_path_str in ["c:\\", "d:\\"] and abs_path_str.endswith("\\"):
                return True
                
        # Critical Unix system paths
        else:
            sensitive_paths = [
                "/bin/",
                "/sbin/",
                "/etc/",
                "/usr/",
                "/var/",
                "/sys/",
                "/proc/",
                "/dev/",
                "/lib/",
                "/lib64/",
            ]
            
            for sensitive in sensitive_paths:
                if abs_path_str.startswith(sensitive):
                    return True
                    
            # Block root directory
            if abs_path_str == "/":
                return True
        
        # Allow user directories, temporary directories, and most other locations
        return False
        
    except Exception:
        return False  # If we can't determine, allow the operation with warning

def _looks_like_ssd(path: Path) -> bool:
    """SSD detection - simplified"""
    try:
        if platform.system() == "Windows":
            # For Windows, we'll use a simpler approach
            # Check if the path is on a likely SSD drive
            drive = path.drive
            if drive:
                # This is a heuristic - you might want to implement proper detection
                return False
        return False
    except Exception:
        return False

def _is_subdir(child: Path, parent: Path) -> bool:
    """Check if child is subdirectory of parent"""
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False