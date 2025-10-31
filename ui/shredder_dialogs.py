"""
shredder_dialogs.py
ENHANCED SHREDDER GUI - Fixed Window Management
"""

import threading
import logging
from pathlib import Path
from typing import Tuple, Optional
import time

import customtkinter as ctk
from tkinter import filedialog, messagebox

from core.secure_delete import shred_file, shred_directory
from ui.theme import CyberTheme, StyledFrame, GlowingButton, DangerButton

LOG = logging.getLogger("shredder_gui")

def new_toplevel(
    parent: ctk.CTk | ctk.CTkToplevel,
    title: str,
    geometry: str,
    modal: bool = True,
    topmost_once: bool = True,
) -> ctk.CTkToplevel:
    """Improved toplevel with better window management"""
    win = ctk.CTkToplevel(parent)
    win.title(title)
    win.geometry(geometry)
    win.configure(fg_color=CyberTheme.COLORS["bg_primary"])
    
    if modal:
        win.grab_set()
    
    win.transient(parent)
    win.lift()
    
    if topmost_once:
        win.attributes("-topmost", True)
        win.after(100, lambda: win.attributes("-topmost", False))
    
    win.focus_force()
    
    # Handle window close properly
    def on_close():
        if modal:
            win.grab_release()
        win.destroy()
    
    win.protocol("WM_DELETE_WINDOW", on_close)
    return win

class ShreddingMenu:
    @staticmethod
    def open_shredding_menu(master: ctk.CTk):
        win = new_toplevel(master, "⚡ SECURE SHREDDER", "520x480")
        win.resizable(False, False)

        header_frame = StyledFrame(win)
        header_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            header_frame, 
            text="⚡ SECURE SHREDDER", 
            font=CyberTheme.FONTS["title"],
            text_color=CyberTheme.COLORS["accent_primary"]
        ).pack(pady=10)
        
        ctk.CTkLabel(
            header_frame,
            text="Military-grade file destruction",
            font=CyberTheme.FONTS["subheading"],
            text_color=CyberTheme.COLORS["text_secondary"]
        ).pack()

        options_frame = StyledFrame(win)
        options_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            options_frame,
            text="Shredding Algorithm:",
            font=CyberTheme.FONTS["body"]
        ).pack(anchor="w", pady=(0, 5))

        algo_var = ctk.StringVar(value="simple_random")  # Default to simple for safety
        algorithms = [
            ("Simple Random (Fast & Safe)", "simple_random"),
            ("US DoD 5220.22-M (3-pass)", "us_dod"),
            ("Gutmann (7-pass Secure)", "gutmann"),
            ("RCMP OPS-II (4-pass)", "rcmp")
        ]

        for text, value in algorithms:
            ctk.CTkRadioButton(
                options_frame,
                text=text,
                variable=algo_var,
                value=value,
                font=CyberTheme.FONTS["body"]
            ).pack(anchor="w", pady=2)

        button_frame = StyledFrame(win)
        button_frame.pack(fill="x", padx=20, pady=20)

        buttons = [
            ("🗑️  Shred FILE", lambda: _file_dialog(win, algo_var.get())),
            ("📁 Shred DIRECTORY", lambda: _dir_dialog(win, algo_var.get())),
            ("🧹 Wipe Free Space", lambda: _wipe_free_space_dialog(win)),
            ("🔒 Close", win.destroy)
        ]

        for text, command in buttons:
            if "Wipe" in text or "Close" in text:
                btn = GlowingButton(button_frame, text=text, command=command, height=40)
            else:
                btn = DangerButton(button_frame, text=text, command=command, height=40)
            btn.pack(pady=8, fill="x")

        status_frame = StyledFrame(win)
        status_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            status_frame,
            text="💀 All operations are irreversible",
            font=CyberTheme.FONTS["body"],
            text_color=CyberTheme.COLORS["accent_danger"]
        ).pack()

def _file_dialog(master, algorithm: str):
    path = filedialog.askopenfilename(
        title="Select file to shred",
        filetypes=[("All files", "*.*")]
    )
    if not path:
        return
    
    passes, keep, obscure = _ask_advanced_opts(master, is_dir=False)
    if passes is None:
        return
    
    if not messagebox.askyesno(
        "CONFIRM DESTRUCTION", 
        f"Shred '{Path(path).name}' using {algorithm.upper()}?\n\n"
        f"• Passes: {passes}\n"
        f"• Algorithm: {algorithm}\n"
        f"• Metadata obfuscation: {'Yes' if obscure else 'No'}\n\n"
        "THIS ACTION IS IRREVERSIBLE!"
    ):
        return
    
    _run_thread(
        master,
        target=_shred_file_thread,
        args=(path, passes, algorithm, keep, obscure),
        title="SHREDDING FILE...",
        show_stop=True
    )

def _dir_dialog(master, algorithm: str):
    path = filedialog.askdirectory(title="Select directory to shred")
    if not path:
        return
    
    # Check if directory is empty
    try:
        dir_path = Path(path)
        if not any(dir_path.iterdir()):
            if not messagebox.askyesno("Empty Directory", "The selected directory is empty. Continue?"):
                return
    except:
        pass
    
    passes, keep, obscure = _ask_advanced_opts(master, is_dir=True)
    if passes is None:
        return
    
    try:
        file_count = sum(1 for _ in Path(path).rglob('*') if _.is_file() and not _.is_symlink())
    except:
        file_count = "unknown"
    
    if not messagebox.askyesno(
        "CONFIRM DESTRUCTION",
        f"Shred directory '{Path(path).name}'?\n\n"
        f"• Files: {file_count}\n"
        f"• Passes: {passes}\n"
        f"• Algorithm: {algorithm}\n"
        f"• Metadata obfuscation: {'Yes' if obscure else 'No'}\n\n"
        "THIS ACTION IS IRREVERSIBLE!"
    ):
        return
    
    _run_thread(
        master,
        target=_shred_dir_thread,
        args=(path, passes, algorithm, keep, obscure),
        title="SHREDDING DIRECTORY...",
        show_stop=True
    )

def _wipe_free_space_dialog(master):
    path = filedialog.askdirectory(title="Select location to wipe free space")
    if not path:
        return
    
    # Safety warning
    if not messagebox.askyesno(
        "WARNING", 
        "Free space wiping will:\n\n"
        "• Create large temporary files\n"
        "• Use significant disk space\n"
        "• Take considerable time\n"
        "• May impact system performance\n\n"
        "Continue?"
    ):
        return
    
    passes = _ask_wipe_passes(master)
    if passes is None:
        return
    
    _run_thread(
        master,
        target=_wipe_free_space_thread,
        args=(path, passes),
        title="WIPING FREE SPACE...",
        show_stop=True
    )

def _ask_advanced_opts(master, *, is_dir=False) -> Tuple[int | None, bool, bool]:
    dlg = new_toplevel(master, "Shredding Options", "380x280")
    
    ctk.CTkLabel(dlg, text="Overwrite passes (1-7):", font=CyberTheme.FONTS["body"]).pack(pady=12)
    passes_var = ctk.StringVar(value="3")
    entry = ctk.CTkEntry(dlg, textvariable=passes_var, width=80)
    entry.pack()

    keep_var = ctk.BooleanVar(value=False)
    obscure_var = ctk.BooleanVar(value=True)
    
    ctk.CTkCheckBox(
        dlg, 
        text="Keep garbled bytes",
        variable=keep_var,
        font=CyberTheme.FONTS["body"]
    ).pack(pady=8)
    
    ctk.CTkCheckBox(
        dlg,
        text="Obfuscate metadata",
        variable=obscure_var,
        font=CyberTheme.FONTS["body"]
    ).pack(pady=8)

    result = {"ok": False}

    def _ok():
        try:
            p = int(passes_var.get())
            if not 1 <= p <= 7:  # Reduced from 35 to 7 for safety
                raise ValueError
            result["passes"] = p
            result["keep"] = bool(keep_var.get())
            result["obscure"] = bool(obscure_var.get())
            result["ok"] = True
            dlg.destroy()
        except ValueError:
            messagebox.showerror("Invalid", "Enter an integer 1-7.")

    GlowingButton(dlg, text="CONFIRM", command=_ok, width=120).pack(pady=20)
    dlg.wait_window()
    
    return (result["passes"], result["keep"], result["obscure"]) if result["ok"] else (None, None, None)

def _ask_wipe_passes(master) -> int | None:
    dlg = new_toplevel(master, "Wipe Passes", "350x200")  # Slightly larger
    
    ctk.CTkLabel(
        dlg, 
        text="Free space wipe passes (1-3):", 
        font=CyberTheme.FONTS["subheading"]
    ).pack(pady=20)
    
    passes_var = ctk.StringVar(value="1")
    entry = ctk.CTkEntry(dlg, textvariable=passes_var, width=100, height=35)
    entry.pack(pady=10)

    result = {"passes": None}

    def _ok():
        try:
            p = int(passes_var.get())
            if not 1 <= p <= 3:
                raise ValueError
            result["passes"] = p
            dlg.destroy()
        except ValueError:
            messagebox.showerror("Invalid", "Please enter an integer between 1-3.")

    # Better button styling
    button_frame = ctk.CTkFrame(dlg, fg_color="transparent")
    button_frame.pack(pady=20)
    
    GlowingButton(
        button_frame,
        text=" START WIPE",
        command=_ok,
        width=150,
        height=45,
        font=CyberTheme.FONTS["subheading"]
    ).pack()
    
    dlg.wait_window()
    return result["passes"]

class _ProgressWindow:
    def __init__(self, master, title, show_stop=False):
        self.win = new_toplevel(master, title, "500x220", modal=False)  # Larger window
        self.win.resizable(False, False)
        self.stop_event = threading.Event()
        self._alive = True
        self._destroying = False
        
        # Main container with padding
        main_container = ctk.CTkFrame(self.win, fg_color=CyberTheme.COLORS["bg_primary"])
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        ctk.CTkLabel(
            main_container, 
            text=title, 
            font=CyberTheme.FONTS["heading"],
            text_color=CyberTheme.COLORS["accent_primary"]
        ).pack(pady=(0, 15))
        
        # Progress bar - wider and more visible
        self.bar = ctk.CTkProgressBar(main_container, width=400, height=25, 
                                    progress_color=CyberTheme.COLORS["accent_primary"])
        self.bar.set(0)
        self.bar.pack(pady=(0, 10))
        
        # Status label with better visibility
        self.status = ctk.CTkLabel(
            main_container, 
            text="Initializing...",
            font=CyberTheme.FONTS["body"],
            text_color=CyberTheme.COLORS["text_primary"],
            wraplength=400  # Prevent text from going outside
        )
        self.status.pack(pady=(0, 20))
        
        # Stop button container for better alignment
        if show_stop:
            button_container = ctk.CTkFrame(main_container, fg_color="transparent")
            button_container.pack(fill="x", pady=10)
            
            # Center the stop button
            button_container.grid_columnconfigure(0, weight=1)
            button_container.grid_columnconfigure(2, weight=1)
            
            self.stop_button = GlowingButton(
                button_container,
                text="⏹️ STOP OPERATION",
                command=self.stop,
                fg_color=CyberTheme.COLORS["accent_danger"],
                hover_color="#ff6666",
                width=180,
                height=40,
                font=CyberTheme.FONTS["subheading"]
            )
            self.stop_button.grid(row=0, column=1, padx=10, pady=5)
        
        # Handle window close properly
        self.win.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Store update timing for real-time progress
        self.last_update_time = 0
        self.update_interval = 0.1  # Update every 100ms for smooth progress

    def _on_close(self):
        """Handle window close safely"""
        self._destroying = True
        self._alive = False
        self.stop_event.set()
        self._safe_destroy()

    def _safe_destroy(self):
        """Safely destroy the window"""
        try:
            if self.win.winfo_exists():
                self.win.after(100, self._destroy_callback)
        except:
            pass

    def _destroy_callback(self):
        """Callback for safe destruction"""
        try:
            if self.win.winfo_exists():
                self.win.destroy()
        except:
            pass

    def stop(self):
        """Stop the current operation"""
        if self._alive and not self._destroying:
            self.stop_event.set()
            self._update_status("Stopping operation...")

    def _update_status(self, text):
        """Update status label safely"""
        if not self._alive or self._destroying:
            return
            
        try:
            if self.status.winfo_exists():
                self.win.after(0, lambda: self._update_status_callback(text))
        except:
            pass

    def _update_status_callback(self, text):
        """Callback for status updates"""
        try:
            if (self._alive and not self._destroying and 
                self.status.winfo_exists()):
                self.status.configure(text=text)
        except:
            pass

    def _update_progress(self, progress):
        """Update progress bar safely"""
        if not self._alive or self._destroying:
            return
            
        try:
            if self.bar.winfo_exists():
                self.win.after(0, lambda: self._update_progress_callback(progress))
        except:
            pass

    def _update_progress_callback(self, progress):
        """Callback for progress updates"""
        try:
            if (self._alive and not self._destroying and 
                self.bar.winfo_exists()):
                self.bar.set(progress)
        except:
            pass

    def update(self, cur, tot, status_msg=""):
        """Safe progress update with real-time smoothing"""
        if not self._alive or self._destroying or self.stop_event.is_set():
            return False
            
        try:
            # Calculate current progress
            progress = cur / tot if tot > 0 else 0.0
            progress = max(0.0, min(1.0, progress))
            
            # Update progress bar (always update for smooth movement)
            self._update_progress(progress)
            
            # Update status message if provided
            if status_msg:
                self._update_status(status_msg)
                
            return True
            
        except Exception as e:
            self._alive = False
            return False

    def close(self):
        """Close the window safely"""
        self._alive = False
        self._destroying = True
        self._safe_destroy()

def _run_thread(master, target, args, title, show_stop=False):
    """Start a threaded operation with progress window"""
    prog = _ProgressWindow(master, title, show_stop=show_stop)
    
    def thread_wrapper():
        try:
            target(*args, prog)
        except Exception as e:
            # Handle any thread exceptions
            logging.error(f"Thread operation failed: {e}")
            try:
                prog.close()
                # Show error in main thread
                master.after(0, lambda: messagebox.showerror("Error", f"Operation failed: {e}"))
            except:
                pass
    
    th = threading.Thread(target=thread_wrapper, daemon=True)
    th.start()

def _shred_file_thread(path, passes, method, keep, obscure, prog: _ProgressWindow):
    """Shred file with safe progress handling"""
    from core.secure_delete import shred_file
    try:
        ok, msg = shred_file(
            path,
            passes=passes,
            method=method,
            keep_bytes=keep,
            keep_root=_select_outdir() if keep else None,
            obscure_metadata=obscure,
            progress=prog.update,
            stop_event=prog.stop_event,
        )
    except Exception as e:
        ok, msg = False, f"Unexpected error: {e}"
    
    # Close progress window and show result
    prog.close()
    _final_popup(ok, msg)

def _shred_dir_thread(path, passes, method, keep, obscure, prog: _ProgressWindow):
    """Shred directory with safe progress handling"""
    from core.secure_delete import shred_directory
    try:
        ok, msg = shred_directory(
            path,
            passes=passes,
            method=method,
            keep_bytes=keep,
            keep_root=_select_outdir() if keep else None,
            obscure_metadata=obscure,
            progress=prog.update,
            stop_event=prog.stop_event,
        )
    except Exception as e:
        ok, msg = False, f"Unexpected error: {e}"
    
    prog.close()
    _final_popup(ok, msg)

def _wipe_free_space_thread(path, passes, prog: _ProgressWindow):
    """Wipe free space with real progress updates"""
    from core.forensic_utilities import ForensicCleaner
    try:
        # Initial progress update
        if not prog.update(0, 1, "Preparing free space wipe..."):
            return
            
        # Perform the wipe with progress callbacks
        success = ForensicCleaner.wipe_free_space(
            path, 
            passes, 
            prog.stop_event,
            progress_callback=prog.update
        )
        
        # Close progress window
        prog.close()
        
        # Show result
        if success:
            messagebox.showinfo("Success", " Free space wiped successfully!\n\nAll deleted files are now permanently unrecoverable.")
        else:
            if prog.stop_event.is_set():
                messagebox.showinfo("Stopped", "⏹ Free space wipe was cancelled")
            else:
                messagebox.showerror("Error", " Free space wiping failed")
                
    except Exception as e:
        prog.close()
        messagebox.showerror("Error", f" Wipe failed: {str(e)}")

def _select_outdir() -> str | None:
    out = filedialog.askdirectory(title="Destination for garbled files")
    return out or None

def _final_popup(ok: bool, msg: str):
    title = "SHREDDER REPORT"
    if ok:
        messagebox.showinfo(title, f"✅ SUCCESS\n{msg}")
        LOG.info(f"SUCCESS: {msg}")
    else:
        messagebox.showerror(title, f"❌ FAILED\n{msg}")
        LOG.error(f"FAILED: {msg}")