from .alphabet import ALPHABET

class CaesarCipher:
    def __init__(self):
        self.alphabet = ALPHABET

    def encrypt_text(self, text: str, key: int) -> str:
        text = text.upper()
        n = len(self.alphabet)
        result = []

        for ch in text:
            if ch in self.alphabet:
                idx = self.alphabet.index(ch)
                result.append(self.alphabet[(idx + key) % n])
            else:
                result.append(ch)

        return "".join(result)

    def decrypt_text(self, text: str, key: int) -> str:
        text = text.upper()
        n = len(self.alphabet)
        result = []

        for ch in text:
            if ch in self.alphabet:
                idx = self.alphabet.index(ch)
                result.append(self.alphabet[(idx - key) % n])
            else:
                result.append(ch)

        return "".join(result)
