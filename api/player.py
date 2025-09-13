# Define Player Class
class Player:
    from .worldobject import WorldObject
    def __init__(self, worldobject_instance, character_type, password):
        self.core = worldobject_instance
        self.core.set_attribute("xp", 0)
        self.core.set_attribute("level", 1)
        self.core.set_attribute("inventory", [])

        self.password = password
        self.character_type = character_type

    def set_attribute(self, key, value):
        self.core.set_attribute(key, value)

    def get_attribute(self, key):
        return self.core.get_attribute(key)

    def gain_xp(self, amount):
        xp = self.core.get_attribute("xp") + amount
        
        while xp >= self.calculate_level():
            self.level_up()

        self.core.set_attribute("xp", xp)
        self.save_to_file()

    def level_up(self):
        level = self.core.get_attribute("level")

        if not level:
            print("ERROR! No Attribute named 'Level'.")
            sys.exit(1)

        level += 1

        print("Level Up! You are now level " + str(level))

        self.core.set_attribute("level", level)
        self.save_to_file()

    def update_player_stats(self, new_attack, new_health, new_defense):
        self.character_type.attack = new_attack
        self.character_type.health = new_health
        self.character_type.defense = new_defense

    def calculate_level(self):
        return self.core.get_attribute("level") * 100

    def save_to_file(self):
        with open("players.txt", "r") as file:
            lines = file.readlines()
        
        with open("players.txt", "w") as file:
            for line in lines:
                if self.core.ign in line:
                    line = (
                        f"{self.core.ign} "
                        f"{self.password} "
                        f"{self.character_type.name} "
                        f"{self.character_type.attack} "
                        f"{self.character_type.health} "
                        f"{self.character_type.defense} "
                        f"{self.core.get_attribute('level')} "
                        f"{self.core.get_attribute('xp')}\n"
                    )
                file.write(line)
