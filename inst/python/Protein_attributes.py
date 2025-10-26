class Protein:
    def __init__(self, name):
        self.name = name
        self.interactions = {}

    def add_interaction(self, protein, likelihood):
        self.interactions[protein] = likelihood