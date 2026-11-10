import unittest
from emochi.models.character import Character
from emochi.models.user import User
from emochi.models.message import Message

class TestModels(unittest.TestCase):
    def test_character_from_dict(self):
        data = {
            "id": "char_123",
            "title": "Borian Walker",
            "description": "Mafia right-hand man",
            "coverURL": "https://image-cdn.flowgpt.com/avatar.webp",
            "thumbnailURL": "https://image-cdn.flowgpt.com/thumb.webp"
        }
        c = Character.from_dict(data)
        self.assertEqual(c.id, "char_123")
        self.assertEqual(c.name, "Borian Walker")
        self.assertEqual(c.avatar_url, "https://image-cdn.flowgpt.com/avatar.webp")
        self.assertEqual(c.thumbnail_url, "https://image-cdn.flowgpt.com/thumb.webp")

    def test_user_from_dict(self):
        data = {
            "id": "usr_99",
            "name": "xellox",
            "email": "truong77kk@gmail.com"
        }
        u = User.from_dict(data)
        self.assertEqual(u.id, "usr_99")
        self.assertEqual(u.username, "xellox")
        self.assertEqual(u.email, "truong77kk@gmail.com")

if __name__ == "__main__":
    unittest.main()
