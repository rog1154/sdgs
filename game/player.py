from operator import truediv
from flask_socketio import emit
from .cards.card import ResourceCard
class Player:
    def __init__(self,player):
        self.resource = {'自然':0,'技術':0,'文化':0,'健康':0,'資金':0}
        self.hand = []
        self.archivement = []
        self.deck = [ResourceCard('自然'),ResourceCard('技術'),ResourceCard('文化'),ResourceCard('健康'),ResourceCard('資金')]
        self.trash = []
        self.player = player
        
    def resource_plus(self,type):
        self.resource[type] += 1

    def draw(self):
        if len(self.deck) == 0:
            for card in self.trash:
                self.deck.append(card)
            self.trash = []
        self.hand.append(self.deck.pop(0))

    def play_resource(self):
        for card in self.hand:
            self.resource_plus(card.name)
            self.trash.append(card)
        self.hand = []

    def start_turn(self):
        for goal in self.archivement:
            if goal.phase == 'start':
                emit('chat',goal.name+'の効果',broadcast = True)
                goal.play(self)

    def end_turn(self,resource):
        self.deck.append(ResourceCard(resource))
        hand_max = 5
        for i in self.archivement:
            if i.target == self.player:
                hand_max += 1
        while len(self.hand) < hand_max:
            self.draw()
    
    def buy(self,field,num,cost):
        goal = field.archivement.pop(num)
        self.archivement.append(goal)
        self.resource[goal.cost] -= cost
    
