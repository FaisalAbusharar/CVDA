# CVDA

## Control via Discord Application

Have you ever been lying in bed or away from home and wished you could control your PC — like shutting it down — without complicated apps or unreliable tools?  
**CVDA** makes it simple, using the power of Discord to give you remote access without any unnecessary bloat.

This software currently only works for Windows systems.
Application itself is 19MB, Dependencies are roughly ~35MB in size. All folders can be removed after executable has been installed & run.
Python 3.10 is around 120 MB. Total application size is: 174MB. 

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
- Implemented slash commands
- Support for multiple keystrokes in a single command
- Works only on one specific server for privacy reasons
- Copy text & images directly to your PC's clipboard
- Retrieve current clipboard contents remotely (Including images)
- Remote file (including image and video) sending to your PC
- User-locked protection (commands can only be run by you).
- Support for function keys in keystroke commands
- Switch tabs remotely from anywhere. 
- Take a screenshot of your desktop and view it.

---

## 🔧 Upcoming Features


- Kill specific running applications by command
- Advanced features, including being able to open apps from the bot by storing the file paths
- Help command for explaination
- Compiler bug fixes.

---

## 🛠️ Setup & Usage Guide

1. Download and install Python 3.10.0 from [https://www.python.org/downloads/release/python-3100/](https://www.python.org/downloads/release/python-3100/).  
2. During the python installation, select add PYTHON to Path once you open the executable.
3. Clone the repository or download the source files.  
4. Setup a Discord bot by following the tutorial [here](https://discordpy.readthedocs.io/en/stable/discord.html).  
5. Open the `config.json` file.  
    - Insert your Discord bot token.  
    - Insert your server ID in the `guild_id` variable.  
    - Insert your user ID or authorized users ID in the `allowed_users` variable.
    - Set the path to your preferred browser.  
    - Set `startup=false` if you do not want it to load on startup.
6. Run the provided `.bat` file to execute the compiler.  
7. Monitor the compiler messages for any errors.  
    - Ensure the compiled `.exe` has been moved to the startup folder if requested.  
8. Check if your Discord bot is online.  
    - If not, you can run the `.exe` manually.  
9. Slash commands may take up to 20 minutes to appear—please wait before reporting issues. 
10. Python 3.10.0 might not work with pyinstaller on some systems, [use python 3.9](https://www.python.org/downloads/release/python-390/) instead. 


## 🔐 Privacy & Usage

This tool is designed for **personal use**. Avoid using it in servers where untrusted users may have access. For maximum safety and control, it's recommended to run CVDA on a private Discord server where only you and the bot are present.

---

## 👨‍💻 Developed by Faisal Abusharar

Don't mind the rough code, it's a WIP.
