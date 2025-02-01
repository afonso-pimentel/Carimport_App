class Ad:
    def __init__(self, source, url, car):
        self.source = source
        self.url = url
        self.car = car

    def __str__(self):
        return f"Ad from {self.source}: {self.car}"
