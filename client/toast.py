import tkinter
from config import COLOR_CARD, COLOR_ACCENT, COLOR_TEXT_PRIMARY, COLOR_TEXT_MUTED, FONT_BOLD, FONT_SMALL

class ToastNotification:
    """
    Manages custom animated, slide-in in-app notification toasts in a Tkinter window.
    """
    def __init__(self, parent_window):
        self.parent = parent_window
        self.frame = None
        self.y_pos = -80

    def show(self, title, message):
        """
        Creates and slides down a notification toast. Fades after 3.5 seconds.
        """
        # Dismiss any currently active toast
        if self.frame:
            try:
                self.frame.destroy()
            except:
                pass
                
        # Card container matching visual style guidelines
        self.frame = tkinter.Frame(
            self.parent,
            bg=COLOR_CARD,
            highlightbackground=COLOR_ACCENT,
            highlightthickness=1,
            padx=10,
            pady=6
        )
        
        # Title Label (Sender Name)
        title_lbl = tkinter.Label(
            self.frame,
            text=title,
            font=FONT_BOLD,
            fg=COLOR_TEXT_PRIMARY,
            bg=COLOR_CARD,
            anchor="w"
        )
        title_lbl.pack(fill="x")
        
        # Message body (truncated if > 50 characters)
        content = message if len(message) < 50 else message[:47] + "..."
        body_lbl = tkinter.Label(
            self.frame,
            text=content,
            font=FONT_SMALL,
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_CARD,
            anchor="w",
            justify="left",
            wraplength=200
        )
        body_lbl.pack(fill="x", pady=(2, 0))
        
        # Initial position off-screen
        self.y_pos = -80
        self.frame.place(relx=0.98, y=self.y_pos, anchor="ne")
        
        def slide_down():
            if self.y_pos < 20:
                self.y_pos += 10
                self.frame.place_configure(y=self.y_pos)
                self.parent.after(15, slide_down)
            else:
                self.parent.after(3500, slide_up)
                
        def slide_up():
            if self.y_pos > -100:
                self.y_pos -= 10
                self.frame.place_configure(y=self.y_pos)
                self.parent.after(15, slide_up)
            else:
                try:
                    self.frame.destroy()
                except:
                    pass
                self.frame = None
                
        slide_down()
        
    def cancel(self):
        """
        Immediately cancels and destroys the toast if active.
        """
        if self.frame:
            try:
                self.frame.destroy()
            except:
                pass
            self.frame = None
