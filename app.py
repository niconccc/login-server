from flask import Flask, request, jsonify
import json
import datetime
import os

app = Flask(__name__)
CAMINHO_ARQUIVO = "usuarios.json"

def carregar_usuarios():
    if not os.path.exists(CAMINHO_ARQUIVO):
        return {}
    with open(CAMINHO_ARQUIVO, "r") as f:
        return json.load(f)

def salvar_usuarios(usuarios):
    with open(CAMINHO_ARQUIVO, "w") as f:
        json.dump(usuarios, f, indent=4)

@app.route("/verificar_login", methods=["POST"])
def verificar_login():
    dados = request.get_json()
    usuario = dados.get("usuario")
    senha = dados.get("senha")
    mac = dados.get("mac")

    usuarios = carregar_usuarios()

    if usuario not in usuarios:
        return jsonify({"status": "erro", "mensagem": "Usuário não autorizado."})

    info = usuarios[usuario]

    if info["senha"] != senha:
        return jsonify({"status": "erro", "mensagem": "Senha incorreta."})

    agora = datetime.datetime.utcnow()

    # Primeira vez: registra o MAC e o tempo
    if info["mac"] is None:
        info["mac"] = mac
        info["ativado_em"] = agora.isoformat()
        salvar_usuarios(usuarios)
        return jsonify({"status": "ok", "mensagem": "Acesso autorizado. MAC registrado!"})

    # Se tentar logar de outro PC
    if info["mac"] != mac:
        return jsonify({"status": "erro", "mensagem": "Este usuário já está vinculado a outro PC."})

    # Verifica tempo restante
    ativado_em = datetime.datetime.fromisoformat(info["ativado_em"])
    tempo_permitido = datetime.timedelta(hours=info["tempo_horas"])
    if agora - ativado_em > tempo_permitido:
        return jsonify({"status": "erro", "mensagem": "Tempo de acesso expirado."})

    return jsonify({"status": "ok", "mensagem": "Login autorizado."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
