import unittest
from emochi.utils.translator import translate_en_to_vi

class TestTranslator(unittest.TestCase):
    def test_translation_basic(self):
        text = "Hello! How are you?"
        res = translate_en_to_vi(text)
        self.assertIsInstance(res, str)
        self.assertTrue(len(res) > 0)

if __name__ == "__main__":
    unittest.main()
