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
import win32clipboard
import win32con
from uuid import UUID

# DO NOT CHANGE THE FILE NAME.

 
# ------------ VARIABLES YOU CHANGE ---------------

browser_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'  # Change this based on your browser path.
discord_token = "" # Add your discord bot token here.
guild_id = 122176734267676 # Add your guild ID here, this allows you to only have the commands work in one server & instant updates.
allowed_users = [730505256153456423, 7120523256153456343] # Add your user ID here, this allows you to choose who is allowed to use the commands. You are allowed multiple people.

Activity = nextcord.Activity(name="CVDA 0.2.8 Beta", type=nextcord.ActivityType.listening) # You can change this aswell, it's optional. .playing .listening .watching are avaliable.

# ------------------------------------------------

keyboard = Controller()


intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="PC-", intents=intents, activity=Activity)



# ---------- GENERAL FUNCTIONS ------------


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
    if userid in allowed_users:
        return True
    else: 
        return False


# --------------- COMPUTER HARDWARE CONTROL ------------------

@bot.slash_command(description="Shutdown the device.", guild_ids=[guild_id])
async def shutdown(interaction: nextcord.Interaction):

    if not isUserAllowed(interaction.user.id): 
        await interaction.send("You are not authorized to use this bot.")
        return
    os.system("shutdown /s /t 0")
    await interaction.send("Shutting down..")



@bot.slash_command(description="Restart the device.", guild_ids=[guild_id])
async def restart(interaction:  nextcord.Interaction):
    if not isUserAllowed(interaction.user.id): 
        await interaction.send("You are not authorized to use this bot.")
        return
    os.system("shutdown /r /t 1")
    await interaction.send("Restarting..")


# --------------- COMPUTER SOFTWARE CONTROL ------------------

@bot.slash_command(description="Input a URL that will be opened on the host device.", guild_ids=[guild_id])
async def web(interaction: nextcord.Interaction, text: str = nextcord.SlashOption(description="The URL to open on the host device.")):
    if not isUserAllowed(interaction.user.id): 
        await interaction.send("You are not authorized to use this bot.")
        return
    try:
        webbrowser.get(browser_path).open(text)
        await interaction.send(f"Opened {text} in your default browser.")
    except Exception as e:
        await interaction.send(f"Failed to open {text}: {e}")




# -------------- COMPUTER KEYSTROKE CONTROL -----------------


@bot.slash_command(description="Send a keystroke to the device that will be inputted.", guild_ids=[guild_id])
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
    
    }

    key = special_keys.get(text.lower(), text)

    try:
        keyboard.press(key)
        keyboard.release(key)
        await interaction.send(f"Pressed key: {text}")
    except ValueError as e:
        await interaction.send(f"Invalid key: {text}")



@bot.slash_command(description="Simillar to the keystroke command, but types out full sentences.", guild_ids=[guild_id])
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


@bot.slash_command(description="Copy to your device's clipboard, Note: Image will always be copied last.", guild_ids=[guild_id])
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



@bot.slash_command(description="Paste your device's clipboard to Discord", guild_ids=[guild_id])
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




@bot.slash_command(description="Upload a file to your device", guild_ids=[guild_id])
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

if __name__ == "__main__":
    bot.run(discord_token) 

# Developed by Faisal Abusharar.. More features soon :D