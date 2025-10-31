"""
hash_generator.py
HASH GENERATOR GUI 
Multi-algorithm hash calculation interface
"""

import threading
import tkinter as tk
from pathlib import Path
from typing import Dict, List
import time

import customtkinter as ctk
from tkinter import filedialog

from core.hash_calculator import HashCalculator
from ui.theme import CyberTheme, StyledFrame, GlowingButton, TerminalText

class HashGenerator:
    """Hash generator interface"""
    
    def __init__(self, master):
        self.master = master
        self.current_operation = None
        self.stop_event = threading.Event()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the hash generator interface"""
        # Main container
        self.frame = StyledFrame(self.master)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_frame = StyledFrame(self.frame)
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            header_frame,
            text=" HASH GENERATOR",
            font=CyberTheme.FONTS["heading"],
            text_color=CyberTheme.COLORS["accent_primary"]
        ).pack(side="left")
        
        # Algorithm selection
        algo_frame = StyledFrame(self.frame)
        algo_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            algo_frame,
            text="Hash Algorithms:",
            font=CyberTheme.FONTS["subheading"]
        ).pack(anchor="w", pady=(0, 10))
        
        self.algo_vars = {}
        algorithms = list(HashCalculator.SUPPORTED_ALGORITHMS.keys())
        
        # Create checkboxes in two columns
        cols_frame = StyledFrame(algo_frame)
        cols_frame.pack(fill="x")
        
        # Split algorithms into two columns
        mid = len(algorithms) // 2
        col1_algos = algorithms[:mid]
        col2_algos = algorithms[mid:]
        
        for i, algo_col in enumerate([col1_algos, col2_algos]):
            col_frame = StyledFrame(cols_frame)
            col_frame.pack(side="left", fill="x", expand=True, padx=10)
            
            for algo in algo_col:
                var = ctk.BooleanVar(value=True)
                self.algo_vars[algo] = var
                
                ctk.CTkCheckBox(
                    col_frame,
                    text=algo,
                    variable=var,
                    font=CyberTheme.FONTS["body"]
                ).pack(anchor="w", pady=2)
        
        # Selection buttons
        select_frame = StyledFrame(algo_frame)
        select_frame.pack(fill="x", pady=10)
        
        ctk.CTkButton(
            select_frame,
            text="Select All",
            command=self._select_all,
            width=100,
            height=30
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            select_frame,
            text="Select None",
            command=self._select_none,
            width=100,
            height=30
        ).pack(side="left", padx=5)
        
        # Input methods
        input_frame = StyledFrame(self.frame)
        input_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            input_frame,
            text="Input Source:",
            font=CyberTheme.FONTS["subheading"]
        ).pack(anchor="w", pady=(0, 10))
        
        # File selection
        file_frame = StyledFrame(input_frame)
        file_frame.pack(fill="x", pady=5)
        
        self.file_path = ctk.StringVar()
        
        ctk.CTkEntry(
            file_frame,
            textvariable=self.file_path,
            placeholder_text="Select a file...",
            font=CyberTheme.FONTS["body"]
        ).pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        GlowingButton(
            file_frame,
            text="Browse File",
            command=self._browse_file,
            width=100
        ).pack(side="right")
        
        # Text input
        text_frame = StyledFrame(input_frame)
        text_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            text_frame,
            text="Or enter text:",
            font=CyberTheme.FONTS["body"]
        ).pack(anchor="w", pady=(0, 5))
        
        self.text_input = ctk.CTkTextbox(
            text_frame,
            height=80,
            font=CyberTheme.FONTS["body"]
        )
        self.text_input.pack(fill="x", pady=5)
        
        # Action buttons
        action_frame = StyledFrame(self.frame)
        action_frame.pack(fill="x", pady=10)
        
        self.generate_btn = GlowingButton(
            action_frame,
            text=" GENERATE HASHES",
            command=self._generate_hashes,
            height=40
        )
        self.generate_btn.pack(side="left", padx=5)
        
        self.stop_btn = GlowingButton(
            action_frame,
            text="⏹️ STOP",
            command=self._stop_operation,
            height=40,
            fg_color=CyberTheme.COLORS["accent_danger"]
        )
        self.stop_btn.pack(side="left", padx=5)
        self.stop_btn.configure(state="disabled")
        
        GlowingButton(
            action_frame,
            text="📋 COPY ALL",
            command=self._copy_all,
            height=40
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            action_frame,
            text="🧹 CLEAR",
            command=self._clear,
            height=40
        ).pack(side="left", padx=5)
        
        # Results area
        ctk.CTkLabel(
            self.frame,
            text="Results:",
            font=CyberTheme.FONTS["subheading"]
        ).pack(anchor="w", pady=(10, 5))
        
        self.results_text = TerminalText(
            self.frame,
            height=200
        )
        self.results_text.pack(fill="both", expand=True, pady=(0, 10))
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.frame, height=8)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=5)
        
        self.progress_label = ctk.CTkLabel(
            self.frame,
            text="Ready",
            font=CyberTheme.FONTS["body"],
            text_color=CyberTheme.COLORS["text_secondary"]
        )
        self.progress_label.pack()
    
    def _select_all(self):
        """Select all algorithms"""
        for var in self.algo_vars.values():
            var.set(True)
    
    def _select_none(self):
        """Deselect all algorithms"""
        for var in self.algo_vars.values():
            var.set(False)
    
    def _browse_file(self):
        """Browse for file"""
        path = filedialog.askopenfilename(title="Select file for hashing")
        if path:
            self.file_path.set(path)
            # Clear text input when file is selected
            self.text_input.delete("1.0", "end")
    
    def _generate_hashes(self):
        """Generate hashes based on input"""
        if self.current_operation and self.current_operation.is_alive():
            return  # Operation already running
            
        # Reset stop event
        self.stop_event.clear()
        
        # Get selected algorithms
        selected_algos = [algo for algo, var in self.algo_vars.items() if var.get()]
        if not selected_algos:
            self._show_error("No algorithms selected!")
            return
        
        # Determine input source
        file_path = self.file_path.get().strip()
        text_input = self.text_input.get("1.0", "end-1c").strip()
        
        # Update UI state
        self.generate_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        
        if file_path:
            self._hash_file(file_path, selected_algos)
        elif text_input:
            self._hash_text(text_input, selected_algos)
        else:
            self._show_error("No input provided! Select a file or enter text.")
            self._reset_ui_state()
    
    def _hash_file(self, file_path: str, algorithms: List[str]):
        """Hash a file with progress tracking and termination support"""
        def progress_callback(current, total):
            if self.stop_event.is_set():
                return False  # Signal to stop
                
            progress = current / total if total > 0 else 0
            self.progress_bar.set(progress)
            self.progress_label.configure(
                text=f"Processing: {current}/{total} bytes ({progress:.1%})"
            )
            return True  # Continue
        
        def hash_thread():
            try:
                self.progress_bar.set(0)
                self.progress_label.configure(text="Starting hash calculation...")
                
                hashes = HashCalculator.calculate_file_hashes(
                    file_path,
                    algorithms,
                    progress_callback
                )
                
                if not self.stop_event.is_set():
                    # Update UI in main thread
                    self.master.after(0, self._display_results, hashes, f"File: {Path(file_path).name}")
                
            except Exception as e:
                if not self.stop_event.is_set():
                    self.master.after(0, self._show_error, f"Hash calculation failed: {e}")
            finally:
                self.master.after(0, self._reset_ui_state)
        
        # Run in thread to avoid blocking UI
        self.current_operation = threading.Thread(target=hash_thread, daemon=True)
        self.current_operation.start()
    
    def _hash_text(self, text: str, algorithms: List[str]):
        """Hash text input"""
        try:
            self.progress_label.configure(text="Calculating text hashes...")
            self.progress_bar.set(0.5)
            
            # Small delay to show progress
            time.sleep(0.1)
            
            if self.stop_event.is_set():
                return
                
            hashes = HashCalculator.calculate_text_hashes(text, algorithms)
            
            if not self.stop_event.is_set():
                self.progress_bar.set(1.0)
                self._display_results(hashes, f"Text: {text[:50]}{'...' if len(text) > 50 else ''}")
            
        except Exception as e:
            if not self.stop_event.is_set():
                self._show_error(f"Text hashing failed: {e}")
        finally:
            self._reset_ui_state()
    
    def _stop_operation(self):
        """Stop current operation"""
        self.stop_event.set()
        self.progress_label.configure(text="Stopping operation...")
        self._reset_ui_state()
    
    def _reset_ui_state(self):
        """Reset UI to ready state"""
        self.generate_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.current_operation = None
    
    def _display_results(self, hashes: Dict[str, str], source: str):
        """Display hash results - FIXED tag_config issue"""
        self.results_text.delete("1.0", "end")
        
        # Header with manual formatting instead of tags
        header_text = f"HASH RESULTS - {source}\n"
        separator = "=" * 50 + "\n\n"
        
        self.results_text.insert("end", header_text)
        self.results_text.insert("end", separator)
        
        # Hashes
        max_algo_len = max(len(algo) for algo in hashes.keys())
        
        for algo, hash_val in sorted(hashes.items()):
            algo_padded = algo.ljust(max_algo_len)
            self.results_text.insert("end", f"{algo_padded}: {hash_val}\n")
        
        self.progress_label.configure(text="Calculation complete!")
    
    def _copy_all(self):
        """Copy all results to clipboard"""
        results = self.results_text.get("1.0", "end-1c")
        if results.strip():
            self.master.clipboard_clear()
            self.master.clipboard_append(results)
            self.progress_label.configure(text="Results copied to clipboard!")
    
    def _clear(self):
        """Clear all inputs and results"""
        self._stop_operation()
        self.file_path.set("")
        self.text_input.delete("1.0", "end")
        self.results_text.delete("1.0", "end")
        self.progress_bar.set(0)
        self.progress_label.configure(text="Ready")
    
    def _show_error(self, message: str):
        """Show error message"""
        self.progress_label.configure(text=f"Error: {message}")
        self.progress_bar.set(0)
        
        # Also show in results area
        self.results_text.delete("1.0", "end")
        self.results_text.insert("end", f"ERROR: {message}\n")