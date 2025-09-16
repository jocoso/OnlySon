from api.helpers import stringformatter, clicksimulator, optionBox
from api.actionables import Storageable, Openable, Examinable, Signaler
from api.core.player import Player
from api.core.game_object import GameObject
from api.core.IO import IO
from src.xml.parsed_objects import parsed_object


class CourtyardSouth:
    def __init__(self, player=None):
        self.signaler = Signaler(False)
        self.io = io
        # Clean up the description (single instance, not repeated)
        description = """\nIt is night when you arrive at La Antigua Manor.\n
The estate looms large in the darkness—a bloated mansion adorned with cheap replicas of Greek statues,desperate in their attempt to mimic a culture once held as superior. But there is no grandeur here—only sad theater, reaching for weakness as though it were strength; the abandonment of something richer in favor of illusions that cling to the air like mildew.

The manor has clearly seen better days. Nature has begun its slow reclamation: vines crawl over the stucco like veins on a dying man; animals nest in its bones, as if they sensed the rot long before any human dared to admit it.

Shattered windows and crooked doors gape like open sores. The air is thick with the scent of damp wood, rust, and something older—something sweet and spoiled. This is no home—only the carcass of a titan, long dead, now left to decompose beneath the crushing weight of its own pretense.\n"""

        examinable = Examinable(description)
        self.core = GameObject(
            "0x21", "Courtyard South", actionables={"examine": examinable}
        )
        self.player = player  # Save player reference here for usage in run()
        self.has_introduced = False

        items = [parsed_object.get(id) for id in ["0x33", "0x34"]]
        items = [item for item in items if item is not None]

        # Storage can contain furniture objects like Desk, Bed
        self.storage = Storageable(items)  # Assuming a Bed class exists

    def examine(self):
        self.io.type_print(self.core.execute_actionable("examine"))

    def run(self, player=None):
        if not player:
            print(
                "ERROR: Scene",
                getattr(self.core, "id", "Unknown"),
                "requires a player instance.",
            )
            return -1

        actions = []
        inventory = self.storage.get_inventory()

        for item in inventory:
            actions.append(f"APPROACH {item.get_name()}")

        if self.has_introduced:
            new_description = """The end of the courtyard is overrun with wild weeds, haunted by unsettling statues, and steeped in memories best left buried."""
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
        if user_next == "esc":
            # return to main menu
            return
        optionBox(
            inventory[user_next - 1], io, player, inventory[user_next - 1].get_name()
        )  # Use -1 for 1-based input

        self.signaler.set_signaler(True)
        return 0


class MainMenu:
    def __init__(self, io):
        self.signaler = Signaler(False)
        self.player = None
        self.io = io

    def run(self):
        global running
        console = IO()

        while True:
            console.type_print("== Main Menu ==")
            stringformatter(["New user", "Login", "Quit"])
            choice = input("> ").strip().lower()
            if choice == "1":
                self.player = self.create_player()
                if self.player:
                    self.signaler.next = True
                    return
            elif choice == "2":
                self.player = self.login()
                if self.player:
                    self.signaler.next = True
                    return
            elif choice == "3":
                self.signaler.next = False
                return
            elif choice == "esc":
                print("Already at main menu.")
            else:
                print("Invalid selection. Try again.")

    def create_player(self):
        print("Create a new player")
        while True:
            player_name = input("Enter your player name: ").strip()
            player_id = "0x11"
            if player_id:
                self.player = Player(player_id, player_name, init_items=[])
                print(f"Player '{player_id}' created successfully.")
                return self.player
            else:
                print("Player name cannot be empty. Please enter a valid name.")

    def login(self):
        print("Login")
        while True:
            player_id = "0x11"
            player_name = input("Enter your player name: ").strip()
            if player_id:
                self.player = Player(player_id, player_name, init_items=[])
                print(f"Welcome back, {player_id}.")
                return self.player
            else:
                print("Player name cannot be empty. Please enter a valid name.")


class Scene:
    def __init__(self, places):

        # Global variables and game loop setup
        self.player_placement = 0
        self.running = True
        self.places = places
        self.current_scene = None

    def play(self, user):
        while self.running and self.player_placement < len(self.places):
            next_idx = self.places[self.player_placement].run(user)

            if next_idx is None or next_idx < 0 or next_idx >= len(self.places):
                self.running = False
                break
            else:
                self.player_placement = next_idx


class ScenePlayer:
    def __init__(self, menu, scene_manager):
        self.menu = menu
        self.player_placement = 0
        self.scene_manager = scene_manager
        self.running = True

    def play_mainmenu(self):
        self.menu.run()

    def play_game(self):
        self.scene_manager.play(self.menu.player)

    def play(self):
        while self.running:
            self.play_mainmenu()
            if self.menu.signaler.get_signal():
                self.play_game()
            else:
                self.running = False


io = IO(0.01)
courtyard = [CourtyardSouth()]
scene_manager = Scene(courtyard)
menu = MainMenu(io)
player = ScenePlayer(menu, scene_manager)
try:
    player.play()
except KeyboardInterrupt:
    print("\nGame interrupted. Exiting...")
