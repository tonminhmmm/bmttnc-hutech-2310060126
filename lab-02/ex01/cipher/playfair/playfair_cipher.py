
class PlayFairCipher:
    def __init__(self) -> None:
        pass

    def create_playfair_matrix(self, key: str) -> list[list[str]]:
        # Chuyển "J" thành "I" trong khóa và chuyển về chữ in hoa
        key = key.replace("J", "I").upper()
        key_set = set(key)

        # Bảng chữ cái I/J gộp chung
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        remaining_letters = [letter for letter in alphabet if letter not in key_set]

        # Khởi tạo danh sách ký tự theo thứ tự hàng dãy
        matrix = list(key)
        for letter in remaining_letters:
            matrix.append(letter)
            if len(matrix) == 25:
                break

        # Chia thành ma trận 5x5
        playfair_matrix = [matrix[i:i+5] for i in range(0, len(matrix), 5)]
        return playfair_matrix

    def find_letter_coords(self, matrix: list[list[str]], letter: str) -> tuple[int, int]:
        # Tìm hàng và cột của 1 ký tự trong ma trận
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == letter:
                    return row, col
        raise ValueError(f"Letter {letter} not found in Playfair matrix")

    def playfair_encrypt(self, plain_text: str, matrix: list[list[str]]) -> str:
        # Chuẩn hóa input: gộp J thành I, chữ hoa
        plain_text = plain_text.replace("J", "I").upper()
        encrypted_text = ""

        # Xử lý theo cặp ký tự
        for i in range(0, len(plain_text), 2):
            pair = plain_text[i:i+2]
            if len(pair) == 1:
                # Nếu còn sót 1 ký tự, thêm "X" vào cặp
                pair += "X"

            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                # Cùng hàng: dịch cột sang phải 1
                encrypted_text += matrix[row1][(col1 + 1) % 5]
                encrypted_text += matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                # Cùng cột: dịch hàng xuống 1
                encrypted_text += matrix[(row1 + 1) % 5][col1]
                encrypted_text += matrix[(row2 + 1) % 5][col2]
            else:
                # Hình chữ nhật: hoán đổi cột
                encrypted_text += matrix[row1][col2]
                encrypted_text += matrix[row2][col1]

        return encrypted_text

    def playfair_decrypt(self, cipher_text: str, matrix: list[list[str]]) -> str:
        cipher_text = cipher_text.upper()
        decrypted_text = ""

        # Giải mã theo cặp ký tự
        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i+2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                # Cùng hàng: dịch cột sang trái 1
                decrypted_text += matrix[row1][(col1 - 1) % 5]
                decrypted_text += matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                # Cùng cột: dịch hàng lên 1
                decrypted_text += matrix[(row1 - 1) % 5][col1]
                decrypted_text += matrix[(row2 - 1) % 5][col2]
            else:
                # Hình chữ nhật: hoán đổi cột
                decrypted_text += matrix[row1][col2]
                decrypted_text += matrix[row2][col1]

        # Loại bỏ ký tự 'X' thêm ở cuối nếu cần
        result = ""
        for i in range(0, len(decrypted_text) - 2, 2):
            if decrypted_text[i] == decrypted_text[i+2]:
                # Nếu ký tự lặp (do thêm X), chỉ lấy một ký tự
                result += decrypted_text[i]
            else:
                result += decrypted_text[i] + decrypted_text[i+1]

        # Xử lý phần cuối
        if decrypted_text[-1] == "X":
            result += decrypted_text[-2]
        else:
            result += decrypted_text[-2] + decrypted_text[-1]

        return result
