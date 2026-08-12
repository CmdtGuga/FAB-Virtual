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
# CONFIGURAÇÃO DO DISCORD
# =====================================


# =====================================
# RECEBER FORMULÁRIO
# =====================================

@app.route("/enviar", methods=["POST"])
def receber_formulario():

    dados = request.json

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
                        "value": nome,
                        "inline": True
                    },

                    {
                        "name": "💬 Discord",
                        "value": discord,
                        "inline": True
                    },

                    {
                        "name": "🎂 Idade",
                        "value": idade,
                        "inline": True
                    },

                    {
                        "name": "📍 Local",
                        "value": local,
                        "inline": False
                    },

                    {
                        "name": "🛫 Simulador",
                        "value": simulador,
                        "inline": True
                    },

                    {
                        "name": "🌐 VATSIM / IVAO",
                        "value": servidor,
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
    # ENVIAR PARA O DISCORD
    # =====================================

    resposta_discord = requests.post(
        WEBHOOK_DISCORD,
        json=mensagem
    )


    # =====================================
    # VERIFICAR SE O DISCORD ACEITOU
    # =====================================

    if resposta_discord.status_code not in [200, 204]:

        print(
            "Erro ao enviar para o Discord:",
            resposta_discord.status_code
        )

        return jsonify({
            "sucesso": False
        }), 500


    return jsonify({
        "sucesso": True
    })


# =====================================
# INICIAR SERVIDOR
# =====================================

if __name__ == "__main__":

    app.run(
        debug=True
    )