from flask import Flask, render_template, request, json
from cipher.caesar.caesar_cipher import CaesarCipher
from cipher.vigenere.vigenere_cipher import VigenereCipher
from cipher.railfence.railfence_cipher import RailFenceCipher
from cipher.playfair.playfair_cipher import PlayFairCipher
from cipher.transposition.transposition_cipher import TranspositionCipher

app = Flask(__name__)
caesar_cipher = CaesarCipher()
vigenere_cipher = VigenereCipher()
railfence_cipher = RailFenceCipher()
playfair_cipher = PlayFairCipher()
transposition_cipher = TranspositionCipher()


# router routes for home page
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/caesar")
def caesar():
    return render_template('caesar.html')

@app.route("/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    text = request.form["inputPlainText"]
    key  = int(request.form["inputKeyPlain"])
    encrypted = caesar_cipher.encrypt_text(text, key)
    return render_template(
        "caesar.html",
        result=encrypted,
        mode="Encrypted",
        inputPlainText=text,
        inputKeyPlain=key
    )

@app.route("/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    text = request.form["inputCipherText"]
    key  = int(request.form["inputKeyCipher"])
    decrypted = caesar_cipher.decrypt_text(text, key)
    return render_template(
        "caesar.html",
        result=decrypted,
        mode="Decrypted",
        inputCipherText=text,
        inputKeyCipher=key
    )
# ------------------ VigenEre ------------------
@app.route("/vigenere")
def vigenere():
    return render_template('vigenere.html')

@app.route("/vigenere/encrypt", methods=["POST"])
def vigenere_encrypt():
    text = request.form["text"]
    key  = request.form["key"]
    encrypted = vigenere_cipher.vigenere_encrypt(text, key)
    return render_template("vigenere.html", result=encrypted, mode="Encrypted")

# Xử lý decrypt
@app.route("/vigenere/decrypt", methods=["POST"])
def vigenere_decrypt():
    text = request.form["text"]
    key  = request.form["key"]
    decrypted = vigenere_cipher.vigenere_decrypt(text, key)
    return render_template("vigenere.html", result=decrypted, mode="Decrypted")


# ------------------ Rail Fence ------------------
@app.route("/railfence")
def railfence():
    return render_template('railfence.html')


@app.route("/railfence/encrypt", methods=["POST"])
def railfence_encrypt():
    text = request.form["text"]
    key  = int(request.form["key"])
    # call rail_fence_encrypt, not railfence_encrypt
    encrypted = railfence_cipher.rail_fence_encrypt(text, key)
    return render_template(
        "railfence.html",
        result=encrypted,
        mode="Encrypted"
    )


@app.route("/railfence/decrypt", methods=["POST"])
def railfence_decrypt():
    text = request.form["text"]
    key  = int(request.form["key"])
    # call rail_fence_decrypt, not railfence_decrypt
    decrypted = railfence_cipher.rail_fence_decrypt(text, key)
    return render_template(
        "railfence.html",
        result=decrypted,
        mode="Decrypted"
    )
# ------------------ Playfair ------------------

@app.route("/playfair")
def playfair():
    return render_template('playfair.html')


@app.route("/playfair/encrypt", methods=["POST"])
def playfair_encrypt():
    text = request.form["text"]
    key  = request.form["key"]          # keep it a string
    matrix = playfair_cipher.create_playfair_matrix(key)
    encrypted = playfair_cipher.playfair_encrypt(text, matrix)
    return render_template(
        "playfair.html",
        result=encrypted,
        mode="Encrypted"
    )


@app.route("/playfair/decrypt", methods=["POST"])
def playfair_decrypt():
    text = request.form["text"]
    key  = request.form["key"]
    matrix = playfair_cipher.create_playfair_matrix(key)
    decrypted = playfair_cipher.playfair_decrypt(text, matrix)
    return render_template(
        "playfair.html",
        result=decrypted,
        mode="Decrypted"
    )
@app.route("/playfair/creatematrix", methods=["POST"])
def playfair_creatematrix():
    key = request.form["key"]
    matrix = playfair_cipher.create_playfair_matrix(key)
    return render_template(
        "playfair.html",
        result=matrix,
        mode="Matrix"
    )

# ------------------ Transposition ------------------

@app.route("/transposition")
def transposition():
    return render_template('transposition.html')


# Xử lý POST từ form Encrypt
@app.route("/transposition/encrypt", methods=["POST"])
def transposition_encrypt_action():
    text = request.form["text"]
    key  = int(request.form["key"])
    encrypted = transposition_cipher.encrypt(text, key)
    return render_template(
        "transposition.html",
        result=encrypted,
        mode="Encrypted"
    )


# Xử lý POST từ form Decrypt
@app.route("/transposition/decrypt", methods=["POST"])
def transposition_decrypt_action():
    text = request.form["text"]
    key  = int(request.form["key"])
    decrypted = transposition_cipher.decrypt(text, key)
    return render_template(
        "transposition.html",
        result=decrypted,
        mode="Decrypted"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
