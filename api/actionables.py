from api.core.IO import IO


# Actionables
class Storageable:
    def __init__(self, inventory=None):
        if inventory is None:
            inventory = []
        self.inventory = inventory

    def get_inventory(self):
        return self.inventory

    def set_inventory(self, new_inventory):
        self.inventory = new_inventory


class Openable:
    """
    Adds the ability for an object to 'open' and allows items to be retrieved.
    """

    def __init__(self, takeable_items):
        self.storageable = Storageable(takeable_items)

    def exec(self, player, obj_name):
        from api.helpers import stringformatter, get_choice

        print(f"Inside {obj_name}, you can see:")

        inventory = self.storageable.get_inventory()

        if inventory:
            stringformatter(inventory)
            print("What would you like to take?")
            pick = get_choice(1, len(inventory), "You can't take that.")
            if 1 <= pick <= len(inventory):
                item_taken = inventory.pop(pick - 1)
                # Use id or str representation for display
                item_name = getattr(item_taken.core, "id", str(item_taken))
                print(f"You took {item_name}")
                player_inventory = player.get_inventory()
                player_inventory.append(item_taken)
                player.set_inventory(player_inventory)
                self.storageable.set_inventory(inventory)
                return item_taken
        else:
            print("There is nothing inside.")
        return None


class Examinable:
    """
    Adds the ability for an object to be examined and display a descriptive message.
    """

    def __init__(self, message):
        self.message = message

    def set_message(self, new_message):
        self.message = new_message

    def exec(self):
        return self.message


class Signaler:
    """
    A class to represent a boolean signal.
    """

    def __init__(self, sign=False):
        self.sign = sign

    def set_signaler(self, sign):
        self.sign = sign

    def get_signal(self):
        return self.sign

    # Provide property next to match usage
    @property
    def next(self):
        return self.sign

    @next.setter
    def next(self, value):
        self.sign = value
