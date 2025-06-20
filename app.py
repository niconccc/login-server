from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Lista de usuários autorizados
usuarios_autorizados = {
    "nico": {
        "senha": "123",
        "mac": None  # Vai ser salvo no primeiro acesso
    }
}

@app.route("/")
def home():
    return "Servidor ativo!"

@app.route("/verificar_login", methods=["POST"])
def verificar_login():
    dados = request.get_json()
    usuario = dados.get("usuario")
    senha = dados.get("senha")
    mac = dados.get("mac")

    user = usuarios_autorizados.get(usuario)

    if user is None or user["senha"] != senha:
        return jsonify({"status": "erro", "mensagem": "Login ou senha incorretos."}), 401

    if user["mac"] is None:
        user["mac"] = mac
        return jsonify({"status": "ok", "mensagem": "Dispositivo autorizado pela primeira vez."})

    if user["mac"] != mac:
        return jsonify({"status": "erro", "mensagem": "Este login já foi usado em outro computador."}), 403

    return jsonify({"status": "ok", "mensagem": "Acesso autorizado!"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
