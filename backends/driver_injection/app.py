from flask_cors import CORS
from flask import Flask, request, jsonify
import controller.order_controller as ctrl

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['POST'])
def inserir_pedido():
    data = request.get_json()   
    mensagem, status = ctrl.inserir_pedido(
        data['orderid'],    
        data['customerid'],
        data['employeename'],
        data['produtos']
    )

    if status >= 400:
        return jsonify({"erro": mensagem}), status
    return jsonify({"mensagem": mensagem}), status

@app.route("/pedido/<int:orderid>", methods=['GET'])
def relatorio_pedido(orderid):
    data, status = ctrl.get_pedido(orderid)

    if status >= 400:
        return jsonify({"erro": data}), status
    return jsonify({"mensagem": data}), status

@app.route("/ranking/<start>/<end>", methods=['GET'])
def relatorio_ranking(start, end):
    data, status = ctrl.get_ranking(start, end)

    if status >= 400:
        return jsonify({"erro": data}), status
    return jsonify({"mensagem": data}), status