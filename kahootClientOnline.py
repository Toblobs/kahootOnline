### Hosted on Github at @Toblobs
### A Synergy Studios Project


from netlib import Server, Client, Signal
from netlib.net.server.connection import Connection

c = Client()

@c.OnSignal("answer_status")

def answer_status(signal):
    print(f"isCorrect: {signal.payload.correct}")
