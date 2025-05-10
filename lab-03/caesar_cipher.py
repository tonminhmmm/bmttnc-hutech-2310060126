import sys, os
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from ui.caesar import Ui_Dialog  # note: Ui_Dialog, not Ui_MainWindow
import requests

class CaesarDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # connect your buttons (they exist on a QDialog)
        self.ui.btn_encrypt.clicked.connect(self.on_encrypt_clicked)
        self.ui.btn_decrypt.clicked.connect(self.on_decrypt_clicked)

    def on_encrypt_clicked(self):
        url = "http://127.0.0.1:5000/api/caesar/encrypt"
        payload = {
            "plain_text": self.ui.txt_plain_text.toPlainText(),
            "key": self.ui.txt_key.toPlainText()
        }
        try:
            resp = requests.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            self.ui.txt_cipher_text.setText(data["encrypted_message"])
            QMessageBox.information(self, "Success", "Encrypted successfully")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Encryption failed:\n{e}")

    def on_decrypt_clicked(self):
        url = "http://127.0.0.1:5000/api/caesar/decrypt"
        payload = {
            "cipher_text": self.ui.txt_cipher_text.toPlainText(),
            "key": self.ui.txt_key.toPlainText()
        }
        try:
            resp = requests.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            self.ui.txt_plain_text.setText(data["decrypted_message"])
            QMessageBox.information(self, "Success", "Decrypted successfully")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Decryption failed:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = CaesarDialog()
    dlg.show()
    sys.exit(app.exec_())
