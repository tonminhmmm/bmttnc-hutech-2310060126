from flask import Flask, request, jsonify
from cipher.rsa import RSACipher
from cipher.ecc import ECCCipher 

app = Flask(__name__)
rsa = RSACipher()
ecc_cipher = ECCCipher()

@app.route("/api/rsa/generate_keys", methods=["GET"])
def rsa_generate_keys():
    rsa.generate_keys()
    return jsonify({"message": "generated successfully"})

@app.route("/api/rsa/encrypt", methods=["POST"])
def rsa_encrypt():
    data = request.json
    message  = data["message"]
    key_type = data["key_type"]  # "public" or "private"
    priv, pub = rsa.load_keys()
    key = pub if key_type == "public" else priv
    encrypted = rsa.encrypt(message, key).hex()
    return jsonify({"encrypted_message": encrypted})

@app.route("/api/rsa/decrypt", methods=["POST"])
def rsa_decrypt():
    data = request.json
    ct_hex   = data["ciphertext"]
    key_type = data["key_type"]
    priv, pub = rsa.load_keys()
    key = priv if key_type == "private" else pub
    decrypted = rsa.decrypt(bytes.fromhex(ct_hex), key)
    return jsonify({"decrypted_message": decrypted})

@app.route("/api/rsa/sign", methods=["POST"])
def rsa_sign():
    data = request.json
    message = data["message"]
    _, pub = rsa.load_keys()
    priv, _ = rsa.load_keys()
    signature = rsa.sign(message, priv).hex()
    return jsonify({"signature": signature})

@app.route("/api/rsa/verify", methods=["POST"])
def rsa_verify():
    data = request.json
    message   = data["message"]
    sig_hex   = data["signature"]
    _, pub    = rsa.load_keys()
    verified  = rsa.verify(message, bytes.fromhex(sig_hex), pub)
    return jsonify({"is_verified": verified})

@app.route('/api/ecc/generate_keys', methods=['GET'])
def ecc_generate_keys():
    ecc_cipher.generate_keys()
    return jsonify({'message': 'Đã tạo khóa thành công'})

@app.route('/api/ecc/sign', methods=['POST'])
def ecc_sign_message():
    data = request.json
    message = data['message']
    private_key, _ = ecc_cipher.load_keys()
    signature = ecc_cipher.sign(message, private_key)
    signature_hex = signature.hex()
    return jsonify({'signature': signature_hex})

@app.route('/api/ecc/verify', methods=['POST'])
def ecc_verify_signature():
    data = request.json
    message = data['message']
    signature_hex = data['signature']
    signature = bytes.fromhex(signature_hex)
    _, public_key = ecc_cipher.load_keys()
    is_verified = ecc_cipher.verify(message, signature, public_key)
    return jsonify({'is_verified': is_verified})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
