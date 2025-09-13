# Helper Functions

def format_list(items):
    """
    Formats a list of objects as a cohesive, comma-separated string.
    Example: ['apple', 'banana', 'cherry'] -> 'apple, banana, cherry'
    """
    return ", ".join(str(item) for item in items)


def get_choice(range_min, range_max, error_msg="You can't pick this option.", caret="> "):
    """
    Prompts user for input within a specified range and returns the selected option as an integer.
    """
    while True:
        try:
            choice = int(input(caret))
            if range_min <= choice <= range_max:
                return choice
            print(error_msg)
        except ValueError:
            print("Please enter a valid number.")


# Simple replacements for missing stringformatter and clicksimulator

def stringformatter(options):
    """
    Displays numbered option list to the player.
    """
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")


def clicksimulator(min_choice, max_choice, error_msg="Invalid choice."):
    """
    Simulated input choice with validation.
    """
    return get_choice(min_choice, max_choice, error_msg)


# Actionables

class Openable:
    """
    Adds the ability for an object to 'open' and allows items to be retrieved.
    """
    def __init__(self, takeable_items):
        self.takeable_items = takeable_items

    def exec(self, player, obj_name):
        print(f"Inside {obj_name}, you can see:")
        if self.takeable_items:
            stringformatter(self.takeable_items)
            print("What would you like to take?")
            pick = get_choice(1, len(self.takeable_items), "You can't take that.")
            if 1 <= pick <= len(self.takeable_items):
                item_taken = self.takeable_items.pop(pick - 1)
                # Use id or str representation for display
                item_name = getattr(item_taken.core, 'id', str(item_taken))
                print(f"You took {item_name}")
                inventory = player.get_inventory()
                inventory.append(item_taken)
                player.set_inventory(inventory)
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

    def exec(self):
        print(self.message)


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


class GameObject:
    """
    Basic GameObject which can execute named actionable (Openable, Examinable, etc.)
    """
    def __init__(self, obj_id, actionables=None):
        self.id = obj_id
        self.actionables = actionables or {}

    def get_id(self):
        return self.id

    def execute_actionable(self, name, *params):
        actionable = self.actionables.get(name)
        if actionable and callable(getattr(actionable, "exec", None)):
            return actionable.exec(*params)


class Storageable:
    def __init__(self, inventory=None):
        if inventory is None:
            inventory = []
        self.inventory = inventory

    def get_inventory(self):
        return self.inventory

    def set_inventory(self, new_inventory):
        self.inventory = new_inventory


class Player:
    def __init__(self, obj_id, init_items=None):
        if init_items is None:
            init_items = []
        examinable = Examinable("A Test Player")
        self.core = GameObject(obj_id, actionables={"examine": examinable})

        self.storage = Storageable(init_items)

    def examine(self):
        self.core.execute_actionable("examine")

    def get_inventory(self):
        return self.storage.get_inventory()

    def set_inventory(self, new_inventory):
        self.storage.set_inventory(new_inventory)

    def __str__(self):
        return f"Player({self.core.get_id()})"


class Note:
    def __init__(self):
        examine = Examinable("The note is so old you fear looking at it will make it turn to dust.")
        self.core = GameObject("A Weary Note", actionables={"examine": examine})

    def examine(self):
        self.core.execute_actionable("examine")

    def __str__(self):
        return "A Weary Note"


class Bed:
    def __init__(self):
        examine = Examinable("The bed is so cozy you could fall asleep by thinking of it.")
        self.core = GameObject("A Bed", actionables={"examine": examine})

    def examine(self):
        self.core.execute_actionable("examine")

    def __str__(self):
        return "A Bed"


class Door:
    def __init__(self, id, message):
        examine = Examinable(message)
        self.core = GameObject(id, actionables={"examine": examine})

    def examine(self):
        self.core.execute_actionable("examine")

    def __str__(self):
        return self.core.get_id()

class Desk:
    def __init__(self):
        examinable = Examinable("A Desk")  # Assign to variable
        openable = Openable([Note(), Bed()])
        self.core = GameObject("Desk", actionables={"examine": examinable, "open": openable})

    def get_id(self):
        return self.core.get_id()

    def examine(self):
        self.core.execute_actionable("examine")

    def open(self, player):
        self.core.execute_actionable("open", player, self.get_id())


class Bedroom:
    def __init__(self, player=None):
        self.signaler = Signaler()

        # Clean up the description (single instance, not repeated)
        description = (
            "It is night when you wake up, surrounded by sweaty cotton sheets.\n"
            "The moonlight softly caresses the air that touches only the skin of your legs, "
            "leaving the rest drowning in darkness."
        )
        examinable = Examinable(description)
        self.core = GameObject("Bedroom", actionables={"examine": examinable})
        self.player = player  # Save player reference here for usage in run()

        # Storage can contain furniture objects like Desk, Bed
        self.storage = Storageable([Desk(), Bed()]) # Assuming a Bed class exists

    def examine(self):
        self.core.execute_actionable("examine")

    def open_desk(self, player):
        # Find Desk in storage and open it
        for obj in self.storage.get_inventory():
            if isinstance(obj, Desk):
                obj.open(player)

    def examine_desk(self):
        for obj in self.storage.get_inventory():
            if isinstance(obj, Desk):
                obj.examine()

    def examine_bed(self):
        for obj in self.storage.get_inventory():
            if isinstance(obj, Bed):
                obj.examine()

    def run(self, player=None):
        if not player:
            print("ERROR: Scene", getattr(self.core, "id", "Unknown"), "requires a player instance.")
            return

        self.examine()
        print("What do you do?")
        stringformatter(["Leave the bed"])
        user_response = clicksimulator(1, 1, "")

        while True:
            print("You left your bed. As you do, you consider what you could do next.")
            print("Your eyes have adapted to the darkness and you can see sections"
                  " of your room you couldn't see before. Including a desk lying in the corner and a door. The walls are bare.")
            print("What do you do next?")
            stringformatter(["Examine the Desk", "Examine the Bed", "Examine Room", "Leave the Room"])
            user_response = clicksimulator(1, 4, "")

            if user_response == 1:
                while True:
                    print("You approach the Desk.")
                    print("What do you want to do?")
                    stringformatter(["Open", "Examine", "Leave"])
                    desk_action = clicksimulator(1, 3, "Not an option.")

                    if desk_action == 1:
                        self.open_desk(player)
                    elif desk_action == 2:
                        self.examine_desk()
                    elif desk_action == 3:
                        break

            elif user_response == 2:
                print("You approach the Bed.")
                self.examine_bed()

            elif user_response == 3:
                print("You examine the Room.")
                self.examine()

            elif user_response == 4:
                break

        self.signaler.set_signaler(True)



class MainMenu:
    def __init__(self):
        self.signaler = Signaler(False)

    def run(self, player=None):
        global user, running
        while True:
            print("== Main Menu ==")
            stringformatter(["New user", "Login", "Quit"])
            choice = input("> ")
            if choice == "1":
                user = self.create_player()
                if user:
                    self.signaler.next = True
                    return
            elif choice == "2":
                user = self.login()
                if user:
                    self.signaler.next = True
                    return
            elif choice == "3":
                running = False
                return
            else:
                print("Invalid selection. Try again.")

    def create_player(self):
        print("Create a new player")
        while True:
            player_id = input("Enter your player name: ").strip()
            if player_id:
                new_player = Player(player_id, init_items=[])
                print(f"Player '{player_id}' created successfully.")
                return new_player
            else:
                print("Player name cannot be empty. Please enter a valid name.")

    def login(self):
        print("Login")
        while True:
            player_id = input("Enter your player name: ").strip()
            if player_id:
                existing_player = Player(player_id, init_items=[])
                print(f"Welcome back, {player_id}.")
                return existing_player
            else:
                print("Player name cannot be empty. Please enter a valid name.")


# Global variables and game loop setup
player_placement = 0
user = None
running = True
places = [MainMenu(), Bedroom()]

while running:
    current_scene = places[player_placement]
    current_scene.run(user)
    if current_scene.signaler.next:
        player_placement += 1
        if player_placement >= len(places):
            running = False
