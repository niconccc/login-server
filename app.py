from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import os

app = Flask(__name__)
autorizados = {}  # Armazena os logins autorizados com validade e link

@app.route("/")
def home():
    return "API Login Server online!"

@app.route("/autorizar", methods=["POST"])
def autorizar():
    data = request.json
    login = data.get("login")
    horas = int(data.get("horas", 1))
    link = data.get("link", "")

    expira = datetime.now() + timedelta(hours=horas)
    autorizados[login] = {"expira": expira, "link": link}
    return jsonify({"status": "ok", "expira": expira.isoformat()})

@app.route("/verificar", methods=["POST"])
def verificar():
    data = request.json
    login = data.get("login")

    if login not in autorizados:
        return jsonify({"status": "negado", "mensagem": "Login não registrado"})

    dados = autorizados[login]
    if datetime.now() > dados["expira"]:
        return jsonify({"status": "expirado", "mensagem": "Tempo expirado"})

    return jsonify({"status": "liberado", "link": dados["link"]})

# CONFIGURAÇÃO PARA FUNCIONAR NO RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
