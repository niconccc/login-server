from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
CORS(app)

USUARIOS_FILE = "usuarios.json"

# Utilitários para ler e salvar JSON
def carregar_usuarios():
    if not os.path.exists(USUARIOS_FILE):
        return {}
    with open(USUARIOS_FILE, "r") as f:
        return json.load(f)

def salvar_usuarios(dados):
    with open(USUARIOS_FILE, "w") as f:
        json.dump(dados, f, indent=4)

@app.route("/")
def home():
    return "Servidor de login ativo com tempo e MAC!"

@app.route("/verificar_login", methods=["POST"])
def verificar_login():
    dados = request.get_json()
    usuario = dados.get("usuario")
    senha = dados.get("senha")
    mac = dados.get("mac")

    usuarios = carregar_usuarios()
    user = usuarios.get(usuario)

    if not user or user["senha"] != senha:
        return jsonify({"status": "erro", "mensagem": "Login ou senha incorretos."}), 401

    if user["mac"] is None:
        user["mac"] = mac
        user["ativado_em"] = datetime.now().isoformat()
        salvar_usuarios(usuarios)
        return jsonify({"status": "ok", "mensagem": "Dispositivo ativado. Tempo de uso iniciado."})

    if user["mac"] != mac:
        return jsonify({"status": "erro", "mensagem": "Este login já foi usado em outro computador."}), 403

    ativado_em = datetime.fromisoformat(user["ativado_em"])
    tempo_total = timedelta(hours=user["tempo_horas"])
    tempo_restante = (ativado_em + tempo_total) - datetime.now()

    if tempo_restante.total_seconds() <= 0:
        return jsonify({"status": "erro", "mensagem": "Tempo de uso expirado."}), 403

    return jsonify({
        "status": "ok",
        "mensagem": f"Acesso autorizado! Tempo restante: {str(tempo_restante).split('.')[0]}"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
