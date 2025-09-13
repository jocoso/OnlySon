import unittest
from api.worldobject import WorldObject  # Ensure you run this as part of a package/module

class TestWorldObject(unittest.TestCase):
    def test_addget_attributes(self):
        # Test ability to add/get attributes
        worldObject = WorldObject("test object")
        worldObject.set_attribute("test", 7)
        self.assertEqual(worldObject.get_attribute("test"), 7, "Failed to retrieve attribute")

if __name__ == "__main__":
    unittest.main()
