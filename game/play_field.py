from .cards import archivement, event

class Field:
    def __init__(self):
        self.archivement = [archivement.Poor(),
                            archivement.Hunger(),
                            archivement.Welfare(),
                            archivement.Education(),
                            archivement.Gender(),
                            archivement.Water(),
                            archivement.Energy(),
                            archivement.Economy(),
                            archivement.Industry(),
                            archivement.Equalty()]
        self.event = [event.Debt()]
