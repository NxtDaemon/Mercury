import json
import os 

# Written By NxtDaemon Any Issues or Additions you would like please contact me here https://nxtdaemon.xyz/contact
#  __    __            __     _______
# |  \  |  \          |  \   |       \
# | ▓▓\ | ▓▓__    __ _| ▓▓_  | ▓▓▓▓▓▓▓\ ______   ______  ______ ____   ______  _______
# | ▓▓▓\| ▓▓  \  /  \   ▓▓ \ | ▓▓  | ▓▓|      \ /      \|      \    \ /      \|       \
# | ▓▓▓▓\ ▓▓\▓▓\/  ▓▓\▓▓▓▓▓▓ | ▓▓  | ▓▓ \▓▓▓▓▓▓\  ▓▓▓▓▓▓\ ▓▓▓▓▓▓\▓▓▓▓\  ▓▓▓▓▓▓\ ▓▓▓▓▓▓▓\
# | ▓▓\▓▓ ▓▓ >▓▓  ▓▓  | ▓▓ __| ▓▓  | ▓▓/      ▓▓ ▓▓    ▓▓ ▓▓ | ▓▓ | ▓▓ ▓▓  | ▓▓ ▓▓  | ▓▓
# | ▓▓ \▓▓▓▓/  ▓▓▓▓\  | ▓▓|  \ ▓▓__/ ▓▓  ▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓ ▓▓ | ▓▓ | ▓▓ ▓▓__/ ▓▓ ▓▓  | ▓▓
# | ▓▓  \▓▓▓  ▓▓ \▓▓\  \▓▓  ▓▓ ▓▓    ▓▓\▓▓    ▓▓\▓▓     \ ▓▓ | ▓▓ | ▓▓\▓▓    ▓▓ ▓▓  | ▓▓
#  \▓▓   \▓▓\▓▓   \▓▓   \▓▓▓▓ \▓▓▓▓▓▓▓  \▓▓▓▓▓▓▓ \▓▓▓▓▓▓▓\▓▓  \▓▓  \▓▓ \▓▓▓▓▓▓ \▓▓   \▓▓


class Color:
    'Class for Colors to be used in Execution'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

    QuestionColor = BOLD+YELLOW
    ErrorColor = RED+BOLD
    InfoColor = CYAN
    SuccessColor = GREEN
    NumColor = BLUE+BOLD

class Notify():
    'Managed what type of message is sent'

    def Error(Message):
        'Error Messages'
        print(f"{Color.ErrorColor}[!] - {Message}{Color.RESET}")

    def Info(Message):
        'Infomation Messages'
        print(f"{Color.InfoColor}[*] - {Message}{Color.RESET}")

    def Success(Message):
        'Success Messages'
        print(f"{Color.SuccessColor}[$] - {Message}{Color.RESET}")

    def Question(Message):
        'Get infomation from user'
        return(input(f"{Color.QuestionColor}[?] - {Message}{Color.RESET}"))


def OutputOpts(Message):
    'Outputs all options'
    print(f"{Color.NumColor}{Message}{Color.RESET}")


# JSON Handling for manaaging paths
with open("conf.json", "r") as f:
    data = f.read()

# Loading JSON Data into variables
data = json.loads(data)
Paths = data["Paths"]
Config = data["Default Configuration"]

# Print out all options and their keys 
Notify.Info("Enter '!' followed by the path for a custom location")
for _ in enumerate(Paths):
    c = _[0]
    _ = _[1]
    OutputOpts(f"[{c}] : {_} -> {Paths[_]}")
    

# Get the location of the Directory to serve up
try:
    Response = Notify.Question("Enter the name of the location you wish to serve up > ")
    if Response.startswith("!"):
        Location = Notify.Question("Enter Custom Path > ")
    else:
        Location = Paths[Response]
    
except Exception as Err:
    Notify.Error(f"Error : {Err} was found")

# Serve files with updog
os.system(f"updog -d {Location} -p 80")
