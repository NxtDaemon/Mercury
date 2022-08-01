import json
import os
import socket 
import logging, coloredlogs
# * SMB Dependencies - Impacket 
from impacket import smbserver, version
from impacket.ntlm import compute_lmhash, compute_nthash
from impacket.examples import logger as IMlogger
# * FTP Dependencies - pyftpdlib 
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


#  __    __            __     _______
# |  \  |  \          |  \   |       \
# | ▓▓\ | ▓▓__    __ _| ▓▓_  | ▓▓▓▓▓▓▓\ ______   ______  ______ ____   ______  _______
# | ▓▓▓\| ▓▓  \  /  \   ▓▓ \ | ▓▓  | ▓▓|      \ /      \|      \    \ /      \|       \
# | ▓▓▓▓\ ▓▓\▓▓\/  ▓▓\▓▓▓▓▓▓ | ▓▓  | ▓▓ \▓▓▓▓▓▓\  ▓▓▓▓▓▓\ ▓▓▓▓▓▓\▓▓▓▓\  ▓▓▓▓▓▓\ ▓▓▓▓▓▓▓\
# | ▓▓\▓▓ ▓▓ >▓▓  ▓▓  | ▓▓ __| ▓▓  | ▓▓/      ▓▓ ▓▓    ▓▓ ▓▓ | ▓▓ | ▓▓ ▓▓  | ▓▓ ▓▓  | ▓▓
# | ▓▓ \▓▓▓▓/  ▓▓▓▓\  | ▓▓|  \ ▓▓__/ ▓▓  ▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓ ▓▓ | ▓▓ | ▓▓ ▓▓__/ ▓▓ ▓▓  | ▓▓
# | ▓▓  \▓▓▓  ▓▓ \▓▓\  \▓▓  ▓▓ ▓▓    ▓▓\▓▓    ▓▓\▓▓     \ ▓▓ | ▓▓ | ▓▓\▓▓    ▓▓ ▓▓  | ▓▓
#  \▓▓   \▓▓\▓▓   \▓▓   \▓▓▓▓ \▓▓▓▓▓▓▓  \▓▓▓▓▓▓▓ \▓▓▓▓▓▓▓\▓▓  \▓▓  \▓▓ \▓▓▓▓▓▓ \▓▓   \▓▓


DETAILED = logging.Formatter("%(asctime)-30s %(module)-15s %(levelname)-8s %funcName)-20s %(message)s")
logger = logging.getLogger()
coloredlogs.install(logger=logger,level=logging.DEBUG)

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
        logger.error(f"{Color.ErrorColor}[!] - {Message}{Color.RESET}")

    def Info(Message):
        'Infomation Messages'
        logger.info(f"{Color.InfoColor}[*] - {Message}{Color.RESET}")

    def Success(Message):
        'Success Messages'
        logger.info(f"{Color.SuccessColor}[$] - {Message}{Color.RESET}")

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
        self.Ports = {"HTTP": 80, "SMB": 443, "FTP" : 21, "RAW" : 5555}  # ! Implement Overrides
        self.ActionOverrides()

    def ActionOverrides(self):
        Overrides = self.Config["PortOverrides"]
        for Protocol, Override in Overrides.items():
            if Override:
                self.Ports.update({Protocol : Override})


    def UpdogManagement(self):
        'Spawns an updog server to server HTTP or HTTPS Files allowing for PS, Curl and WGET alongside manual transfer'
        os.system(
            f"python -m updog -d {self.Location} -p {self.Ports.get('HTTP')}")
        var = input("RUNNING UPDOG SERVER > ")

    def ImpacketSMB(self):
        'Spawns an Impacket SMB to directly transfer files via SMB protocol'
        Comment = "PrivEsc Transfer SMB"
        IMlogger.init(True)
        logging.getLogger().setLevel(logging.DEBUG)
        Server = smbserver.SimpleSMBServer(
            listenAddress="0.0.0.0", listenPort=self.Ports.get('SMB'))
        Server.addShare("MERCURY", self.Location, Comment)
        Server.setSMB2Support(True)  # ! Unsure if a setting is needed
        Server.start()

    def PyFTP(self):
        'Spawns a FTP Server and creates user "Mercury" with password "password", additionally allows anonymous mode and spawn you in the set location'
        Authorizer = DummyAuthorizer() 
        Authorizer.add_user("Mercury", "password", self.Location, perm="elradfmw")
        Authorizer.add_anonymous(self.Location) # * Comment out this line if you want it to not use anonymous mode.
        Handler = FTPHandler
        Handler.authorizer = Authorizer
        Server = FTPServer(("0.0.0.0", self.Ports.get('FTP')), Handler)
        Server.serve_forever()

    def RawSocket(self):
        'Used to transfer files directly to host machine via programs like Netcat or programs with socket permissions'
        "Tip : when connecting use the 'tail' command to make life easier e.g. 'nc IP PORT | tail -n +2 | tee FILENAME"
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as S:
            S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # * Fixes the TIME_WAIT state being forced onto sockets
            S.bind(("0.0.0.0",self.Ports.get("RAW")))
            S.listen()
            Notify.Info(f"Socket 0.0.0.0:{self.Ports.get('RAW')} has been opened and is listening")
            

            while True:
                conn, addr = S.accept()
                
                Notify.Info(f"Connection from {addr}")

                with conn:
                    conn.send(b"Connection Opened Awaiting Response from Mercury Client.\n")
                    Files = os.listdir(self.Location)
                    Name = ""

                    while Name not in Files:
                        Notify.Info(f"Files in Folder -> {Files}")
                        Name = Notify.Question("Please Enter the Filename > ")

                    with open(os.path.join(self.Location,Name),"r") as f:
                        Content = f.read()

                    conn.sendall(Content.encode()) 
                    Notify.Info(f"Sending File Contents to {addr}")
                    conn.close() # ! Adjustment needed to ensure content is fully sent before closing 
        
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
    ConfigFile = "" #* Use if you want to directly override the location
    

    # * Get Config File
    
    if not ConfigFile:
        HomeMarker = "HOME" if os.name == "posix" else "UserProfile"
        BASE = os.getenv(HomeMarker)
        Location = ["Code","DeliveryManagement","personal.conf.json"]
        ConfigFile = os.path.join(BASE,*Location)
        
    # Get Values from Config File
    with open(ConfigFile, "r") as f:
        data = json.loads(f.read())
    Paths = data["Paths"]
    Config = data["Config"]

    # Instantiate Deliver
    D = Deliver(Paths, Config)
    D.ManageLocation()
    D.RawSocket()
