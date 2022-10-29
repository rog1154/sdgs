class Event:
    def __init__(self,name):
        self.name = name

class Debt(Event):
    def __init__(self):
        super().__init__('国債発効')
    
    def play(self,player):
        for i in range(3):
            player.draw()