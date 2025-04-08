import sys
sys.path.append('../')
import dao.order_dao as dao
from model.order_model import Order

def inserir_pedido(orderid, customerid, employeeid):
    con_db = dao.conectar_bd()
    sessao = con_db.cursor()

    sessao.execute(f"SELECT customerid FROM northwind.customers WHERE customerid = '{customerid}'")
    cliente_existe = sessao.fetchall()

    sessao.execute(f"SELECT employeeid FROM northwind.employees WHERE employeeid = '{employeeid}'")
    func_existe = sessao.fetchall()

    sessao.execute(f"SELECT employeeid FROM northwind.orders WHERE orderid = '{orderid}'")
    order_existe = sessao.fetchall()

    if cliente_existe == []:
        return f"Cliente {customerid} não existe"
    if func_existe == []:
        return f"Funcionário {employeeid} não existe"
    if order_existe != []:
        return f"Pedido com id {orderid} já existe"
    
    pedido = Order(orderid, customerid, employeeid)
    res = dao.inserir_pedido(pedido)
    sessao.close()
    con_db.close()
    return res

if __name__ == '__main__':
    res = inserir_pedido(21, 'ALFKI', 5)
    print(res)