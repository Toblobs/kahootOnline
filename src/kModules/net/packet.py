### Hosted on Github at @Toblobs
### A Synergy Studios Project

from datetime import datetime

class Packet:

    """A representation of a packet which stores data
       for a singular message sent."""

    def __init__(self, comm, det):

        self.comm = comm
        self.det = det

        self.time_created = datetime.now().strftime('%d %m %y - %H:%M:%S')

    def __str__(self):

        return f'Packet <comm, det, time> {self.comm}, {self.det}, {self.time_created}'

    def unwrap(self, sep):

        """Returns a string representation of the packet."""

        return f'{self.comm}{sep}{self.det}{sep}{self.time_created}'

