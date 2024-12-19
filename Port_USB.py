import os
import ctypes
import sys
from colorama import Fore, Style, init
import winreg

# Initialize colorama
init(autoreset=True)

# Function to check if the script is run as administrator
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Function to get the current USB port state from the registry
def get_usb_ports_state():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\USBSTOR", 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(key, "Start")
        winreg.CloseKey(key)
        if value == 3:
            return "enabled"
        elif value == 4:
            return "disabled"
        else:
            return "unknown"
    except Exception as e:
        return "unknown"

# Function to set the USB port state (enable or disable)
def set_usb_ports_state(state):
    if state == "disable":
        # Disable USB ports
        os.system('reg add "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\USBSTOR" /v Start /t REG_DWORD /d 4 /f')
        print(Fore.RED + "\n✘ USB ports disabled.\n")
    elif state == "enable":
        # Enable USB ports
        os.system('reg add "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\USBSTOR" /v Start /t REG_DWORD /d 3 /f')
        print(Fore.GREEN + "\n✔ USB ports enabled.\n")

def main():
    print(Fore.CYAN + """
    #############################################
    #                                           #
    #         USB Port Management Tool          #
    #                                           #
    #############################################
    """)

    # Display current status of USB ports
    current_status = get_usb_ports_state()
    print(Fore.MAGENTA + f"USB port status: {Fore.CYAN}{current_status}")

    while True:
        print(Fore.YELLOW + """
        1. Open (Enable) USB ports
        2. Close (Disable) USB ports
        3. Exit
        """)
        action = input(Fore.CYAN + "Enter your choice: ").lower()

        if action == "2" or action == "close":
            set_usb_ports_state("disable")
        elif action == "1" or action == "open":
            set_usb_ports_state("enable")
        elif action == "3" or action == "exit":
            print(Fore.BLUE + "Exiting the program. Have a great day!\n")
            break
        else:
            print(Fore.RED + "\nInvalid option. Please try again.\n")
            

if __name__ == "__main__":
    # Check if the script is running as an administrator
    if is_admin():
        main()
    else:
        print(Fore.RED + "This script needs to be run as an administrator.")
        # Re-run the script with administrator privileges
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
