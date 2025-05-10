import sys
import requests
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from ui.ecc import  Ui_ECCDialog  

class ECCApp(QDialog):
    def __init__(self):
        super().__init__()
        self.ui =  Ui_ECCDialog()
        self.ui.setupUi(self)

        # Nối sự kiện
        self.ui.btn_gen_keys.clicked.connect(self.on_generate_keys)
        self.ui.btn_sign.clicked.connect(self.on_sign)
        self.ui.btn_verify.clicked.connect(self.on_verify)

    def on_generate_keys(self):
        """Gọi API tạo cặp private/public key"""
        try:
            resp = requests.get("http://127.0.0.1:5000/api/ecc/generate_keys")
            resp.raise_for_status()
            data = resp.json()
            QMessageBox.information(self, "Success", data.get("message", "Đã tạo khóa thành công"))
            # Nếu API trả về public key, bạn có thể hiển thị ở txt_info
            # self.ui.txt_info.setText(data.get("public_key_pem", ""))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Generate keys failed: {e}")

    def on_sign(self):
        """Gọi API ký message"""
        message = self.ui.txt_info.toPlainText().strip()
        if not message:
            QMessageBox.warning(self, "Input needed", "Bạn phải nhập thông tin ở ô Information trước")
            return

        payload = {"message": message}
        try:
            resp = requests.post("http://127.0.0.1:5000/api/ecc/sign", json=payload)
            resp.raise_for_status()
            data = resp.json()
            sig_hex = data.get("signature", "")
            self.ui.txt_sign.setText(sig_hex)
            QMessageBox.information(self, "Signed", "Đã ký thành công")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Signing failed: {e}")

    def on_verify(self):
        """Gọi API xác thực chữ ký"""
        message   = self.ui.txt_info.toPlainText().strip()
        signature = self.ui.txt_sign.toPlainText().strip()
        if not message or not signature:
            QMessageBox.warning(self, "Input needed", "Cần cả thông tin và chữ ký để verify")
            return

        payload = {"message": message, "signature": signature}
        try:
            resp = requests.post("http://127.0.0.1:5000/api/ecc/verify", json=payload)
            resp.raise_for_status()
            data = resp.json()
            if data.get("is_verified"):
                QMessageBox.information(self, "Verified", "Chữ ký hợp lệ")
            else:
                QMessageBox.warning(self, "Invalid", "Chữ ký không hợp lệ")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Verify failed: {e}")

if __name__ == "__main__":
    app    = QApplication(sys.argv)
    window = ECCApp()
    window.show()
    sys.exit(app.exec_())
