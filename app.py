from flask import Flask, request, jsonify
import sqlite3
import os
from datetime import datetime, timedelta

app = Flask(__name__)
DB = "usuarios.db"

def init_db():
    if not os.path.exists(DB):
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                login TEXT PRIMARY KEY,
                liberado_ate TEXT,
                link_app TEXT
            )
        ''')
        conn.commit()
        conn.close()

@app.route('/verificar', methods=['POST'])
def verificar():
    login = request.json.get("login")
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT liberado_ate, link_app FROM usuarios WHERE login=?", (login,))
    row = c.fetchone()
    conn.close()

    if row:
        liberado_ate_str, link = row
        agora = datetime.utcnow()
        liberado_ate = datetime.fromisoformat(liberado_ate_str)
        if agora <= liberado_ate:
            return jsonify({"status": "liberado", "link": link})
        else:
            return jsonify({"status": "expirado"})
    return jsonify({"status": "nao_encontrado"})

@app.route('/autorizar', methods=['POST'])
def autorizar():
    login = request.json.get("login")
    horas = int(request.json.get("horas", 1))
    link = request.json.get("link")

    liberado_ate = datetime.utcnow() + timedelta(hours=horas)
    liberado_iso = liberado_ate.isoformat()

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("REPLACE INTO usuarios (login, liberado_ate, link_app) VALUES (?, ?, ?)", (login, liberado_iso, link))
    conn.commit()
    conn.close()

    return jsonify({"status": "autorizado", "expira": liberado_iso})

if __name__ == '__main__':
    init_db()
    app.run()
