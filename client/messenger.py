import tkinter
from tkinter import messagebox
from client import Client
from datetime import datetime
import re

from config import (
    COLOR_BG, COLOR_CARD, COLOR_TEXT_PRIMARY, COLOR_TEXT_MUTED,
    COLOR_ACCENT, COLOR_ACCENT_HOVER, COLOR_ERROR, COLOR_SUCCESS,
    FONT_TITLE, FONT_BODY, FONT_BOLD, FONT_SMALL, FONT_TOGGLE
)
from ui_screens import LoginScreen, RegistrationScreen, ForgotPasswordScreen, DashboardScreen
from toast import ToastNotification

class App:
    """
    Main application controller (MVC architecture). Coordinates client socket,
    sub-screens, and local state management.
    """
    def __init__(self):
        # Windows taskbar grouping fix: tells Windows to display the custom icon on the taskbar.
        # This MUST be called before initializing the Tk root window.
        try:
            import sys
            if sys.platform == "win32":
                import ctypes
                myappid = "messenger.chat.client.1.0"
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception as e:
            print(f"Could not set AppUserModelID: {e}")

        self.root = tkinter.Tk()
        self.root.title("Messenger")
        self.root.geometry("800x600")

        # Set title bar window icon dynamically (from local file or bundled PyInstaller resources)
        try:
            import sys
            import os
            if getattr(sys, 'frozen', False):
                icon_path = os.path.join(sys._MEIPASS, "icon.ico")
            else:
                icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")

            if os.path.exists(icon_path):
                from PIL import Image, ImageTk
                img = Image.open(icon_path)
                photo = ImageTk.PhotoImage(img)
                self.root.iconphoto(True, photo)
                self.root._icon_image = photo  # Keep a reference to prevent garbage collection
        except Exception as e:
            print(f"Could not load window icon: {e}")

        self.bg_color = COLOR_BG
        self.bg_card = COLOR_CARD
        self.fg_primary = COLOR_TEXT_PRIMARY
        self.fg_secondary = COLOR_TEXT_MUTED
        self.accent_color = COLOR_ACCENT
        self.accent_hover = COLOR_ACCENT_HOVER
        self.error_color = COLOR_ERROR
        self.success_color = COLOR_SUCCESS
        
        self.root.configure(bg=self.bg_color)

        self.client = Client()
        self.current_user = None      # {"email": ..., "name": ...}
        self.active_chat = None       # email or "__broadcast__"
        self.active_chat_name = ""
        self.online_users = []        # [{"email": ..., "name": ...}]
        self.recent_chats = []        # [{"email": ..., "name": ...}]
        self.broadcast_history = []   # [{"sender": ..., "content": ..., "time": ...}]
        self.found_user = None
        self.unread_counts = {}       # email (lowercase) -> unread count (int)
        
        # Instantiate modular screens and notification toast
        self.login_screen = LoginScreen(self.root, self)
        self.registration_screen = RegistrationScreen(self.root, self)
        self.forgot_password_screen = ForgotPasswordScreen(self.root, self)
        self.dashboard_screen = DashboardScreen(self.root, self)
        self.toast = ToastNotification(self.root)

        # Handle window closure protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Connect to server initially
        self.connect_to_server()

        # Show initial screen
        self.show_frame(self.login_screen)
        self.root.mainloop()

    def show_frame(self, frame):
        """
        Switches between active screens by packing the target and forgetting others.
        """
        self.login_screen.pack_forget()
        self.registration_screen.pack_forget()
        self.forgot_password_screen.pack_forget()
        self.dashboard_screen.pack_forget()

        if frame == self.dashboard_screen:
            frame.pack(fill="both", expand=True)
        else:
            frame.pack(pady=50)

    def toggle_password_visibility(self, entry, button):
        """
        Toggles password visibility in Entry widgets between masked and clear text.
        """
        if entry.cget("show") == "*":
            entry.config(show="")
            button.config(fg=self.accent_color)
        else:
            entry.config(show="*")
            button.config(fg=self.fg_secondary)

    def get_contact_name(self, email):
        """
        Resolves names for email addresses from online users and recent chats cache.
        """
        email_lower = email.lower()
        for c in self.recent_chats:
            if c["email"].lower() == email_lower:
                return c["name"]
        for u in self.online_users:
            if u["email"].lower() == email_lower:
                return u["name"]
        return email.split("@")[0]

    def show_toast(self, title, message):
        """
        Delegates in-app slide-down notifications to the ToastNotification manager.
        """
        self.toast.show(title, message)

    # ------------------ Action Methods ------------------

    def connect_to_server(self):
        """
        Initiates connection to the background socket server.
        """
        if self.client.connect(self.on_server_message):
            self.login_screen.feedback_lbl.config(text="Connected to server.", fg=self.success_color)
            return True
        else:
            self.login_screen.feedback_lbl.config(text="Server connection failed. Is it running?", fg=self.error_color)
            return False

    def on_server_message(self, data):
        """
        Socket callback executed on incoming messages, routed thread-safely to Tkinter main thread.
        """
        self.root.after(0, lambda: self.process_message(data))

    def login(self):
        """
        Submits login request to server.
        """
        email = self.login_screen.email_entry.get().strip()
        password = self.login_screen.password_entry.get().strip()

        if not email or not password:
            self.login_screen.feedback_lbl.config(text="Email and Password are required.", fg=self.error_color)
            return

        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, email):
            self.login_screen.feedback_lbl.config(text="Invalid email format.", fg=self.error_color)
            return

        if not self.client.socket:
            if not self.connect_to_server():
                return

        self.login_screen.feedback_lbl.config(text="Logging in...", fg=self.fg_primary)
        self.client.send({
            "action": "login",
            "email": email,
            "password": password
        })

    def register_account(self):
        """
        Submits registration info including OTP to verify account creation.
        """
        name = self.registration_screen.name_entry.get().strip()
        email = self.registration_screen.email_entry.get().strip()
        password = self.registration_screen.password_entry.get().strip()
        otp = self.registration_screen.otp_entry.get().strip()

        if not name or not email or not password or not otp:
            self.registration_screen.feedback_lbl.config(text="All fields (including OTP) are required.", fg=self.error_color)
            return

        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, email):
            self.registration_screen.feedback_lbl.config(text="Invalid email format.", fg=self.error_color)
            return

        try:
            otp_val = int(otp)
        except ValueError:
            self.registration_screen.feedback_lbl.config(text="OTP must be numerical.", fg=self.error_color)
            return

        if not self.client.socket:
            if not self.connect_to_server():
                return

        self.registration_screen.feedback_lbl.config(text="Registering user...", fg=self.fg_primary)
        self.client.send({
            "action": "register",
            "name": name,
            "email": email,
            "password": password,
            "otp": otp_val
        })

    def send_registration_otp(self):
        """
        Requests the server to dispatch a registration OTP to the specified email.
        """
        email = self.registration_screen.email_entry.get().strip()
        if not email:
            self.registration_screen.feedback_lbl.config(text="Email is required to send OTP.", fg=self.error_color)
            return

        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, email):
            self.registration_screen.feedback_lbl.config(text="Invalid email format.", fg=self.error_color)
            return

        if not self.client.socket:
            if not self.connect_to_server():
                return
        self.registration_screen.feedback_lbl.config(text="Requesting OTP...", fg=self.fg_primary)
        self.client.send({"action": "register_send_otp", "email": email})

    def send_password_reset_otp(self):
        """
        Requests a password reset OTP.
        """
        email = self.forgot_password_screen.email_entry.get().strip()
        if not email:
            self.forgot_password_screen.feedback_lbl.config(text="Email is required.", fg=self.error_color)
            return

        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, email):
            self.forgot_password_screen.feedback_lbl.config(text="Invalid email format.", fg=self.error_color)
            return

        if not self.client.socket:
            if not self.connect_to_server():
                return
        self.forgot_password_screen.feedback_lbl.config(text="Requesting OTP...", fg=self.fg_primary)
        self.client.send({"action": "forgot_password", "email": email})

    def verify_password_reset_otp(self):
        """
        Verifies the reset OTP against the database store.
        """
        email = self.forgot_password_screen.email_entry.get().strip()
        otp = self.forgot_password_screen.otp_entry.get().strip()
        if not email or not otp:
            self.forgot_password_screen.feedback_lbl.config(text="Email and OTP are required.", fg=self.error_color)
            return
        try:
            otp_val = int(otp)
        except ValueError:
            self.forgot_password_screen.feedback_lbl.config(text="OTP must be numerical.", fg=self.error_color)
            return
        if not self.client.socket:
            if not self.connect_to_server():
                return
        self.client.send({"action": "verify_otp", "email": email, "otp": otp_val})

    def reset_password(self):
        """
        Resets user password with the newly submitted choice.
        """
        email = self.forgot_password_screen.email_entry.get().strip()
        new_password = self.forgot_password_screen.new_password_entry.get().strip()
        if not email or not new_password:
            self.forgot_password_screen.feedback_lbl.config(text="Email and new password are required.", fg=self.error_color)
            return
        if not self.client.socket:
            if not self.connect_to_server():
                return
        self.client.send({"action": "reset_password", "email": email, "new_password": new_password})

    def logout(self):
        """
        Gracefully disconnects user session and updates state variables.
        """
        self.client.send({"action": "logout"})
        self.client.disconnect()
        self.current_user = None
        self.active_chat = None
        self.active_chat_name = ""
        self.online_users = []
        self.recent_chats = []
        self.broadcast_history = []

        self.toast.cancel()

        self.dashboard_screen.profile_name_lbl.config(text="User: Offline")
        self.login_screen.email_entry.delete(0, "end")
        self.login_screen.password_entry.delete(0, "end")
        self.login_screen.feedback_lbl.config(text="")
        
        self.dashboard_screen.welcome_pane.pack(fill="both", expand=True)
        self.dashboard_screen.chat_pane.pack_forget()

        self.show_frame(self.login_screen)
        self.connect_to_server()

    def search_user(self):
        """
        Queries user database by email address.
        """
        email = self.dashboard_screen.search_entry.get().strip()
        if not email:
            self.dashboard_screen.search_result_lbl.config(text="Type an email first.", fg="red")
            return
        if self.current_user and email == self.current_user["email"]:
            self.dashboard_screen.search_result_lbl.config(text="Cannot search yourself.", fg="red")
            return
        self.dashboard_screen.search_result_lbl.config(text="Searching...", fg="black")
        self.dashboard_screen.search_result_card.pack_forget()
        self.client.send({"action": "find_user", "email": email})

    def start_chat_with_found_user(self):
        """
        Initializes a chat screen with a search-resolved user.
        """
        if self.found_user:
            self.dashboard_screen.open_chat(self.found_user["email"], self.found_user["name"], self.found_user["online"])
            self.dashboard_screen.search_result_card.pack_forget()
            self.dashboard_screen.search_entry.delete(0, "end")
            self.dashboard_screen.search_result_lbl.config(text="")
            self.found_user = None

    def on_message_enter(self, event):
        """
        Handles chat entry Return bindings (Enter sends, Shift+Enter adds line breaks).
        """
        if event.state & 0x0001:  # Shift + Enter
            return None  # Let default behavior occur (insert newline)
        else:
            self.send_message()
            return "break"  # Prevent default newline insertion on plain Enter

    def send_message(self):
        """
        Dispatches private or broadcast message payload to server.
        """
        content = self.dashboard_screen.message_entry.get("1.0", "end-1c").strip()
        if not content or not self.active_chat:
            return

        if self.active_chat == "__broadcast__":
            self.client.send({"action": "broadcast", "content": content})
            self.broadcast_history.append({
                "sender": self.current_user["email"],
                "content": content,
                "time": datetime.now().strftime("%I:%M %p")
            })
            self.dashboard_screen.append_message("You", content, is_broadcast=True)
        else:
            self.client.send({"action": "message", "to": self.active_chat, "content": content})
            self.dashboard_screen.append_message("You", content)

        self.dashboard_screen.message_entry.delete("1.0", "end")
        self.client.send({"action": "get_recent_chats"})

    # ------------------ Message Processing ------------------

    def process_message(self, data):
        """
        Unpacks incoming server action JSON payloads.
        """
        status = data.get("status")
        action = data.get("action")

        if status == "ok":
            if action == "login":
                self.current_user = {"email": data["email"], "name": data["name"]}
                self.dashboard_screen.profile_name_lbl.config(text=f"User: {data['name']}")
                self.show_main_app()
                
            elif action == "register":
                self.registration_screen.feedback_lbl.config(text=data["message"], fg=self.success_color)
                self.root.after(1500, lambda: self.show_frame(self.login_screen))
                
            elif action == "register_send_otp":
                self.registration_screen.feedback_lbl.config(text=data["message"], fg=self.success_color)
                
            elif action == "forgot_password":
                self.forgot_password_screen.feedback_lbl.config(text=data["message"], fg=self.success_color)
            elif action == "verify_otp":
                self.forgot_password_screen.feedback_lbl.config(text=data["message"], fg=self.success_color)
            elif action == "reset_password":
                self.forgot_password_screen.feedback_lbl.config(text=data["message"], fg=self.success_color)
                self.root.after(1500, lambda: self.show_frame(self.login_screen))
                
            elif action == "find_user":
                email = data["email"]
                name = data["name"]
                online = data.get("online", False)
                self.dashboard_screen.search_result_lbl.config(text="")
                
                self.found_user = {"email": email, "name": name, "online": online}
                
                self.dashboard_screen.search_result_card.pack(fill="x", padx=5, pady=5)
                status_str = "online" if online else "offline"
                self.dashboard_screen.search_result_name.config(text=f"{name}\n({status_str})")

        elif status == "error":
            msg = data.get("message", "Error occurred.")
            if action == "login":
                self.login_screen.feedback_lbl.config(text=msg, fg=self.error_color)
            elif action == "register" or action == "register_send_otp":
                self.registration_screen.feedback_lbl.config(text=msg, fg=self.error_color)
            elif action == "forgot_password" or action == "verify_otp" or action == "reset_password":
                self.forgot_password_screen.feedback_lbl.config(text=msg, fg=self.error_color)
            elif action == "find_user":
                self.dashboard_screen.search_result_lbl.config(text=msg, fg=self.error_color)
                self.dashboard_screen.search_result_card.pack_forget()

        elif status == "online_users":
            self.online_users = data.get("users", [])
            self.dashboard_screen.update_contacts_list()

        elif status == "recent_chats":
            self.recent_chats = data.get("chats", [])
            self.dashboard_screen.update_contacts_list()

        elif status == "chat_history":
            partner = data.get("partner")
            if self.active_chat and self.active_chat.lower() == partner.lower():
                self.dashboard_screen.chat_display.config(state="normal")
                self.dashboard_screen.chat_display.delete("1.0", "end")
                self.dashboard_screen.last_displayed_date = None
                for msg in data.get("history", []):
                    is_sent = msg["sender"].lower() == self.current_user["email"].lower()
                    sender = "You" if is_sent else self.active_chat_name
                    self.dashboard_screen.append_message(sender, msg["content"], timestamp=msg.get("time"))
                self.dashboard_screen.chat_display.config(state="disabled")

        elif status == "message":
            sender_mail = data.get("from")
            content = data.get("content")
            if self.active_chat and self.active_chat.lower() == sender_mail.lower():
                self.dashboard_screen.append_message(self.active_chat_name, content, timestamp=data.get("time"))
            else:
                self.unread_counts[sender_mail.lower()] = self.unread_counts.get(sender_mail.lower(), 0) + 1
                self.dashboard_screen.update_contacts_list()
                sender_name = self.get_contact_name(sender_mail)
                self.show_toast(sender_name, content)
                self.client.send({"action": "get_recent_chats"})

        elif status == "broadcast":
            sender_mail = data.get("from")
            content = data.get("content")
            self.broadcast_history.append({
                "sender": sender_mail,
                "content": content,
                "time": data.get("time") if data.get("time") else datetime.now().strftime("%I:%M %p")
            })
            if self.active_chat and self.active_chat == "__broadcast__":
                self.dashboard_screen.append_message(sender_mail, content, is_broadcast=True, timestamp=data.get("time"))
            else:
                self.unread_counts["__broadcast__"] = self.unread_counts.get("__broadcast__", 0) + 1
                self.dashboard_screen.update_contacts_list()
                sender_name = self.get_contact_name(sender_mail)
                self.show_toast(f"Broadcast from {sender_name}", content)

    def show_main_app(self):
        """
        Transitions to main dashboard view and queries lists.
        """
        self.show_frame(self.dashboard_screen)
        self.client.send({"action": "get_recent_chats"})
        self.client.send({"action": "get_online_users"})

    def on_contact_double_click(self, event):
        """
        Double-click contact callback to open direct chats.
        """
        selection = self.dashboard_screen.curselection() if hasattr(self.dashboard_screen, 'curselection') else self.dashboard_screen.contacts_listbox.curselection()
        if selection:
            index = selection[0]
            contact = self.dashboard_screen.contacts_data[index]
            self.dashboard_screen.open_chat(contact["email"], contact["name"], contact["online"])

    def on_closing(self):
        """
        Gracefully notifies server of exit and destroys Tkinter app event loop.
        """
        try:
            self.client.send({"action": "logout"})
        except:
            pass
        self.client.disconnect()
        self.root.destroy()

if __name__ == "__main__":
    App()
