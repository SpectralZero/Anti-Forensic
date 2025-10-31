"""
main_window.py
ANTI-FORENSIC TOOLKIT - MAIN WINDOW
interface for digital forensic countermeasures
ENHANCED VERSION - Advanced System Intelligence & Network Forensics
"""

import customtkinter as ctk
from pathlib import Path
import threading
import tkinter.messagebox as messagebox

from ui.theme import CyberTheme, StyledFrame, GlowingButton, StatusLED
from ui.shredder_dialogs import ShreddingMenu
from ui.hash_generator import HashGenerator
from core.system_info import AvancedSystemInfo

class AntiForensicApp:
    """Main application class"""
    
    def __init__(self):
        self.root = None
        self.setup_app()
    
    def setup_app(self):
        """Setup the main application"""
        # Configure CTk
        CyberTheme.setup_theme()
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("⚡ ANTI-FORENSIC TOOLKIT - v2.0")
        self.root.geometry("900x700")
        self.root.minsize(1200, 800)
        
        # Configure grid weights for responsiveness
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Sidebar
        self.sidebar = StyledFrame(self.root, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(7, weight=1)
        
        # Main content area
        self.main_content = StyledFrame(self.root)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.setup_sidebar()
        self.setup_dashboard()
    
    def setup_sidebar(self):
        """Setup the navigation sidebar"""
        # Logo/Title
        title_frame = StyledFrame(self.sidebar)
        title_frame.pack(fill="x", padx=15, pady=20)
        
        ctk.CTkLabel(
            title_frame,
            text="Advanced v2.0",
            font=CyberTheme.FONTS["title"],
            text_color=CyberTheme.COLORS["accent_primary"]
        ).pack()
        
        ctk.CTkLabel(
            title_frame,
            text="Advanced Forensic Intelligence",
            font=CyberTheme.FONTS["subheading"],
            text_color=CyberTheme.COLORS["text_secondary"]
        ).pack(pady=(5, 0))
        
        # Navigation buttons
        nav_buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("🗑️ Secure Shredder", self.show_shredder),
            ("🔐 Hash Generator", self.show_hash_generator),
            ("⚡ Quick Clean", self.show_quick_clean),
            ("🛡️ System Intel", self.show_system_info),
            ("⚙️ Settings", self.show_settings),
        ]
        
        self.nav_buttons = {}
        
        for text, command in nav_buttons:
            btn = GlowingButton(
                self.sidebar,
                text=text,
                command=command,
                height=40,
                anchor="w"
            )
            btn.pack(fill="x", padx=10, pady=5)
            self.nav_buttons[text] = btn
        
        # System status
        status_frame = StyledFrame(self.sidebar)
        status_frame.pack(fill="x", padx=10, pady=20, side="bottom")
        
        ctk.CTkLabel(
            status_frame,
            text="System Status:",
            font=CyberTheme.FONTS["subheading"]
        ).pack(anchor="w", pady=(0, 10))
        
        # Status indicators
        status_items = [
            ("Forensic Ready", "on"),
            ("SSD Detected", "warning"),
            ("Admin Rights", "off"),
            ("Secure Mode", "danger"),
        ]
        
        for text, status in status_items:
            item_frame = StyledFrame(status_frame)
            item_frame.pack(fill="x", pady=3)
            
            ctk.CTkLabel(
                item_frame,
                text=text,
                font=CyberTheme.FONTS["body"],
                text_color=CyberTheme.COLORS["text_secondary"]
            ).pack(side="left")
            
            led = StatusLED(item_frame)
            led.pack(side="right")
            
            if status == "on":
                led.set_on()
            elif status == "warning":
                led.set_warning()
            elif status == "danger":
                led.set_danger()
            else:
                led.set_off()
    
    def setup_dashboard(self):
        """Setup the main dashboard"""
        # Clear existing content
        for widget in self.main_content.winfo_children():
            widget.destroy()
        
        # Header
        header_frame = StyledFrame(self.main_content)
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            header_frame,
            text="📊 ADVANCED DASHBOARD",
            font=CyberTheme.FONTS["heading"],
            text_color=CyberTheme.COLORS["accent_primary"]
        ).pack(side="left")
        
        # Quick actions grid
        actions_frame = StyledFrame(self.main_content)
        actions_frame.pack(fill="both", expand=True)
        
        # Create 2x2 grid for quick actions
        actions = [
            {
                "title": "🚀 Secure Shredder",
                "description": "Military-grade file destruction\nMultiple algorithms\nMetadata obfuscation",
                "command": self.show_shredder,
                "color": CyberTheme.COLORS["accent_danger"]
            },
            {
                "title": "🔐 Hash Generator", 
                "description": "Multi-algorithm hashing\nFile & text support\nPerformance benchmarking",
                "command": self.show_hash_generator,
                "color": CyberTheme.COLORS["accent_primary"]
            },
            {
                "title": "⚡ Quick Clean",
                "description": "One-click system cleaning\nBrowser data removal\nLog file wiping",
                "command": self.show_quick_clean,
                "color": CyberTheme.COLORS["accent_warning"]
            },
            {
                "title": "🛡️ System Intel",
                "description": "forensic analysis\nAdvanced threat detection\nNetwork intelligence",
                "command": self.show_system_info,
                "color": CyberTheme.COLORS["accent_success"]
            }
        ]
        
        # Create action buttons in grid
        for i, action in enumerate(actions):
            row = i // 2
            col = i % 2
            
            action_btn = GlowingButton(
                actions_frame,
                text=action["title"],
                command=action["command"],
                height=120,
                fg_color=action["color"],
                font=CyberTheme.FONTS["subheading"]
            )
            action_btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            # Add description label
            desc_label = ctk.CTkLabel(
                actions_frame,
                text=action["description"],
                font=CyberTheme.FONTS["body"],
                text_color=CyberTheme.COLORS["text_secondary"],
                justify="center"
            )
            desc_label.grid(row=row, column=col, padx=20, pady=(80, 20), sticky="sew")
        
        # Configure grid weights
        for i in range(2):
            actions_frame.grid_rowconfigure(i, weight=1)
            actions_frame.grid_columnconfigure(i, weight=1)
        
        # Recent activity
        activity_frame = StyledFrame(self.main_content)
        activity_frame.pack(fill="x", pady=(20, 0))
        
        ctk.CTkLabel(
            activity_frame,
            text="Recent Activity:",
            font=CyberTheme.FONTS["subheading"]
        ).pack(anchor="w", pady=(10, 5))
        
        activity_text = ctk.CTkTextbox(
            activity_frame,
            height=80,
            font=CyberTheme.FONTS["monospace"]
        )
        activity_text.pack(fill="x", pady=(0, 10))
        activity_text.insert("1.0", "• System initialized\n•  v2.0 Ready\n• Enhanced forensic capabilities active")
        activity_text.configure(state="disabled")
    
    def show_dashboard(self):
        """Show dashboard view"""
        self.setup_dashboard()
        self._update_nav_highlight("📊 Dashboard")
    
    def show_shredder(self):
        """Show secure shredder"""
        self._clear_content()
        
        # Header
        header_frame = StyledFrame(self.main_content)
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            header_frame,
            text="🗑️ SECURE SHREDDER",
            font=CyberTheme.FONTS["heading"],
            text_color=CyberTheme.COLORS["accent_danger"]
        ).pack(side="left")
        
        # Launch shredder menu
        GlowingButton(
            header_frame,
            text="OPEN SHREDDER MENU",
            command=lambda: ShreddingMenu.open_shredding_menu(self.root),
            height=40,
            fg_color=CyberTheme.COLORS["accent_danger"]
        ).pack(side="right")
        
        # Information
        info_frame = StyledFrame(self.main_content)
        info_frame.pack(fill="x", pady=10)
        
        info_text = """
⚡ ADVANCED SHREDDING CAPABILITIES:

• Multiple Algorithms:
  - Simple Random (Fast wiping)
  - US DoD 5220.22-M (3-pass military standard)
  - Gutmann Method (35-pass maximum security)
  - RCMP OPS-II (4-pass Canadian standard)

• Advanced Features:
  - Metadata obfuscation (timestamps, filenames)
  - Multiple secure renames
  - SSD detection and warnings
  - Optional garbled file preservation

• Security Notes:
  - All operations are IRREVERSIBLE
  - SSD wiping may not be physically effective
  - Always verify important deletions
  - Use appropriate method for your security needs
        """
        
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=CyberTheme.FONTS["monospace"],
            justify="left"
        )
        info_label.pack(fill="x", padx=20, pady=45)
        
        self._update_nav_highlight("🗑️ Secure Shredder")
    
    def show_hash_generator(self):
        """Show hash generator"""
        self._clear_content()
        
        # Header
        header_frame = StyledFrame(self.main_content)
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            header_frame,
            text="🔐 HASH GENERATOR",
            font=CyberTheme.FONTS["heading"],
            text_color=CyberTheme.COLORS["accent_primary"]
        ).pack(side="left")
        
        # Create hash generator instance
        self.hash_generator = HashGenerator(self.main_content)
        
        self._update_nav_highlight("🔐 Hash Generator")
    
    def show_quick_clean(self):
        """Show quick cleaning options"""
        self._clear_content()
        
        header_frame = StyledFrame(self.main_content)
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            header_frame,
            text="⚡ QUICK CLEAN",
            font=CyberTheme.FONTS["heading"],
            text_color=CyberTheme.COLORS["accent_warning"]
        ).pack(side="left")
        
        # Quick clean options
        from core.forensic_utilities import ForensicCleaner
        
        clean_actions = [
            ("🧹 Clear Browser Data", lambda: self._run_clean_action(ForensicCleaner.clear_browser_data, "Browser data")),
            ("📋 Clear System Logs", lambda: self._run_clean_action(ForensicCleaner.clear_system_logs, "System logs")),
            ("💾 Wipe Free Space", self._wipe_free_space_dialog),
            ("🚀 FULL SYSTEM CLEAN", self._full_clean)
        ]
        
        for text, command in clean_actions:
            btn = GlowingButton(
                self.main_content,
                text=text,
                command=command,
                height=50,
                fg_color=CyberTheme.COLORS["accent_warning"]
            )
            btn.pack(fill="x", pady=8)
        
        self._update_nav_highlight("⚡ Quick Clean")
    
    def show_system_info(self):
        """Show system intelligence with threaded loading"""
        self._clear_content()
        
        header_frame = StyledFrame(self.main_content)
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            header_frame,
            text="🛡️ SYSTEM INTELLIGENCE",
            font=CyberTheme.FONTS["heading"],
            text_color=CyberTheme.COLORS["accent_success"]
        ).pack(side="left")
        
        # Refresh button
        self.refresh_btn = GlowingButton(
            header_frame,
            text="🔄 REFRESH INTEL",
            command=self._refresh_system_info,
            height=40
        )
        self.refresh_btn.pack(side="right")
        
        # Create tabs for different intelligence categories
        self.system_info_tabs = ctk.CTkTabview(self.main_content)
        self.system_info_tabs.pack(fill="both", expand=True, pady=10)
        
        # Add enhanced tabs
        tabs = [
            "Collection Info", "System Intel", "Hardware", "Network Intel", 
            "User Forensics", "Security", "Process Intel", "Software", 
            "Browser Intel", "System Artifacts", "Threat Intel"
        ]
        
        for tab in tabs:
            self.system_info_tabs.add(tab)
            # Add placeholder text immediately
            self._add_placeholder_to_tab(tab, "🔄 Collecting intelligence...")
        
        # Start loading system info in thread
        self._load_system_info_threaded()

    def _add_placeholder_to_tab(self, tab_name, message):
        """Add placeholder text to a tab"""
        try:
            tab = self.system_info_tabs.tab(tab_name)
            # Clear existing content
            for widget in tab.winfo_children():
                widget.destroy()
            
            text_widget = ctk.CTkTextbox(tab, font=CyberTheme.FONTS["monospace"])
            text_widget.pack(fill="both", expand=True, padx=10, pady=10)
            text_widget.insert("1.0", message)
            text_widget.configure(state="disabled")
        except Exception as e:
            print(f"Error adding placeholder to {tab_name}: {e}")

    def _refresh_system_info(self):
        """Refresh system information"""
        self.refresh_btn.configure(state="disabled")
        self._load_system_info_threaded()

    def _load_system_info_threaded(self):
        """Load system information in a separate thread to prevent GUI freezing"""
        # Show loading message in all tabs
        for tab_name in self.system_info_tabs._tab_dict.keys():
            self._add_placeholder_to_tab(tab_name, "🔄 Collecting intelligence...\n\nPlease wait, this may take 10-20 seconds...")
        
        # Start collection in thread
        thread = threading.Thread(target=self._collect_system_info, daemon=True)
        thread.start()

    def _collect_system_info(self):
        """Collect system information in background thread"""
        try:
            # Use the enhanced SystemInfo
            system_info = AvancedSystemInfo.get_forensic_info()
            
            # Update GUI in main thread
            self.root.after(0, lambda: self._display_all_system_info(system_info))
            
        except Exception as e:
            error_msg = f"❌ Failed to collect intelligence: {str(e)}"
            self.root.after(0, lambda: self._display_system_info_error(error_msg))

    def _display_all_system_info(self, system_info):
        """Display all system information in tabs (called from main thread)"""
        try:
            # Update each tab with enhanced data
            self._display_collection_info(self.system_info_tabs.tab("Collection Info"), system_info.get("collection_metadata", {}))
            self._display_system_intel(self.system_info_tabs.tab("System Intel"), system_info.get("system_intelligence", {}))
            self._display_hardware_forensics(self.system_info_tabs.tab("Hardware"), system_info.get("hardware_forensics", {}))
            self._display_network_intel(self.system_info_tabs.tab("Network Intel"), system_info.get("network_intelligence", {}))
            self._display_user_forensics(self.system_info_tabs.tab("User Forensics"), system_info.get("user_forensics", {}))
            self._display_security_posture(self.system_info_tabs.tab("Security"), system_info.get("security_posture", {}))
            self._display_process_forensics(self.system_info_tabs.tab("Process Intel"), system_info.get("process_forensics", {}))
            self._display_software_inventory(self.system_info_tabs.tab("Software"), system_info.get("software_inventory", {}))
            self._display_browser_forensics(self.system_info_tabs.tab("Browser Intel"), system_info.get("browser_forensics", {}))
            self._display_system_artifacts(self.system_info_tabs.tab("System Artifacts"), system_info.get("system_artifacts", {}))
            self._display_threat_indicators(self.system_info_tabs.tab("Threat Intel"), system_info.get("threat_indicators", {}))
            
            # Re-enable refresh button
            self.refresh_btn.configure(state="normal")
            
        except Exception as e:
            self._display_system_info_error(f"❌ Failed to display intelligence: {str(e)}")

    def _display_system_info_error(self, error_msg):
        """Display error message in all tabs"""
        for tab_name in self.system_info_tabs._tab_dict.keys():
            self._add_placeholder_to_tab(tab_name, error_msg)
        self.refresh_btn.configure(state="normal")

    def _display_collection_info(self, parent, collection_metadata):
        """Display collection metadata"""
        text_widget = ctk.CTkTextbox(parent, font=CyberTheme.FONTS["monospace"])
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        if "error" in collection_metadata:
            info_text = f"❌ ERROR: {collection_metadata['error']}"
        else:
            info_text = "=== COLLECTION METADATA ===\n"
            info_text += "=" * 40 + "\n\n"
            
            info_text += "🛡️ INTELLIGENCE COLLECTION\n\n"
            
            for key, value in collection_metadata.items():
                info_text += f"{key.replace('_', ' ').title()}: {value}\n"
        
        text_widget.insert("1.0", info_text)
        text_widget.configure(state="disabled")

    def _display_system_intel(self, parent, system_intelligence):
        """Display enhanced system intelligence"""
        text_widget = ctk.CTkTextbox(parent, font=CyberTheme.FONTS["monospace"])
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        if "error" in system_intelligence:
            info_text = f"❌ ERROR: {system_intelligence['error']}"
        else:
            info_text = "=== SYSTEM INTELLIGENCE ===\n"
            info_text += "=" * 40 + "\n\n"
            
            # Identification
            identification = system_intelligence.get("identification", {})
            info_text += "🔍 IDENTIFICATION:\n"
            for key, value in identification.items():
                info_text += f"  {key.replace('_', ' ').title()}: {value}\n"
            info_text += "\n"
            
            # Platform Details
            platform_details = system_intelligence.get("platform_details", {})
            info_text += "💻 PLATFORM DETAILS:\n"
            for key, value in platform_details.items():
                info_text += f"  {key.replace('_', ' ').title()}: {value}\n"
            info_text += "\n"
            
            # Environment
            environment = system_intelligence.get("environment", {})
            info_text += "🌐 ENVIRONMENT:\n"
            for key, value in environment.items():
                info_text += f"  {key.replace('_', ' ').title()}: {value}\n"
        
        text_widget.insert("1.0", info_text)
        text_widget.configure(state="disabled")

    def _display_hardware_forensics(self, parent, hardware_forensics):
        """Display enhanced hardware forensics"""
        text_widget = ctk.CTkTextbox(parent, font=CyberTheme.FONTS["monospace"])
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        if "error" in hardware_forensics:
            info_text = f"❌ ERROR: {hardware_forensics['error']}"
        else:
            info_text = "=== HARDWARE FORENSICS ===\n"
            info_text += "=" * 40 + "\n\n"
            
            # CPU Forensics
            cpu_forensics = hardware_forensics.get("cpu_forensics", {})
            if "error" not in cpu_forensics:
                info_text += "💻 CPU FORENSICS:\n"
                info_text += f"  Physical Cores: {cpu_forensics.get('physical_cores', 'N/A')}\n"
                info_text += f"  Logical Cores: {cpu_forensics.get('logical_cores', 'N/A')}\n"
                info_text += f"  Current Usage: {cpu_forensics.get('current_usage', 'N/A')}\n"
                info_text += f"  Frequency: {cpu_forensics.get('current_frequency', 'N/A')}\n"
                info_text += "\n"
            
            # Memory Forensics
            memory_forensics = hardware_forensics.get("memory_forensics", {})
            if "error" not in memory_forensics:
                info_text += "🧠 MEMORY FORENSICS:\n"
                info_text += f"  Total: {memory_forensics.get('total', 'N/A')}\n"
                info_text += f"  Available: {memory_forensics.get('available', 'N/A')}\n"
                info_text += f"  Used: {memory_forensics.get('used', 'N/A')}\n"
                info_text += f"  Usage: {memory_forensics.get('usage_percent', 'N/A')}\n"
                info_text += "\n"
            
            # Storage Forensics
            storage_forensics = hardware_forensics.get("storage_forensics", {})
            if "error" not in storage_forensics:
                partitions = storage_forensics.get("partitions", [])
                info_text += f"💾 STORAGE FORENSICS: {len(partitions)} partitions\n"
                for partition in partitions[:3]:  # Show first 3 partitions
                    info_text += f"  Device: {partition.get('device', 'N/A')}\n"
                    info_text += f"  Mount: {partition.get('mountpoint', 'N/A')}\n"
                    info_text += f"  Size: {partition.get('total_size', 'N/A')}\n"
                    info_text += f"  Usage: {partition.get('usage_percent', 'N/A')}\n"
                    info_text += "  ---\n"
        
        text_widget.insert("1.0", info_text)
        text_widget.configure(state="disabled")

    def _display_network_intel(self, parent, network_intelligence):
        """Display enhanced network intelligence"""
        text_widget = ctk.CTkTextbox(parent, font=CyberTheme.FONTS["monospace"])
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        if "error" in network_intelligence:
            info_text = f"❌ ERROR: {network_intelligence['error']}"
        else:
            info_text = "=== NETWORK INTELLIGENCE ===\n"
            info_text += "=" * 40 + "\n\n"
            
            # Public Network
            public_network = network_intelligence.get("public_network", {})
            info_text += "🌐 PUBLIC NETWORK:\n"
            info_text += f"  Public IP: {public_network.get('public_ip', 'N/A')}\n"
            
            geolocation = public_network.get("geolocation", {})
            if geolocation:
                info_text += f"  City: {geolocation.get('city', 'N/A')}\n"
                info_text += f"  Region: {geolocation.get('region', 'N/A')}\n"
                info_text += f"  Country: {geolocation.get('country', 'N/A')}\n"
            info_text += "\n"
            
            # Local Network
            local_network = network_intelligence.get("local_network", {})
            info_text += "🔗 LOCAL NETWORK:\n"
            local_ips = local_network.get("local_ip_addresses", {})
            for interface, ips in list(local_ips.items())[:3]:
                info_text += f"  {interface}: {', '.join(ips[:2])}\n"
            info_text += f"  Gateway: {local_network.get('default_gateway', 'N/A')}\n"
            info_text += "\n"
            
            # Connections
            connections = network_intelligence.get("connections", {})
            tcp_conns = connections.get("tcp_connections", [])
            udp_conns = connections.get("udp_connections", [])
            info_text += f"📡 NETWORK CONNECTIONS: {len(tcp_conns)} TCP, {len(udp_conns)} UDP\n"
        
        text_widget.insert("1.0", info_text)
        text_widget.configure(state="disabled")

    def _display_user_forensics(self, parent, user_forensics):
        """Display enhanced user forensics"""
        text_widget = ctk.CTkTextbox(parent, font=CyberTheme.FONTS["monospace"])
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        if "error" in user_forensics:
            info_text = f"❌ ERROR: {user_forensics['error']}"
        else:
            info_text = "=== USER FORENSICS ===\n"
            info_text += "=" * 40 + "\n\n"
            
            # User Sessions
            user_sessions = user_forensics.get("user_sessions", [])
            info_text += f"👥 USER SESSIONS: {len(user_sessions)}\n"
            for session in user_sessions[:5]:
                info_text += f"  User: {session.get('username', 'N/A')}\n"
                info_text += f"  From: {session.get('host', 'N/A')}\n"
                info_text += f"  Started: {session.get('started', 'N/A')}\n"
                info_text += "  ---\n"
            info_text += "\n"
            
            # Recent Activity
            recent_activity = user_forensics.get("recent_activity", {})
            windows_recent = recent_activity.get("windows_recent", [])
            downloads = recent_activity.get("downloads", [])
            info_text += f"📄 RECENT ACTIVITY: {len(windows_recent)} recent files, {len(downloads)} downloads\n"
            
            # User Environment
            user_environment = user_forensics.get("user_environment", {})
            info_text += f"🏠 USER ENVIRONMENT: {len(user_environment.get('environment_variables', {}))} variables\n"
        
        text_widget.insert("1.0", info_text)
        text_widget.configure(state="disabled")

    def _display_security_posture(self, parent, security_posture):
        """Display enhanced security posture"""
        text_widget = ctk.CTkTextbox(parent, font=CyberTheme.FONTS["monospace"])
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        if "error" in security_posture:
            info_text = f"❌ ERROR: {security_posture['error']}"
        else:
            info_text = "=== SECURITY POSTURE ===\n"
            info_text += "=" * 40 + "\n\n"
            
            # Privilege Analysis
            privilege_analysis = security_posture.get("privilege_analysis", {})
            info_text += "⚡ PRIVILEGE ANALYSIS:\n"
            info_text += f"  Admin Privileges: {privilege_analysis.get('admin_privileges', 'N/A')}\n"
            info_text += f"  Integrity Level: {privilege_analysis.get('integrity_level', 'N/A')}\n"
            info_text += f"  User Groups: {len(privilege_analysis.get('user_groups', []))}\n"
            info_text += "\n"
            
            # Firewall Status
            firewall_status = security_posture.get("firewall_status", {})
            info_text += f"🔥 FIREWALL: {firewall_status.get('status', 'N/A')}\n\n"
            
            # UAC Status
            uac_status = security_posture.get("uac_status", {})
            info_text += f"🛡️ UAC: {uac_status.get('level', 'N/A')}\n\n"
            
            # Antivirus Status - Enhanced Detailed Version
            antivirus_status = security_posture.get("antivirus_status", {})
            info_text += f"🦠 ANTIVIRUS: {antivirus_status.get('status', 'N/A')}\n"
            info_text += f"  Products: {antivirus_status.get('count', 0)} detected\n"

            detected_products = antivirus_status.get('detected_products', [])
            if detected_products:
                info_text += "  Detected Products:\n"
                for i, product in enumerate(detected_products, 1):
                    if isinstance(product, dict):
                        product_name = product.get('name', 'Unknown Product')
                        product_path = product.get('path', 'N/A')
                        product_type = product.get('type', 'N/A')
                        
                        info_text += f"    {i}. {product_name}\n"
                        info_text += f"       Path: {product_path}\n"
                        info_text += f"       Type: {product_type}\n"
                    elif isinstance(product, str):
                        info_text += f"    {i}. {product}\n"
            else:
                info_text += "  No antivirus products detected\n"

        text_widget.insert("1.0", info_text)
        text_widget.configure(state="disabled")

    def _display_process_forensics(self, parent, process_forensics):
        """Display enhanced process forensics"""
        text_widget = ctk.CTkTextbox(parent, font=CyberTheme.FONTS["monospace"])
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        if "error" in process_forensics:
            info_text = f"❌ ERROR: {process_forensics['error']}"
        else:
            info_text = "=== PROCESS FORENSICS ===\n"
            info_text += "=" * 40 + "\n\n"
            
            process_list = process_forensics.get("process_list", [])
            total_processes = process_forensics.get("total_processes", 0)
            suspicious_indicators = process_forensics.get("suspicious_indicators", {})
            
            info_text += f"🔄 TOTAL PROCESSES: {total_processes}\n\n"
            info_text += f"🚨 SUSPICIOUS INDICATORS:\n"
            info_text += f"  Suspicious Names: {len(suspicious_indicators.get('suspicious_names', []))}\n"
            info_text += f"  High Memory Usage: {len(suspicious_indicators.get('high_memory_usage', []))}\n"
            info_text += f"  High CPU Usage: {len(suspicious_indicators.get('high_cpu_usage', []))}\n\n"
            
            info_text += "📊 TOP PROCESSES BY MEMORY:\n"
            for proc in process_list[:10]:
                info_text += f"  {proc.get('name', 'N/A')} (PID: {proc.get('pid', 'N/A')})\n"
                info_text += f"    Memory: {proc.get('memory_mb', 'N/A')} ({proc.get('memory_percent', 'N/A')}%)\n"
                info_text += f"    CPU: {proc.get('cpu_percent', 'N/A')}%\n"
                info_text += f"    User: {proc.get('username', 'N/A')}\n"
                info_text += "    ---\n"
        
        text_widget.insert("1.0", info_text)
        text_widget.configure(state="disabled")

    def _display_software_inventory(self, parent, software_inventory):
        """Display enhanced software inventory"""
        text_widget = ctk.CTkTextbox(parent, font=CyberTheme.FONTS["monospace"])
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        if "error" in software_inventory:
            info_text = f"❌ ERROR: {software_inventory['error']}"
        else:
            info_text = "=== SOFTWARE INVENTORY ===\n"
            info_text += "=" * 40 + "\n\n"
            
            installed_programs = software_inventory.get("installed_programs", [])
            running_services = software_inventory.get("running_services", [])
            
            info_text += f"📦 INSTALLED PROGRAMS: {len(installed_programs)}\n"
            for program in installed_programs[:15]:
                info_text += f"  • {program.get('name', 'N/A')}\n"
            info_text += "\n"
            
            info_text += f"🛠️ RUNNING SERVICES: {len(running_services)}\n"
            for service in running_services[:10]:
                info_text += f"  • {service.get('name', 'N/A')} ({service.get('status', 'N/A')})\n"
        
        text_widget.insert("1.0", info_text)
        text_widget.configure(state="disabled")

    def _display_browser_forensics(self, parent, browser_forensics):
        """Display enhanced browser forensics"""
        text_widget = ctk.CTkTextbox(parent, font=CyberTheme.FONTS["monospace"])
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        if "error" in browser_forensics:
            info_text = f"❌ ERROR: {browser_forensics['error']}"
        else:
            info_text = "=== BROWSER FORENSICS ===\n"
            info_text += "=" * 40 + "\n\n"
            
            detected_browsers = browser_forensics.get("detected_browsers", {})
            forensic_artifacts = browser_forensics.get("forensic_artifacts", {})
            
            info_text += "🌐 DETECTED BROWSERS:\n"
            for browser, info in detected_browsers.items():
                if info.get("installed", False):
                    info_text += f"  ✅ {browser}: INSTALLED\n"
                    info_text += f"     Profile: {info.get('profile_path', 'N/A')}\n"
                else:
                    info_text += f"  ❌ {browser}: NOT INSTALLED\n"
            info_text += "\n"
            
            info_text += "🔍 FORENSIC ARTIFACTS AVAILABLE:\n"
            for artifact, status in forensic_artifacts.items():
                if artifact != "note":
                    info_text += f"  • {artifact.title()}: {status}\n"
        
        text_widget.insert("1.0", info_text)
        text_widget.configure(state="disabled")

    def _display_system_artifacts(self, parent, system_artifacts):
        """Display system artifacts"""
        text_widget = ctk.CTkTextbox(parent, font=CyberTheme.FONTS["monospace"])
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        if "error" in system_artifacts:
            info_text = f"❌ ERROR: {system_artifacts['error']}"
        else:
            info_text = "=== SYSTEM ARTIFACTS ===\n"
            info_text += "=" * 40 + "\n\n"
            
            event_logs = system_artifacts.get("event_logs", [])
            prefetch_files = system_artifacts.get("prefetch_files", [])
            system_logs = system_artifacts.get("system_logs", [])
            
            info_text += f"📊 EVENT LOGS: {len(event_logs)} available\n"
            info_text += f"📁 PREFETCH FILES: {len(prefetch_files)} files\n"
            info_text += f"📋 SYSTEM LOGS: {len(system_logs)} log files\n\n"
            
            info_text += "🔍 RECENT PREFETCH FILES:\n"
            for prefetch in prefetch_files[:5]:
                info_text += f"  • {prefetch.get('filename', 'N/A')}\n"
        
        text_widget.insert("1.0", info_text)
        text_widget.configure(state="disabled")

    def _display_threat_indicators(self, parent, threat_indicators):
        """Display threat indicators"""
        text_widget = ctk.CTkTextbox(parent, font=CyberTheme.FONTS["monospace"])
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        if "error" in threat_indicators:
            info_text = f"❌ ERROR: {threat_indicators['error']}"
        else:
            info_text = "=== THREAT INDICATORS ===\n"
            info_text += "=" * 40 + "\n\n"
            
            suspicious_processes = threat_indicators.get("suspicious_processes", [])
            network_anomalies = threat_indicators.get("network_anomalies", [])
            persistence_mechanisms = threat_indicators.get("persistence_mechanisms", [])
            
            info_text += f"🚨 SUSPICIOUS PROCESSES: {len(suspicious_processes)}\n"
            for proc in suspicious_processes:
                info_text += f"  ⚠️ {proc.get('process', 'N/A')} (PID: {proc.get('pid', 'N/A')})\n"
                info_text += f"    Risk: {proc.get('risk_level', 'N/A')}\n"
            info_text += "\n"
            
            info_text += f"🌐 NETWORK ANOMALIES: {len(network_anomalies)}\n"
            for anomaly in network_anomalies[:5]:
                info_text += f"  • {anomaly.get('type', 'N/A')} (Port: {anomaly.get('port', 'N/A')})\n"
            info_text += "\n"
            
            info_text += f"🕵️ PERSISTENCE MECHANISMS: {len(persistence_mechanisms)} known types\n"
            for mechanism in persistence_mechanisms[:5]:
                info_text += f"  • {mechanism}\n"
        
        text_widget.insert("1.0", info_text)
        text_widget.configure(state="disabled")
    
    def show_settings(self):
        """Show application settings"""
        self._clear_content()
        
        header_frame = StyledFrame(self.main_content)
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            header_frame,
            text="⚙️ SETTINGS",
            font=CyberTheme.FONTS["heading"]
        ).pack(side="left")
        
        # Settings will be implemented in future version
        coming_soon = ctk.CTkLabel(
            self.main_content,
            text="Settings panel coming in v2.0\n\nAdvanced configuration options\nTheme customization\nPerformance settings",
            font=CyberTheme.FONTS["heading"],
            text_color=CyberTheme.COLORS["text_secondary"],
            justify="center"
        )
        coming_soon.pack(expand=True)
        
        self._update_nav_highlight("⚙️ Settings")
    
    def _clear_content(self):
        """Clear main content area"""
        for widget in self.main_content.winfo_children():
            widget.destroy()
    
    def _update_nav_highlight(self, active_button):
        """Update navigation button highlights"""
        for text, button in self.nav_buttons.items():
            if text == active_button:
                button.configure(fg_color=CyberTheme.COLORS["accent_primary"])
            else:
                button.configure(fg_color=CyberTheme.COLORS["bg_tertiary"])
    
    def _run_clean_action(self, action_func, action_name):
        """Run a cleaning action with confirmation"""
        if messagebox.askyesno("Confirm", f"Clear {action_name}? This cannot be undone."):
            success = action_func()
            if success:
                messagebox.showinfo("Success", f"{action_name} cleared successfully")
            else:
                messagebox.showerror("Error", f"Failed to clear {action_name}")
    
    def _wipe_free_space_dialog(self):
        """Open wipe free space dialog"""
        from ui.shredder_dialogs import _wipe_free_space_dialog
        _wipe_free_space_dialog(self.root)
    
    def _full_clean(self):
        """Perform comprehensive full system clean"""
        if not messagebox.askyesno(
            "🚨 FULL SYSTEM CLEAN - DANGER", 
            "THIS WILL PERFORM DESTRUCTIVE CLEANING:\n\n"
            "• 🧹 Clear ALL browser data & cache\n"
            "• 📋 Wipe system and application logs\n" 
            "• 🗑️  Delete temporary files from system\n"
            "• 📄 Remove recent documents history\n"
            "• 🌐 Clear DNS and network cache\n\n"
            "🔒 Some operations require admin rights\n"
            "⏰ This will take several minutes\n"
            "♻️  Some changes require system restart\n\n"
            "THIS ACTION IS IRREVERSIBLE!\n\n"
            "Are you absolutely sure you want to continue?"
        ):
            return
        
        # Create progress window for full clean
        self._run_full_clean_thread()

    def _full_clean_completed(self, success, message, progress_win):
        """Handle completion of full system clean"""
        try:
            if progress_win and progress_win.winfo_exists():
                progress_win.destroy()
        except:
            pass
        
        if success:
            messagebox.showinfo(
                "✅ FULL SYSTEM CLEAN COMPLETE",
                f"{message}\n\n"
                "Recommended actions:\n"
                "• Restart your computer for full effect\n"
                "• Some applications may need re-login\n"
                "• Check browser settings if needed"
            )
        else:
            messagebox.showerror(
                "❌ FULL SYSTEM CLEAN FAILED",
                f"{message}\n\n"
                "Some operations may have completed.\n"
                "Check logs for details."
            )
        
    def _run_full_clean_thread(self):
        """Run full system clean in thread with progress"""
        progress_win = ctk.CTkToplevel(self.root)
        progress_win.title("⚡ FULL SYSTEM CLEAN")
        progress_win.geometry("500x400")
        progress_win.resizable(False, False)
        progress_win.transient(self.root)
        progress_win.grab_set()
        progress_win.configure(fg_color=CyberTheme.COLORS["bg_primary"])
        
        # Header
        ctk.CTkLabel(
            progress_win,
            text="⚡ FULL SYSTEM CLEAN IN PROGRESS",
            font=CyberTheme.FONTS["heading"],
            text_color=CyberTheme.COLORS["accent_danger"]
        ).pack(pady=20)
        
        # Progress frame
        progress_frame = StyledFrame(progress_win)
        progress_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Current step label
        current_step = ctk.CTkLabel(
            progress_frame,
            text="Initializing full system clean...",
            font=CyberTheme.FONTS["subheading"],
            text_color=CyberTheme.COLORS["text_primary"],
            wraplength=400
        )
        current_step.pack(pady=10)
        
        # Progress bar
        progress_bar = ctk.CTkProgressBar(progress_frame, width=400, height=20)
        progress_bar.set(0)
        progress_bar.pack(pady=10)
        
        # Results area
        results_text = ctk.CTkTextbox(
            progress_frame,
            height=150,
            font=CyberTheme.FONTS["monospace"],
            state="disabled"
        )
        results_text.pack(fill="x", pady=10)
        
        # Stop button
        stop_button = GlowingButton(
            progress_frame,
            text="⏹️ STOP CLEANING",
            command=lambda: stop_event.set(),
            fg_color=CyberTheme.COLORS["accent_danger"],
            width=200
        )
        stop_button.pack(pady=10)
        
        stop_event = threading.Event()
        completed_steps = 0
        total_steps = 5
        
        def update_progress(step_name, completed):
            """Update progress in main thread"""
            nonlocal completed_steps
            
            try:
                if progress_win.winfo_exists():
                    if completed:
                        # Add to results
                        results_text.configure(state="normal")
                        results_text.insert("end", f"✅ {step_name}\n")
                        results_text.see("end")
                        results_text.configure(state="disabled")
                        
                        # Update progress bar
                        completed_steps += 1
                        progress_bar.set(completed_steps / total_steps)
                    else:
                        # Update current step
                        current_step.configure(text=step_name)
            except:
                pass
        
        def full_clean_thread():
            """Perform full clean in background thread"""
            try:
                from core.forensic_utilities import ForensicCleaner
                
                # Perform the full clean
                success, summary = ForensicCleaner.perform_full_system_clean(
                    progress_callback=update_progress
                )
                
                # Update UI in main thread
                self.root.after(0, lambda: self._full_clean_completed(success, summary, progress_win))
                
            except Exception as e:
                error_msg = f"Clean failed: {e}"
                self.root.after(0, lambda: self._full_clean_completed(False, error_msg, progress_win))
        
        # Start the cleaning thread
        thread = threading.Thread(target=full_clean_thread, daemon=True)
        thread.start()
        
        # Center the window
        progress_win.update_idletasks()
        x = (progress_win.winfo_screenwidth() // 2) - (500 // 2)
        y = (progress_win.winfo_screenheight() // 2) - (400 // 2)
        progress_win.geometry(f"+{x}+{y}")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = AntiForensicApp()
    app.run()