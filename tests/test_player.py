import unittest
from unittest.mock import mock_open, patch
from api.player import Player

class TestPlayer(unittest.TestCase):
    def test_create_player(self):
        from api.charactertype import CharacterType
        character_type = CharacterType("test", 10, 11, 12)
        # Test ability to add/get attributes
        player = Player("test_player", character_type, "test_password")
        
        xp = player.core.get_attribute("xp")
        level = player.core.get_attribute("level")
        password = player.password
        player_charactertype = player.character_type
        self.assertEqual(xp, 0, "Failed Retrieving XP")
        self.assertEqual(level, 1, "Failed Retrieving Level")
        self.assertEqual(password, "test_password", "Failed Retrieving Password")
        self.assertIsInstance(player_charactertype, CharacterType)

    def test_xp(self):
        from api.charactertype import CharacterType
        character_type = CharacterType("test", 10, 11, 12)
        player = Player("test_player", character_type, "test_password")
        
        prev_xp = player.core.get_attribute("xp")
        player.gain_xp(20)
        post_xp = player.core.get_attribute("xp")
        self.assertEqual(post_xp, prev_xp + 20, "XP hasn't been update")

    def test_level_up(self):
        from api.charactertype import CharacterType
        character_type = CharacterType("test", 10, 11, 12)
        player = Player("test_player", character_type, "test_password")
        
        prev_level = player.core.get_attribute("level")
        player.gain_xp(500)
        post_level = player.core.get_attribute("level")
        self.assertTrue(prev_level < post_level, "Level did not increase.")

    def test_update_level_stats(self):
        from api.charactertype import CharacterType
        character_type = CharacterType("test", 1, 2, 3)
        player = Player("test_player", character_type, "test_password")
        new_attack = 22
        new_health = 35
        new_defense = 69
        player.update_player_stats(new_attack, new_health, new_defense)
        self.assertEqual(new_attack, player.character_type.attack, "Attack stat was not updated correctly")
        self.assertEqual(new_health, player.character_type.health, "Health stat was not updated correctly")
        self.assertEqual(new_defense, player.character_type.defense, "Defense stat was not updated correctly")

    def test_save_to_file(self):
        # Sample content of players.txt
        mocked_file_content = (
            "player1 pass1 witch 10 100 5 1 0\n"
            "test_player oldpass demon 15 150 10 2 20\n"
        )

        # Expected line after update for test_player
        updated_line = "test_player test_password demon 10 11 12 1 0\n"

        m_open = mock_open(read_data=mocked_file_content)

        with patch("builtins.open", m_open):
            # Call save_to_file on your actual Player instance
            # (You might need to create this instance similar to other tests)
            from api.charactertype import CharacterType
            character_type = CharacterType("demon", 10, 11, 12)
            player = Player("test_player", character_type, "test_password")
            player.save_to_file()

        # Gather all written data from mock calls
        written_calls = m_open().write.call_args_list
        written_content = "".join(call.args[0] for call in written_calls)

        # Assert that the player line got updated
        self.assertIn(updated_line, written_content)
        # Assert other lines remain
        self.assertIn("player1 pass1 witch 10 100 5 1 0\n", written_content)

if __name__ == "__main__":
    unittest.main()
