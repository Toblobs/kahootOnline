### Hosted on Github at @Toblobs
### A Synergy Studios Project

version = '1.0.6'

from netlib import Server, Signal
from netlib.net.server.connection import Connection
from uuid import uuid4

from kModules.kQuestions import *


class GameRunner:
    """Runs a Kahoot Game."""

    def __init__(self):
        pass

class KahootServer:
    """The server, which creates Question objects and
       broadcasts info to clients. Uses #signal."""

    def __init__(self):

        self.ip = Server.get_host_machine()
        self.port = 4747
        
        self._server = Server(self.ip, self.port)

        self.client_uuid = None

    def setup_server(self, s: Server):

        self.client_uuid = {}

        @self._server.OnConnection
        def handle_conn(conn: Connection):

            print(f"[+] Client {conn} connected to the server")
            print(f"[*] Connections: {self.connections()}")
            
            @conn.OnSignal("/message")
            def handle_message(signal: Signal):
                print(f"[>] Client {conn} sent message: {signal.payload.content}")
            
            @conn.OnSignal("/uuid/set")
            def set_uuid(signal: Signal):

                self.client_uuid[conn] = signal.payload.uuid
                print(f"[+] Client {conn} set as conn-UUID: {signal.payload.uuid}")
                
        @self._server.OnDisconnection
        print(f"[!] Client disconnected from server")
        print(f"[*] Connections: {self.connections()}")
                  
    def run(self):

        print(f"[*] Started as {self.ip}:{self.port}")

        self.setup_server(self._server)
        self._server.run()

#-------------------------------------------------------------------#
        
kServer = KahootServer()

kServer.run()
