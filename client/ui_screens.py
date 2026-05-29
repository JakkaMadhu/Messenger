import tkinter
from tkinter import scrolledtext
from config import (
    COLOR_BG, COLOR_CARD, COLOR_TEXT_PRIMARY, COLOR_TEXT_MUTED,
    COLOR_ACCENT, COLOR_ACCENT_HOVER, COLOR_ERROR, COLOR_SUCCESS,
    FONT_TITLE, FONT_BODY, FONT_BOLD, FONT_SMALL, FONT_TOGGLE
)
from utils import parse_datetime, get_date_label

# ------------------ Styled Widget Factories ------------------

def create_card_frame(parent, padx=30, pady=30, **kwargs):
    """
    Creates a styled card container matching visual guidelines.
    """
    return tkinter.Frame(parent, bg=COLOR_CARD, bd=0, padx=padx, pady=pady, **kwargs)

def create_themed_label(parent, text, font=FONT_SMALL, fg=COLOR_TEXT_MUTED, bg=COLOR_CARD, **kwargs):
    """
    Creates a themed text label inside card containers.
    """
    return tkinter.Label(parent, text=text, font=font, bg=bg, fg=fg, **kwargs)

def create_themed_entry(parent, width=35, show=None, **kwargs):
    """
    Creates a dark-theme styled Entry input field.
    """
    return tkinter.Entry(
        parent, width=width, show=show, font=FONT_BODY,
        bg=COLOR_BG, fg=COLOR_TEXT_PRIMARY, insertbackground=COLOR_TEXT_PRIMARY,
        bd=1, relief="solid", highlightthickness=0, **kwargs
    )

def create_primary_button(parent, text, command, width=25, height=1, **kwargs):
    """
    Creates a modern accented primary action button.
    """
    return tkinter.Button(
        parent, text=text, command=command, font=FONT_BOLD,
        bg=COLOR_ACCENT, fg=COLOR_TEXT_PRIMARY,
        activebackground=COLOR_ACCENT_HOVER, activeforeground=COLOR_TEXT_PRIMARY,
        bd=0, relief="flat", cursor="hand2", width=width, height=height, **kwargs
    )

def create_link_button(parent, text, command, font=FONT_SMALL, bg=COLOR_CARD, fg=COLOR_ACCENT, activeforeground=COLOR_ACCENT_HOVER, **kwargs):
    """
    Creates an unbordered click action link.
    """
    return tkinter.Button(
        parent, text=text, command=command, font=font,
        bg=bg, fg=fg, activebackground=bg, activeforeground=activeforeground,
        bd=0, relief="flat", cursor="hand2", **kwargs
    )

# ------------------ Modular Screens ------------------

class LoginScreen(tkinter.Frame):
    """
    Tkinter view for the Login / Sign In screen.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        
        card = create_card_frame(self)
        card.pack(padx=20, pady=20)

        # Header Title
        create_themed_label(card, text="Sign In", font=FONT_TITLE, fg=COLOR_TEXT_PRIMARY).grid(row=0, column=0, columnspan=2, pady=(0, 25))

        # Email Entry
        create_themed_label(card, text="Email Address", anchor="w").grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 2))
        self.email_entry = create_themed_entry(card, width=35)
        self.email_entry.grid(row=2, column=0, columnspan=2, ipady=5, pady=(0, 15))

        # Password Entry
        create_themed_label(card, text="Password", anchor="w").grid(row=3, column=0, columnspan=2, sticky="w", pady=(5, 2))
        
        password_frame = tkinter.Frame(card, bg=COLOR_CARD)
        password_frame.grid(row=4, column=0, columnspan=2, pady=(0, 10), sticky="ew")

        self.password_entry = create_themed_entry(password_frame, width=30, show="*")
        self.password_entry.pack(side="left", ipady=5, fill="x", expand=True)

        self.password_toggle_btn = tkinter.Button(
            password_frame, text="👁", 
            command=lambda: self.controller.toggle_password_visibility(self.password_entry, self.password_toggle_btn),
            font=FONT_TOGGLE, bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
            activebackground=COLOR_CARD, activeforeground=COLOR_TEXT_PRIMARY,
            bd=0, relief="flat", cursor="hand2", padx=5
        )
        self.password_toggle_btn.pack(side="right", padx=(5, 0))

        # Feedback Label
        self.feedback_lbl = create_themed_label(card, text="", fg=COLOR_ERROR)
        self.feedback_lbl.grid(row=5, column=0, columnspan=2, pady=(0, 10))

        # Login Button
        login_btn = create_primary_button(card, text="Login", command=self.controller.login)
        login_btn.grid(row=6, column=0, columnspan=2, ipady=4, pady=(5, 15))

        # Links Panel
        links_frame = tkinter.Frame(card, bg=COLOR_CARD)
        links_frame.grid(row=7, column=0, columnspan=2, sticky="ew")

        forgot_btn = create_link_button(
            links_frame, text="Forgot Password?",
            command=lambda: self.controller.show_frame(self.controller.forgot_password_screen)
        )
        forgot_btn.pack(side="left")

        register_btn = create_link_button(
            links_frame, text="Create Account",
            command=lambda: self.controller.show_frame(self.controller.registration_screen)
        )
        register_btn.pack(side="right")


class RegistrationScreen(tkinter.Frame):
    """
    Tkinter view for the Account Registration screen.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        card = create_card_frame(self)
        card.pack(padx=20, pady=20)

        # Header Title
        create_themed_label(card, text="Create Account", font=FONT_TITLE, fg=COLOR_TEXT_PRIMARY).grid(row=0, column=0, columnspan=3, pady=(0, 25))

        # Full Name Entry
        create_themed_label(card, text="Full Name", anchor="w").grid(row=1, column=0, columnspan=3, sticky="w", pady=(5, 2))
        self.name_entry = create_themed_entry(card, width=35)
        self.name_entry.grid(row=2, column=0, columnspan=3, ipady=5, pady=(0, 15))

        # Email & Send OTP Entry
        create_themed_label(card, text="Email Address", anchor="w").grid(row=3, column=0, columnspan=3, sticky="w", pady=(5, 2))
        self.email_entry = create_themed_entry(card, width=22)
        self.email_entry.grid(row=4, column=0, columnspan=2, ipady=5, pady=(0, 15), sticky="w")
        
        send_otp_btn = create_primary_button(card, text="Send OTP", command=self.controller.send_registration_otp, width=10)
        send_otp_btn.grid(row=4, column=2, ipady=4, pady=(0, 15), padx=(5, 0), sticky="e")

        # Password Entry
        create_themed_label(card, text="Password", anchor="w").grid(row=5, column=0, columnspan=3, sticky="w", pady=(5, 2))
        
        password_frame = tkinter.Frame(card, bg=COLOR_CARD)
        password_frame.grid(row=6, column=0, columnspan=3, pady=(0, 15), sticky="ew")

        self.password_entry = create_themed_entry(password_frame, width=30, show="*")
        self.password_entry.pack(side="left", ipady=5, fill="x", expand=True)

        self.password_toggle_btn = tkinter.Button(
            password_frame, text="👁", 
            command=lambda: self.controller.toggle_password_visibility(self.password_entry, self.password_toggle_btn),
            font=FONT_TOGGLE, bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
            activebackground=COLOR_CARD, activeforeground=COLOR_TEXT_PRIMARY,
            bd=0, relief="flat", cursor="hand2", padx=5
        )
        self.password_toggle_btn.pack(side="right", padx=(5, 0))

        # OTP Entry
        create_themed_label(card, text="OTP Verification Code", anchor="w").grid(row=7, column=0, columnspan=3, sticky="w", pady=(5, 2))
        self.otp_entry = create_themed_entry(card, width=35)
        self.otp_entry.grid(row=8, column=0, columnspan=3, ipady=5, pady=(0, 10))

        # Feedback Label
        self.feedback_lbl = create_themed_label(card, text="", fg=COLOR_ERROR)
        self.feedback_lbl.grid(row=9, column=0, columnspan=3, pady=(0, 10))

        # Register Button
        register_btn = create_primary_button(card, text="Register", command=self.controller.register_account)
        register_btn.grid(row=10, column=0, columnspan=3, ipady=4, pady=(5, 15))

        back_btn = create_link_button(
            card, text="Back to Login",
            command=lambda: self.controller.show_frame(self.controller.login_screen)
        )
        back_btn.grid(row=11, column=0, columnspan=3, pady=5)


class ForgotPasswordScreen(tkinter.Frame):
    """
    Tkinter view for the Forgot Password / Reset Password screen.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        card = create_card_frame(self)
        card.pack(padx=20, pady=20)

        # Header Title
        create_themed_label(card, text="Forgot Password", font=FONT_TITLE, fg=COLOR_TEXT_PRIMARY).grid(row=0, column=0, columnspan=3, pady=(0, 25))

        # Email Entry
        create_themed_label(card, text="Email Address", anchor="w").grid(row=1, column=0, columnspan=3, sticky="w", pady=(5, 2))
        self.email_entry = create_themed_entry(card, width=22)
        self.email_entry.grid(row=2, column=0, columnspan=2, ipady=5, pady=(0, 15), sticky="w")
        
        send_otp_btn = create_primary_button(card, text="Send OTP", command=self.controller.send_password_reset_otp, width=10)
        send_otp_btn.grid(row=2, column=2, ipady=4, pady=(0, 15), padx=(5, 0), sticky="e")

        # OTP Entry
        create_themed_label(card, text="OTP Code", anchor="w").grid(row=3, column=0, columnspan=3, sticky="w", pady=(5, 2))
        self.otp_entry = create_themed_entry(card, width=22)
        self.otp_entry.grid(row=4, column=0, columnspan=2, ipady=5, pady=(0, 15), sticky="w")
        
        verify_otp_btn = create_primary_button(card, text="Verify OTP", command=self.controller.verify_password_reset_otp, width=10)
        verify_otp_btn.grid(row=4, column=2, ipady=4, pady=(0, 15), padx=(5, 0), sticky="e")

        # New Password Entry
        create_themed_label(card, text="New Password", anchor="w").grid(row=5, column=0, columnspan=3, sticky="w", pady=(5, 2))
        
        new_password_frame = tkinter.Frame(card, bg=COLOR_CARD)
        new_password_frame.grid(row=6, column=0, columnspan=2, pady=(0, 10), sticky="ew")

        self.new_password_entry = create_themed_entry(new_password_frame, width=17, show="*")
        self.new_password_entry.pack(side="left", ipady=5, fill="x", expand=True)

        self.password_toggle_btn = tkinter.Button(
            new_password_frame, text="👁", 
            command=lambda: self.controller.toggle_password_visibility(self.new_password_entry, self.password_toggle_btn),
            font=FONT_TOGGLE, bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
            activebackground=COLOR_CARD, activeforeground=COLOR_TEXT_PRIMARY,
            bd=0, relief="flat", cursor="hand2", padx=5
        )
        self.password_toggle_btn.pack(side="right", padx=(5, 0))
        
        reset_btn = create_primary_button(card, text="Reset Pass", command=self.controller.reset_password, width=10)
        reset_btn.grid(row=6, column=2, ipady=4, pady=(0, 10), padx=(5, 0), sticky="e")

        # Feedback Label
        self.feedback_lbl = create_themed_label(card, text="", fg=COLOR_ERROR)
        self.feedback_lbl.grid(row=7, column=0, columnspan=3, pady=(0, 10))

        # Back Button
        back_btn = create_link_button(
            card, text="Back to Login",
            command=lambda: self.controller.show_frame(self.controller.login_screen)
        )
        back_btn.grid(row=8, column=0, columnspan=3, pady=5)


class DashboardScreen(tkinter.Frame):
    """
    Tkinter view for the Main Chat Dashboard (Sidebar + Chat Area).
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.contacts_data = []
        self.last_displayed_date = None

        # Left sidebar frame (Search + Contacts)
        left_frame = tkinter.Frame(self, width=250, bd=2, relief="groove")
        left_frame.pack(side="left", fill="y")
        left_frame.pack_propagate(False)

        # Current profile label
        self.profile_name_lbl = tkinter.Label(left_frame, text="User: Offline", font=("Arial", 10, "bold"), anchor="w")
        self.profile_name_lbl.pack(fill="x", padx=5, pady=5)
        
        tkinter.Button(left_frame, text="Logout", command=self.controller.logout).pack(fill="x", padx=5, pady=2)

        # Divider
        tkinter.Frame(left_frame, height=2, bd=1, relief="sunken").pack(fill="x", pady=5)

        # Search User Row
        tkinter.Label(left_frame, text="Search User by Email:").pack(anchor="w", padx=5)
        search_sub = tkinter.Frame(left_frame)
        search_sub.pack(fill="x", padx=5, pady=2)
        
        self.search_entry = tkinter.Entry(search_sub, width=20)
        self.search_entry.pack(side="left", fill="x", expand=True)
        tkinter.Button(search_sub, text="Go", command=self.controller.search_user).pack(side="right", padx=(2, 0))

        self.search_result_lbl = tkinter.Label(left_frame, text="", fg="blue", wraplength=230)
        self.search_result_lbl.pack(fill="x", padx=5)

        # Found User Frame
        self.search_result_card = tkinter.Frame(left_frame, bd=1, relief="solid")
        self.search_result_name = tkinter.Label(self.search_result_card, text="", font=("Arial", 9, "bold"))
        self.search_result_name.pack(fill="x", padx=2, pady=2)
        
        self.chat_now_btn = tkinter.Button(self.search_result_card, text="Start Chat", command=self.controller.start_chat_with_found_user)
        self.chat_now_btn.pack(pady=2)

        # Divider
        tkinter.Frame(left_frame, height=2, bd=1, relief="sunken").pack(fill="x", pady=5)

        # Contacts listbox
        tkinter.Label(left_frame, text="Contacts (Double Click to Chat):", font=("Arial", 9, "bold")).pack(anchor="w", padx=5)
        
        contacts_sub = tkinter.Frame(left_frame)
        contacts_sub.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.contacts_scrollbar = tkinter.Scrollbar(contacts_sub)
        self.contacts_scrollbar.pack(side="right", fill="y")
        
        self.contacts_listbox = tkinter.Listbox(contacts_sub, yscrollcommand=self.contacts_scrollbar.set)
        self.contacts_listbox.pack(side="left", fill="both", expand=True)
        self.contacts_scrollbar.config(command=self.contacts_listbox.yview)

        # Double click to open chat
        self.contacts_listbox.bind("<Double-Button-1>", self.controller.on_contact_double_click)

        # Right pane frame (Welcome Screen or Chat Area)
        self.right_frame = tkinter.Frame(self)
        self.right_frame.pack(side="right", fill="both", expand=True)

        # Welcome Screen
        self.welcome_pane = tkinter.Frame(self.right_frame)
        self.welcome_pane.pack(fill="both", expand=True)
        tkinter.Label(self.welcome_pane, text="Welcome to Messenger", font=("Arial", 16, "bold")).pack(pady=100)
        tkinter.Label(self.welcome_pane, text="Select a contact from the list on the left to start a conversation.").pack()

        # Chat Pane (starts hidden)
        self.chat_pane = tkinter.Frame(self.right_frame)

        # Chat Header
        self.chat_header_lbl = tkinter.Label(self.chat_pane, text="Chatting with: None", font=("Arial", 12, "bold"), bd=1, relief="solid")
        self.chat_header_lbl.pack(fill="x", padx=5, pady=5)

        # Text View for Messages
        self.chat_display = scrolledtext.ScrolledText(self.chat_pane, state="disabled", wrap="word")
        self.chat_display.pack(fill="both", expand=True, padx=5, pady=5)
        self.chat_display.tag_configure("left_msg", justify="left", foreground="black")
        self.chat_display.tag_configure("right_msg", justify="right", foreground="black")
        self.chat_display.tag_configure("left_time", justify="left", foreground="black", font=("Segoe UI", 9, "bold"))
        self.chat_display.tag_configure("right_time", justify="right", foreground="black", font=("Segoe UI", 9, "bold"))
        self.chat_display.tag_configure("date_header", justify="center", foreground=COLOR_TEXT_MUTED, font=("Segoe UI", 9, "bold"))

        # Send controls
        send_frame = tkinter.Frame(self.chat_pane)
        send_frame.pack(fill="x", padx=5, pady=5)
        
        self.message_entry = tkinter.Text(send_frame, height=3, wrap="word", font=FONT_BODY)
        self.message_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.message_entry.bind("<Return>", self.controller.on_message_enter)
        
        tkinter.Button(send_frame, text="Send", command=self.controller.send_message, width=10).pack(side="right")

    # ------------------ Rendering & Display Logic ------------------

    def update_contacts_list(self):
        """
        Refreshes contact Listbox entries combining Broadcast, Online, and Recent chats.
        """
        self.contacts_listbox.delete(0, "end")
        self.contacts_data = []

        # 1. Add Broadcast
        unread_counts = self.controller.unread_counts
        broadcast_unread = unread_counts.get("__broadcast__", 0)
        broadcast_badge = f" ({broadcast_unread})" if broadcast_unread > 0 else ""
        self.contacts_listbox.insert("end", f"📢 Broadcast to All{broadcast_badge}")
        self.contacts_data.append({"email": "__broadcast__", "name": "Broadcast to All", "online": True})

        # Merge recent and online users
        merged = {}
        for c in self.controller.recent_chats:
            merged[c["email"]] = {"name": c["name"], "online": False}

        for u in self.controller.online_users:
            if self.controller.current_user and u["email"] == self.controller.current_user["email"]:
                continue
            merged[u["email"]] = {"name": u["name"], "online": True}

        # Populating listbox
        for email, info in merged.items():
            status_str = "online" if info["online"] else "offline"
            unread = unread_counts.get(email.lower(), 0)
            badge = f" ({unread})" if unread > 0 else ""
            display_text = f"{info['name']} - {status_str}{badge}"
            self.contacts_listbox.insert("end", display_text)
            self.contacts_data.append({"email": email, "name": info["name"], "online": info["online"]})

    def open_chat(self, email, name, is_online):
        """
        Initializes messaging frame with selected partner.
        """
        self.controller.active_chat = email
        self.controller.active_chat_name = name
        self.last_displayed_date = None
        
        # Clear unread count for this contact
        if email.lower() in self.controller.unread_counts:
            self.controller.unread_counts[email.lower()] = 0
            self.update_contacts_list()

        self.welcome_pane.pack_forget()
        self.chat_pane.pack(fill="both", expand=True)

        header_text = f"Chatting with: {name} ({email})" if email != "__broadcast__" else "Broadcast message to all online users"
        self.chat_header_lbl.config(text=header_text)

        self.chat_display.config(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.config(state="disabled")

        if email == "__broadcast__":
            self.load_broadcast_history()
        else:
            self.controller.client.send({"action": "get_chat_history", "partner": email})

    def load_broadcast_history(self):
        """
        Reloads chat scrollbox messages from local broadcast memory cache.
        """
        self.chat_display.config(state="normal")
        self.chat_display.delete("1.0", "end")
        self.last_displayed_date = None
        for msg in self.controller.broadcast_history:
            sender = "You" if msg["sender"] == self.controller.current_user["email"] else msg["sender"]
            self.append_message(sender, msg["content"], is_broadcast=True, timestamp=msg.get("time"))
        self.chat_display.config(state="disabled")

    def append_message(self, sender, content, is_broadcast=False, timestamp=None):
        """
        Appends messages to the scrolled text widget with layout/tag configurations.
        """
        self.chat_display.config(state="normal")
        dt = parse_datetime(timestamp)
        time_str = dt.strftime("%I:%M %p")
        
        # Check if date divider is needed
        date_label = get_date_label(dt)
        if date_label != getattr(self, "last_displayed_date", None):
            self.chat_display.insert("end", f"\n{date_label}\n\n", "date_header")
            self.last_displayed_date = date_label
            
        is_me = (sender == "You")
        
        if is_broadcast:
            msg_text = f"[BROADCAST] {sender}:\n{content}\n"
        else:
            msg_text = f"{content}\n"
            
        time_text = f"{time_str}\n\n"

        if is_me:
            self.chat_display.insert("end", msg_text, "right_msg")
            self.chat_display.insert("end", time_text, "right_time")
        else:
            self.chat_display.insert("end", msg_text, "left_msg")
            self.chat_display.insert("end", time_text, "left_time")
            
        self.chat_display.see("end")
        self.chat_display.config(state="disabled")
