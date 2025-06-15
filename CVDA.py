from nextcord.ext import commands
import nextcord
import os
import webbrowser
from pynput.keyboard import Key, Controller
import pyperclip
import win32clipboard
from PIL import Image
import io

# DO NOT CHANGE THE FILE NAME.

 
# ------------ VARIABLES YOU CHANGE ---------------

browser_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'  # Change this based on your browser path.
discord_token = "" # Add your discord bot token here.
guild_id = 4221727342164639211 # Add your guild ID here, this allows you to only have the commands work in one server & instant updates.

Activity = nextcord.Activity(name="CVDA 0.1.4 Beta", type=nextcord.ActivityType.streaming) # You can change this aswell, it's optional. .playing .listening .watching are avaliable.

# ------------------------------------------------

keyboard = Controller()


intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="PC-", intents=intents, activity=Activity)



# --------------- COMPUTER HARDWARE CONTROL ------------------

@bot.slash_command(description="Shutdown the device.", guild_ids=[guild_id])
async def shutdown(interaction: nextcord.Interaction):
    os.system("shutdown /s /t 0")
    await interaction.send("Shutting down..")



@bot.slash_command(description="Restart the device.", guild_ids=[guild_id])
async def restart(interaction:  nextcord.Interaction):
    os.system("shutdown /r /t 1")
    await interaction.send("Restarting..")


# --------------- COMPUTER SOFTWARE CONTROL ------------------

@bot.slash_command(description="Input a URL that will be opened on the host device.", guild_ids=[guild_id])
async def web(interaction: nextcord.Interaction, text: str = nextcord.SlashOption(description="The URL to open on the host device.")):
    try:
        webbrowser.get(browser_path).open(text)
        await interaction.send(f"Opened {text} in your default browser.")
    except Exception as e:
        await interaction.send(f"Failed to open {text}: {e}")




# -------------- COMPUTER KEYSTROKE CONTROL -----------------


@bot.slash_command(description="Send a keystroke to the device that will be inputted.", guild_ids=[guild_id])
async def keystroke(interaction: nextcord.Interaction, text: str = nextcord.SlashOption(description="The key to press (e.g. 'enter', 'space', 'a').") ):

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


@bot.slash_command(description="Copy to your device's clipboard", guild_ids=[guild_id])
async def clipboard(
    interaction: nextcord.Interaction, text: str = nextcord.SlashOption(description="Text to copy to the clipboard"),
    pasteAfter: str = nextcord.SlashOption(
        choices={"Yes": "yes", "No": "no"},
        required=False,
        default="no",
        description="Paste the clipboard after copying it",
        name="paste_clipboard",
    ),
):
    
    pyperclip.copy(text)

    if pasteAfter == "yes":
        keyboard.type(pyperclip.paste())

    await interaction.send(f"Successfully copied to your device's clipboard.")


@bot.slash_command(description="Paste your device's clipboard to Discord", guild_ids=[guild_id])
async def paste(interaction: nextcord.Interaction):
    await interaction.response.defer()  # in case it takes a bit of time

    text = pyperclip.paste()
    if text:
        await interaction.send(f"**Clipboard Text:**\n{text}")
    else:
        await interaction.send("No text found in clipboard.")


    try:
        win32clipboard.OpenClipboard()
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
            data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
            win32clipboard.CloseClipboard()

      
            image = Image.open(io.BytesIO(data))


            image_bytes = io.BytesIO()
            image.save(image_bytes, format='PNG')
            image_bytes.seek(0)

            file = nextcord.File(image_bytes, filename="clipboard.png")
            await interaction.send("**Clipboard Image:**", file=file)
        else:
            win32clipboard.CloseClipboard()
    except Exception as e:
        await interaction.send(f"Error while reading image: {e}")




bot.run(discord_token) 

# Developed by Faisal Abusharar.. More features soon :D