import customtkinter as ctk
from tkinter import messagebox, filedialog
import json
import datetime
import threading
import time
from shared import load_json_file, save_json_file, log_event

class AdminApp:
    def __init__(self, username):
        self.username = username
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        
        self.root = ctk.CTk()
        self.root.title(f"SecureVault - Admin Dashboard [{username}]")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # Center the window
        self.center_window()
        
        # Auto-refresh flag
        self.auto_refresh = True
        
        # Log admin session start
        log_event(self.username, "admin_session_start", f"Admin dashboard opened by {username}")
        
        self.setup_ui()
        self.refresh_data()
        self.start_auto_refresh()
        
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def setup_ui(self):
        # Header with admin info and controls
        header_frame = ctk.CTkFrame(self.root, height=90)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        # Left side - Admin info
        admin_info_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        admin_info_frame.pack(side="left", fill="y", padx=15, pady=15)
        
        title_label = ctk.CTkLabel(
            admin_info_frame, text="🛡️ SecureVault Admin Dashboard",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(anchor="w")
        
        admin_label = ctk.CTkLabel(
            admin_info_frame, text=f"👨‍💼 Administrator: {self.username} | 🔑 Role: ADMIN",
            font=ctk.CTkFont(size=12), text_color="orange"
        )
        admin_label.pack(anchor="w")
        
        session_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session_label = ctk.CTkLabel(
            admin_info_frame, text=f"🕒 Session: {session_time} | 🔄 Auto-refresh: ON",
            font=ctk.CTkFont(size=10), text_color="gray70"
        )
        session_label.pack(anchor="w")
        
        # Right side - Controls
        controls_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        controls_frame.pack(side="right", fill="y", padx=15, pady=15)
        
        refresh_button = ctk.CTkButton(
            controls_frame, text="🔄 Refresh Now", width=120, height=30,
            command=self.manual_refresh, font=ctk.CTkFont(size=11)
        )
        refresh_button.pack(pady=(0, 5))
        
        logout_button = ctk.CTkButton(
            controls_frame, text="🚪 Logout", width=120, height=30,
            command=self.logout, font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=("#CC4125", "#8B0000"), hover_color=("#B23A1F", "#A00000")
        )
        logout_button.pack()
        
        # Main tabview
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_users_tab()
        self.create_logs_tab()
        self.create_files_tab()
        self.create_activity_tab()
        self.create_tools_tab()
        
        # Status bar
        self.status_frame = ctk.CTkFrame(self.root, height=40)
        self.status_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.status_frame.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame, text="🟢 Admin Dashboard Active - Monitoring System",
            font=ctk.CTkFont(size=12), text_color="green"
        )
        self.status_label.pack(pady=10)
        
    def create_dashboard_tab(self):
        tab = self.tabview.add("📊 Dashboard")
        
        # Stats section
        stats_frame = ctk.CTkFrame(tab)
        stats_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            stats_frame, text="📈 System Statistics", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 15))
        
        # Stats grid
        stats_grid = ctk.CTkFrame(stats_frame)
        stats_grid.pack(fill="x", padx=20, pady=(0, 20))
        
        # Statistics cards
        self.total_users_label = ctk.CTkLabel(
            stats_grid, text="👥 Total Users: 0", 
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("#1f538d", "#14375e"), corner_radius=10, height=60
        )
        self.total_users_label.grid(row=0, column=0, padx=8, pady=8, sticky="ew")
        
        self.total_logs_label = ctk.CTkLabel(
            stats_grid, text="📋 Total Logs: 0", 
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("#1f538d", "#14375e"), corner_radius=10, height=60
        )
        self.total_logs_label.grid(row=0, column=1, padx=8, pady=8, sticky="ew")
        
        self.total_files_label = ctk.CTkLabel(
            stats_grid, text="📁 Files Accessed: 0", 
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("#1f538d", "#14375e"), corner_radius=10, height=60
        )
        self.total_files_label.grid(row=0, column=2, padx=8, pady=8, sticky="ew")
        
        self.active_sessions_label = ctk.CTkLabel(
            stats_grid, text="🔄 Active Sessions: 0", 
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("#1f538d", "#14375e"), corner_radius=10, height=60
        )
        self.active_sessions_label.grid(row=1, column=0, padx=8, pady=8, sticky="ew")
        
        self.encryption_ops_label = ctk.CTkLabel(
            stats_grid, text="🔐 Encryption Ops: 0", 
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("#1f538d", "#14375e"), corner_radius=10, height=60
        )
        self.encryption_ops_label.grid(row=1, column=1, padx=8, pady=8, sticky="ew")
        
        self.last_activity_label = ctk.CTkLabel(
            stats_grid, text="🕒 Last Activity: N/A", 
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("#1f538d", "#14375e"), corner_radius=10, height=60
        )
        self.last_activity_label.grid(row=1, column=2, padx=8, pady=8, sticky="ew")
        
        # Configure grid weights
        for i in range(3):
            stats_grid.grid_columnconfigure(i, weight=1)
            
        # Recent activity section
        activity_frame = ctk.CTkFrame(tab)
        activity_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        activity_header = ctk.CTkFrame(activity_frame, height=50)
        activity_header.pack(fill="x", padx=15, pady=(15, 5))
        activity_header.pack_propagate(False)
        
        ctk.CTkLabel(
            activity_header, text="⚡ Recent System Activity", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left", pady=15)
        
        self.auto_refresh_label = ctk.CTkLabel(
            activity_header, text="🔄 Auto-refresh: ON", 
            font=ctk.CTkFont(size=10), text_color="green"
        )
        self.auto_refresh_label.pack(side="right", pady=15)
        
        self.activity_text = ctk.CTkTextbox(activity_frame, height=200)
        self.activity_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
    def create_users_tab(self):
        tab = self.tabview.add("👥 Users")
        
        # Header with controls
        header = ctk.CTkFrame(tab, height=60)
        header.pack(fill="x", padx=20, pady=(20, 10))
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header, text="👥 Registered Users Management", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left", padx=15, pady=15)
        
        refresh_users_button = ctk.CTkButton(
            header, text="🔄 Refresh Users", 
            command=self.refresh_users, width=130, height=30
        )
        refresh_users_button.pack(side="right", padx=15, pady=15)
        
        # Users display
        users_frame = ctk.CTkFrame(tab)
        users_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.users_text = ctk.CTkTextbox(
            users_frame, font=ctk.CTkFont(family="Courier New", size=11)
        )
        self.users_text.pack(fill="both", expand=True, padx=15, pady=15)
        
    def create_logs_tab(self):
        tab = self.tabview.add("📋 System Logs")
        
        # Controls
        controls_frame = ctk.CTkFrame(tab, height=60)
        controls_frame.pack(fill="x", padx=20, pady=(20, 10))
        controls_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            controls_frame, text="📋 Complete System Activity Logs", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left", padx=15, pady=15)
        
        controls_right = ctk.CTkFrame(controls_frame, fg_color="transparent")
        controls_right.pack(side="right", padx=15, pady=15)
        
        filter_button = ctk.CTkButton(
            controls_right, text="🔍 Filter", 
            command=self.show_log_filter, width=80, height=30
        )
        filter_button.pack(side="left", padx=(0, 5))
        
        refresh_logs_button = ctk.CTkButton(
            controls_right, text="🔄 Refresh", 
            command=self.refresh_logs, width=80, height=30
        )
        refresh_logs_button.pack(side="left")
        
        # Logs display
        logs_frame = ctk.CTkFrame(tab)
        logs_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.logs_text = ctk.CTkTextbox(
            logs_frame, font=ctk.CTkFont(family="Courier New", size=10)
        )
        self.logs_text.pack(fill="both", expand=True, padx=15, pady=15)
        
    def create_files_tab(self):
        tab = self.tabview.add("📁 File Tracking")
        
        # Header
        header = ctk.CTkFrame(tab, height=60)
        header.pack(fill="x", padx=20, pady=(20, 10))
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header, text="📁 File Access Monitoring", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left", padx=15, pady=15)
        
        refresh_files_button = ctk.CTkButton(
            header, text="🔄 Refresh Files", 
            command=self.refresh_files, width=130, height=30
        )
        refresh_files_button.pack(side="right", padx=15, pady=15)
        
        # Files display
        files_frame = ctk.CTkFrame(tab)
        files_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.files_text = ctk.CTkTextbox(
            files_frame, font=ctk.CTkFont(family="Courier New", size=11)
        )
        self.files_text.pack(fill="both", expand=True, padx=15, pady=15)
        
    def create_activity_tab(self):
        tab = self.tabview.add("🔐 Encryption Activity")
        
        # Header
        header = ctk.CTkFrame(tab, height=60)
        header.pack(fill="x", padx=20, pady=(20, 10))
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header, text="🔐 Encryption/Decryption Activity Monitor", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left", padx=15, pady=15)
        
        refresh_activity_button = ctk.CTkButton(
            header, text="🔄 Refresh Activity", 
            command=self.refresh_encryption_activity, width=150, height=30
        )
        refresh_activity_button.pack(side="right", padx=15, pady=15)
        
        # Activity display
        activity_frame = ctk.CTkFrame(tab)
        activity_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.encryption_activity_text = ctk.CTkTextbox(
            activity_frame, font=ctk.CTkFont(family="Courier New", size=11)
        )
        self.encryption_activity_text.pack(fill="both", expand=True, padx=15, pady=15)
        
    def create_tools_tab(self):
        tab = self.tabview.add("🛠️ Admin Tools")
        
        # Tools grid
        tools_main_frame = ctk.CTkFrame(tab)
        tools_main_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            tools_main_frame, text="🛠️ Administrative Tools & System Management", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 15))
        
        # Tools grid layout
        tools_grid = ctk.CTkFrame(tools_main_frame)
        tools_grid.pack(fill="x", padx=20, pady=(0, 20))
        
        # Row 1 - Data Management
        refresh_all_button = ctk.CTkButton(
            tools_grid, text="🔄 Refresh All Data", 
            command=self.refresh_data, height=45, width=180,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        refresh_all_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        clear_logs_button = ctk.CTkButton(
            tools_grid, text="🗑️ Clear System Logs", 
            command=self.clear_logs, height=45, width=180,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#CC4125", "#8B0000"), hover_color=("#B23A1F", "#A00000")
        )
        clear_logs_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        export_button = ctk.CTkButton(
            tools_grid, text="💾 Export All Data", 
            command=self.export_data, height=45, width=180,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        export_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        
        # Row 2 - System Management
        backup_button = ctk.CTkButton(
            tools_grid, text="💾 Create Backup", 
            command=self.create_backup, height=45, width=180,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        backup_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        system_info_button = ctk.CTkButton(
            tools_grid, text="ℹ️ System Info", 
            command=self.show_system_info, height=45, width=180,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        system_info_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        toggle_refresh_button = ctk.CTkButton(
            tools_grid, text="⏸️ Toggle Auto-Refresh", 
            command=self.toggle_auto_refresh, height=45, width=180,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        toggle_refresh_button.grid(row=1, column=2, padx=10, pady=10, sticky="ew")
        
        # Configure grid weights
        for i in range(3):
            tools_grid.grid_columnconfigure(i, weight=1)
            
        # Tools output section
        output_frame = ctk.CTkFrame(tab)
        output_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        ctk.CTkLabel(
            output_frame, text="📤 Tool Output & System Messages", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 5))
        
        self.tools_output_text = ctk.CTkTextbox(output_frame, height=200)
        self.tools_output_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
    def manual_refresh(self):
        """Manual refresh triggered by button"""
        self.refresh_data()
        self.update_status("🔄 Manual refresh completed")
        
    def start_auto_refresh(self):
        """Start auto-refresh thread"""
        def auto_refresh_loop():
            while self.auto_refresh:
                time.sleep(10)  # Refresh every 10 seconds
                if self.auto_refresh:
                    self.root.after(0, self.refresh_data)
        
        refresh_thread = threading.Thread(target=auto_refresh_loop, daemon=True)
        refresh_thread.start()
        
    def toggle_auto_refresh(self):
        """Toggle auto-refresh on/off"""
        self.auto_refresh = not self.auto_refresh
        status_text = "ON" if self.auto_refresh else "OFF"
        color = "green" if self.auto_refresh else "red"
        
        self.auto_refresh_label.configure(
            text=f"🔄 Auto-refresh: {status_text}",
            text_color=color
        )
        
        if self.auto_refresh:
            self.start_auto_refresh()
            self.update_status("🔄 Auto-refresh enabled")
        else:
            self.update_status("⏸️ Auto-refresh disabled")
            
        log_event(self.username, "admin_toggle_refresh", f"Auto-refresh {status_text}")
        
    def refresh_data(self):
        """Refresh all dashboard data"""
        try:
            # Load all data files
            users_data = load_json_file("data/users_data.json")
            logs_data = load_json_file("data/system_logs.json")
            files_data = load_json_file("data/files_data.json")
            encryption_data = load_json_file("data/encryption_activity.json")
            
            # Calculate statistics
            total_users = len(users_data)
            total_logs = len(logs_data)
            total_files = len(files_data)
            
            # Count encryption operations
            encryption_ops = len(encryption_data)
            
            # Count active sessions (recent logins without logout)
            active_sessions = self.count_active_sessions(logs_data)
            
            # Get last activity timestamp
            last_activity = self.get_last_activity(logs_data)
            
            # Update dashboard stats
            self.total_users_label.configure(text=f"👥 Total Users: {total_users}")
            self.total_logs_label.configure(text=f"📋 Total Logs: {total_logs}")
            self.total_files_label.configure(text=f"📁 Files Accessed: {total_files}")
            self.active_sessions_label.configure(text=f"🔄 Active Sessions: {active_sessions}")
            self.encryption_ops_label.configure(text=f"🔐 Encryption Ops: {encryption_ops}")
            self.last_activity_label.configure(text=f"🕒 Last Activity: {last_activity}")
            
            # Update recent activity display
            self.update_recent_activity(logs_data)
            
            # Update other tabs if they're currently visible
            current_tab = self.tabview.get()
            if "Users" in current_tab:
                self.update_users_display(users_data)
            elif "Logs" in current_tab:
                self.update_logs_display(logs_data)
            elif "Files" in current_tab:
                self.update_files_display(files_data)
            elif "Activity" in current_tab:
                self.update_encryption_activity_display(encryption_data)
                
        except Exception as e:
            self.update_status(f"❌ Refresh failed: {str(e)}")
            
    def count_active_sessions(self, logs_data):
        """Count currently active user sessions"""
        recent_logins = {}
        cutoff_time = datetime.datetime.now() - datetime.timedelta(hours=1)
        
        for log in logs_data:
            try:
                log_time = datetime.datetime.fromisoformat(log.get('timestamp', ''))
                if log_time > cutoff_time:
                    username = log.get('username', '')
                    action = log.get('action', '')
                    
                    if 'login' in action and 'client_session_start' in action:
                        recent_logins[username] = log_time
                    elif 'logout' in action and username in recent_logins:
                        del recent_logins[username]
            except:
                continue
                
        return len(recent_logins)
        
    def get_last_activity(self, logs_data):
        """Get timestamp of last system activity"""
        if not logs_data:
            return "No activity"
            
        try:
            latest_log = max(logs_data, key=lambda x: x.get('timestamp', ''))
            timestamp = latest_log.get('timestamp', '')
            if timestamp:
                dt = datetime.datetime.fromisoformat(timestamp)
                return dt.strftime("%H:%M:%S")
        except:
            pass
            
        return "Unknown"
        
    def update_recent_activity(self, logs_data):
        """Update recent activity display"""
        self.activity_text.delete("0.0", "end")
        
        # Get last 15 log entries
        recent_logs = sorted(logs_data, key=lambda x: x.get('timestamp', ''), reverse=True)[:15]
        
        activity_text = "⚡ LIVE SYSTEM ACTIVITY MONITOR\n"
        activity_text += "=" * 80 + "\n"
        activity_text += f"🕒 Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        activity_text += f"📊 Showing {len(recent_logs)} most recent entries\n"
        activity_text += "=" * 80 + "\n\n"
        
        for i, log in enumerate(recent_logs, 1):
            timestamp = log.get('timestamp', 'Unknown')
            username = log.get('username', 'Unknown')
            action = log.get('action', 'Unknown')
            details = log.get('details', 'No details')
            
            # Format timestamp
            try:
                dt = datetime.datetime.fromisoformat(timestamp)
                formatted_time = dt.strftime("%H:%M:%S")
                formatted_date = dt.strftime("%Y-%m-%d")
            except:
                formatted_time = timestamp[:8] if len(timestamp) > 8 else timestamp
                formatted_date = timestamp[:10] if len(timestamp) > 10 else timestamp
            
            # Color-code different actions
            action_icon = self.get_action_icon(action)
            
            activity_text += f"{i:2d}. {action_icon} [{formatted_time}] {username}\n"
            activity_text += f"    📅 Date: {formatted_date}\n"
            activity_text += f"    ⚡ Action: {action}\n"
            activity_text += f"    📝 Details: {details}\n"
            activity_text += "-" * 60 + "\n\n"
            
        self.activity_text.insert("0.0", activity_text)
        
    def get_action_icon(self, action):
        """Get appropriate icon for action type"""
        action_icons = {
            'login': '🔓',
            'logout': '🔒',
            'register': '📝',
            'file_access': '📁',
            'text_encryption': '🔐',
            'text_decryption': '🔓',
            'admin_session_start': '🛡️',
            'admin_logout': '🚪',
            'client_session_start': '👤',
            'client_logout': '👋'
        }
        return action_icons.get(action, '⚡')
        
    def update_users_display(self, users_data):
        """Update users tab display"""
        self.users_text.delete("0.0", "end")
        
        users_text = "👥 REGISTERED USERS DATABASE\n"
        users_text += "=" * 80 + "\n"
        users_text += f"📊 Total Users: {len(users_data)}\n"
        users_text += f"🕒 Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        users_text += "=" * 80 + "\n\n"
        
        # Separate admins and users
        admins = {k: v for k, v in users_data.items() if v.get('role') == 'admin'}
        regular_users = {k: v for k, v in users_data.items() if v.get('role') == 'user'}
        
        # Display admins first
        if admins:
            users_text += "🛡️  ADMINISTRATORS:\n" + "-" * 40 + "\n"
            for username, info in admins.items():
                users_text += f"👤 Username: {username}\n"
                users_text += f"🔑 Role: {info.get('role', 'user').upper()}\n"
                users_text += f"🔒 Password Hash: {info.get('password_hash', 'N/A')[:30]}...\n"
                users_text += f"🆔 User ID: {hash(username) % 10000:04d}\n\n"
                
        # Display regular users
        if regular_users:
            users_text += "👤 REGULAR USERS:\n" + "-" * 40 + "\n"
            for username, info in regular_users.items():
                # Get user activity summary
                activity_summary = self.get_user_activity_summary(username)
                
                users_text += f"👤 Username: {username}\n"
                users_text += f"🔑 Role: {info.get('role', 'user').upper()}\n"
                users_text += f"🔒 Password Hash: {info.get('password_hash', 'N/A')[:30]}...\n"
                users_text += f"🆔 User ID: {hash(username) % 10000:04d}\n"
                users_text += f"📊 Activity: {activity_summary}\n\n"
                
        self.users_text.insert("0.0", users_text)
        
    def get_user_activity_summary(self, username):
        """Get activity summary for a specific user"""
        try:
            logs_data = load_json_file("data/system_logs.json")
            user_logs = [log for log in logs_data if log.get('username') == username]
            
            login_count = len([log for log in user_logs if 'login' in log.get('action', '')])
            file_access_count = len([log for log in user_logs if 'file_access' in log.get('action', '')])
            encryption_count = len([log for log in user_logs if 'encryption' in log.get('action', '')])
            
            return f"Logins: {login_count}, Files: {file_access_count}, Encryption: {encryption_count}"
        except:
            return "No activity recorded"
            
    def update_logs_display(self, logs_data):
        """Update system logs display"""
        self.logs_text.delete("0.0", "end")
        
        logs_text = "📋 COMPLETE SYSTEM ACTIVITY LOGS\n"
        logs_text += "=" * 100 + "\n"
        logs_text += f"📊 Total Log Entries: {len(logs_data)}\n"
        logs_text += f"🕒 Report Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        logs_text += "=" * 100 + "\n\n"
        
        # Sort logs by timestamp (newest first)
        sorted_logs = sorted(logs_data, key=lambda x: x.get('timestamp', ''), reverse=True)
        
        for i, log in enumerate(sorted_logs, 1):
            timestamp = log.get('timestamp', 'Unknown')
            username = log.get('username', 'Unknown')
            action = log.get('action', 'Unknown')
            details = log.get('details', 'No details')
            
            # Format timestamp
            try:
                dt = datetime.datetime.fromisoformat(timestamp)
                formatted_datetime = dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                formatted_datetime = timestamp
                
            action_icon = self.get_action_icon(action)
            
            logs_text += f"{i:3d}. {action_icon} [{formatted_datetime}] USER: {username}\n"
            logs_text += f"     ⚡ ACTION: {action}\n"
            logs_text += f"     📝 DETAILS: {details}\n"
            logs_text += "-" * 80 + "\n\n"
            
        self.logs_text.insert("0.0", logs_text)
        
    def update_files_display(self, files_data):
        """Update file tracking display"""
        self.files_text.delete("0.0", "end")
        
        files_text = "📁 FILE ACCESS MONITORING REPORT\n"
        files_text += "=" * 100 + "\n"
        files_text += f"📊 Total Files Tracked: {len(files_data)}\n"
        files_text += f"🕒 Report Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        files_text += "=" * 100 + "\n\n"
        
        if not files_data:
            files_text += "📭 No file activity recorded yet.\n"
        else:
            # Sort by last access time
            sorted_files = sorted(
                files_data.items(), 
                key=lambda x: x[1].get('last_access', ''), 
                reverse=True
            )
            
            for i, (filename, info) in enumerate(sorted_files, 1):
                files_text += f"{i:2d}. 📄 FILE: {filename}\n"
                files_text += f"    📂 Path: {info.get('full_path', 'N/A')}\n"
                files_text += f"    📊 Size: {info.get('file_size', 0)} bytes\n"
                files_text += f"    🔢 Access Count: {info.get('accessed_count', 0)}\n"
                files_text += f"    🕒 First Access: {info.get('first_access', 'Never')}\n"
                files_text += f"    🕕 Last Access: {info.get('last_access', 'Never')}\n"
                
                accessed_by = info.get('accessed_by', [])
                if accessed_by:
                    files_text += f"    👥 Accessed By: {', '.join(accessed_by)}\n"
                else:
                    files_text += f"    👥 Accessed By: Unknown\n"
                    
                files_text += "-" * 70 + "\n\n"
                
        self.files_text.insert("0.0", files_text)
        
    def update_encryption_activity_display(self, encryption_data):
        """Update encryption activity display"""
        self.encryption_activity_text.delete("0.0", "end")
        
        activity_text = "🔐 ENCRYPTION/DECRYPTION ACTIVITY MONITOR\n"
        activity_text += "=" * 100 + "\n"
        activity_text += f"📊 Total Operations: {len(encryption_data)}\n"
        activity_text += f"🕒 Report Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        activity_text += "=" * 100 + "\n\n"
        
        if not encryption_data:
            activity_text += "📭 No encryption/decryption activity recorded yet.\n"
        else:
            # Sort by timestamp (newest first)
            sorted_activity = sorted(
                encryption_data, 
                key=lambda x: x.get('timestamp', ''), 
                reverse=True
            )
            
            # Group by user for better analysis
            user_stats = {}
            for activity in sorted_activity:
                username = activity.get('username', 'Unknown')
                if username not in user_stats:
                    user_stats[username] = {'encryption': 0, 'decryption': 0}
                action = activity.get('action', '')
                if action in user_stats[username]:
                    user_stats[username][action] += 1
                    
            # Display user statistics
            activity_text += "👥 USER ACTIVITY SUMMARY:\n" + "-" * 50 + "\n"
            for username, stats in user_stats.items():
                total_ops = stats['encryption'] + stats['decryption']
                activity_text += f"👤 {username}: {total_ops} operations (🔐 {stats['encryption']} encrypt, 🔓 {stats['decryption']} decrypt)\n"
            activity_text += "\n"
            
            # Display detailed activity log
            activity_text += "🔍 DETAILED ACTIVITY LOG:\n" + "-" * 50 + "\n"
            for i, activity in enumerate(sorted_activity[:20], 1):  # Show last 20 operations
                timestamp = activity.get('timestamp', 'Unknown')
                username = activity.get('username', 'Unknown')
                action = activity.get('action', 'Unknown')
                
                try:
                    dt = datetime.datetime.fromisoformat(timestamp)
                    formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    formatted_time = timestamp
                    
                action_icon = "🔐" if action == "encryption" else "🔓"
                
                activity_text += f"{i:2d}. {action_icon} [{formatted_time}] {username}\n"
                activity_text += f"    ⚡ Operation: {action.upper()}\n"
                
                if action == "encryption":
                    orig_len = activity.get('original_length', 0)
                    enc_len = activity.get('encrypted_length', 0)
                    activity_text += f"    📊 Data: {orig_len} chars → {enc_len} chars (Base64)\n"
                elif action == "decryption":
                    enc_len = activity.get('encrypted_length', 0)
                    dec_len = activity.get('decrypted_length', 0)
                    activity_text += f"    📊 Data: {enc_len} chars (Base64) → {dec_len} chars\n"
                    
                session_id = activity.get('session_id', 'N/A')
                activity_text += f"    🆔 Session: {session_id}\n"
                activity_text += "-" * 60 + "\n\n"
                
        self.encryption_activity_text.insert("0.0", activity_text)
        
    def refresh_users(self):
        """Refresh users tab"""
        users_data = load_json_file("data/users_data.json")
        self.update_users_display(users_data)
        self.update_status("👥 User data refreshed")
        
    def refresh_logs(self):
        """Refresh logs tab"""
        logs_data = load_json_file("data/system_logs.json")
        self.update_logs_display(logs_data)
        self.update_status("📋 System logs refreshed")
        
    def refresh_files(self):
        """Refresh files tab"""
        files_data = load_json_file("data/files_data.json")
        self.update_files_display(files_data)
        self.update_status("📁 File tracking data refreshed")
        
    def refresh_encryption_activity(self):
        """Refresh encryption activity tab"""
        encryption_data = load_json_file("data/encryption_activity.json")
        self.update_encryption_activity_display(encryption_data)
        self.update_status("🔐 Encryption activity refreshed")
        
    def show_log_filter(self):
        """Show log filtering options"""
        filter_window = ctk.CTkToplevel(self.root)
        filter_window.title("Log Filter")
        filter_window.geometry("400x300")
        filter_window.transient(self.root)
        filter_window.grab_set()
        
        # Center the filter window
        filter_window.update_idletasks()
        x = (filter_window.winfo_screenwidth() // 2) - (200)
        y = (filter_window.winfo_screenheight() // 2) - (150)
        filter_window.geometry(f"400x300+{x}+{y}")
        
        # Filter options
        ctk.CTkLabel(filter_window, text="🔍 Log Filter Options", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        # User filter
        ctk.CTkLabel(filter_window, text="Filter by User:").pack(anchor="w", padx=20)
        user_entry = ctk.CTkEntry(filter_window, placeholder_text="Enter username or leave empty")
        user_entry.pack(fill="x", padx=20, pady=(5, 15))
        
        # Action filter
        ctk.CTkLabel(filter_window, text="Filter by Action:").pack(anchor="w", padx=20)
        action_entry = ctk.CTkEntry(filter_window, placeholder_text="Enter action type or leave empty")
        action_entry.pack(fill="x", padx=20, pady=(5, 15))
        
        # Apply filter button
        def apply_filter():
            user_filter = user_entry.get().strip()
            action_filter = action_entry.get().strip()
            self.apply_log_filter(user_filter, action_filter)
            filter_window.destroy()
            
        apply_button = ctk.CTkButton(filter_window, text="Apply Filter", command=apply_filter)
        apply_button.pack(pady=20)
        
    def apply_log_filter(self, user_filter, action_filter):
        """Apply filters to log display"""
        logs_data = load_json_file("data/system_logs.json")
        
        # Filter logs
        filtered_logs = logs_data
        if user_filter:
            filtered_logs = [log for log in filtered_logs if user_filter.lower() in log.get('username', '').lower()]
        if action_filter:
            filtered_logs = [log for log in filtered_logs if action_filter.lower() in log.get('action', '').lower()]
            
        self.update_logs_display(filtered_logs)
        self.update_status(f"🔍 Filter applied: {len(filtered_logs)} of {len(logs_data)} logs shown")
        
    def clear_logs(self):
        """Clear all system logs with confirmation"""
        result = messagebox.askyesno(
            "⚠️ Confirm Clear Logs", 
            "Are you sure you want to clear ALL system logs?\n\n"
            "This action will permanently delete:\n"
            "• All user activity logs\n"
            "• All admin activity logs\n"
            "• All system event logs\n\n"
            "This action CANNOT be undone!"
        )
        
        if result:
            try:
                # Backup logs before clearing
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_filename = f"logs_backup_{timestamp}.json"
                
                logs_data = load_json_file("data/system_logs.json")
                save_json_file(f"data/backups/{backup_filename}", logs_data)
                
                # Clear logs
                save_json_file("data/system_logs.json", [])
                
                # Log the clearing action
                log_event(self.username, "admin_clear_logs", f"All system logs cleared by admin (backup saved as {backup_filename})")
                
                # Refresh display
                self.refresh_data()
                
                self.tools_output_text.delete("0.0", "end")
                self.tools_output_text.insert("0.0", 
                    f"✅ LOGS CLEARED SUCCESSFULLY\n"
                    f"🕒 Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"💾 Backup saved: {backup_filename}\n"
                    f"🗑️ All previous logs have been permanently deleted.\n"
                    f"📊 System logs reset to zero entries."
                )
                
                self.update_status("🗑️ All system logs cleared successfully")
                
            except Exception as e:
                error_msg = f"Failed to clear logs: {str(e)}"
                messagebox.showerror("Clear Logs Error", error_msg)
                log_event(self.username, "admin_clear_logs_error", error_msg)
                self.update_status("❌ Log clearing failed")
                
    def export_data(self):
        """Export all system data to JSON file"""
        try:
            # Load all data
            users_data = load_json_file("data/users_data.json")
            logs_data = load_json_file("data/system_logs.json")
            files_data = load_json_file("data/files_data.json")
            encryption_data = load_json_file("data/encryption_activity.json")
            
            # Create comprehensive export data structure
            export_data = {
                "export_info": {
                    "exported_by": self.username,
                    "export_timestamp": datetime.datetime.now().isoformat(),
                    "system_name": "SecureVault",
                    "version": "1.0",
                    "export_type": "complete_system_backup"
                },
                "system_statistics": {
                    "total_users": len(users_data),
                    "total_logs": len(logs_data),
                    "total_files_tracked": len(files_data),
                    "total_encryption_operations": len(encryption_data),
                    "admin_users": len([u for u in users_data.values() if u.get('role') == 'admin']),
                    "regular_users": len([u for u in users_data.values() if u.get('role') == 'user'])
                },
                "users_data": users_data,
                "system_logs": logs_data,
                "files_data": files_data,
                "encryption_activity": encryption_data
            }
            
            # Ask user for save location
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"securevault_complete_export_{timestamp}.json"
            
            file_path = filedialog.asksaveasfilename(
                title="Export Complete System Data",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialname=default_filename
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
                
                log_event(self.username, "admin_export_data", f"Complete system data exported to: {file_path}")
                
                self.tools_output_text.delete("0.0", "end")
                self.tools_output_text.insert("0.0", 
                    f"✅ COMPLETE DATA EXPORT SUCCESSFUL\n"
                    f"🕒 Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"📁 File: {file_path}\n"
                    f"📊 Export Contents:\n"
                    f"   • Users: {len(users_data)} accounts\n"
                    f"   • Logs: {len(logs_data)} entries\n"
                    f"   • Files: {len(files_data)} tracked\n"
                    f"   • Encryption Ops: {len(encryption_data)} operations\n\n"
                    f"💾 All system data successfully exported!"
                )
                
                messagebox.showinfo("Export Complete", 
                    f"✅ Complete system data exported successfully!\n\n"
                    f"📁 Location: {file_path}\n"
                    f"📊 Contains: {len(users_data)} users, {len(logs_data)} logs, "
                    f"{len(files_data)} files, {len(encryption_data)} encryption operations"
                )
                
                self.update_status("💾 Complete data export successful")
                
        except Exception as e:
            error_msg = f"Failed to export data: {str(e)}"
            messagebox.showerror("Export Error", error_msg)
            log_event(self.username, "admin_export_error", error_msg)
            self.update_status("❌ Data export failed")
            
    def create_backup(self):
        """Create system backup"""
        try:
            # Ensure backup directory exists
            backup_dir = "data/backups"
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"system_backup_{timestamp}.json"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            # Create backup data
            backup_data = {
                "backup_info": {
                    "created_by": self.username,
                    "backup_timestamp": datetime.datetime.now().isoformat(),
                    "backup_type": "automated_system_backup"
                },
                "users_data": load_json_file("data/users_data.json"),
                "system_logs": load_json_file("data/system_logs.json"),
                "files_data": load_json_file("data/files_data.json"),
                "encryption_activity": load_json_file("data/encryption_activity.json")
            }
            
            # Save backup
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
                
            log_event(self.username, "admin_create_backup", f"System backup created: {backup_filename}")
            
            self.tools_output_text.delete("0.0", "end")
            self.tools_output_text.insert("0.0", 
                f"✅ SYSTEM BACKUP CREATED\n"
                f"🕒 Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"📁 File: {backup_filename}\n"
                f"📂 Location: {backup_path}\n\n"
                f"💾 Complete system state backed up successfully!"
            )
            
            self.update_status(f"💾 Backup created: {backup_filename}")
            
        except Exception as e:
            error_msg = f"Backup creation failed: {str(e)}"
            messagebox.showerror("Backup Error", error_msg)
            self.update_status("❌ Backup creation failed")
            
    def show_system_info(self):
        """Show detailed system information"""
        try:
            # Gather system information
            users_data = load_json_file("data/users_data.json")
            logs_data = load_json_file("data/system_logs.json")
            files_data = load_json_file("data/files_data.json")
            encryption_data = load_json_file("data/encryption_activity.json")
            
            # Calculate detailed statistics
            admin_count = len([u for u in users_data.values() if u.get('role') == 'admin'])
            user_count = len([u for u in users_data.values() if u.get('role') == 'user'])
            
            # Get date ranges
            if logs_data:
                log_dates = [log.get('timestamp', '') for log in logs_data if log.get('timestamp')]
                if log_dates:
                    first_log = min(log_dates)
                    last_log = max(log_dates)
                else:
                    first_log = last_log = "N/A"
            else:
                first_log = last_log = "N/A"
            
            system_info = f"""🖥️ SECUREVAULT SYSTEM INFORMATION
{'=' * 80}
🕒 Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
👨‍💼 Requested by: {self.username}

📊 SYSTEM STATISTICS:
{'.' * 40}
👥 Total Users: {len(users_data)}
   🛡️ Administrators: {admin_count}
   👤 Regular Users: {user_count}

📋 Activity Statistics:
   📝 Total Log Entries: {len(logs_data)}
   📁 Files Tracked: {len(files_data)}
   🔐 Encryption Operations: {len(encryption_data)}

📅 System Timeline:
   🎯 First Activity: {first_log}
   🕒 Latest Activity: {last_log}

🔧 SYSTEM HEALTH:
{'.' * 40}
📁 Data Directory: ✅ Operational
📊 JSON Files: ✅ All files accessible
🔄 Auto-refresh: ✅ {'ON' if self.auto_refresh else 'OFF'}
🛡️ Admin Access: ✅ Functional

💾 STORAGE INFORMATION:
{'.' * 40}"""
            
            try:
                # File sizes
                users_size = os.path.getsize("data/users_data.json")
                logs_size = os.path.getsize("data/system_logs.json")
                files_size = os.path.getsize("data/files_data.json")
                
                system_info += f"""
📁 users_data.json: {users_size} bytes
📋 system_logs.json: {logs_size} bytes  
📂 files_data.json: {files_size} bytes
📊 Total Data Size: {users_size + logs_size + files_size} bytes"""
            except:
                system_info += "\n📊 File size information unavailable"
                
            self.tools_output_text.delete("0.0", "end")
            self.tools_output_text.insert("0.0", system_info)
            
            self.update_status("ℹ️ System information displayed")
            
        except Exception as e:
            error_msg = f"Failed to generate system info: {str(e)}"
            messagebox.showerror("System Info Error", error_msg)
            self.update_status("❌ System info generation failed")
            
    def update_status(self, message):
        """Update status bar"""
        self.status_label.configure(text=message)
        # Auto-clear status after 5 seconds
        self.root.after(5000, lambda: self.status_label.configure(text="🟢 Admin Dashboard Active - Monitoring System"))
        
    def logout(self):
        """Logout and return to login screen"""
        # Stop auto-refresh
        self.auto_refresh = False
        
        # Log detailed logout information
        session_duration = datetime.datetime.now()
        log_event(
            self.username, 
            "admin_logout", 
            f"Admin session ended by {self.username} at {session_duration.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        # Show logout confirmation
        self.update_status("🚪 Logging out...")
        self.root.after(1000, self._complete_logout)
        
    def _complete_logout(self):
        """Complete the logout process"""
        self.root.destroy()
        
        # Restart main application
        try:
            from main import LoginApp
            app = LoginApp()
            app.run()
        except ImportError:
            # Fallback if main import fails
            import sys
            sys.exit()
        
    def run(self):
        """Run the admin application"""
        # Set up window close protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def on_closing(self):
        """Handle window closing event"""
        self.auto_refresh = False
        log_event(
            self.username, 
            "admin_window_closed", 
            f"Admin dashboard closed by {self.username}"
        )
        self.root.destroy()

if __name__ == "__main__":
    # For testing purposes
    print("This is the admin module. Please run main.py to start the application.")
