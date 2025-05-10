# rsa_cipher.py
import sys
import requests
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
# import Ui_RsaDialog từ file giao diện mới
from ui.rsa import Ui_Dialog  

class MyApp(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # kết nối các nút với hàm gọi API
        self.ui.btn_gen_keys.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_encrypt .clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt .clicked.connect(self.call_api_decrypt)
        self.ui.btn_sign    .clicked.connect(self.call_api_sign)
        self.ui.btn_verify  .clicked.connect(self.call_api_verify)

    def call_api_gen_keys(self):
        url = "http://127.0.0.1:5000/api/rsa/generate_keys"
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            data = resp.json()
            QMessageBox.information(self, "Success", data["message"])
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/encrypt"
        payload = {
            "message":  self.ui.txt_plain_text.toPlainText(),
            "key_type": "public"
        }
        try:
            resp = requests.post(url, json=payload)
            resp.raise_for_status()
            encrypted = resp.json()["encrypted_message"]
            self.ui.txt_cipher_text.setText(encrypted)
            QMessageBox.information(self, "Encrypted", "Encrypted Successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/decrypt"
        payload = {
            "ciphertext": self.ui.txt_cipher_text.toPlainText(),
            "key_type":   "private"
        }
        try:
            resp = requests.post(url, json=payload)
            resp.raise_for_status()
            decrypted = resp.json()["decrypted_message"]
            self.ui.txt_plain_text.setText(decrypted)
            QMessageBox.information(self, "Decrypted", "Decrypted Successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def call_api_sign(self):
        url = "http://127.0.0.1:5000/api/rsa/sign"
        payload = {"message": self.ui.txt_info.toPlainText()}
        try:
            resp = requests.post(url, json=payload)
            resp.raise_for_status()
            signature = resp.json()["signature"]
            self.ui.txt_sign.setText(signature)
            QMessageBox.information(self, "Signed", "Signed Successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def call_api_verify(self):
        url = "http://127.0.0.1:5000/api/rsa/verify"
        payload = {
            "message":   self.ui.txt_info.toPlainText(),
            "signature": self.ui.txt_sign.toPlainText()
        }
        try:
            resp = requests.post(url, json=payload)
            resp.raise_for_status()
            ok = resp.json().get("is_verified", False)
            if ok:
                QMessageBox.information(self, "Verified", "Signature is valid")
            else:
                QMessageBox.warning(self, "Failed", "Signature verification failed")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app    = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
