import os
import subprocess
import sys

package_name = "pyinstaller"

user_profile_path = os.environ['USERPROFILE']
username = os.path.basename(user_profile_path)


# ------------------ VARIABLES YOU CAN EDIT --------------------

STARTUP = True # Automatically move into startup folder after compiling


# ------------- EDIT IF YOU KNOW WHAT YOU ARE DOING ---------------

src = os.path.abspath(".\\dist\\CVDA.exe")
dst = f"C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"



def tryInstallPackages(packages):
    commands = [
        [sys.executable, "-m", "pip", "install"],
        ["pip", "install"],
        ["pip3", "install"],
    ]

    for package in packages:
        installed = False
        for base_cmd in commands:
            cmd = base_cmd + [package]
            try:
                print(f"Trying to install {package} using: {' '.join(cmd)}")
                result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode == 0:
                    print(f"{package} installed successfully.")
                    installed = True
                    break
            except Exception as e:
                print(f"Failed to install {package} with error: {e}")
        if not installed:
            print(f"All installation methods failed for {package}. Please install it manually.")
            return False
    return True


def compile():
    try: 
        os.system("pyinstaller --onefile --noconsole CVDA.py")
    except Exception as e:
        print("Pyinstaller failed to compile, check if the script is avaliable in the same directory.")
        print(e)
        return False

    if STARTUP == True:
   
        try:
            os.system("taskkill /f /im  CVDA.exe")
            subprocess.run(f'move /Y "{src}" "{dst}"', shell=True)
            os.startfile(f"C:/Users/{username}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/CVDA.exe")
        except:
            print("Failed to move program to startup folder, may need to be done manually. Or dst variable may need to be edited.")
            print("\n \n Move failed, starting application anyway.")
            os.startfile(f"./dst/CVDA.exe")
    
    else:
        os.startfile(f"./dst/CVDA.exe")


    return True


def findPackagesInstalled():
    packages_to_install = ["pyinstaller", "nextcord", "pyperclip", "pynput", "pillow", "pywin32"]
    try:
        import PyInstaller
        packages_to_install.remove("pyinstaller")
    except:
        print('Pyinstaller not installed, requesting install.')

    try:
        import nextcord
        packages_to_install.remove("nextcord")
    except:
        print('Nextcord not installed, requesting install.')

    try:
        import pyperclip
        packages_to_install.remove("pyperclip")
    except:
        print('Pyperclip not installed, requesting install.')

    try:
        import pynput
        packages_to_install.remove("pynput")
    except:
        print('Pynput not installed, requesting install.')

    try:
        import PIL
        packages_to_install.remove("pillow")
    except:
        print('Pillow not installed, requesting install.')

    try:
        import win32clipboard
        packages_to_install.remove("pywin32")
    except:
        print('Pywin32 not installed, requesting install.')

    if not packages_to_install:
        print("All packages installed, proceeding with download")
        return True
    else:
        print(f"Dependencies missing, installing {packages_to_install}")
        result = tryInstallPackages(packages=packages_to_install)
        if result == True:
            return True
        else:
            return False

    

packageReuslt = findPackagesInstalled()
if packageReuslt == False:
    print("\n \n \n An error has occurred in the compiler.")
    quit()


compileResult = compile()
if compileResult == True:
    print(" \n \n \n Completed Compiler... Application has started, check to see if your discord bot is currently online.")
else:
    print("\n \n \n An error has occurred in the compiler.")

