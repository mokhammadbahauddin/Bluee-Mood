"""
Blue Mood - Secure Login System
Features:
- Separate Login & Signup Views
- Password Hashing (SHA-256)
- JSON Data Storage
- Dark/Glassmorphism UI Design
"""

import customtkinter as ctk
import json
import os
import hashlib
import time

# File storage for user credentials
USER_FILE = "user_data.json"

class LoginWindow(ctk.CTk):
    """
    Main authentication window.
    Handles user login, registration, and session initialization.
    """

    def __init__(self):
        super().__init__()

        # --- THEME CONFIGURATION ---
        # Dark theme palette consistent with main app
        self.colors = {
            "bg": "#161616",           # Deep dark background
            "card_bg": "#212121",      # Slightly lighter card
            "input_bg": "#303030",     # Input field background
            "blue_primary": "#5FAEF8", # Brand blue
            "blue_hover": "#4A9DE8",   # Hover state
            "text_main": "#FFFFFF",    # Primary text
            "text_dim": "#A1A1AA",     # Secondary text
            "accent": "#FF4081",       # Pink accent for special actions
            "error": "#FF6B6B",        # Red for errors
            "success": "#4ADE80"       # Green for success
        }

        # Window Setup
        self.title("Blue Mood Login")
        self.geometry("1400x900")
        self.after(200, lambda: self.state('zoomed'))

        self.configure(fg_color=self.colors["bg"])

        # Key Bindings
        self.bind("<Escape>", lambda e: self.quit())
        self.bind("<Return>", lambda e: self.handle_action())

        # State Variables
        self.on_login_success = None
        self.is_register_mode = False  # Toggle between Login (False) and Register (True)
        self.animation_callbacks = []

        # Initialize UI
        self.create_ui()

    def create_ui(self):
        """Builds the UI components."""

        # 1. Main Card Container (Centered)
        self.card = ctk.CTkFrame(
            self,
            fg_color=self.colors["card_bg"],
            corner_radius=24,
            border_width=1,
            border_color="#2a2a2a",
            width=420,
            height=600
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False) # Force size

        # 2. Inner Content Wrapper
        self.content = ctk.CTkFrame(self.card, fg_color="transparent")
        self.content.pack(expand=True, fill="both", padx=40, pady=40)

        # 3. Logo Section
        logo_bg = ctk.CTkFrame(
            self.content,
            fg_color=self.colors["blue_primary"],
            corner_radius=12,
            width=48,
            height=48
        )
        logo_bg.pack(pady=(0, 20))
        logo_bg.pack_propagate(False)
        ctk.CTkLabel(logo_bg, text="🎵", font=ctk.CTkFont(size=24)).pack(expand=True)

        # 4. Dynamic Title Section
        self.title_label = ctk.CTkLabel(
            self.content,
            text="Welcome Back",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=self.colors["text_main"]
        )
        self.title_label.pack(pady=(0, 8))

        self.subtitle_label = ctk.CTkLabel(
            self.content,
            text="Dive into the music",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text_dim"]
        )
        self.subtitle_label.pack(pady=(0, 30))

        # 5. Form Fields
        # Username
        ctk.CTkLabel(
            self.content,
            text="Username",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.colors["text_dim"]
        ).pack(anchor="w", pady=(0, 6))

        self.username_entry = ctk.CTkEntry(
            self.content,
            placeholder_text="Enter username",
            width=340,
            height=48,
            fg_color=self.colors["input_bg"],
            border_width=0,
            corner_radius=12,
            font=ctk.CTkFont(size=13),
            text_color=self.colors["text_main"]
        )
        self.username_entry.pack(pady=(0, 15))

        # Password
        ctk.CTkLabel(
            self.content,
            text="Password",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.colors["text_dim"]
        ).pack(anchor="w", pady=(0, 6))

        self.password_entry = ctk.CTkEntry(
            self.content,
            placeholder_text="••••••••",
            width=340,
            height=48,
            fg_color=self.colors["input_bg"],
            border_width=0,
            corner_radius=12,
            show="•",
            font=ctk.CTkFont(size=13),
            text_color=self.colors["text_main"]
        )
        self.password_entry.pack(pady=(0, 15))

        # 6. Action Button (Login / Register)
        self.action_btn = ctk.CTkButton(
            self.content,
            text="Log In  →",
            width=340,
            height=48,
            fg_color=self.colors["blue_primary"],
            hover_color=self.colors["blue_hover"],
            corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["text_main"],
            command=self.handle_action
        )
        self.action_btn.pack(pady=(20, 10))

        # 7. Status Message Area
        self.status_label = ctk.CTkLabel(
            self.content,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=self.colors["error"]
        )
        self.status_label.pack(pady=(0, 10))

        # 8. Mode Switcher (Footer)
        self.switch_mode_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        self.switch_mode_frame.pack(side="bottom", pady=10)

        self.switch_text = ctk.CTkLabel(
            self.switch_mode_frame,
            text="Don't have an account?",
            font=ctk.CTkFont(size=11),
            text_color=self.colors["text_dim"]
        )
        self.switch_text.pack(side="left", padx=(0, 5))

        self.switch_btn = ctk.CTkButton(
            self.switch_mode_frame,
            text="Create Account",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.colors["accent"],
            fg_color="transparent",
            hover_color=self.colors["input_bg"],
            width=100,
            height=20,
            command=self.toggle_mode
        )
        self.switch_btn.pack(side="left")

        # 9. App Version / Footer
        ctk.CTkLabel(
            self,
            text="BLUE MOOD MUSIC v2.0 • SECURE LOGIN",
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color="#404040"
        ).place(relx=0.5, rely=0.96, anchor="center")

    def toggle_mode(self):
        """
        Switches the interface between Login Mode and Registration Mode.
        Updates labels, button text, and clears errors.
        """
        self.is_register_mode = not self.is_register_mode
        self.status_label.configure(text="") # Clear errors

        if self.is_register_mode:
            # Switch to Register View
            self.title_label.configure(text="Create Account")
            self.subtitle_label.configure(text="Join the rhythm today")
            self.action_btn.configure(text="Sign Up  →")
            self.switch_text.configure(text="Already have an account?")
            self.switch_btn.configure(text="Log In")
            # Visual cue: Change button color for register
            self.action_btn.configure(fg_color=self.colors["accent"], hover_color="#E91E63")
        else:
            # Switch to Login View
            self.title_label.configure(text="Welcome Back")
            self.subtitle_label.configure(text="Dive into the music")
            self.action_btn.configure(text="Log In  →")
            self.switch_text.configure(text="Don't have an account?")
            self.switch_btn.configure(text="Create Account")
            # Restore blue color
            self.action_btn.configure(fg_color=self.colors["blue_primary"], hover_color=self.colors["blue_hover"])

    def _hash_password(self, password):
        """
        Securely hashes a password using SHA-256.
        Never store passwords in plain text!
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def load_users(self):
        """Loads user database from JSON file."""
        if os.path.exists(USER_FILE):
            try:
                with open(USER_FILE, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {} # Return empty dict if file is corrupted
        return {}

    def save_users(self, users):
        """Saves user database to JSON file."""
        try:
            with open(USER_FILE, 'w') as f:
                json.dump(users, f, indent=2)
        except Exception as e:
            self.show_status(f"System Error: {str(e)}", True)

    def handle_action(self):
        """
        Main logic handler for Login/Register button click.
        """
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # 1. Validation
        if not username or not password:
            self.show_status("Please fill in all fields.", True)
            self._shake_animation()
            return

        users = self.load_users()
        hashed_password = self._hash_password(password)

        if self.is_register_mode:
            # --- REGISTRATION LOGIC ---
            if username in users:
                self.show_status("Username already exists.", True)
                self._shake_animation()
            else:
                # Create new user record
                users[username] = {
                    "password": hashed_password,
                    "created_at": time.time(),
                    "role": "user" # Default role
                }
                self.save_users(users)
                self.show_status("Account created! Logging in...", False)

                # Auto-login after delay
                self.after(1500, lambda: self.finish_login(username))

        else:
            # --- LOGIN LOGIC ---
            if username not in users:
                self.show_status("User not found.", True)
                self._shake_animation()
            else:
                stored_password = users[username].get("password")
                if stored_password == hashed_password:
                    self.show_status("Login Successful!", False)
                    self.finish_login(username)
                else:
                    self.show_status("Incorrect password.", True)
                    self._shake_animation()
                    self.password_entry.delete(0, 'end')

    def finish_login(self, username):
        """Triggers the success callback to launch the main app."""
        if self.on_login_success:
            self.on_login_success(username)

    def show_status(self, message, is_error):
        """Displays a status message with auto-hide."""
        color = self.colors["error"] if is_error else self.colors["success"]
        self.status_label.configure(text=message, text_color=color)

        # Clear previous timer if exists
        self.cleanup()

        # Auto hide after 3 seconds
        if message:
            callback_id = self.after(3000, lambda: self.status_label.configure(text=""))
            self.animation_callbacks.append(callback_id)

    def _shake_animation(self):
        """Simple visual feedback for errors (simulated shake)."""
        original_x = self.card.winfo_x()

        # A simple movement sequence
        movements = [5, -10, 10, -10, 5, 0]
        delay = 0

        for move in movements:
            self.after(delay, lambda m=move: self.card.place(relx=0.5, x=m, anchor="center"))
            delay += 50

    def cleanup(self):
        """Cancels pending animations to prevent errors on destroy."""
        for callback_id in self.animation_callbacks:
            try:
                self.after_cancel(callback_id)
            except:
                pass
        self.animation_callbacks.clear()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = LoginWindow()
    app.mainloop()