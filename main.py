# Helper Functions


def format_list(items):
    """
    Formats a list of objects as a cohesive, comma-separated string.
    Example: ['apple', 'banana', 'cherry'] -> 'apple, banana, cherry'
    """
    return ", ".join(str(item) for item in items)


def get_choice(
    range_min, range_max, error_msg="You can't pick this option.", caret="> "
):
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
                item_name = getattr(item_taken.core, "id", str(item_taken))
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

    def set_message(self, new_message):
        self.message = new_message

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
    Basic game object capable of executing named actionables such as Openable and Examinable.

    Attributes:
        id (str): Unique identifier for the game object.
        actionables (dict): Dictionary mapping action names to actionable objects.

    Methods:
        get_id(): Returns the unique ID of the game object.
        execute_actionable(name, *params): Executes the specified actionable if available.
        has_actionable(name): Checks if the given actionable is available.
    """

    def __init__(self, obj_id, actionables=None):
        self.id = obj_id
        self.actionables = actionables or {}

    def get_id(self):
        """Return the unique ID of the game object."""
        return self.id

    def execute_actionable(self, name, *params):
        """
        Execute the named actionable if it exists and has an exec method.

        Args:
            name (str): Name of the actionable to execute.
            *params: Parameters to pass to the actionable's exec method.

        Returns:
            Any: The return value of the actionable's exec method, if called.
        """
        actionable = self.actionables.get(name)
        if actionable and callable(getattr(actionable, "exec", None)):
            return actionable.exec(*params)

    def get_actionable(self, name):
        """
        Retrieve an actionable object by its name.
        Args:
            name (str): The name of the actionable.

        Returns:
            The actionable object if found, else None.
        """
        return self.actionables.get(name)

    def has_actionable(self, name):
        """
        Check if the game object has the specified actionable.

        Args:
            name (str): Name of the actionable.

        Returns:
            bool: True if the actionable exists, False otherwise.
        """
        return name in self.actionables


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
        examine = Examinable(
            "The note is so old you fear looking at it will make it turn to dust."
        )
        self.core = GameObject("A Weary Note", actionables={"examine": examine})

    def examine(self):
        self.core.execute_actionable("examine")

    def __str__(self):
        return "A Weary Note"


class Statue:
    def __init__(self):
        examine = Examinable("The ivory statues loom over you with impassive faces.")
        self.core = GameObject("A Statue", actionables={"examine": examine})

    def get_id(self):
        return self.core.get_id()

    def examine(self):
        self.core.execute_actionable("examine")

    def __str__(self):
        return "A Bed"


def optionBox(gameObject, *params):
    actions = {}
    string_actions = []
    open_box = True

    if gameObject.core.has_actionable("examine"):
        string_actions.append(f"EXAMINE {gameObject.get_id()}")
        actions[len(actions)] = {
            "method": lambda: gameObject.core.execute_actionable("examine")
        }
    if gameObject.core.has_actionable("open"):
        string_actions.append(f"OPEN {gameObject.core.get_id()}")
        actions[len(actions)] = {
            "method": lambda: gameObject.core.execute_actionable("open", params),
        }
    string_actions.append("CLOSE OPTION BOX")

    def close_box():
        nonlocal open_box
        open_box = False

    actions[len(actions)] = {"method": close_box}

    while open_box:
        stringformatter(string_actions)
        user_choice = clicksimulator(1, len(string_actions))
        actions[user_choice - 1]["method"]()


class Courtyard:
    def __init__(self, player=None):
        self.signaler = Signaler(False)

        # Clean up the description (single instance, not repeated)
        description = """\nIt is night when you arrive at La Antigua Manor.\n
The estate looms large in the darkness—a bloated mansion adorned with cheap replicas of Greek statues,desperate in their attempt to mimic a culture once held as superior. But there is no grandeur here—only sad theater, reaching for weakness as though it were strength; the abandonment of something richer in favor of illusions that cling to the air like mildew.

The manor has clearly seen better days. Nature has begun its slow reclamation: vines crawl over the stucco like veins on a dying man; animals nest in its bones, as if they sensed the rot long before any human dared to admit it.

Shattered windows and crooked doors gape like open sores. The air is thick with the scent of damp wood, rust, and something older—something sweet and spoiled. This is no home—only the carcass of a titan, long dead, now left to decompose beneath the crushing weight of its own pretense.\n"""

        examinable = Examinable(description)
        self.core = GameObject("Courtyard", actionables={"examine": examinable})
        self.player = player  # Save player reference here for usage in run()
        self.has_introduced = False

        # Storage can contain furniture objects like Desk, Bed
        self.storage = Storageable([Statue()])  # Assuming a Bed class exists

    def examine(self):
        self.core.execute_actionable("examine")

    def run(self, player=None):
        if not player:
            print(
                "ERROR: Scene",
                getattr(self.core, "id", "Unknown"),
                "requires a player instance.",
            )
            return

        actions = []
        inventory = self.storage.get_inventory()

        for item in inventory:
            actions.append(f"APPROACH {item.get_id()}")

        if self.has_introduced:
            new_description = """The courtyard is overrun with wild weeds, haunted by unsettling statues, and steeped in memories best left buried."""
            examinable = self.core.get_actionable("examine")
            if not isinstance(examinable, Examinable):
                raise TypeError("Unknown Examinable")
            examinable.set_message(new_description)
            self.examine()  # Show updated message on revisit
        else:
            self.examine()
            self.has_introduced = True

        stringformatter(actions)
        user_next = clicksimulator(1, len(actions))
        optionBox(inventory[user_next - 1])  # Use -1 for 1-based input

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
places = [MainMenu(), Courtyard()]

while running:
    current_scene = places[player_placement]
    current_scene.run(user)
    if current_scene.signaler.get_signal():
        player_placement += 1
        if player_placement >= len(places):
            running = False
