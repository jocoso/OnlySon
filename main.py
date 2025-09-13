import sys
import os

from api.worldobject import WorldObject
from api.charactertype import CharacterType
from api.signaler import Signaler
from api.player import Player

caret = '>'
running = True
user = None

witch = CharacterType("witch", 100, 1150, 100)
demon = CharacterType("demon", 275, 900, 175)
vampire = CharacterType("vampire", 200, 1000, 150)

def listformatter(object_array):
    for i, obj in enumerate(object_array):
        print(f"{i + 1} - {obj.core.ign}")
    print(f"{len(object_array) + 1} - Leave")

def stringformatter(string_array):
    for i, string in enumerate(string_array):
        print(f"{i + 1} - {string}")

def clicksimulator(range_min, range_max, error=None, caret="> "):
    while True:
        try:
            choice = int(input(caret))
            if choice < range_min or choice > range_max:
                print(error or "You can't pick this option.")
            else:
                return choice
        except ValueError:
            print("Please enter a valid number")

# Decorators for game object actions
def examinable(generic_message):
    def decorator(cls):
        def examine(self, instance_message=None):
            if instance_message:
                print(instance_message)
            else:
                print(generic_message)
        cls.examine = examine
        return cls
    return decorator

def openable(prompt="Item"):
    def decorator(cls):
        cls.has_open = True
        def open_method(self, player, takeable_items):
            print(f"Inside of {prompt} you can see:")
            if takeable_items:
                listformatter(takeable_items)
                print("What would you like to take?")
                pick = clicksimulator(1, len(takeable_items) + 1, "You can't take that.")
                if pick <= len(takeable_items):
                    inventory = player.get_attribute("inventory")
                    item_taken = takeable_items[pick - 1]
                    print(f"You took {item_taken.core.ign}")
                    inventory.append(item_taken)
                    del takeable_items[pick - 1]
                    player.set_attribute("inventory", inventory)
            else:
                print("There is nothing inside.")
        setattr(cls, "open", open_method)
        return cls
    return decorator

def readable(prompt):
    def decorator(cls):
        def read(self, player):
            print(f"{player.core.ign} reads the note:")
            print("===\n" + prompt + "\n===")
        cls.read = read
        return cls
    return decorator

def dialogueformatter(player, message):
    print(f"{player.core.ign}: {message}")

@examinable("A weary note so old you fear it may crumble if you do so much as touch it")
@readable("Don't let them know who you are. "
          "They are civilized and you are a monster; "
          "they will kill you without mercy. "
          "Such are the ways of the civilized.")
class Note: 
    def __init__(self):
        self.core = WorldObject("A Weary Note")

class Openable:
    def __init__(self, takeable_items):
        self.takeable_items = takeable_items
    def open(self, player, obj_name):
        print(f"Inside of {obj_name} you can see:")
        if self.takeable_items:
            listformatter(self.takeable_items)
            print("What would you like to take?")
            pick = clicksimulator(1, len(self.takeable_items) + 1, "You can't take that.")
            if pick <= len(self.takeable_items):
                item_taken = self.takeable_items[pick - 1]
                print(f"You took {item_taken.core.ign}")
                inventory = player.get_attribute("inventory")
                inventory.append(item_taken)
                del self.takeable_items[pick - 1]
                player.set_attribute("inventory", inventory)
        else:
            print("There is nothing inside.")

class Examinable:
    def __init__(self, message):
        self.message = message
    def examine(self, params=None):
        print(self.message)

class GameObject:
    def __init__(self, core, actionables):
        self.core = core
        self.actionables = actionables
    def get_id(self):
        return self.core.ign
    def action(self, name, params=None):
        if name in self.actionables and callable(self.actionables[name]):
            self.actionables[name](params)

@examinable("The bed looks soft and alluring.")
class Bed:
    def __init__(self):
        self.core = WorldObject("A Bed")

@examinable("The door is made out of wood.")
class Door:
    def __init__(self, instance_message=None):
        self.instance_message = instance_message
        self.core = WorldObject("A Door")

def next_place(scene, player):
    global player_placement, running
    if scene.signaler.next:
        player_placement += 1
        if player_placement >= len(places):
            running = False
        else:
            places[player_placement].run(player)

class Bedroom:
    def __init__(self, player):
        self.signaler = Signaler(False)
        self.core = WorldObject("Bedroom")
        self.examinable = Examinable("The Desk is Beautiful")
        self.openable = Openable([Note()])
        self.desk = GameObject(
            WorldObject("Desk"),
            {
                "examine": self.examinable.examine,
                "open": lambda player: self.openable.open(player, "Desk")
            }
        )
    def run(self, player=None):
        if not player:
            print("ERROR: Scene", self.core.ign, "requires a player instance.")
            return
        print("It is night when you wake up, surrounded by sweaty cotton sheets.")
        print("The moonlight softly caresses the air that touches only the skin of your legs, leaving the rest drowning in darkness.")
        print("What do you do?")
        stringformatter(["Leave the bed"])
        user_response = clicksimulator(1, 1, "")
        while True:
            print("You left your bed. As you do, you consider what could you do next.")
            print("Your eyes have adapted to the darkness and you can see sections")
            print("of your room you couldn't see before. Including a desk lying in the corner and a door. The walls are bare.")
            print("What do you do next?")
            stringformatter(["Examine the Desk", "Leave the Room"])
            user_response = clicksimulator(1, 2, "")
            if user_response == 1:
                while True:
                    print("You approach the Desk.")
                    print("What do you want to do?")
                    stringformatter(["Open", "Leave"])
                    desk_action = clicksimulator(1, 2, "Not an option.")
                    if desk_action == 1:
                        self.desk.action("open", player)
                    if desk_action == 2:
                        break
            if user_response == 2:
                break
        self.signaler.next = True

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
        while True:
            player_name = input("Enter your in-game username: ")
            password = input("Enter your password: ")
            user_exists = False
            if os.path.exists("players.txt"):
                with open("players.txt", "r") as file:
                    for line in file:
                        if line.startswith(player_name + " "):
                            print("User is already taken. Please choose a different username.")
                            user_exists = True
                            break
            if not user_exists:
                while True:
                    print("Choose your character type (This choice only affects the skills and stats):")
                    stringformatter(["Witch", "Demon", "Vampire"])
                    choice = input("> ")
                    if choice == "1":
                        player = Player(WorldObject(player_name), witch, password)
                        break
                    elif choice == "2":
                        player = Player(WorldObject(player_name), demon, password)
                        break
                    elif choice == "3":
                        player = Player(WorldObject(player_name), vampire, password)
                        break
                    else:
                        print("Invalid choice, try again.")
                with open("players.txt", "a") as f:
                    f.write(
                        f"{player.core.ign} "
                        f"{player.password} "
                        f"{player.character_type.name} "
                        f"{player.character_type.attack} "
                        f"{player.character_type.health} "
                        f"{player.character_type.defense} "
                        f"{player.core.get_attribute('level')} "
                        f"{player.core.get_attribute('xp')}\n"
                    )
                    print("User created successfully!")
                return player
    def login(self):
        max_fields = 8
        while True:
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            player_found = False
            user = None  
            if not os.path.exists("players.txt"):
                print("No users found. Please create one first.")
                return None
            with open("players.txt", "r") as file:
                for line in file:
                    fields = line.split()
                    if len(fields) == max_fields:
                        stored_username, stored_password = fields[0], fields[1]
                        if username == stored_username and password == stored_password:
                            character_type = CharacterType(fields[2], int(fields[3]), int(fields[4]), int(fields[5]))
                            player = Player(WorldObject(stored_username), character_type, stored_password)
                            player.level = int(fields[6])
                            player.xp = int(fields[7])
                            player_found = True
                            return player
            if not player_found:
                print("Invalid username or password. Please try again.")

player_placement = 0
places = [MainMenu(), Bedroom(None)]
current_scene = None

while running:
    current_scene = places[player_placement]
    current_scene.run(user)
    if current_scene.signaler.next:
        player_placement += 1
        if player_placement >= len(places):
            running = False
