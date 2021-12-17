### Hosted on Github at @Toblobs
### A Synergy Studios Project

class Printer:

    """Printing out borders, tables and the like"""

    def __init__(self):
        pass

    def print_border(self, sp):

        if sp == 'single-border':
            print('-' * 30)
            
        elif sp == 'double-border':
            print('_' * 30)
            print('-' * 30)
            print()

        elif sp == 'equals-border':
            print('=' * 30)

    def print_spaces(self, sp):

        if sp == 'double-space':
                print()
                print()
