### Hosted on Github at @Toblobs
### A Synergy Studios Project

version = '1.0.3'

from netlib import Client, Signal
from netlib.net.server.connection import Connection
from uuid import uuid4


class KahootClient:
    """The client, which accepts questions and
       answers them by sending back socket data."""


    def __init__(self):

        self.ip = "10.130.65.253"
        self.port = 4747

        self.loc = 'EU-1'

        self._client = Client(self.ip, self.port)

        self.uuid4 = uuid4()

    def setup_client(self, c: Client):

        @self._client.OnConnect
        def handle_connnection():

             print(f"[+] Connected to server {self.loc} at {self.ip}:{self.port}")
             self.send(Signal({"uuid": self.uuid4}, "/uuid/set"))

             print(f"[+] Sent server {self.loc} UUID: <{self.uuid4}>")
    
             @self._client.OnSignal("/message")
             def display_message(signal: Signal):
                
                content = signal.payload.content
                print(content)

    def connect(self):
        
        self.setup_client(self._client)
        self._client.connect()

    def send(self, data):
        
        self._client.send(data)




#-------------------------------------------------------------------#

kClient = KahootClient()

kClient.connect()



