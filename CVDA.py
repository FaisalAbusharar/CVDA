from nextcord.ext import commands
import nextcord
import os
import webbrowser

from pynput.keyboard import Key, Controller



# DO NOT CHANGE THE FILE NAME.


# ------------ VARIABLES YOU CHANGE ---------------

browser_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'  # Change this based on your browser path.
discord_token = "" # Add your discord bot token here.

# ------------------------------------------------

keyboard = Controller()


intents = nextcord.Intents.default()
intents.message_content = True

# the prefix is not used in this example
bot = commands.Bot(command_prefix="PC-", intents=intents)

# --------------- COMPUTER HARDWARE CONTROL ------------------

@bot.slash_command(description="Shutdown the computer.")
async def shutdown(interaction: nextcord.Interaction):
    os.system("shutdown /s /t 0")
    await interaction.send("Shutting down..")



@bot.slash_command(description="Restart the computer.")
async def restart(interaction:  nextcord.Interaction):
    os.system("shutdown /r /t 1")
    await interaction.send("Restarting..")


# --------------- COMPUTER SOFTWARE CONTROL ------------------

@bot.slash_command(description="Input a URL that will be opened on the host device.")
async def web(interaction: nextcord.Interaction, arg: str):
    try:
        webbrowser.get(browser_path).open(arg)
        await interaction.send(f"Opened {arg} in your default browser.")
    except Exception as e:
        await interaction.send(f"Failed to open {arg}: {e}")




# -------------- COMPUTER KEYSTROKE CONTROL -----------------


@bot.slash_command(description="Send a keystroke to the computer that will be inputted.")
async def keystroke(interaction: nextcord.Interaction, arg: str):

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



@bot.slash_command(description="Simillar to the keystroke command, but types out full sentences.")
async def type(ctx, arg):
    pass


bot.run(discord_token) 

# Developed by Faisal Abusharar.. More features soon :D