from flask import Flask, request, jsonify
import controller.order_controller as ctrl

app = Flask(__name__)

@app.route("/", methods=['POST'])
def inserir_pedido():
    data = request.get_json()
    mensagem, status = ctrl.inserir_pedido(
        data['orderid'],
        data['customerid'],
        data['employeeid'],
        data['produtos']
    )
    
    if status >= 400:
        return jsonify({"erro": mensagem}), status
    return jsonify({"mensagem": mensagem}), status