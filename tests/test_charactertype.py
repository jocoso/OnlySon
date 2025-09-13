import unittest
from api.charactertype import CharacterType  # Ensure you run this as part of a package/module

class TestCharacterType(unittest.TestCase):
    def test_create_charactertype(self):
        # Test ability to add/get attributes
        charactertype = CharacterType("test", 10, 11, 12)
        self.assertEqual(charactertype.name, "test", "Failed to retrieve IGN")
        self.assertEqual(charactertype.attack, 10, "Failed to retrieve attack")
        self.assertEqual(charactertype.health, 11, "Failed to retrieve health")
        self.assertEqual(charactertype.defense, 12, "Failed to retrieve defense")

if __name__ == "__main__":
    unittest.main()
