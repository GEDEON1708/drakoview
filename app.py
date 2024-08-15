import sys
import codecs
from flask import Flask, jsonify, send_file, request
import os

# Configuração de suporte a UTF-8
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

app = Flask(__name__)

# Pasta onde as imagens serão armazenadas
IMAGEM_PASTA = 'imagens'

# Exemplo simplificado de dragões
dragões = [
    {"name": "Asaprata", "identifier": "asaprata", "color": "silver", "description": "Dragão da prata"},
    {"name": "Caraxes", "identifier": "caraxes", "color": "red", "description": "Dragão vermelho"},
]

@app.route('/dragões', methods=['GET'])
def get_dragões():
    """Retorna a lista de todos os dragões no formato JSON."""
    return jsonify(dragões)

@app.route('/dragões/<id>', methods=['GET'])
def get_dragão(id):
    """Rota para obter um dragão específico pelo ID."""
    dragão = next((d for d in dragões if d["identifier"] == id), None)
    if dragão:
        return jsonify(dragão)
    return jsonify({"erro": "Dragão não encontrado"}), 404

@app.route('/dragões/imagem/<id>', methods=['GET'])
def get_imagem_dragão(id):
    """Rota para obter a imagem do dragão."""
    imagem_path = os.path.join(IMAGEM_PASTA, f"{id}.jpg")
    if os.path.exists(imagem_path):
        return send_file(imagem_path)
    return jsonify({"erro": "Imagem do dragão não encontrada"}), 404

@app.route('/dragões', methods=['POST'])
def adicionar_dragão():
    """Rota para adicionar um novo dragão."""
    data = request.json
    if not data or not all(k in data for k in ("name", "identifier", "color", "description")):
        return jsonify({"erro": "Dados insuficientes para criar um dragão."}), 400

    dragões.append(data)
    return jsonify(data), 201

# Rotas para obter trajetórias e nuvens de pontos podem ser adicionadas aqui, conforme necessário

if __name__ == '__main__':
    app.run(debug=True)
