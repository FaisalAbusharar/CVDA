from nextcord.ext import commands
import nextcord
import os
import webbrowser
from pynput.keyboard import Key, Controller



# DO NOT CHANGE THE FILE NAME.


# ------------ VARIABLES YOU CHANGE ---------------

browser_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'  # Change this based on your browser path.
discord_token = "" # Add your discord bot token here.
guild_id = 1121367322514849521 # Add your guild ID here, this allows you to only have the commands work in one server & instant updates.

Activity = nextcord.Activity(name="CVDA 0.1.1 Beta", type=nextcord.ActivityType.streaming) # You can change this aswell, it's optional. .playing .listening .watching are avaliable.

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
async def web(interaction: nextcord.Interaction, arg: str = nextcord.SlashOption(description="The URL to open on the host device.")):
    try:
        webbrowser.get(browser_path).open(arg)
        await interaction.send(f"Opened {arg} in your default browser.")
    except Exception as e:
        await interaction.send(f"Failed to open {arg}: {e}")




# -------------- COMPUTER KEYSTROKE CONTROL -----------------


@bot.slash_command(description="Send a keystroke to the device that will be inputted.", guild_ids=[guild_id])
async def keystroke(interaction: nextcord.Interaction, arg: str = nextcord.SlashOption(description="The key to press (e.g. 'enter', 'space', 'a').") ):

    arg = arg.lower()

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

    key = special_keys.get(arg.lower(), arg)

    try:
        keyboard.press(key)
        keyboard.release(key)
        await interaction.send(f"Pressed key: {arg}")
    except ValueError as e:
        await interaction.send(f"Invalid key: {arg}")



@bot.slash_command(description="Simillar to the keystroke command, but types out full sentences.", guild_ids=[guild_id])
async def type(
    interaction: nextcord.Interaction,arg: str = nextcord.SlashOption(description="The full sentence to type on the host device."), 
               sendEnter: str = nextcord.SlashOption(
    name="send_enter",
    choices={"Yes": "yes", "No": "no"},
    required=False,
    default="no",
    description="Press enter after typing the message."
    ),):


    # This is a really specific edge case, but who knows, might be helpful.
    for char in arg:
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
    
    await interaction.send(f"Typed {arg} on your device.")



bot.run(discord_token) 

# Developed by Faisal Abusharar.. More features soon :D