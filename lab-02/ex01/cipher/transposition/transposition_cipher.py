import math

class TranspositionCipher:
    def __init__(self):
        pass

    def encrypt(self, text, key):
        encrypted_text = ''
        for col in range(key):
            pointer = col
            while pointer < len(text):
                encrypted_text += text[pointer]
                pointer += key
        return encrypted_text

    def decrypt(self, text, key):
        # số hàng (rows) khi dựng ma trận
        rows = math.ceil(len(text) / key)
        # số cột dài hơn 1 kí tự (có phần dư)
        num_long_cols = len(text) % key

        # cắt chuỗi ciphertext thành từng cột
        cols = []
        start = 0
        for col in range(key):
            col_len = rows if col < num_long_cols else rows - 1
            cols.append(text[start : start + col_len])
            start += col_len

        # đọc ngược theo hàng để ghép lại plaintext
        plaintext = []
        for r in range(rows):
            for c in cols:
                if r < len(c):
                    plaintext.append(c[r])
        return ''.join(plaintext)
