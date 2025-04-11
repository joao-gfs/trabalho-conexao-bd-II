import sys
sys.path.append('../')
import dao.order_dao as dao
from model.order_model import Order, Order_Details

def inserir_pedido(orderid, customerid, employeename, produtos=[]):
    con_db = dao.conectar_bd()
    if con_db == None:
        return "Erro de conexão com banco de dados", 500
    sessao = con_db.cursor()

    sessao.execute(f"SELECT customerid FROM northwind.customers WHERE customerid = '{customerid}'")
    cliente_existe = sessao.fetchall()

    sessao.execute(f"SELECT employeeid FROM northwind.employees WHERE firstname = '{employeename}'")
    employee_tuple = sessao.fetchone()

    sessao.execute(f"SELECT employeeid FROM northwind.orders WHERE orderid = '{orderid}'")
    order_existe = sessao.fetchall()

    if cliente_existe == []:
        return f"Cliente {customerid} não existe", 404
    if employee_tuple == None:
        return f"Funcionário {employeename} não existe", 404
    if order_existe != []:
        return f"Pedido com id {orderid} já existe", 409
    
    employeeid = employee_tuple[0]
    pedido = Order(orderid, customerid, employeeid)

    for produto in produtos:
        sessao.execute(f"SELECT productid FROM northwind.products WHERE productid = '{produto['productid']}'")
        prod_existe = sessao.fetchall()
        if prod_existe == []:
            return f"Produto {produto['productid']} não existe", 404

    for produto in produtos:
        details = Order_Details(pedido.orderid, produto['productid'], produto['unitprice'], produto['quantity'])
        pedido.inserir_produto(details)

    res = dao.inserir_pedido(pedido)
    sessao.close()
    con_db.close()
    return res

if __name__ == '__main__':
    produtos = [
        {"productid": 1, "unitprice": 14.00, "quantity": 10},
        {"productid": 2, "unitprice": 18.00, "quantity": 5}
    ]

    # Substitua "Nancy" pelo nome de um funcionário que exista na sua tabela 'employees'
    mensagem, status = inserir_pedido(114, 'ALFKI', 'sancy', produtos)

    if status == 200:
        print("Sucesso:", mensagem)
    else:
        print(f"Erro ({status}):", mensagem)