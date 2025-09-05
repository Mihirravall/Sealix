import customtkinter as ctk
from tkinter import messagebox
import hashlib
import datetime
import json
import os

class CyberSecurityApp:
    def __init__(self):
        # File-based user storage
        self.users_file = "users_data.json"
        self.load_users_from_file()
        
        # Add admin user if not exists
        self.create_admin_user()
        
        # UI Setup
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        
        self.root = ctk.CTk()
        self.root.title("CyberSec Authentication System")
        self.root.geometry("500x600")
        self.root.configure(fg_color="#0a0a0a")
        
        # Current user info
        self.current_user = None
        self.current_role = None
        
        # Create main container
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Show login page initially
        self.show_login_page()
    
    def load_users_from_file(self):
        """Load users from JSON file"""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as f:
                    self.users_data = json.load(f)
                print(f"Debug - Loaded {len(self.users_data)} users from file")
            else:
                self.users_data = {}
                print("Debug - Created new users data structure")
        except Exception as e:
            print(f"Debug - Error loading users file: {e}")
            self.users_data = {}
    
    def save_users_to_file(self):
        """Save users to JSON file"""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users_data, f, indent=2)
            print("Debug - Users data saved to file successfully")
        except Exception as e:
            print(f"Debug - Error saving users file: {e}")
    
    def create_admin_user(self):
        """Create admin user 'sagar' with password 'devprit' if not exists"""
        admin_username = "sagar"
        admin_password = "devprit"
        
        if admin_username not in self.users_data:
            hashed_pw = self.hash_password(admin_password)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            self.users_data[admin_username] = {
                "password": hashed_pw,
                "role": "admin",
                "timestamp": timestamp
            }
            self.save_users_to_file()
            print("Debug - Admin user 'sagar' created successfully")
        else:
            print("Debug - Admin user 'sagar' already exists")
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def clear_frame(self):
        """Clear all widgets from main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_registration_page(self):
        """Display registration page"""
        self.clear_frame()
        
        # Header with cyber theme
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="#1a1a1a", corner_radius=15)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Cyber-themed title
        title_label = ctk.CTkLabel(header_frame, 
                                 text="🔐 SECURE REGISTRATION", 
                                 font=("Courier New", 24, "bold"),
                                 text_color="#00ff41")
        title_label.pack(pady=15)
        
        subtitle_label = ctk.CTkLabel(header_frame, 
                                    text="» Initialize New User Account «", 
                                    font=("Courier New", 12),
                                    text_color="#888888")
        subtitle_label.pack(pady=(0, 15))
        
        # Registration form
        form_frame = ctk.CTkFrame(self.main_frame, fg_color="#1a1a1a", corner_radius=15)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # Username field
        ctk.CTkLabel(form_frame, text="USERNAME:", font=("Courier New", 12, "bold"), text_color="#00ff41").pack(pady=(20, 5))
        self.reg_username = ctk.CTkEntry(form_frame, 
                                       placeholder_text="Enter username",
                                       font=("Courier New", 12),
                                       fg_color="#2a2a2a",
                                       border_color="#00ff41",
                                       width=300)
        self.reg_username.pack(pady=(0, 15))
        
        # Password field
        ctk.CTkLabel(form_frame, text="PASSWORD:", font=("Courier New", 12, "bold"), text_color="#00ff41").pack(pady=(0, 5))
        self.reg_password = ctk.CTkEntry(form_frame, 
                                       placeholder_text="Enter password",
                                       font=("Courier New", 12),
                                       fg_color="#2a2a2a",
                                       border_color="#00ff41",
                                       show="*",
                                       width=300)
        self.reg_password.pack(pady=(0, 15))
        
        # Confirm password field
        ctk.CTkLabel(form_frame, text="CONFIRM PASSWORD:", font=("Courier New", 12, "bold"), text_color="#00ff41").pack(pady=(0, 5))
        self.reg_confirm = ctk.CTkEntry(form_frame, 
                                      placeholder_text="Confirm password",
                                      font=("Courier New", 12),
                                      fg_color="#2a2a2a",
                                      border_color="#00ff41",
                                      show="*",
                                      width=300)
        self.reg_confirm.pack(pady=(0, 20))
        
        # Buttons
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(fill="x")
        
        register_btn = ctk.CTkButton(button_frame, 
                                   text="🛡️ REGISTER ACCOUNT",
                                   command=self.register_user,
                                   font=("Courier New", 14, "bold"),
                                   fg_color="#00aa33",
                                   hover_color="#00cc44",
                                   height=40,
                                   width=200)
        register_btn.pack(pady=10)
        
        login_btn = ctk.CTkButton(button_frame, 
                                text="🔓 BACK TO LOGIN",
                                command=self.show_login_page,
                                font=("Courier New", 12),
                                fg_color="transparent",
                                border_color="#00ff41",
                                border_width=2,
                                hover_color="#1a3d1a",
                                height=35,
                                width=150)
        login_btn.pack(pady=5)
    
    def show_login_page(self):
        """Display login page"""
        self.clear_frame()
        
        # Header
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="#1a1a1a", corner_radius=15)
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ctk.CTkLabel(header_frame, 
                                 text="🔑 SECURE LOGIN", 
                                 font=("Courier New", 24, "bold"),
                                 text_color="#00ff41")
        title_label.pack(pady=15)
        
        subtitle_label = ctk.CTkLabel(header_frame, 
                                    text="» Authenticate User Access «", 
                                    font=("Courier New", 12),
                                    text_color="#888888")
        subtitle_label.pack(pady=(0, 15))
        
        # Login form
        form_frame = ctk.CTkFrame(self.main_frame, fg_color="#1a1a1a", corner_radius=15)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # Username field
        ctk.CTkLabel(form_frame, text="USERNAME:", font=("Courier New", 12, "bold"), text_color="#00ff41").pack(pady=(20, 5))
        self.login_username = ctk.CTkEntry(form_frame, 
                                         placeholder_text="Enter username",
                                         font=("Courier New", 12),
                                         fg_color="#2a2a2a",
                                         border_color="#00ff41",
                                         width=300)
        self.login_username.pack(pady=(0, 15))
        
        # Password field
        ctk.CTkLabel(form_frame, text="PASSWORD:", font=("Courier New", 12, "bold"), text_color="#00ff41").pack(pady=(0, 5))
        self.login_password = ctk.CTkEntry(form_frame, 
                                         placeholder_text="Enter password",
                                         font=("Courier New", 12),
                                         fg_color="#2a2a2a",
                                         border_color="#00ff41",
                                         show="*",
                                         width=300)
        self.login_password.pack(pady=(0, 20))
        
        # Admin info box
        info_frame = ctk.CTkFrame(self.main_frame, fg_color="#1a1a2a", corner_radius=10)
        info_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(info_frame, 
                   text="ℹ️ ADMIN ACCESS INFO", 
                   font=("Courier New", 10, "bold"),
                   text_color="#6666ff").pack(pady=(10, 5))
        ctk.CTkLabel(info_frame, 
                   text="Admin Username: sagar | Admin Password: devprit", 
                   font=("Courier New", 9),
                   text_color="#aaaaaa").pack(pady=(0, 10))
        
        # Buttons
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(fill="x")
        
        login_btn = ctk.CTkButton(button_frame, 
                                text="🔓 LOGIN",
                                command=self.login_user,
                                font=("Courier New", 14, "bold"),
                                fg_color="#0066cc",
                                hover_color="#0088ff",
                                height=40,
                                width=200)
        login_btn.pack(pady=10)
        
        register_btn = ctk.CTkButton(button_frame, 
                                   text="📝 CREATE NEW ACCOUNT",
                                   command=self.show_registration_page,
                                   font=("Courier New", 12),
                                   fg_color="transparent",
                                   border_color="#00ff41",
                                   border_width=2,
                                   hover_color="#1a3d1a",
                                   height=35,
                                   width=180)
        register_btn.pack(pady=5)
    
    def show_dashboard(self):
        """Display user dashboard after successful login"""
        self.clear_frame()
        
        # Header with user info
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="#1a1a1a", corner_radius=15)
        header_frame.pack(fill="x", pady=(0, 20))
        
        if self.current_role == "admin":
            title_text = "🛡️ ADMIN DASHBOARD"
            title_color = "#ff4444"
        else:
            title_text = "👤 USER DASHBOARD"
            title_color = "#00ff41"
        
        title_label = ctk.CTkLabel(header_frame, 
                                 text=title_text, 
                                 font=("Courier New", 24, "bold"),
                                 text_color=title_color)
        title_label.pack(pady=15)
        
        user_info = ctk.CTkLabel(header_frame, 
                               text=f"» Welcome, {self.current_user} | Role: {self.current_role.upper()} «", 
                               font=("Courier New", 12),
                               text_color="#888888")
        user_info.pack(pady=(0, 15))
        
        # Dashboard content
        content_frame = ctk.CTkFrame(self.main_frame, fg_color="#1a1a1a", corner_radius=15)
        content_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        if self.current_role == "admin":
            self.show_admin_content(content_frame)
        else:
            self.show_user_content(content_frame)
        
        # Logout button
        logout_btn = ctk.CTkButton(self.main_frame, 
                                 text="🚪 LOGOUT",
                                 command=self.logout,
                                 font=("Courier New", 12),
                                 fg_color="#cc3333",
                                 hover_color="#ff4444",
                                 height=35,
                                 width=120)
        logout_btn.pack(pady=10)
    
    def show_admin_content(self, parent):
        """Show admin-specific content"""
        ctk.CTkLabel(parent, 
                   text="ADMIN CONTROL PANEL", 
                   font=("Courier New", 16, "bold"),
                   text_color="#ff4444").pack(pady=20)
        
        # User management section
        users_frame = ctk.CTkFrame(parent, fg_color="#2a2a2a", corner_radius=10)
        users_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(users_frame, 
                   text="📊 REGISTERED USERS:", 
                   font=("Courier New", 12, "bold"),
                   text_color="#ffffff").pack(pady=(10, 5))
        
        # Display all users
        users_text = ""
        for username, user_data in self.users_data.items():
            role_icon = "👑" if user_data["role"] == "admin" else "👤"
            users_text += f"{role_icon} {username} | {user_data['role'].upper()} | {user_data['timestamp']}\n"
        
        users_display = ctk.CTkTextbox(users_frame, 
                                     height=150,
                                     font=("Courier New", 10),
                                     fg_color="#1a1a1a")
        users_display.pack(fill="x", padx=10, pady=(0, 10))
        users_display.insert("1.0", users_text if users_text else "No users found")
        users_display.configure(state="disabled")
        
        # File info
        file_info_label = ctk.CTkLabel(users_frame, 
                                     text=f"📁 Data stored in: {self.users_file}", 
                                     font=("Courier New", 9),
                                     text_color="#888888")
        file_info_label.pack(pady=(0, 10))
    
    def show_user_content(self, parent):
        """Show regular user content"""
        ctk.CTkLabel(parent, 
                   text="USER PANEL", 
                   font=("Courier New", 16, "bold"),
                   text_color="#00ff41").pack(pady=20)
        
        # User info
        info_frame = ctk.CTkFrame(parent, fg_color="#2a2a2a", corner_radius=10)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(info_frame, 
                   text="🔐 ACCOUNT INFORMATION", 
                   font=("Courier New", 12, "bold"),
                   text_color="#ffffff").pack(pady=(10, 5))
        
        # Get user info from file data
        user_data = self.users_data.get(self.current_user, {})
        
        if user_data:
            info_text = f"Username: {self.current_user}\nRole: {user_data['role'].upper()}\nRegistered: {user_data['timestamp']}\nStatus: AUTHENTICATED ✅\nData Source: File-based storage"
        else:
            info_text = "User information not available"
        
        info_display = ctk.CTkTextbox(info_frame, 
                                    height=120,
                                    font=("Courier New", 10),
                                    fg_color="#1a1a1a")
        info_display.pack(fill="x", padx=10, pady=(0, 10))
        info_display.insert("1.0", info_text)
        info_display.configure(state="disabled")
    
    def register_user(self):
        """Handle user registration"""
        username = self.reg_username.get().strip()
        password = self.reg_password.get()
        confirm = self.reg_confirm.get()

        print(f"Debug - Registration attempt: username='{username}', password_len={len(password)}, confirm_len={len(confirm)}")

        if not username or not password or not confirm:
            messagebox.showerror("❌ Error", "All fields are required")
            return

        if password != confirm:
            messagebox.showerror("❌ Error", "Passwords do not match")
            return

        if len(password) < 3:
            messagebox.showerror("❌ Error", "Password must be at least 3 characters long")
            return

        if username in self.users_data:
            messagebox.showerror("❌ Error", "Username already exists")
            return

        try:
            hashed_pw = self.hash_password(password)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Add user to data structure
            self.users_data[username] = {
                "password": hashed_pw,
                "role": "user",
                "timestamp": timestamp
            }
            
            # Save to file
            self.save_users_to_file()
            
            print(f"Debug - User registration successful: {username}")
            messagebox.showinfo("✅ Success", "Registration successful!\nPlease login with your credentials.")
            
            # Clear the form fields
            self.reg_username.delete(0, 'end')
            self.reg_password.delete(0, 'end')
            self.reg_confirm.delete(0, 'end')
            
            self.show_login_page()
            
        except Exception as e:
            print(f"Debug - Unexpected error during registration: {e}")
            messagebox.showerror("❌ Error", f"Registration failed: {str(e)}")
    
    def login_user(self):
        """Handle user login"""
        username = self.login_username.get().strip()
        password = self.login_password.get()

        print(f"Debug - Login attempt: username='{username}', password_len={len(password)}")

        if not username or not password:
            messagebox.showerror("❌ Error", "Username and password are required")
            return

        try:
            # Check if user exists in file data
            if username not in self.users_data:
                print("Debug - User doesn't exist in file")
                messagebox.showerror("❌ Error", "User not found")
                return
            
            user_data = self.users_data[username]
            hashed_pw = self.hash_password(password)
            
            print(f"Debug - Checking password for user: {username}")
            
            if user_data["password"] == hashed_pw:
                self.current_user = username
                self.current_role = user_data["role"]
                print(f"Debug - Login successful: user={self.current_user}, role={self.current_role}")
                
                messagebox.showinfo("✅ Success", f"Login successful!\nWelcome, {username}")
                
                # Clear the form fields
                self.login_username.delete(0, 'end')
                self.login_password.delete(0, 'end')
                
                self.show_dashboard()
            else:
                print("Debug - Password doesn't match")
                messagebox.showerror("❌ Error", "Invalid password")
                
        except Exception as e:
            print(f"Debug - Login error: {e}")
            messagebox.showerror("❌ Error", f"Login failed: {str(e)}")
    
    def logout(self):
        """Handle user logout"""
        self.current_user = None
        self.current_role = None
        messagebox.showinfo("🔒 Logged Out", "You have been logged out successfully")
        self.show_login_page()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    app = CyberSecurityApp()
    app.run()