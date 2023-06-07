class Gene:
    def __init__(self, route, distance):
        self.route = route
        self.distance = distance

    def __gt__(self, other):
        return self.distance > other.distance

    def __lt__(self, other):
        return self.distance < other.distance