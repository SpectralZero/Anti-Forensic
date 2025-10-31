"""
theme.py
Modern Cyberpunk Theme for Anti-Forensic Toolkit
aesthetic with dark colors and neon accents
"""

import customtkinter as ctk

class CyberTheme:
    """Cyberpunk-inspired theme configuration"""
    
    # Color palette - Dark with neon accents (using valid RGB colors)
    COLORS = {
        "bg_primary": "#0a0a12",
        "bg_secondary": "#151520",
        "bg_tertiary": "#1e1e2d",
        "accent_primary": "#00ffff",  # Cyan
        "accent_secondary": "#ff00ff",  # Magenta
        "accent_danger": "#ff4444",  # Red
        "accent_warning": "#ffaa00",  # Amber
        "accent_success": "#00ff88",  # Green
        "text_primary": "#ffffff",
        "text_secondary": "#a0a0c0",
        "text_muted": "#666688",
        "border_light": "#2a2a3a",
        "border_glow": "#00cccc"  # Changed from invalid #00ffff36 to solid color
    }
    
    # Font configurations
    FONTS = {
        "title": ("Consolas", 24, "bold"),
        "heading": ("Consolas", 18, "bold"),
        "subheading": ("Consolas", 21, "bold"),
        "body": ("Segoe UI", 16),
        "monospace": ("Consolas", 18),
        "console": ("Cascadia Code", 14)
    }
    
    @classmethod
    def setup_theme(cls):
        """Configure CTk with our theme"""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Override CTk default colors
        ctk.ThemeManager.theme["color"] = {
            "fg": cls.COLORS["bg_primary"],
            "fg2": cls.COLORS["bg_secondary"],
            "bg": cls.COLORS["bg_primary"],
            "bg2": cls.COLORS["bg_secondary"],
            "accent": cls.COLORS["accent_primary"],
            "text": cls.COLORS["text_primary"],
            "text2": cls.COLORS["text_secondary"],
            "border": cls.COLORS["border_light"]
        }

class StyledFrame(ctk.CTkFrame):
    """Styled frame with cyberpunk aesthetics"""
    
    def __init__(self, master, **kwargs):
        kwargs.setdefault("fg_color", CyberTheme.COLORS["bg_secondary"])
        kwargs.setdefault("border_color", CyberTheme.COLORS["border_light"])
        kwargs.setdefault("border_width", 1)
        super().__init__(master, **kwargs)

class GlowingButton(ctk.CTkButton):
    """Button with glow effect on hover"""
    
    def __init__(self, master, **kwargs):
        # Remove any invalid color parameters
        kwargs.pop("border_glow", None)
        
        kwargs.setdefault("fg_color", CyberTheme.COLORS["accent_primary"])
        kwargs.setdefault("text_color", CyberTheme.COLORS["bg_primary"])
        kwargs.setdefault("hover_color", CyberTheme.COLORS["accent_secondary"])
        kwargs.setdefault("font", CyberTheme.FONTS["body"])
        kwargs.setdefault("border_width", 2)
        kwargs.setdefault("border_color", CyberTheme.COLORS["accent_primary"])
        
        super().__init__(master, **kwargs)
        
        # Store original border color
        self.original_border_color = CyberTheme.COLORS["accent_primary"]
        
        # Bind hover effects
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _on_enter(self, event=None):
        """Handle mouse enter event"""
        try:
            self.configure(border_color=CyberTheme.COLORS["border_glow"])
        except Exception as e:
            # Fallback if border color is invalid
            self.configure(border_color=CyberTheme.COLORS["accent_secondary"])
    
    def _on_leave(self, event=None):
        """Handle mouse leave event - FIXED: added event parameter with default"""
        try:
            self.configure(border_color=self.original_border_color)
        except Exception as e:
            # Fallback to original color
            pass

class DangerButton(GlowingButton):
    """Red danger button for destructive operations"""
    
    def __init__(self, master, **kwargs):
        kwargs["fg_color"] = CyberTheme.COLORS["accent_danger"]
        kwargs["border_color"] = CyberTheme.COLORS["accent_danger"]
        kwargs["hover_color"] = "#ff6666"
        super().__init__(master, **kwargs)
        self.original_border_color = CyberTheme.COLORS["accent_danger"]

class TerminalText(ctk.CTkTextbox):
    """Terminal-style text widget"""
    
    def __init__(self, master, **kwargs):
        kwargs.setdefault("fg_color", CyberTheme.COLORS["bg_primary"])
        kwargs.setdefault("text_color", CyberTheme.COLORS["accent_primary"])
        kwargs.setdefault("font", CyberTheme.FONTS["console"])
        kwargs.setdefault("border_width", 1)
        kwargs.setdefault("border_color", CyberTheme.COLORS["accent_primary"])
        super().__init__(master, **kwargs)

class StatusLED(ctk.CTkLabel):
    """LED-style status indicator"""
    
    def __init__(self, master, **kwargs):
        kwargs.setdefault("text", "●")
        kwargs.setdefault("font", ("Arial", 18))
        kwargs.setdefault("width", 20)
        kwargs.setdefault("height", 20)
        super().__init__(master, **kwargs)
        self.set_off()
    
    def set_on(self, color=None):
        """Turn LED on with specified color"""
        if color is None:
            color = CyberTheme.COLORS["accent_success"]
        self.configure(text_color=color)
    
    def set_off(self):
        """Turn LED off"""
        self.configure(text_color=CyberTheme.COLORS["text_muted"])
    
    def set_warning(self):
        """Set LED to warning color"""
        self.configure(text_color=CyberTheme.COLORS["accent_warning"])
    
    def set_danger(self):
        """Set LED to danger color"""
        self.configure(text_color=CyberTheme.COLORS["accent_danger"])

class ProgressWindow(ctk.CTkToplevel):
    """Standard progress window for long operations"""
    
    def __init__(self, master, title, width=500, height=200):
        super().__init__(master)
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)
        self.configure(fg_color=CyberTheme.COLORS["bg_primary"])
        self.transient(master)
        self.grab_set()
        
        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")
        
        # Header
        ctk.CTkLabel(
            self,
            text=title,
            font=CyberTheme.FONTS["heading"],
            text_color=CyberTheme.COLORS["accent_primary"]
        ).pack(pady=20)
        
        self.progress_bar = ctk.CTkProgressBar(self, width=400, height=20)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)
        
        self.status_label = ctk.CTkLabel(
            self,
            text="Initializing...",
            font=CyberTheme.FONTS["body"],
            text_color=CyberTheme.COLORS["text_secondary"],
            wraplength=400
        )
        self.status_label.pack(pady=10)
    
    def update_progress(self, progress, status=""):
        """Update progress (0.0 to 1.0) and status"""
        try:
            self.progress_bar.set(max(0.0, min(1.0, progress)))
            if status:
                self.status_label.configure(text=status)
            self.update_idletasks()
            return True
        except:
            return False