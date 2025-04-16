import sys
sys.path.append('../')
import dao.order_dao as dao
from model.models import Orders, OrderDetails, Products, Customers, Employees

def inserir_pedido(orderid, customerid, employeename, produtos=[]):
    try:
        sessao = dao.criar_sessao()
    except Exception as e:
        return e, 500
    
    if produtos == []:
        return "Lista de produtos vazia", 400
    
    cliente = sessao.query(Customers).filter(Customers.customerid == customerid).first()
    employee = sessao.query(Employees).filter(Employees.firstname == employeename).first()
    order_existe = sessao.query(Orders).filter(Orders.orderid == orderid).first()
    
    if cliente == None:
        return f"Cliente {customerid} não existe", 404
    if employee == None:
        return f"Funcionário {employeename} não existe", 404
    if order_existe != None:
        return f"Pedido com id {orderid} já existe", 409
    
    employeeid = employee.employeeid

    details = []
    for produto in produtos:
        prod = sessao.query(Products).filter(Products.productid == produto['productid']).first()
        if prod == None:
            return f"Produto {produto['productid']} não existe", 404
        unitprice = prod.unitprice

        details.append(OrderDetails(
            orderid=orderid, 
            productid=produto['productid'], 
            unitprice=unitprice, 
            quantity=produto['quantity'])
        )

    pedido = Orders(
        orderid=orderid, 
        customerid=customerid, 
        employeeid=employeeid, 
        order_details=details
    )

    res = dao.inserir_pedido(pedido)

    sessao.close()
    return res

def get_pedido(orderid):
    try:
        data = buscar_pedido(orderid)
        if not data:
            return "Pedido não encontrado", 404
        return data, 200
    except Exception as e:
        return str(e), 500

def get_ranking(start, end):
    try:
        data = buscar_ranking(start, end)
        if not data:
            return "Ranking não encontrado", 400
        return data, 200
    except Exception as e:
        return str(e), 500
