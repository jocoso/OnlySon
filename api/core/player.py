class Player:
    def __init__(self, obj_id, obj_name, io, init_items=None):
        from api.actionables import Storageable, Examinable
        from api.core.game_object import GameObject
        from api.core.IO import IO

        if init_items is None:
            init_items = []
        self.io = io
        examinable = Examinable("A Test Player", self.io)
        self.core = GameObject(obj_id, obj_name, actionables={"examine": examinable})
        self.storage = Storageable(init_items)

    def examine(self):
        self.core.execute_actionable("examine")

    def get_inventory(self):
        return self.storage.get_inventory()

    def set_inventory(self, new_inventory):
        self.storage.set_inventory(new_inventory)

    def __str__(self):
        return f"Player({self.core.get_id()})"
