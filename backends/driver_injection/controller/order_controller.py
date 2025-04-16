import sys
sys.path.append('../')
import dao.order_dao as dao
from model.models import Orders, OrderDetails

def inserir_pedido(orderid, customerid, employeename, produtos=[]):
    con_db = dao.conectar_bd()
    if con_db == None:
        return "Erro de conexão com banco de dados", 500
    sessao = con_db.cursor()

    if produtos == []:
        return "Lista de produtos vazia", 400

    sessao.execute(f"SELECT customerid FROM northwind.customers WHERE customerid = '{customerid}'")
    cliente_existe = sessao.fetchall()

    sessao.execute(f"SELECT employeeid FROM northwind.employees WHERE firstname = '{employeename}'")
    employee_tuple = sessao.fetchone()

    sessao.execute(f"SELECT orderid FROM northwind.orders WHERE orderid = '{orderid}'")
    order_existe = sessao.fetchall()

    if cliente_existe == []:
        return f"Cliente {customerid} não existe", 404
    if employee_tuple == None:
        return f"Funcionário {employeename} não existe", 404
    if order_existe != []:
        return f"Pedido com id {orderid} já existe", 409
    
    employeeid = employee_tuple[0]
    pedido = Orders(orderid=orderid, customerid=customerid, employeeid=employeeid)

    details = []
    for produto in produtos:
        sessao.execute(f"SELECT unitprice FROM northwind.products WHERE productid = '{produto['productid']}'")
        preco = sessao.fetchall()
        if preco == []:
            return f"Produto {produto['productid']} não existe", 404
        unitprice = (preco[0])[0]

        details.append(OrderDetails(orderid=pedido.orderid, productid=produto['productid'], unitprice=unitprice, quantity=produto['quantity']))

    res = dao.inserir_pedido(pedido, details)

    sessao.close()
    con_db.close()
    return res

def get_pedido(orderid):
    con_db = dao.conectar_bd()
    if con_db is None:
        return "Erro de conexão com banco de dados", 500

    try:
        data = dao.buscar_pedido(orderid, con_db)
        if not data:
            return "Pedido não encontrado", 404
        return data, 200
    except Exception as e:
        return str(e), 500
    finally:
        con_db.close()

def get_ranking(start, end):
    con_db = dao.conectar_bd()
    if con_db is None:
        return "Erro de conexão com o banco de dados", 500

    try:
        data = dao.buscar_ranking(start, end, con_db)
        if not data:
            return "Ranking de funcionários não encontrado", 404
        return data, 200
    except Exception as e:
        return str(e), 500
    finally: 
        con_db.close()
