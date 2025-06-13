# CVDA

## Control via Discord Application

Have you ever been lying in bed or away from home and wished you could control your PC — like shutting it down — without complicated apps or unreliable tools?  
**CVDA** makes it simple, using the power of Discord to give you remote access without any unnecessary bloat.

---

## 🚀 How It Works

CVDA connects to your computer through a custom Discord bot that listens for specific commands you send. The program automatically compiles itself into an executable and places it in the system startup folder, ensuring it runs every time your PC boots.  
*(If you prefer to disable this, simply change `STARTUP=True` to `STARTUP=False` in the compile.py file.)*

---

## ✅ Current Features

- Remotely shut down your computer via Discord
- Open any website on your preferred browser remotely
- Send individual keystrokes to your computer (single key per command)
- Control system volume through keystroke commands
- Auto-compiler that handles setup and startup integration automatically

---

## 🔧 Upcoming Features

- Support for multiple keystrokes in a single command
- Remote image sending to your PC
- Copy text directly to your PC’s clipboard
- Retrieve current clipboard contents remotely
- Kill specific running applications by command
- User-locked protection (commands can only be run by you).

---

## 🛠️ Setup & Usage Guide

1. Clone the repository or download the source files.
2. Open the `CVDA.py` file.
    - Insert your Discord bot token.
    - Set the path to your preferred browser.
    - (Optional) Change the command prefix if desired.
3. Open the `compile.py` file.
    - Set `STARTUP=False` if you do not want the bot to run on startup.
4. Run the provided `.bat` file to execute the compiler.
5. Monitor the compiler messages for any errors.
    - Ensure the compiled `.exe` has been moved to the startup folder if requested.
6. Check if your Discord bot is online.
    - If not, you can run the `.exe` manually.
7. Start sending commands to your bot using your prefix.
    - Example: `PC-shutdown` or `PC-web youtube.com`

---

## 🔐 Privacy & Usage

This tool is designed for **personal use**. Avoid using it in servers where untrusted users may have access. For maximum safety and control, it's recommended to run CVDA on a private Discord server where only you and the bot are present.

---

## 👨‍💻 Developed by Faisal Abusharar

Don't mind the rough code, it's a WIP.
