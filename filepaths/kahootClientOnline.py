### Hosted on Github at @Toblobs
### A Synergy Studios Project


from netlib import Server, Client, Signal
from netlib.net.server.connection import Connection


class MetaClient:
    """Original Signal Client"""

    def setup_client(c: Client):
	@c.OnSignal("/message")
	def display_message(signal: Signal):
		content = signal.payload.content

		print(content)

    def send_message(c: Client, content: str):
            c.send(Signal({
                    "content": content
            }, "/message"))

            wait(1)


#m = MetaClient()
#m.setup_client(c1)


#m.c1.connect()
