import customtkinter as ctk
from tkinter import filedialog, messagebox
import base64
import os
import datetime
from shared import (
    load_json_file, save_json_file, log_event, 
    get_user_encryption_key
)
from cryptography.fernet import Fernet

class ClientApp:
    def __init__(self, username):
        self.username = username
        self.encryption_key = get_user_encryption_key(username)
        self.fernet = Fernet(self.encryption_key)
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        
        self.root = ctk.CTk()
        self.root.title(f"SecureVault - Client Dashboard [{username}]")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Center the window
        self.center_window()
        
        # Log client session start
        log_event(self.username, "client_session_start", f"Client interface opened by {username}")
        
        self.setup_ui()
        
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def setup_ui(self):
        # Header with user info and status
        header_frame = ctk.CTkFrame(self.root, height=80)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        # Left side - User info
        user_info_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        user_info_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        title_label = ctk.CTkLabel(
            user_info_frame, text=f"🔒 SecureVault Client",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(anchor="w")
        
        user_label = ctk.CTkLabel(
            user_info_frame, text=f"👤 User: {self.username} | 🔑 Role: CLIENT",
            font=ctk.CTkFont(size=12), text_color="gray"
        )
        user_label.pack(anchor="w")
        
        # Session info
        session_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session_label = ctk.CTkLabel(
            user_info_frame, text=f"🕒 Session: {session_time}",
            font=ctk.CTkFont(size=10), text_color="gray70"
        )
        session_label.pack(anchor="w")
        
        # Right side - Logout
        logout_button = ctk.CTkButton(
            header_frame, text="🚪 Logout", width=120, height=35,
            command=self.logout, font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=("#CC4125", "#8B0000"), hover_color=("#B23A1F", "#A00000")
        )
        logout_button.pack(side="right", padx=20, pady=22)
        
        # Main content area with tabs
        self.tabview = ctk.CTkTabview(self.root, height=500)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Create tabs
        self.create_file_tab()
        self.create_encrypt_tab()
        self.create_decrypt_tab()
        
        # Status bar
        self.status_frame = ctk.CTkFrame(self.root, height=40)
        self.status_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.status_frame.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame, text="🟢 Ready - SecureVault Client Active",
            font=ctk.CTkFont(size=12), text_color="green"
        )
        self.status_label.pack(pady=10)
        
    def create_file_tab(self):
        tab = self.tabview.add("📁 File Manager")
        
        # File operations section
        file_ops_frame = ctk.CTkFrame(tab)
        file_ops_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            file_ops_frame, text="📂 File Operations", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
        
        # File selection controls
        controls_frame = ctk.CTkFrame(file_ops_frame, fg_color="transparent")
        controls_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        select_button = ctk.CTkButton(
            controls_frame, text="📂 Select File", 
            command=self.select_file, height=35, width=150,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        select_button.pack(side="left", padx=(0, 10))
        
        clear_button = ctk.CTkButton(
            controls_frame, text="🗑️ Clear", 
            command=self.clear_file_content, height=35, width=100,
            font=ctk.CTkFont(size=12)
        )
        clear_button.pack(side="left")
        
        # File info display
        self.file_info_frame = ctk.CTkFrame(file_ops_frame)
        self.file_info_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.file_path_label = ctk.CTkLabel(
            self.file_info_frame, text="📄 No file selected", 
            font=ctk.CTkFont(size=12), anchor="w"
        )
        self.file_path_label.pack(fill="x", padx=10, pady=5)
        
        self.file_size_label = ctk.CTkLabel(
            self.file_info_frame, text="📊 Size: N/A", 
            font=ctk.CTkFont(size=10), text_color="gray", anchor="w"
        )
        self.file_size_label.pack(fill="x", padx=10, pady=(0, 5))
        
        # File content display
        content_frame = ctk.CTkFrame(tab)
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        ctk.CTkLabel(
            content_frame, text="📋 File Content Preview:", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 5))
        
        # Scrollable text widget with line numbers
        self.file_content_text = ctk.CTkTextbox(
            content_frame, font=ctk.CTkFont(family="Courier New", size=11)
        )
        self.file_content_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
    def create_encrypt_tab(self):
        tab = self.tabview.add("🔐 Encrypt")
        
        # Encryption section
        encrypt_frame = ctk.CTkFrame(tab)
        encrypt_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            encrypt_frame, text="🔐 Text Encryption Module", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(20, 15))
        
        # User key info
        key_info_frame = ctk.CTkFrame(encrypt_frame, height=50)
        key_info_frame.pack(fill="x", padx=15, pady=(0, 15))
        key_info_frame.pack_propagate(False)
        
        key_label = ctk.CTkLabel(
            key_info_frame, text=f"🔑 Using encryption key for: {self.username}",
            font=ctk.CTkFont(size=12, weight="bold"), text_color="green"
        )
        key_label.pack(pady=15)
        
        # Input section
        input_section = ctk.CTkFrame(encrypt_frame)
        input_section.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        ctk.CTkLabel(
            input_section, text="📝 Enter text to encrypt:", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 5))
        
        self.encrypt_input_text = ctk.CTkTextbox(
            input_section, height=150, 
            placeholder_text="Type your secret message here..."
        )
        self.encrypt_input_text.pack(fill="x", padx=15, pady=(0, 10))
        
        # Encrypt button
        encrypt_button = ctk.CTkButton(
            input_section, text="🔒 ENCRYPT TEXT", 
            command=self.encrypt_text, height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        encrypt_button.pack(pady=15)
        
        # Output section
        ctk.CTkLabel(
            input_section, text="🔐 Encrypted Result (Base64):", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        self.encrypt_output_text = ctk.CTkTextbox(
            input_section, height=150,
            placeholder_text="Encrypted text will appear here..."
        )
        self.encrypt_output_text.pack(fill="x", padx=15, pady=(0, 15))
        
        # Copy button
        copy_button = ctk.CTkButton(
            input_section, text="📋 Copy Encrypted Text", 
            command=self.copy_encrypted_text, height=30, width=150
        )
        copy_button.pack(pady=(0, 15))
        
    def create_decrypt_tab(self):
        tab = self.tabview.add("🔓 Decrypt")
        
        # Decryption section
        decrypt_frame = ctk.CTkFrame(tab)
        decrypt_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            decrypt_frame, text="🔓 Text Decryption Module", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(20, 15))
        
        # User key info
        key_info_frame = ctk.CTkFrame(decrypt_frame, height=50)
        key_info_frame.pack(fill="x", padx=15, pady=(0, 15))
        key_info_frame.pack_propagate(False)
        
        key_label = ctk.CTkLabel(
            key_info_frame, text=f"🔑 Using decryption key for: {self.username}",
            font=ctk.CTkFont(size=12, weight="bold"), text_color="green"
        )
        key_label.pack(pady=15)
        
        # Input section
        input_section = ctk.CTkFrame(decrypt_frame)
        input_section.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        ctk.CTkLabel(
            input_section, text="🔐 Enter encrypted text (Base64):", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 5))
        
        self.decrypt_input_text = ctk.CTkTextbox(
            input_section, height=150,
            placeholder_text="Paste your encrypted Base64 text here..."
        )
        self.decrypt_input_text.pack(fill="x", padx=15, pady=(0, 10))
        
        # Decrypt button
        decrypt_button = ctk.CTkButton(
            input_section, text="🔓 DECRYPT TEXT", 
            command=self.decrypt_text, height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        decrypt_button.pack(pady=15)
        
        # Output section
        ctk.CTkLabel(
            input_section, text="📝 Decrypted Result:", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        self.decrypt_output_text = ctk.CTkTextbox(
            input_section, height=150,
            placeholder_text="Decrypted message will appear here..."
        )
        self.decrypt_output_text.pack(fill="x", padx=15, pady=(0, 15))
        
        # Copy button
        copy_decrypt_button = ctk.CTkButton(
            input_section, text="📋 Copy Decrypted Text", 
            command=self.copy_decrypted_text, height=30, width=150
        )
        copy_decrypt_button.pack(pady=(0, 15))
        
    def select_file(self):
        """Select and display file content"""
        file_path = filedialog.askopenfilename(
            title="Select a file to view",
            filetypes=[
                ("Text files", "*.txt"),
                ("Python files", "*.py"),
                ("JSON files", "*.json"),
                ("Log files", "*.log"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Get file info
                file_size = os.path.getsize(file_path)
                file_name = os.path.basename(file_path)
                
                # Read file content
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    
                # Update UI
                self.file_content_text.delete("0.0", "end")
                self.file_content_text.insert("0.0", content)
                
                self.file_path_label.configure(text=f"📄 {file_name}")
                self.file_size_label.configure(text=f"📊 Size: {file_size} bytes | Lines: {len(content.splitlines())}")
                
                # Log file access with detailed info
                log_event(
                    self.username, 
                    "file_access", 
                    f"Accessed file: {file_name} (Size: {file_size} bytes, Path: {file_path})"
                )
                
                # Update file metadata for admin tracking
                self.update_file_metadata(file_path, "accessed")
                
                # Update status
                self.update_status(f"✅ File loaded: {file_name}")
                
            except Exception as e:
                error_msg = f"Could not read file: {str(e)}"
                messagebox.showerror("File Error", error_msg)
                log_event(self.username, "file_access_error", f"Failed to access file: {file_path} - Error: {str(e)}")
                self.update_status("❌ File loading failed")
                
    def clear_file_content(self):
        """Clear file content display"""
        self.file_content_text.delete("0.0", "end")
        self.file_path_label.configure(text="📄 No file selected")
        self.file_size_label.configure(text="📊 Size: N/A")
        log_event(self.username, "file_clear", "File content cleared")
        self.update_status("🗑️ File content cleared")
        
    def encrypt_text(self):
        """Encrypt user input text"""
        text = self.encrypt_input_text.get("0.0", "end-1c").strip()
        
        if not text:
            messagebox.showwarning("Input Required", "Please enter text to encrypt")
            return
            
        try:
            # Encrypt the text
            encrypted_bytes = self.fernet.encrypt(text.encode('utf-8'))
            encrypted_b64 = base64.b64encode(encrypted_bytes).decode('utf-8')
            
            # Display result
            self.encrypt_output_text.delete("0.0", "end")
            self.encrypt_output_text.insert("0.0", encrypted_b64)
            
            # Log encryption activity with details
            log_event(
                self.username, 
                "text_encryption", 
                f"Encrypted text (Original length: {len(text)} chars, Encrypted length: {len(encrypted_b64)} chars)"
            )
            
            # Update file metadata for encryption activity
            self.log_encryption_activity(len(text), len(encrypted_b64))
            
            # Update status
            self.update_status(f"🔒 Text encrypted successfully ({len(text)} → {len(encrypted_b64)} chars)")
            
        except Exception as e:
            error_msg = f"Encryption failed: {str(e)}"
            messagebox.showerror("Encryption Error", error_msg)
            log_event(self.username, "encryption_error", f"Encryption failed: {str(e)}")
            self.update_status("❌ Encryption failed")
            
    def decrypt_text(self):
        """Decrypt user input text"""
        encrypted_text = self.decrypt_input_text.get("0.0", "end-1c").strip()
        
        if not encrypted_text:
            messagebox.showwarning("Input Required", "Please enter encrypted text to decrypt")
            return
            
        try:
            # Validate base64 format
            try:
                encrypted_bytes = base64.b64decode(encrypted_text.encode('utf-8'))
            except Exception:
                raise ValueError("Invalid Base64 format")
            
            # Decrypt the text
            decrypted_bytes = self.fernet.decrypt(encrypted_bytes)
            decrypted_text = decrypted_bytes.decode('utf-8')
            
            # Display result
            self.decrypt_output_text.delete("0.0", "end")
            self.decrypt_output_text.insert("0.0", decrypted_text)
            
            # Log decryption activity with details
            log_event(
                self.username, 
                "text_decryption", 
                f"Decrypted text (Encrypted length: {len(encrypted_text)} chars, Decrypted length: {len(decrypted_text)} chars)"
            )
            
            # Update file metadata for decryption activity
            self.log_decryption_activity(len(encrypted_text), len(decrypted_text))
            
            # Update status
            self.update_status(f"🔓 Text decrypted successfully ({len(encrypted_text)} → {len(decrypted_text)} chars)")
            
        except Exception as e:
            error_msg = f"Decryption failed: {str(e)}"
            messagebox.showerror("Decryption Error", error_msg)
            log_event(self.username, "decryption_error", f"Decryption failed: {str(e)}")
            self.update_status("❌ Decryption failed")
            
    def copy_encrypted_text(self):
        """Copy encrypted text to clipboard"""
        encrypted_text = self.encrypt_output_text.get("0.0", "end-1c")
        if encrypted_text.strip():
            self.root.clipboard_clear()
            self.root.clipboard_append(encrypted_text)
            log_event(self.username, "copy_encrypted", "Copied encrypted text to clipboard")
            self.update_status("📋 Encrypted text copied to clipboard")
        else:
            messagebox.showwarning("Nothing to Copy", "No encrypted text available")
            
    def copy_decrypted_text(self):
        """Copy decrypted text to clipboard"""
        decrypted_text = self.decrypt_output_text.get("0.0", "end-1c")
        if decrypted_text.strip():
            self.root.clipboard_clear()
            self.root.clipboard_append(decrypted_text)
            log_event(self.username, "copy_decrypted", "Copied decrypted text to clipboard")
            self.update_status("📋 Decrypted text copied to clipboard")
        else:
            messagebox.showwarning("Nothing to Copy", "No decrypted text available")
            
    def update_file_metadata(self, file_path, action):
        """Update file metadata for admin tracking"""
        files_data = load_json_file("data/files_data.json")
        
        file_key = os.path.basename(file_path)
        current_time = datetime.datetime.now().isoformat()
        
        if file_key not in files_data:
            files_data[file_key] = {
                "full_path": file_path,
                "accessed_count": 0,
                "first_access": None,
                "last_access": None,
                "accessed_by": [],
                "file_size": 0
            }
            
        # Update metadata
        files_data[file_key]["accessed_count"] += 1
        files_data[file_key]["last_access"] = current_time
        files_data[file_key]["file_size"] = os.path.getsize(file_path)
        
        if files_data[file_key]["first_access"] is None:
            files_data[file_key]["first_access"] = current_time
            
        # Track which users accessed the file
        if self.username not in files_data[file_key]["accessed_by"]:
            files_data[file_key]["accessed_by"].append(self.username)
            
        save_json_file("data/files_data.json", files_data)
        
    def log_encryption_activity(self, original_length, encrypted_length):
        """Log encryption activity for admin monitoring"""
        activity_data = load_json_file("data/encryption_activity.json")
        
        activity_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "username": self.username,
            "action": "encryption",
            "original_length": original_length,
            "encrypted_length": encrypted_length,
            "session_id": f"{self.username}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        }
        
        activity_data.append(activity_entry)
        save_json_file("data/encryption_activity.json", activity_data)
        
    def log_decryption_activity(self, encrypted_length, decrypted_length):
        """Log decryption activity for admin monitoring"""
        activity_data = load_json_file("data/encryption_activity.json")
        
        activity_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "username": self.username,
            "action": "decryption",
            "encrypted_length": encrypted_length,
            "decrypted_length": decrypted_length,
            "session_id": f"{self.username}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        }
        
        activity_data.append(activity_entry)
        save_json_file("data/encryption_activity.json", activity_data)
        
    def update_status(self, message):
        """Update status bar with message"""
        self.status_label.configure(text=message)
        # Auto-clear status after 5 seconds
        self.root.after(5000, lambda: self.status_label.configure(text="🟢 Ready - SecureVault Client Active"))
        
    def logout(self):
        """Logout and return to login screen"""
        # Log detailed logout information
        session_duration = datetime.datetime.now()
        log_event(
            self.username, 
            "client_logout", 
            f"Client session ended by {self.username} at {session_duration.strftime('%Y-%m-%d %H:%M:%S')}"
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
        """Run the client application"""
        # Set up window close protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def on_closing(self):
        """Handle window closing event"""
        log_event(
            self.username, 
            "client_window_closed", 
            f"Client window closed by {self.username}"
        )
        self.root.destroy()

if __name__ == "__main__":
    # For testing purposes
    print("This is the client module. Please run main.py to start the application.")
