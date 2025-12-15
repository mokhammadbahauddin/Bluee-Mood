"""
Blue Mood - Main Entry Point (Robust Windows Restart)
"""

import customtkinter as ctk
import json
import os
import sys
import subprocess
import time
from login import LoginWindow

# Session File
SESSION_FILE = "session.json"

class BlueMoodApp:
    def __init__(self):
        self.current_user = None
        self.current_role = "user"  # <--- Tambahkan variabel default role
        self.music_app = None
        self.login_window = None

        # 1. Cek Sesi
        # 1. Cek Sesi (Update logika get_saved_session)
        saved_data = self.get_saved_session()

        if saved_data:
            self.current_user = saved_data.get("username")
            self.current_role = saved_data.get("role", "user")  # Ambil role
            print(f"✓ Auto-login: {self.current_user} ({self.current_role})")
            self.launch_music_player()
        else:
            self.show_login()

    def get_saved_session(self):
        """Mengembalikan dictionary data sesi, bukan cuma username"""
        if os.path.exists(SESSION_FILE):
            try:
                with open(SESSION_FILE, 'r') as f:
                    return json.load(f)  # Return full dict
            except:
                pass
        return None

    def save_session(self, username, role):
        """Simpan username DAN role ke file sesi"""
        with open(SESSION_FILE, 'w') as f:
            json.dump({"username": username, "role": role}, f)

    def clear_session(self):
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)

    def show_login(self):
        """Menampilkan jendela login dan menunggu sampai ditutup."""
        print("--- Opening Login Window ---")
        self.login_window = LoginWindow()
        self.login_window.on_login_success = self.handle_login_success
        self.login_window.mainloop()

        # Jika user login sukses, variable self.current_user sudah terisi
        if self.current_user:
            self.launch_music_player()
        else:
            print("Aplikasi ditutup tanpa login.")
            sys.exit()

    def handle_login_success(self, username, role):
        """Callback saat login berhasil (Terima role dari login.py)"""
        print(f"✓ Credentials verified for: {username} as {role}")
        self.current_user = username
        self.current_role = role
        self.save_session(username, role)  # Simpan sesi lengkap

        if self.login_window:
            self.login_window.destroy()
            self.login_window = None

    def handle_logout(self):
        """
        Logout Handler:
        Menggunakan teknik DETACHED PROCESS untuk Windows agar restart berhasil.
        """
        print(f"👋 Logging out {self.current_user}...")
        self.clear_session()

        # 1. Matikan GUI Lama secara paksa
        if self.music_app:
            try:
                self.music_app.is_running = False
                self.music_app.quit()
            except: pass

        print("🔄 Restarting Application...")

        # 2. Persiapkan Path Absolut (PENTING!)
        # sys.argv[0] kadang hanya berisi "main.py" relatif, kita butuh path lengkap
        python_executable = sys.executable
        script_path = os.path.abspath(__file__)

        # 3. Jalankan Proses Baru yang Terpisah (DETACHED)
        try:
            # CREATE_NEW_CONSOLE (flag 0x00000010) atau DETACHED_PROCESS (0x00000008)
            # Ini mencegah proses baru mati saat proses lama mati
            creation_flags = 0x00000000
            if sys.platform == "win32":
                creation_flags = subprocess.CREATE_NO_WINDOW # Agar tidak muncul console hitam pop-up

            subprocess.Popen([python_executable, script_path], creationflags=creation_flags)

        except Exception as e:
            print(f"Gagal restart otomatis: {e}")
            # Fallback jika gagal (metode lama)
            subprocess.Popen([sys.executable, script_path])

        # 4. Matikan Proses Lama
        sys.exit(0)

    def launch_music_player(self):
        try:
            print("🚀 Loading gui.py...")
            from gui import App as MusicPlayerApp

            # MASUKKAN ROLE KE DALAM GUI
            self.music_app = MusicPlayerApp(user_role=self.current_role)

            if hasattr(self.music_app, 'username_var'):
                self.music_app.username_var.set(self.current_user)
                self.music_app.player.username = self.current_user

            self.music_app.logout_callback = self.handle_logout

            print("✅ GUI Started.")
            self.music_app.mainloop()
        except Exception as e:
            print(f"❌ CRASH ERROR in gui.py: {e}")
            import traceback
            traceback.print_exc()
            self.handle_logout()

if __name__ == "__main__":
    app = BlueMoodApp()