import json
import os
import logging
from impacket import smbserver, version
from impacket.ntlm import compute_lmhash, compute_nthash
from impacket.examples import logger as IMlogger

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


class Deliver():
    'Different Methods of Transfering Files'

    def __init__(self, Paths, Config):
        self.Paths = Paths
        self.Config = Config
        self.Location = False
        self.Ports = {"HTTP": 80, "SMB": 443}  # ! Implement Overides

    def UpdogManagement(self):
        'Uses Updog to server files allowing for PS, Curl and WGET alongside manual transfer'
        os.system(
            f"python -m updog -d {self.Location} -p {self.Ports.get('HTTP')}")
        var = input("RUNNING UPDOG SERVER > ")

    def ImpacketSMB(self):
        'Allows for SMB to directly transfer'
        Comment = "PrivEsc Transfer SMB"
        IMlogger.init(True)
        logging.getLogger().setLevel(logging.DEBUG)
        Server = smbserver.SimpleSMBServer(
            listenAddress="0.0.0.0", listenPort=self.Ports.get('SMB'))
        Server.addShare("MERCURY", self.Location, Comment)
        Server.setSMB2Support(True)  # ! Unsure if a setting is needed
        Server.start()

    def ManageLocation(self):
        IndexHelperArr = {}
        Notify.Info("Enter '!' followed by the path for a custom location")
        for _ in enumerate(Paths):
            c = _[0]
            Name = _[1]
            OutputOpts(f"[{c}] : {Name} -> {Paths[Name]}")
            IndexHelperArr.update({c: Name})

        # Get the location of the Directory to serve up
        try:
            Response = Notify.Question(
                "Enter the name of the location you wish to serve up > ")
            if Response.startswith("!"):
                self.Location = Response[1:].rstrip()
                Notify.Info(f"Path Found as : {self.Location}")
            else:
                self.Location = Paths[IndexHelperArr[int(Response)]]
        except Exception as Exc:
            Notify.Error(f"Encounter Error : `{Exc}`")


if __name__ == "__main__":
    # Get Config File
    # ! Alternatively use environment variables with the following syntax `os.getenv("ENV_VAR_NAME") `
    # os.getenv("HOME") + "/DeliveryManagement/conf.json"
    ConfigFile = "C:\\Users\\Owner\\DeliveryManagement\\personal.conf.json"

    # Get Values from Config File
    with open(ConfigFile, "r") as f:
        data = json.loads(f.read())
    Paths = data["Paths"]
    Config = data["Default Configuration"]

    # Instantiate Deliver
    D = Deliver(Paths, Config)
    D.ManageLocation()
    D.UpdogManagement()
