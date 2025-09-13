# Define World Objects
class WorldObject:
    def __init__(self, ign):
        self.ign = ign
        self.attributes = {}
    def set_attribute(self, key, value):
        self.attributes[key] = value
    def get_attribute(self, key):

        return self.attributes[key]
