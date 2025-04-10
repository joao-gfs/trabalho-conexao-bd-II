import psycopg

def conectar_bd():
    try:
        bd = psycopg.connect(
            host='localhost',
            dbname='northwind',
            user='postgres',
            password='pgsql456'
        )
        return bd
    except Exception as e:
        print(e)
        return None

def inserir_pedido(pedido):
    con = conectar_bd()
    if con == None:
        return "Erro de conexão com banco de dados", 500
    sessao = con.cursor()

    try:
        sessao.execute(
            f"INSERT INTO northwind.orders (orderid, customerid, employeeid) VALUES ({pedido.orderid}, '{pedido.customerid}', {pedido.employeeid});"
        )
        for produto in pedido.products:
            inserir_order_detail(sessao, produto)

        con.commit()

        return "Pedido inserido com sucesso!", 200
    except Exception as e:
        return f"Erro ao inserir pedido: {e}", 400
    finally:
        sessao.close()
        con.close()

def inserir_order_detail(sessao, order_detail):
    try:
        sessao.execute(
            f"INSERT INTO northwind.order_details (orderid, productid, unitprice, quantity) VALUES ({order_detail.orderid}, {order_detail.productid}, {order_detail.unitprice}, {order_detail.quantity})"
        )
    except Exception as e:
        raise Exception(f"Erro ao inserir pedido: {e}")