class Gene:
    def __init__(self, route, distance):
        self.route = route
        self.distance = distance

    def get_distance(self):
        return self.distance

    def get_route(self):
        return self.route
