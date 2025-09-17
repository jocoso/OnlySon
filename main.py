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
paper = Materials.Paper((1280, 720), 60, "7 Days Before I Die")
characters = [Character()]
items = [Item()]
chapters = [Chapter()]


# Create a Book using the Characters, Items, Pen and Chapters
class Book:
    def __init__(self, chapters, items, characters, paper):
        self.chapters = chapters
        self.items = items
        self.characters = characters
        self.paper = paper

        self.paper.init()

    def read(self):
        self.paper.read()


# Read the Book activating the main loop
if __name__ == "__main__":
    Book(chapters, items, characters, paper).read()
