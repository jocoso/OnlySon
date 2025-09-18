import api.Materials as Materials


# Create Characters
class Character:
    def __init__(self, data=None):
        pass


# Create Items
class Item:
    def __init__(self, data=None):
        pass


# Create the Chapters
class Chapter:
    def __init__(self, data=None):
        pass


# Instantiate Book's Requirement
pen = Materials.Pen("7 Days Before I Die", indentation=50)
characters = [Character()]
items = [Item()]
chapters = [Chapter()]


# Create a Book using the Characters, Items, Pen and Chapters
class Book:
    def __init__(self, chapters, items, characters, material):
        self.chapters = chapters
        self.items = items
        self.characters = characters
        self.material = material

        self.material.init()
        pen.print_title("The Adventure Begins")

    def read(self):
        self.material.read()


# Read the Book activating the main loop
if __name__ == "__main__":
    Book(chapters, items, characters, pen).read()
