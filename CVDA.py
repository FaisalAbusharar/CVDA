from nextcord.ext import commands
import nextcord
import os
import webbrowser
from pynput.keyboard import Key, Controller
import pyperclip
import time
from PIL import Image, ImageGrab
import io
import ctypes
from pathlib import Path
import subprocess
import win32clipboard
import win32con
from uuid import UUID
import json


#! DO NOT CHANGE THE FILE NAME.

 
# ------------ VARIABLES YOU CHANGE ---------------


Activity = nextcord.Activity(name="CVDA 1.0.2", type=nextcord.ActivityType.listening) # You can change this aswell, it's optional. .playing .listening .watching are avaliable.

# ------------------------------------------------


def load_config():
    config = None


    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except:
        pass


    if config is None:
        try:
            localappdata = os.environ['LOCALAPPDATA'].replace("\\", "/")
            with open(f"{localappdata}/CVDA/config.json") as f:
                config = json.load(f)
        except:
            pass

    if config is None:
        print("Error, config.json was not found in the local appdata nor the directory where the .exe is stored. quitting..")
        quit()

    return config

def get_config_value(key: str, alter=False, lst=None):
    # lst expected to be [appkey, apppath]
    if lst is None:
        lst = []

    config = load_config() or {}

    if not alter:
        if key in config:
            return config[key]
        else:
            raise KeyError(f"'{key}' not found in config.json")

    else:


        appkey, apppath = lst


        config[appkey] = apppath

  
        try:
            with open("config.json", "w") as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            # If writing to local config.json fails, try fallback path
            try:
                localappdata = os.environ['LOCALAPPDATA'].replace("\\", "/")
                fallback_path = f"{localappdata}/CVDA/config.json"
                with open(fallback_path, "w") as f:
                    json.dump(config, f, indent=4)
            except Exception as e2:
                raise RuntimeError(f"Failed to save config: {e2}") from e2

        return config.get(key, None)
        
        
        

        

keyboard = Controller()


intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="PC-", intents=intents, activity=Activity)



#! ---------- GENERAL FUNCTIONS ------------


def get_downloads_folder():
    # The GUID for the Downloads folder
    guid = UUID('{374DE290-123F-4565-9164-39C4925E467B}')
    guid_bytes = (ctypes.c_byte * 16).from_buffer_copy(guid.bytes_le)

    SHGetKnownFolderPath = ctypes.windll.shell32.SHGetKnownFolderPath
    SHGetKnownFolderPath.argtypes = [ctypes.POINTER(ctypes.c_byte * 16), ctypes.c_uint32, ctypes.c_void_p, ctypes.POINTER(ctypes.c_wchar_p)]

    path_ptr = ctypes.c_wchar_p()
    result = SHGetKnownFolderPath(ctypes.byref(guid_bytes), 0, None, ctypes.byref(path_ptr))

    if result != 0:
        raise ctypes.WinError(result)

    return Path(path_ptr.value)



def isUserAllowed(userid):
    if userid in get_config_value("allowed_users"):
        return True
    else: 
        return False


#& --------------- COMPUTER HARDWARE CONTROL ------------------

@bot.slash_command(description="Shutdown the device.", guild_ids=[get_config_value("guild_id")])
async def shutdown(interaction: nextcord.Interaction):

    if not isUserAllowed(interaction.user.id): 
        await interaction.send("You are not authorized to use this bot.")
        return
    os.system("shutdown /s /t 0")
    await interaction.send("Shutting down..")



@bot.slash_command(description="Restart the device.", guild_ids=[get_config_value("guild_id")])
async def restart(interaction:  nextcord.Interaction):
    if not isUserAllowed(interaction.user.id): 
        await interaction.send("You are not authorized to use this bot.")
        return
    os.system("shutdown /r /t 1")
    await interaction.send("Restarting..")


#$ --------------- COMPUTER SOFTWARE CONTROL ------------------

@bot.slash_command(description="Input a URL that will be opened on the host device.", guild_ids=[get_config_value("guild_id")])
async def web(interaction: nextcord.Interaction, text: str = nextcord.SlashOption(description="The URL to open on the host device.")):
    if not isUserAllowed(interaction.user.id): 
        await interaction.send("You are not authorized to use this bot.")
        return
    try:
        webbrowser.get(get_config_value("browser_path")).open(text)
        await interaction.send(f"Opened {text} in your default browser.")
    except Exception as e:
        await interaction.send(f"Failed to open {text}: {e}")


@bot.slash_command(description="Upload a file to your device", guild_ids=[get_config_value("guild_id")])
async def upload(interaction: nextcord.Interaction, file: nextcord.Attachment):
    if not isUserAllowed(interaction.user.id): 
        await interaction.send("You are not authorized to use this bot.")
        return

    await interaction.send("Received your file.")
    
    image_bytes = await file.read()
    os.path.splitext(file.filename)[1]

    

    downloads = get_downloads_folder()
    save_path = f"{downloads}/CVDA_TRANSFER_{int(time.time())}{os.path.splitext(file.filename)[1]}"



    with open(save_path, "wb") as f:
        f.write(image_bytes)

    await interaction.send("File saved successfully.")


@bot.slash_command(description="Take a screenshot and send it.", guild_ids=[get_config_value("guild_id")])
async def screenshot(interaction: nextcord.Interaction):
    if not isUserAllowed(interaction.user.id):
        await interaction.send("You are not authorized to use this bot.")
        return

    # Take screenshot
    screenshot = ImageGrab.grab()
    
    # Save to BytesIO
    img_bytes = io.BytesIO()
    screenshot.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # Send as a file
    file = nextcord.File(img_bytes, filename="screenshot.png")
    await interaction.send("Here is the current screen:", file=file)


@bot.slash_command(description="Kill a specific application running by task manager.", guild_ids=[get_config_value("guild_id")])
async def killapp(interaction: nextcord.Interaction, appid: str = nextcord.SlashOption(description="The exact App ID of the executable, e.g. chrome.exe")):
    if not isUserAllowed(interaction.user.id):
        await interaction.send("You are not authorized to use this bot.")
        return
    
    exit = os.system(f"taskkill /f /im  {appid}")

    if exit == 0:
        await interaction.send(f"Application {appid} has been closed.")
    else:
        await interaction.send(f"Application {appid} was not found")



@bot.slash_command(description="Lock your computer.", guild_ids=[get_config_value("guild_id")])
async def lock(interaction: nextcord.Interaction):
    if not isUserAllowed(interaction.user.id):
        await interaction.send("You are not authorized to use this bot.")
        return
    
    ctypes.windll.user32.LockWorkStation()
    await interaction.send("Successfully locked your computer.")
    

    


#* -------------- COMPUTER KEYSTROKE CONTROL -----------------


@bot.slash_command(description="Send a keystroke to the device that will be inputted.", guild_ids=[get_config_value("guild_id")])
async def keystroke(interaction: nextcord.Interaction, text: str = nextcord.SlashOption(description="The key to press (e.g. 'enter', 'space', 'a').") ):
    if not isUserAllowed(interaction.user.id): 
        await interaction.send("You are not authorized to use this bot.")
        return

    text = text.lower()

    special_keys = {
    "space": Key.space,
    "shift": Key.shift,
    "ctrl": Key.ctrl_l,
    "enter": Key.enter,
    "esc": Key.esc,
    "backspace": Key.backspace,
    "up": Key.up,
    "down": Key.down,
    "left": Key.left,
    "right": Key.right,
    "volumeup": Key.media_volume_up,
    "volumedown": Key.media_volume_down,
    "f1": Key.f1,
    "f2": Key.f2,
    "f3": Key.f3,
    "f4": Key.f4,
    "f5": Key.f5,
    "f6": Key.f6,
    "f7": Key.f7,
    "f8": Key.f8,
    "f9": Key.f9,
    "f10": Key.f10,
    "f11": Key.f11,
    "f12": Key.f12,
    
    }

    key = special_keys.get(text.lower(), text)

    try:
        keyboard.press(key)
        keyboard.release(key)
        await interaction.send(f"Pressed key: {text}")
    except ValueError as e:
        await interaction.send(f"Invalid key: {text}")



@bot.slash_command(description="Simillar to the keystroke command, but types out full sentences.", guild_ids=[get_config_value("guild_id")])
async def type(
    interaction: nextcord.Interaction,text: str = nextcord.SlashOption(description="The full sentence to type on the host device."), 
               sendEnter: str = nextcord.SlashOption(
    name="send_enter",
    choices={"Yes": "yes", "No": "no"},
    required=False,
    default="no",
    description="Press enter after typing the message."
    ),):

    if not isUserAllowed(interaction.user.id): 
        await interaction.send("You are not authorized to use this bot.")
        return


      # This is a really specific edge case, but who knows, might be helpful.
    for char in text:
        if char == '\n':
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
        elif char == '\t':
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
        else:
            keyboard.type(char)


    if sendEnter == "yes":
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
    
    await interaction.send(f"Typed {text} on your device.")


@bot.slash_command(description="Copy to your device's clipboard, Note: Image will always be copied last.", guild_ids=[get_config_value("guild_id")])
async def clipboard(
    interaction: nextcord.Interaction, text: str = nextcord.SlashOption(description="Text to copy to the clipboard", required=False, default=None),
    image: nextcord.Attachment = nextcord.SlashOption(description="Copy an image to the clipboard", required=False, default=None),
    pasteAfter: str = nextcord.SlashOption(
        choices={"Yes": "yes", "No": "no"},
        required=False,
        default="no",
        description="Paste the clipboard after copying it",
        name="paste_clipboard",
    ),
):
    

    if not isUserAllowed(interaction.user.id): 
        await interaction.send("You are not authorized to use this bot.")
        return
    


    if image == None and text == None:
        await interaction.send("You have not inputted text or an image.")
        return
    
    if text != None:
        pyperclip.copy(text)
        if pasteAfter == "yes":
            keyboard.type(pyperclip.paste())


    if image != None:    
        data = await image.read()

      
        with open("temp_file", "wb") as f:
            f.write(data)

  
        image = Image.open("temp_file")

        output = io.BytesIO()
        image.convert("RGB").save(output, "BMP")  # BMP needed for CF_DIB
        data = output.getvalue()[14:]  # Skip BMP header for CF_DIB format
        output.close()

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_DIB, data)
        win32clipboard.CloseClipboard()


        if pasteAfter == "yes":
            keyboard.press(Key.ctrl)
            keyboard.press('v')
            keyboard.release('v')
            keyboard.release(Key.ctrl)



    os.remove("./temp_file")
    await interaction.send(f"Successfully copied to your device's clipboard.")



@bot.slash_command(description="Paste your device's clipboard to Discord", guild_ids=[get_config_value("guild_id")])
async def paste(interaction: nextcord.Interaction):
    if not isUserAllowed(interaction.user.id): 
        await interaction.send("You are not authorized to use this bot.")
        return

    await interaction.response.defer()


    text = pyperclip.paste()
    if text:
        await interaction.send(f"**Clipboard Text:**\n{text}")
    else:
        await interaction.send("No text found in clipboard.")

    try:
        clipboard_content = ImageGrab.grabclipboard()

        if clipboard_content is None:
            await interaction.send("No image or file found in clipboard.")
            return

        if isinstance(clipboard_content, list):

            for file_path in clipboard_content:
                ext = os.path.splitext(file_path)[1].lower()
                if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp']:
                    image = Image.open(file_path)
                    
                    image_bytes = io.BytesIO()
                    image.save(image_bytes, format='PNG')
                    image_bytes.seek(0)

                    filename = f"clipboard_{int(time.time())}.png"
                    file = nextcord.File(image_bytes, filename=filename)
                    await interaction.send(f"**Image from file path:** `{os.path.basename(file_path)}`", file=file)
                    return
            await interaction.send("No valid image file found in copied files.")
            return


        image_bytes = io.BytesIO()
        clipboard_content.save(image_bytes, format='PNG')
        image_bytes.seek(0)

        filename = f"clipboard_{int(time.time())}.png"
        file = nextcord.File(image_bytes, filename=filename)
        await interaction.send("**Clipboard Image:**", file=file)

    except Exception as e:
        await interaction.send(f"Error while reading image: `{e}`")




@bot.slash_command(description="Switch Tabs", guild_ids=[get_config_value("guild_id")])
async def switchtab(interaction: nextcord.Interaction, amount: int = nextcord.SlashOption
                    (description="The amount of tabs to switch through", default=1, required=False, name="amount")):
    
    if not isUserAllowed(interaction.user.id): 
        await interaction.send("You are not authorized to use this bot.")
        return


    keyboard.press(Key.alt_l)

    time.sleep(0.2)
    for i in range(amount):
        keyboard.tap(Key.tab)
        time.sleep(0.1)
    keyboard.release(Key.alt_l)
    time.sleep(0.2)

    await interaction.send(f"Switched tabs {amount} times.")


from pynput.keyboard import Key, Controller
keyboard = Controller()

@bot.slash_command(description="Activate a keyboard shortcut.", guild_ids=[get_config_value("guild_id")])
async def shortcut(interaction: nextcord.Interaction, keys: str = nextcord.SlashOption(description="The key combo (e.g. ctrl+shift+esc)")):
    if not isUserAllowed(interaction.user.id):
        await interaction.send("You are not authorized to use this bot.")
        return


    special_keys = {
        "space": Key.space,
        "shift": Key.shift,
        "ctrl": Key.ctrl_l,
        "alt": Key.alt_l,
        "enter": Key.enter,
        "esc": Key.esc,
        "backspace": Key.backspace,
        "up": Key.up,
        "down": Key.down,
        "left": Key.left,
        "right": Key.right,
        "tab": Key.tab,
        "capslock": Key.caps_lock,
        "cmd": Key.cmd,
        "win": Key.cmd,
        "delete": Key.delete,
        "home": Key.home,
        "end": Key.end,
        "pageup": Key.page_up,
        "pagedown": Key.page_down,
        "f1": Key.f1,
        "f2": Key.f2,
        "f3": Key.f3,
        "f4": Key.f4,
        "f5": Key.f5,
        "f6": Key.f6,
        "f7": Key.f7,
        "f8": Key.f8,
        "f9": Key.f9,
        "f10": Key.f10,
        "f11": Key.f11,
        "f12": Key.f12,
    }

    try:
        key_combo = keys.lower().split('+')
        key_sequence = []

        for k in key_combo:
            key_sequence.append(special_keys.get(k.strip(), k.strip()))

     
        for k in key_sequence:
            keyboard.press(k)

     
        for k in reversed(key_sequence):
            keyboard.release(k)

        await interaction.send(f"Shortcut executed: {keys}")
    except Exception as e:
        await interaction.send(f"Failed to execute shortcut: {e}")



#& ---------- ADVANCED FUNCTIONS ------------

@bot.slash_command(description="Allows you store a path of an application, with an ID", guild_ids=[get_config_value("guild_id")])
async def saveapp(interaction: nextcord.Interaction, 
                  appkey: str = nextcord.SlashOption(description="This is what you will use to open the app, the key.", required=True
                                                                                        ) ,apppath: str = nextcord.SlashOption(description="The exact path to the application, used to open the application.", required=True)):
    if not isUserAllowed(interaction.user.id): 
        await interaction.send("You are not authorized to use this bot.")
        return
    get_config_value(alter=True, key="ignore", lst=[appkey, apppath])
    await interaction.send("Successfully added Key & Path to your config.")


@bot.slash_command(description="Allows you store a path of an application, with an ID", guild_ids=[get_config_value("guild_id")])
async def loadapp(interaction: nextcord.Interaction, 
                  appkey: str = nextcord.SlashOption(description="The key you stored the app with.", required=True),
                  directpath: str = nextcord.SlashOption(description="Is this a direct path or a key?", choices=["Yes", "No"], default="No", required=False)):
    
    if not isUserAllowed(interaction.user.id): 
        await interaction.send("You are not authorized to use this bot.")
        return
    if directpath=="No": path = get_config_value(appkey)
    else: path = appkey
    result = subprocess.run([path], capture_output=True, text=True)
    if result.returncode == 0:
        await interaction.send("Successfully opened your app.")
    else:
        await interaction.send("App cannot be opened.")


#$ ------------- HELP COMMAND --------------
@bot.slash_command(description="List all commands and their usage details.", guild_ids=[get_config_value("guild_id")])
async def help(interaction: nextcord.Interaction):
    if not isUserAllowed(interaction.user.id): 
        await interaction.send("You are not authorized to use this bot.")
        return

    embed = nextcord.Embed(
        title="📘 Help Menu — CVDA Commands",
        description="Use the following commands to interact with your host device.",
        color=nextcord.Color.blue()
    )

    embed.add_field(
        name="🖥️ System Control",
        value=(
            "**/shutdown** - Instantly shuts down the device.\n"
            "**/restart** - Restarts the device after 1 second."
        ),
        inline=False
    )

    embed.add_field(
        name="🌐 Web & File Control",
        value=(
            "**/web text:** `<url>` — Opens a website.\n"
            "Example: `/web text:https://google.com`\n\n"
            "**/upload file:** `<attachment>` — Uploads a file to the host machine.\n\n"
            "**/screenshot** — Captures the current screen.\n\n"
            "**/killapp appid:** `<name.exe>` — Kills a process.\n"
            "Example: `/killapp appid:chrome.exe`"
        ),
        inline=False
    )

    embed.add_field(
        name="⌨️ Keyboard & Input",
        value=(
            "**/keystroke text:** `<key>` — Simulates a keypress.\n"
            "Example: `/keystroke text:enter`\n\n"
            "**/type text:** `<sentence>` | `send_enter:` Yes/No — Types a sentence.\n"
            "Example: `/type text:'Hello' send_enter:Yes`\n\n"
            "**/clipboard text/image:** Copies text or image to clipboard.\n"
            "Supports `paste_clipboard:` Yes/No.\n\n"
            "**/paste** — Pastes clipboard content back to Discord.\n\n"
            "**/switchtab amount:** `<number>` — Switches windows using Alt+Tab.\n"
            "Example: `/switchtab amount:2`"
        ),
        inline=False
    )

    embed.add_field(
        name="⚙️ App Management",
        value=(
            "**/saveapp appkey:** `<shortcut>` | `apppath:` `<path>` — Save an app path.\n"
            "Example: `/saveapp appkey:chrome apppath:'C:/Path/chrome.exe'`\n\n"
            "**/loadapp appkey:** `<shortcut_or_path>` | `directpath:` Yes/No — Open app.\n"
            "Example: `/loadapp appkey:chrome directpath:No`"
        ),
        inline=False
    )

    embed.set_footer(text="Use commands responsibly. Only authorized users can access them.")
    
    await interaction.send(embed=embed)



print(get_config_value("guild_id"))
if __name__ == "__main__":
    bot.run(get_config_value("discord_token")) 

#todo: Developed by Faisal Abusharar.. More features soon :D