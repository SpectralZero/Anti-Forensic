"""
DIGITAL FORENSIC UTILITIES - Fixed Path Detection
"""

import os
import shutil
import tempfile
import logging
from pathlib import Path
from typing import Callable, List, Optional, Tuple
import platform
import subprocess
import threading
import time
import glob
import sys

LOG = logging.getLogger("forensic_utilities")

class ForensicCleaner:
    """Forensic cleaning utilities with working path detection"""
    
    @staticmethod
    def wipe_free_space(
        directory: str | Path, 
        passes: int = 1,
        stop_event: Optional[threading.Event] = None,
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> bool:
        """
        Wipe free space with CRITICAL SAFETY CHECKS
        """
        try:
            directory = Path(directory)
            if not directory.exists():
                LOG.error(f"Directory does not exist: {directory}")
                return False
            
            # CRITICAL: Check if this is Python installation directory
            python_dirs = [
                Path(sys.executable).parent,  # Python executable directory
                Path(sys.executable).parent.parent,  # Python root directory
                Path(__file__).parent,  # Current script directory
            ]
            
            for python_dir in python_dirs:
                if python_dir.exists() and _is_subdir(directory, python_dir):
                    LOG.error(f"CRITICAL: Attempted to wipe Python installation directory: {directory}")
                    return False
            
            # Check if directory contains Python files
            try:
                python_files = list(directory.rglob("*.py"))
                if python_files and len(python_files) > 10:  # If many Python files, likely Python installation
                    LOG.error(f"CRITICAL: Directory contains Python installation: {directory}")
                    return False
            except:
                pass
            
            # Enhanced system drive detection
            if _is_sensitive_system_drive(directory):
                LOG.error(f"Attempted to wipe sensitive system drive: {directory}")
                return False
            
            # Get free space
            try:
                stat = shutil.disk_usage(str(directory))
                free_space = stat.free
            except OSError as e:
                LOG.error(f"Cannot get disk usage for {directory}: {e}")
                return False
            
            # CRITICAL: Don't wipe drives with Python installations
            if _contains_python_installation(directory):
                LOG.error(f"CRITICAL: Drive contains Python installation: {directory}")
                return False
            
            # Safety limit - reduced to 1GB for testing
            max_wipe_size = 1 * 1024 * 1024 * 1024  # 1GB
            free_space = min(free_space, max_wipe_size)
            
            LOG.info(f"SAFE WIPING: {free_space / (1024**3):.2f} GB free space in {directory}")
            
            # Rest of the method remains the same...
            chunk_size = 10 * 1024 * 1024  # 10MB chunks
            temp_files = []
            
            total_bytes_to_write = free_space * passes
            total_bytes_written = 0
            
            for pass_num in range(passes):
                if stop_event and stop_event.is_set():
                    LOG.info("Free space wipe cancelled by user")
                    return False
                    
                LOG.info(f"Free space wipe pass {pass_num + 1}/{passes}")
                
                # Update progress at start of pass
                if progress_callback:
                    if not progress_callback(total_bytes_written, total_bytes_to_write, 
                                        f"Starting pass {pass_num + 1}/{passes}"):
                        return False
                
                bytes_written_this_pass = 0
                
                while bytes_written_this_pass < free_space:
                    if stop_event and stop_event.is_set():
                        break
                        
                    try:
                        # Create temp file
                        with tempfile.NamedTemporaryFile(
                            dir=directory, 
                            delete=False,
                            prefix=f"wipe_{pass_num}_",
                            suffix=".tmp"
                        ) as temp_file:
                            temp_files.append(temp_file.name)
                            
                            # Write data in chunks with progress updates
                            while bytes_written_this_pass < free_space:
                                if stop_event and stop_event.is_set():
                                    break
                                    
                                chunk_size_actual = min(chunk_size, free_space - bytes_written_this_pass)
                                chunk = os.urandom(chunk_size_actual)
                                temp_file.write(chunk)
                                bytes_written_this_pass += chunk_size_actual
                                total_bytes_written += chunk_size_actual
                                
                                # Update progress every 50MB for smooth updates
                                if progress_callback and bytes_written_this_pass % (5 * chunk_size) == 0:
                                    progress_percent = (total_bytes_written / total_bytes_to_write) * 100
                                    status = (f"Pass {pass_num + 1}/{passes} - "
                                            f"{progress_percent:.1f}% complete - "
                                            f"{bytes_written_this_pass / (1024**3):.1f}GB / {free_space / (1024**3):.1f}GB")
                                    
                                    if not progress_callback(total_bytes_written, total_bytes_to_write, status):
                                        stop_event.set()
                                        break
                                
                                # Small delay to prevent system overload but allow progress updates
                                time.sleep(0.001)
                                
                    except OSError as e:
                        LOG.warning(f"Disk write error (may be full): {e}")
                        break
                    except Exception as e:
                        LOG.error(f"Unexpected error during wipe: {e}")
                        break
                
                # Update progress after each pass
                if progress_callback and not stop_event.is_set():
                    progress_percent = (total_bytes_written / total_bytes_to_write) * 100
                    if not progress_callback(total_bytes_written, total_bytes_to_write, 
                                        f"Completed pass {pass_num + 1}/{passes} - {progress_percent:.1f}%"):
                        stop_event.set()
                        break
                
                # Clean up temp files after each pass
                for temp_file in temp_files:
                    try:
                        if os.path.exists(temp_file):
                            os.unlink(temp_file)
                    except OSError as e:
                        LOG.warning(f"Could not delete temp file {temp_file}: {e}")
                temp_files.clear()
                
                if stop_event and stop_event.is_set():
                    break
            
            def _contains_python_installation(path: Path) -> bool:
                """Check if path contains Python installation files"""
                try:
                    python_indicators = [
                        "python.exe", "python3.exe", "pip.exe",
                        "Lib", "DLLs", "Scripts", "Include",
                        "site-packages", "dist-packages"
                    ]
                    
                    for indicator in python_indicators:
                        if (path / indicator).exists():
                            return True
                            
                    # Check for Python in parent directories
                    current = path
                    for _ in range(3):  # Check 3 levels up
                        if any((current / indicator).exists() for indicator in python_indicators):
                            return True
                        current = current.parent
                        if current == current.parent:  # Reached root
                            break
                            
                    return False
                except:
                    return True  # If unsure, block the operation

            def _is_subdir(child: Path, parent: Path) -> bool:
                """Check if child is subdirectory of parent"""
                try:
                    child.relative_to(parent)
                    return True
                except ValueError:
                    return False
            # Final progress update
            if progress_callback and not stop_event.is_set():
                progress_callback(total_bytes_to_write, total_bytes_to_write, "Free space wipe completed!")
            
            LOG.info("Free space wipe completed successfully")
            return True
            
        except Exception as e:
            LOG.error(f"Free space wiping failed: {e}")
            return False
    
    
    @staticmethod
    def clear_system_logs() -> bool:
        """Clear system logs - improved for user mode operation"""
        try:
            system = platform.system()
            
            if system == "Windows":
                return ForensicCleaner._clear_windows_logs()
            elif system == "Linux":
                return ForensicCleaner._clear_linux_logs()
            elif system == "Darwin":
                return ForensicCleaner._clear_macos_logs()
            else:
                LOG.warning(f"Unsupported platform: {system}")
                return False
                
        except Exception as e:
            LOG.error(f"Log clearing failed: {e}")
            return False
    
    @staticmethod
    def _clear_windows_logs() -> bool:
        """Clear Windows event logs - works without admin privileges for some logs"""
        try:
            # Try to clear event logs that don't require admin
            logs = ["Application", "System"]
            cleared = 0
            
            for log in logs:
                try:
                    result = subprocess.run([
                        "wevtutil", "clear-log", log
                    ], capture_output=True, check=False, text=True, timeout=30)
                    
                    if result.returncode == 0:
                        cleared += 1
                        LOG.info(f"Cleared Windows log: {log}")
                    else:
                        LOG.warning(f"Could not clear {log} log: {result.stderr}")
                except subprocess.TimeoutExpired:
                    LOG.warning(f"Timeout clearing {log} log")
                except Exception as e:
                    LOG.warning(f"Error clearing {log} log: {e}")
            
            # Also clear recent user logs
            user_logs_path = Path.home() / "AppData" / "Local" / "Temp"
            if user_logs_path.exists():
                try:
                    for log_file in user_logs_path.glob("*.log"):
                        try:
                            log_file.unlink()
                            cleared += 1
                        except:
                            pass
                except:
                    pass
            
            LOG.info(f"Cleared {cleared} Windows log items")
            return cleared > 0
            
        except Exception as e:
            LOG.error(f"Windows log clearing failed: {e}")
            return False
    
    @staticmethod
    def _clear_linux_logs() -> bool:
        """Clear Linux logs - works in user mode for user logs"""
        try:
            cleared = 0
            home = Path.home()
            
            # Clear user-specific logs
            user_logs = [
                home / ".bash_history",
                home / ".zsh_history",
                home / ".local/share/recently-used.xbel",
            ]
            
            for log_file in user_logs:
                if log_file.exists():
                    try:
                        log_file.write_text("")
                        cleared += 1
                        LOG.info(f"Cleared user log: {log_file}")
                    except Exception as e:
                        LOG.warning(f"Could not clear {log_file}: {e}")
            
            # Try to clear system logs if we have permission
            system_logs = [
                "/var/log/auth.log",
                "/var/log/syslog",
            ]
            
            for log_file in system_logs:
                if os.path.exists(log_file):
                    try:
                        with open(log_file, 'w') as f:
                            f.write("")
                        cleared += 1
                    except PermissionError:
                        pass  # Expected without root
                    except Exception as e:
                        LOG.warning(f"Could not clear {log_file}: {e}")
            
            LOG.info(f"Cleared {cleared} Linux log items")
            return cleared > 0
            
        except Exception as e:
            LOG.error(f"Linux log clearing failed: {e}")
            return False
    
    @staticmethod
    def _clear_macos_logs() -> bool:
        """Clear macOS logs - works in user mode"""
        try:
            cleared = 0
            home = Path.home()
            
            # Clear user logs
            user_logs = [
                home / ".bash_history",
                home / ".zsh_history",
                home / "Library/Logs",
            ]
            
            for log_path in user_logs:
                if log_path.exists():
                    try:
                        if log_path.is_file():
                            log_path.write_text("")
                            cleared += 1
                        else:
                            for log_file in log_path.rglob("*.log"):
                                try:
                                    log_file.write_text("")
                                    cleared += 1
                                except:
                                    pass
                    except Exception as e:
                        LOG.warning(f"Could not clear {log_path}: {e}")
            
            LOG.info(f"Cleared {cleared} macOS log items")
            return cleared > 0
            
        except Exception as e:
            LOG.error(f"macOS log clearing failed: {e}")
            return False
    
    @staticmethod
    def clear_browser_data() -> bool:
        """Clear browser data with improved detection"""
        try:
            home = Path.home()
            browsers = {
                "Chrome": [
                    home / "AppData/Local/Google/Chrome/User Data/Default/Cache",
                    home / "AppData/Local/Google/Chrome/User Data/Default/Code Cache",
                    home / "AppData/Local/Google/Chrome/User Data/Default/GPUCache",
                    home / ".config/google-chrome/default/Cache",
                    home / ".config/google-chrome/default/Code Cache",
                ],
                "Firefox": [
                    home / "AppData/Roaming/Mozilla/Firefox/Profiles/*/cache2",
                    home / "AppData/Roaming/Mozilla/Firefox/Profiles/*/thumbnails",
                    home / ".mozilla/firefox/*/cache2",
                    home / ".mozilla/firefox/*/thumbnails",
                ],
                "Edge": [
                    home / "AppData/Local/Microsoft/Edge/User Data/Default/Cache",
                    home / "AppData/Local/Microsoft/Edge/User Data/Default/Code Cache",
                    home / "AppData/Local/Microsoft/Edge/User Data/Default/GPUCache",
                ],
                "Opera": [
                    home / "AppData/Roaming/Opera Software/Opera Stable/Cache",
                    home / "AppData/Roaming/Opera Software/Opera Stable/Code Cache",
                ],
                "Brave": [
                    home / "AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/Cache",
                    home / "AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/Code Cache",
                ]
            }
            
            cleared_count = 0
            
            for browser, paths in browsers.items():
                for path_pattern in paths:
                    # Handle both specific paths and patterns
                    if '*' in str(path_pattern):
                        # Use glob for patterns
                        matches = glob.glob(str(path_pattern), recursive=True)
                        paths_to_clear = [Path(match) for match in matches]
                    else:
                        paths_to_clear = [path_pattern]
                    
                    for path in paths_to_clear:
                        if path.exists():
                            try:
                                if path.is_file():
                                    path.unlink()
                                    cleared_count += 1
                                    LOG.info(f"Cleared {browser} file: {path}")
                                else:
                                    # Clear entire cache directory
                                    try:
                                        shutil.rmtree(path, ignore_errors=True)
                                        cleared_count += 1
                                        LOG.info(f"Cleared {browser} cache: {path}")
                                    except Exception as e:
                                        LOG.warning(f"Could not clear cache {path}: {e}")
                                        # Try individual files
                                        for item in path.rglob('*'):
                                            try:
                                                if item.is_file():
                                                    item.unlink()
                                                    cleared_count += 1
                                            except:
                                                pass
                            except Exception as e:
                                LOG.warning(f"Could not clear {path}: {e}")
            
            # Also clear general browser cache files
            cache_patterns = [
                "*.cache",
                "Cache_Data*",
                "*.tmp",
                "blob_storage*",
            ]
            
            for pattern in cache_patterns:
                for cache_file in home.rglob(pattern):
                    try:
                        if cache_file.is_file():
                            cache_file.unlink()
                            cleared_count += 1
                    except:
                        pass
            
            LOG.info(f"Cleared {cleared_count} browser cache items")
            return cleared_count > 0
            
        except Exception as e:
            LOG.error(f"Browser data clearing failed: {e}")
            return False
        

    @staticmethod
    def clear_temp_files() -> bool:
        """Clear temporary files from system and user directories"""
        try:
            cleared_count = 0
            
            # System temp directories
            temp_dirs = [
                Path(os.environ.get('TEMP', 'C:\\Windows\\Temp')),
                Path(os.environ.get('TMP', 'C:\\Windows\\Temp')),
                Path.home() / "AppData" / "Local" / "Temp",
                Path("/tmp") if platform.system() != "Windows" else None,
            ]
            
            for temp_dir in temp_dirs:
                if temp_dir and temp_dir.exists():
                    try:
                        for item in temp_dir.iterdir():
                            try:
                                if item.is_file():
                                    item.unlink()
                                    cleared_count += 1
                                elif item.is_dir():
                                    # Skip system directories in temp
                                    if item.name not in ['.', '..', 'Low']:
                                        shutil.rmtree(item, ignore_errors=True)
                                        cleared_count += 1
                            except (PermissionError, OSError):
                                continue
                        LOG.info(f"Cleared temp directory: {temp_dir}")
                    except Exception as e:
                        LOG.warning(f"Could not clear temp directory {temp_dir}: {e}")
            
            # Browser temp files
            browser_temp_patterns = [
                "*.tmp",
                "*.temp",
                "*.log",
                "cache*",
                "temp*"
            ]
            
            for pattern in browser_temp_patterns:
                for temp_file in Path.home().rglob(pattern):
                    try:
                        if temp_file.is_file():
                            temp_file.unlink()
                            cleared_count += 1
                    except:
                        pass
            
            LOG.info(f"Cleared {cleared_count} temporary files")
            return cleared_count > 0
            
        except Exception as e:
            LOG.error(f"Temp file clearing failed: {e}")
            return False

    @staticmethod
    def clear_recent_documents() -> bool:
        """Clear recent documents and activity history"""
        try:
            cleared_count = 0
            
            if platform.system() == "Windows":
                # Windows recent documents
                recent_locations = [
                    Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Recent",
                    Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Recent" / "AutomaticDestinations",
                    Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Recent" / "CustomDestinations",
                ]
                
                for recent_dir in recent_locations:
                    if recent_dir.exists():
                        try:
                            for item in recent_dir.iterdir():
                                try:
                                    if item.is_file():
                                        item.unlink()
                                        cleared_count += 1
                                except:
                                    pass
                            LOG.info(f"Cleared recent documents: {recent_dir}")
                        except Exception as e:
                            LOG.warning(f"Could not clear recent documents {recent_dir}: {e}")
            
            # Cross-platform recent files
            recent_patterns = [
                "*recent*",
                "*history*",
                "*thumbnails*",
                "*cache*"
            ]
            
            config_dirs = [
                Path.home() / "AppData" / "Roaming",
                Path.home() / ".config",
                Path.home() / ".local" / "share",
            ]
            
            for config_dir in config_dirs:
                if config_dir.exists():
                    for pattern in recent_patterns:
                        for recent_file in config_dir.rglob(pattern):
                            try:
                                if recent_file.is_file() and recent_file.stat().st_size < 10 * 1024 * 1024:  # Skip large files
                                    recent_file.unlink()
                                    cleared_count += 1
                            except:
                                pass
            
            LOG.info(f"Cleared {cleared_count} recent document entries")
            return cleared_count > 0
            
        except Exception as e:
            LOG.error(f"Recent documents clearing failed: {e}")
            return False

    @staticmethod
    def clear_dns_cache() -> bool:
        """Clear DNS cache"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(["ipconfig", "/flushdns"], capture_output=True, text=True, check=False)
                if result.returncode == 0:
                    LOG.info("DNS cache cleared successfully")
                    return True
            elif platform.system() == "Linux":
                result = subprocess.run(["sudo", "systemd-resolve", "--flush-caches"], capture_output=True, check=False)
                if result.returncode == 0:
                    LOG.info("DNS cache cleared successfully")
                    return True
            elif platform.system() == "Darwin":
                result = subprocess.run(["sudo", "killall", "-HUP", "mDNSResponder"], capture_output=True, check=False)
                if result.returncode == 0:
                    LOG.info("DNS cache cleared successfully")
                    return True
            return False
        except Exception as e:
            LOG.error(f"DNS cache clearing failed: {e}")
            return False

    @staticmethod
    def perform_full_system_clean(progress_callback: Optional[Callable[[str, bool], None]] = None) -> Tuple[bool, str]:
        """
        Perform comprehensive system cleaning with better error handling
        Returns (success, summary_message)
        """
        try:
            steps = [
                ("Clearing browser data...", ForensicCleaner.clear_browser_data),
                ("Clearing system logs...", ForensicCleaner.clear_system_logs),
                ("Clearing temporary files...", ForensicCleaner.clear_temp_files),
                #("Clearing recent documents...", ForensicCleaner.clear_recent_documents),   # Need more works 
                ("Clearing DNS cache...", ForensicCleaner.clear_dns_cache),
            ]
            
            results = []
            admin_warning = False
            
            for step_name, step_function in steps:
                if progress_callback:
                    progress_callback(step_name, False)  # In progress
                
                try:
                    success = step_function()
                    results.append((step_name, success))
                    
                    # Check if we had admin issues
                    if step_name == "Clearing system logs..." and not success:
                        admin_warning = True
                    
                    if progress_callback:
                        progress_callback(step_name, success)  # Completed
                    
                    # Small delay to show progress
                    time.sleep(0.5)
                    
                except Exception as e:
                    LOG.error(f"Step {step_name} failed: {e}")
                    results.append((step_name, False))
            
            # Generate summary
            successful_steps = [name for name, success in results if success]
            failed_steps = [name for name, success in results if not success]
            
            summary = f"Full System Clean Complete:\n\n"
            summary += f"✅ Successful: {len(successful_steps)} steps\n"
            summary += f"❌ Failed: {len(failed_steps)} steps\n\n"
            
            if successful_steps:
                summary += "Successful operations:\n• " + "\n• ".join(successful_steps) + "\n\n"
            
            if failed_steps:
                summary += "Failed operations:\n• " + "\n• ".join(failed_steps) + "\n\n"
            
            # Add specific warnings
            if admin_warning:
                summary += "⚠️  Admin Rights Note: Some system logs require administrator privileges to clear.\n"
                summary += "   Run as Administrator for complete cleaning.\n\n"
            
            # Check browser data results
            browser_steps = [name for name in successful_steps if "browser" in name.lower()]
            if not browser_steps:
                summary += "💡 Tip: Browser data clearing may work better when browsers are closed.\n"
            
            overall_success = len(successful_steps) >= 3  # Consider success if 3+ steps worked
            
            return overall_success, summary
            
        except Exception as e:
            LOG.error(f"Full system clean failed: {e}")
            return False, f"Full system clean failed: {e}"    

def _is_sensitive_system_drive(path: Path) -> bool:
    """Improved system drive detection - only blocks critical system roots"""
    try:
        abs_path = path.absolute()
        abs_path_str = str(abs_path).lower()
        
        if platform.system() == "Windows":
            # Only block actual system root drives, not subdirectories
            sensitive_roots = [
                "c:\\windows\\",
                "c:\\program files\\",
                "c:\\programdata\\",
                "c:\\system32\\",
            ]
            
            for sensitive in sensitive_roots:
                if abs_path_str.startswith(sensitive):
                    return True
            
            # Allow wiping in user directories, temp directories, etc.
            allowed_paths = [
                "c:\\users\\",
                "c:\\temp\\",
                "c:\\tmp\\",
                str(Path.home()).lower() + "\\",
            ]
            
            for allowed in allowed_paths:
                if abs_path_str.startswith(allowed):
                    return False
            
            # Block root of system drive
            if abs_path_str in ["c:\\", "c:"]:
                return True
                
        else:  # Linux/Mac
            sensitive_roots = [
                "/bin/",
                "/sbin/",
                "/etc/",
                "/usr/",
                "/var/",
                "/sys/",
                "/proc/",
                "/dev/",
            ]
            
            for sensitive in sensitive_roots:
                if abs_path_str.startswith(sensitive):
                    return True
            
            # Allow user directories
            if abs_path_str.startswith(str(Path.home()).lower()):
                return False
            
            # Block root directory
            if abs_path_str == "/":
                return True
        
        return False
        
    except Exception:
        return False  # If unsure, allow the operation

def _has_admin_privileges() -> bool:
    """Check admin privileges"""
    try:
        if platform.system() == "Windows":
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            return os.geteuid() == 0
    except:
        return False

