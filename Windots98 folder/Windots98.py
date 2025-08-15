import tkinter as tk
from tkinter import messagebox, colorchooser
from datetime import datetime
import time

USERNAME = "Gavin"
PASSWORD = "1998"
WALLPAPER = "skyblue"

class Windots98:
    def __init__(self, root):
        self.root = root
        self.root.attributes("-fullscreen", True)
        self.wallpaper = WALLPAPER
        self.selection_box = None
        self.start_x = self.start_y = 0
        self.show_startup()

    def show_startup(self):
        self.clear()
        self.root.configure(bg="black")
        logo = tk.Label(self.root, text="🌐 Windots 98", font=("Arial", 48), fg="cyan", bg="black")
        logo.pack(expand=True)
        self.root.after(2500, self.show_login)

    def show_login(self):
        self.clear()
        self.root.configure(bg=self.wallpaper)
        icon = tk.Label(self.root, text="👤", font=("Arial", 64), bg=self.wallpaper)
        icon.pack(pady=20)
        label = tk.Label(self.root, text="Welcome Gavin", font=("Arial", 16), bg=self.wallpaper)
        label.pack()
        self.user_entry = tk.Entry(self.root)
        self.user_entry.pack(pady=5)
        self.pass_entry = tk.Entry(self.root, show="*")
        self.pass_entry.pack(pady=5)
        tk.Button(self.root, text="Login", command=self.check_login).pack(pady=10)

    def check_login(self):
        if self.user_entry.get() == USERNAME and self.pass_entry.get() == PASSWORD:
            self.show_desktop()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

    def show_desktop(self):
        self.clear()
        self.root.configure(bg=self.wallpaper)
        self.root.bind("<Button-3>", self.right_click)
        self.root.bind("<ButtonPress-1>", self.start_box)
        self.root.bind("<B1-Motion>", self.drag_box)
        self.root.bind("<ButtonRelease-1>", self.end_box)
        self.create_taskbar()
        self.create_icons()

    def create_taskbar(self):
        bar = tk.Frame(self.root, bg="gray", height=40)
        bar.pack(side="bottom", fill="x")
        tk.Button(bar, text="🟦 Start", command=self.open_start).pack(side="left")
        self.clock_label = tk.Label(bar, text="", bg="gray")
        self.clock_label.pack(side="right", padx=10)
        tk.Label(bar, text="🔋100%", bg="gray").pack(side="right", padx=10)
        tk.Label(bar, text=datetime.now().strftime("%Y-%m-%d"), bg="gray").pack(side="right", padx=10)
        self.update_clock()

    def update_clock(self):
        self.clock_label.config(text=time.strftime("%H:%M:%S"))
        self.root.after(1000, self.update_clock)

    def create_icons(self):
        apps = [("📝 Notepad", self.notepad), ("📄 WordPad", self.wordpad),
                ("🎨 Paint", self.paint), ("ℹ️ WinAbout", self.winabout),
                ("⚙️ Settings", self.settings)]
        for i, (name, func) in enumerate(apps):
            tk.Button(self.root, text=name, command=func).place(x=20, y=20 + i*60)

    def open_start(self):
        menu = tk.Toplevel(self.root)
        menu.title("Start Menu")
        menu.geometry("200x300+0+300")
        tk.Label(menu, text="👤 " + USERNAME, font=("Arial", 14)).pack(pady=5)
        for label, func in [("Notepad", self.notepad), ("WordPad", self.wordpad),
                            ("Paint", self.paint), ("WinAbout", self.winabout),
                            ("Settings", self.settings), ("Shutdown", self.shutdown)]:
            tk.Button(menu, text=label, command=func).pack(fill="x", pady=2)

    def right_click(self, event):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Display Settings", command=self.change_wallpaper)
        menu.add_command(label="Personalization", command=self.settings)
        menu.add_separator()
        menu.add_command(label="Shutdown", command=self.shutdown)
        menu.post(event.x_root, event.y_root)

    def change_wallpaper(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.wallpaper = color
            self.root.configure(bg=color)

    def notepad(self):
        self.editor_window("Notepad", "Type notes here...")

    def wordpad(self):
        self.editor_window("WordPad", "Start writing...")

    def editor_window(self, title, content):
        win = tk.Toplevel(self.root)
        win.title(title)
        txt = tk.Text(win)
        txt.insert("1.0", content)
        txt.pack(expand=True, fill="both")

    def paint(self):
        win = tk.Toplevel(self.root)
        win.title("Paint")
        canvas = tk.Canvas(win, bg="white", width=400, height=300)
        canvas.pack()
        canvas.bind("<B1-Motion>", lambda e: canvas.create_oval(e.x, e.y, e.x+3, e.y+3, fill="black"))

    def winabout(self):
        messagebox.showinfo("About", "Windots 98\nVersion 2.0\nDesigned by Gavin & Python 🐍")

    def settings(self):
        win = tk.Toplevel(self.root)
        win.title("Settings")
        tk.Label(win, text="Change Username:").pack()
        entry = tk.Entry(win)
        entry.pack()
        tk.Button(win, text="Save", command=lambda: self.set_user(entry.get())).pack()

    def set_user(self, name):
        global USERNAME
        if name:
            USERNAME = name
            messagebox.showinfo("Saved", "Username updated!")

    def shutdown(self):
        self.clear()
        self.root.configure(bg="black")
        msg = tk.Label(self.root, text="🛑 Windots 98 is shutting down...", font=("Arial", 24), fg="red", bg="black")
        msg.pack(expand=True)
        self.root.after(3000, self.root.quit)

    def start_box(self, event):
        self.start_x, self.start_y = event.x, event.y
        if self.selection_box:
            self.selection_box.destroy()
        self.selection_box = tk.Frame(self.root, bg="lightblue", highlightbackground="blue", highlightthickness=1)
        self.selection_box.place(x=self.start_x, y=self.start_y)

    def drag_box(self, event):
        cur_x, cur_y = event.x, event.y
        x = min(self.start_x, cur_x)
        y = min(self.start_y, cur_y)
        width = abs(cur_x - self.start_x)
        height = abs(cur_y - self.start_y)
        self.selection_box.place(x=x, y=y, width=width, height=height)

    def end_box(self, event):
        if self.selection_box:
            self.selection_box.destroy()
            self.selection_box = None

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Launch the OS
root = tk.Tk()
app = Windots98(root)
root.mainloop()