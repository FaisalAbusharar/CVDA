from nextcord.ext import commands
import nextcord
import os
import webbrowser

from pynput.keyboard import Key, Controller



# DO NOT CHANGE THE FILE NAME.


# ------------ VARIABLES YOU CHANGE ---------------

browser_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'  # Change this based on your browser path.
discord_token = "" # Add your discord bot token here.
prefix = "PC-" # The prefix in which you type the commands.

# ------------------------------------------------

keyboard = Controller()


intents = nextcord.Intents.default()
intents.message_content = True

# the prefix is not used in this example
bot = commands.Bot(command_prefix=prefix, intents=intents)



@bot.command()
async def shutdown(ctx):
    os.system("shutdown /s /t 0")
    await ctx.send("Shutting down..")


@bot.command()
async def web(ctx, arg):
    try:
        webbrowser.get(browser_path).open(arg)
        await ctx.send(f"Opened {arg} in your default browser.")
    except Exception as e:
        await ctx.send(f"Failed to open {arg}: {e}")


@bot.command()
async def restart(ctx, arg):
    os.system("shutdown /r /t 1")
    await ctx.send("Restarting..")

@bot.command()
async def keystroke(ctx, arg):

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
        await ctx.send(f"Pressed key: {arg}")
    except ValueError as e:
        await ctx.send(f"Invalid key: {arg}")



bot.run(discord_token) # Add your token here

# Developed by Faisal Abusharar.. More features soon :D