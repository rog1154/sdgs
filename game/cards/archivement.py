class Archivement:
    def __init__(self,name,phase,cost):
        self.name = name
        self.phase = phase
        self.cost = cost
        self.target = None

class Exchange(Archivement):
    def __init__(self,name,phase,cost):
        super().__init__(name,phase,cost)

    def play(self,player,type,plus):
        if player.resource[type] >= 2:
            player.resource[type] -= 2
            player.resource_plus(plus)

class Poor(Archivement):
    def __init__(self):
        super().__init__('貧困', 'start','健康')

    def play(self,player):
        player.draw()

class Hunger(Archivement):
    def __init__(self):
        super().__init__('飢餓', 'start', '健康')

    def play(self,player):
        player.resource_plus('健康')

class Welfare(Exchange):
    def __init__(self):
        super().__init__('福祉', 'buy', '健康')

    def play(self,player,type):
        super().play(player,type,'健康')

class Education(Archivement):
    def __init__(self):
        super().__init__('教育', 'start', '文化')

    def play(self,player):
        player.resource_plus('文化')

class Gender(Exchange):
    def __init__(self):
        super().__init__('ジェンダー', 'buy', '文化')

    def play(self,player,type):
        super().play(player,type,'文化')

class Water(Exchange):
    def __init__(self):
        super().__init__('水', 'buy', '自然')

    def play(self,player,type):
        super().play(player,type,'自然')

class Energy(Archivement):
    def __init__(self):
        super().__init__('エネルギー', 'start', '技術')

    def play(self,player):
        player.resource_plus('技術')

class Economy(Exchange):
    def __init__(self):
        super().__init__('経済', 'buy', '技術')

    def play(self,player,type):
        super().play(player,type,'技術')

class Industry(Archivement):
    def __init__(self):
        super().__init__('産業', 'start', '技術')

    def play(self,player):
        player.resource_plus('技術')

class Equalty(Archivement):
    def __init__(self):
        super().__init__('平等', 'start', '文化')

    def play(self,player):
        player.resource_plus('文化')

