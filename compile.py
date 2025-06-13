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



def tryInstallPyinstaller():
    commands = [
            [sys.executable, "-m", "pip", "install", "pyinstaller"],
            ["pip", "install", "pyinstaller"],
            ["pip3", "install", "pyinstaller"],
        ]

    for cmd in commands:
        try:
            print(f"Trying to install using: {' '.join(cmd)}")
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                print("PyInstaller installed successfully.")
                return True
        except Exception as e:
                print(f"Failed with error: {e}")

    print("All installation methods failed. Please install PyInstaller manually.")
    return False

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


    return True


try:
    import PyInstaller
    print("Pyinstaller is installed... compiling")
    
except:
    print("Pyinstaller is not installed, downloading..")
    installerResult = tryInstallPyinstaller()
    if installerResult == False:
        print("\n \n \n Program failed to install pyinstaller.. Ending.")




compileResult = compile()
if compileResult == True:
    print(" \n \n \n Completed Compiler... Application has started, check to see if your discord bot is currently online.")
else:
    print("\n \n \n An error has occurred in the compiler.")

