import unittest
import api.Materials as Materials


class TestPaperMethods(unittest.TestCase):
    def setUp(self):
        self.paper = Materials.Paper((640, 480), 30, "Test Caption")

    def test_print(self):
        # Test that print sets buffer correctly
        test_text = "Hello, World!"
        self.paper.print(test_text)
        self.assertEqual(self.paper.buffer, test_text)

    def test_get_buffer(self):
        # Test that get_buffer return the buffer
        test_text = "Test Buffer"
        self.paper.print(test_text)
        self.assertEqual(self.paper.get_buffer(), test_text)

    def test_drawtext(self):
        # This is not practical to unit test, as it requires a pygame surface.
        # A simple call can check it doesn't error out after init.
        self.paper.init()
        try:
            self.paper.draw_text("Test", 36, (0, 0, 0), 0, 0)
        except Exception as e:
            self.fail(f"draw_text() raised exception {e}")

    def test_read(self):
        # Not practical to unit tes: runs event loop forever
        # We check that the attribute running is True after init
        self.paper.init()
        self.assertTrue(self.paper.running)


if __name__ == "__main__":
    unittest.main()
