import random

class UtilMisc:
    
    @classmethod
    def generate_word(length: int = 5, prefix: str = 'mapset_'):
        _signs = "abcdefghijklmnopqrstuvwxyz1234567890"

        word = ""
        for i in range(length):
            word += random.choice(_signs)

        return prefix + word
    
    