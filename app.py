from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Dados válidos
usuarios_autorizados = {
    "nico": "123"
}

@app.route("/verificar_login", methods=["POST"])
def verificar_login():
    dados = request.get_json()
    usuario = dados.get("usuario")
    senha = dados.get("senha")

    if usuarios_autorizados.get(usuario) == senha:
        return jsonify({"status": "ok", "mensagem": "Acesso autorizado!"})
    else:
        return jsonify({"status": "erro", "mensagem": "Login ou senha incorretos."}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
