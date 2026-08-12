from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

CORS(app)

load_dotenv()

WEBHOOK_DISCORD = os.getenv("WEBHOOK_DISCORD")


# =====================================
# RECEBER FORMULÁRIO
# =====================================

@app.route("/enviar", methods=["POST"])
def receber_formulario():

    try:

        dados = request.get_json()

        nome = dados.get("nome")
        discord = dados.get("discord")
        idade = dados.get("idade")
        local = dados.get("local")
        simulador = dados.get("simulador")
        servidor = dados.get("servidor")

        # =====================================
        # MOSTRAR NO TERMINAL
        # =====================================

        print()
        print("================================")
        print("       NOVO CADASTRO FAB")
        print("================================")
        print("Nome:", nome)
        print("Discord:", discord)
        print("Idade:", idade)
        print("Local:", local)
        print("Simulador:", simulador)
        print("VATSIM/IVAO:", servidor)
        print("================================")
        print()

        # =====================================
        # MENSAGEM PARA O DISCORD
        # =====================================

        mensagem = {
            "embeds": [
                {
                    "title": "🛩️ Novo cadastro — FAB Virtual",

                    "description":
                        "Um novo candidato preencheu o formulário.",

                    "fields": [

                        {
                            "name": "👤 Nome",
                            "value": str(nome),
                            "inline": True
                        },

                        {
                            "name": "💬 Discord",
                            "value": str(discord),
                            "inline": True
                        },

                        {
                            "name": "🎂 Idade",
                            "value": str(idade),
                            "inline": True
                        },

                        {
                            "name": "📍 Local",
                            "value": str(local),
                            "inline": False
                        },

                        {
                            "name": "🛫 Simulador",
                            "value": str(simulador),
                            "inline": True
                        },

                        {
                            "name": "🌐 VATSIM / IVAO",
                            "value": str(servidor),
                            "inline": True
                        }

                    ],

                    "footer": {
                        "text": "FAB Virtual • Sistema de Cadastro"
                    }
                }
            ]
        }

        # =====================================
        # VERIFICAR WEBHOOK
        # =====================================

        if not WEBHOOK_DISCORD:

            print("ERRO: WEBHOOK_DISCORD não foi configurado.")

            return jsonify({
                "sucesso": False,
                "erro": "Webhook não configurado."
            }), 500

        # =====================================
        # ENVIAR PARA O DISCORD
        # =====================================

        resposta_discord = requests.post(
            WEBHOOK_DISCORD,
            json=mensagem,
            timeout=10
        )

        # =====================================
        # VERIFICAR RESPOSTA DO DISCORD
        # =====================================

        if resposta_discord.status_code not in [200, 204]:

            print(
                "Erro ao enviar para o Discord:",
                resposta_discord.status_code,
                resposta_discord.text
            )

            return jsonify({
                "sucesso": False
            }), 500

        print("Cadastro enviado para o Discord com sucesso!")

        return jsonify({
            "sucesso": True
        })

    except Exception as erro:

        print("ERRO NO SERVIDOR:")
        print(erro)

        return jsonify({
            "sucesso": False,
            "erro": str(erro)
        }), 500


# =====================================
# ROTA PRINCIPAL
# =====================================

@app.route("/", methods=["GET"])
def inicio():

    return "Servidor FAB Virtual online!"


# =====================================
# INICIAR SERVIDOR
# =====================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )