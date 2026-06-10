# RADWAVE

A ransomware **simulation and educational demo** built with Python and Tkinter.  
Designed for cybersecurity learning — demonstrates file encryption, countdowns, and decryption flow without any C2 or network component.

> **FOR EDUCATIONAL USE ONLY.**  
> Do not deploy against systems you do not own. Unauthorized use is illegal.

---

## Features

- **Fernet symmetric encryption** — encrypts all files in the working directory on close
- **Dual countdown timers** — simulates "pay deadline" and "price increase" pressure
- **Ransomware-style UI** — dark themed Tkinter GUI mimicking real ransom notes
- **Password-gated decryption** — correct key restores all files instantly
- **Safe by design** — no network calls, no C2, no persistence mechanism

---

## Project Structure

```
.
├── radware.py          # v1 — base implementation
├── radware2.py         # v2 — iterative improvements
├── radware3.py         # v3 — latest version
├── radware.spec        # PyInstaller spec for v1
├── radware2.spec       # PyInstaller spec for v2
├── radware3.spec       # PyInstaller spec for v3
├── build/              # PyInstaller build artifacts
├── dist/               # Compiled binaries
└── README.md
```

---

## Requirements

```bash
pip install cryptography
```

Tkinter is included with standard Python. If missing:

```bash
# Termux
pkg install python-tkinter

# Debian/Ubuntu
sudo apt install python3-tk
```

---

## Usage

### Run from source
```bash
python radware3.py
```

### Run standalone (no dependencies needed)
Pre-compiled binaries are available in `dist/` — just execute directly:

```bash
# Linux / Termux (aarch64)
./dist/radware3

# Windows
dist\radware3.exe
```

> No Python installation or `pip install` required. Everything is bundled via PyInstaller.

- **Closing the window** triggers encryption of all files in the current directory  
  (excludes `vlc.py`, `key.key`, `dec.py` and the script itself)
- Enter the password in the bottom bar and click **Decrypt** to restore files
- `key.key` is generated on first encrypt and must be present to decrypt

---

## Building a Binary (PyInstaller)

```bash
pip install pyinstaller

# Standard build
pyinstaller --onefile radware3.py

# Using the spec file
pyinstaller radware3.spec
```

Output binary lands in `dist/`.

> **Termux/ARM note:** Requires Vite 5 / PyInstaller compatible with aarch64.  
> If you hit CPU incompatibility errors, downgrade PyInstaller:  
> `pip install pyinstaller==5.13.2`

---

## How It Works

| Event | Action |
|---|---|
| Window closed | `encrypt()` runs — Fernet key generated, all files encrypted, key saved to `key.key` |
| Correct password entered | `decrypt()` runs — reads `key.key`, restores all files |
| Wrong password | Popup: ACCESS DENIED |
| `key.key` missing | Popup: decryption impossible |

---

## Disclaimer

This project is intended strictly for:
- CTF practice
- Malware analysis education
- Demonstrating encryption concepts

The author is not responsible for any misuse.
