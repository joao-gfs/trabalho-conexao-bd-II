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


def inserir_order(sessao, pedido):
    sessao.execute(
        "INSERT INTO northwind.orders (orderid, customerid, employeeid) VALUES (%s, %s, %s);",
        (pedido.orderid, pedido.customerid, pedido.employeeid)
    )

def inserir_order_details(sessao, order_details):
    for detail in order_details:
        sessao.execute(
            "INSERT INTO northwind.order_details (orderid, productid, unitprice, quantity) VALUES (%s, %s, %s, %s);",
            (detail.orderid, detail.productid, detail.unitprice, detail.quantity)
        )

def inserir_pedido(pedido, order_details):
    con = conectar_bd()
    if con is None:
        return "Erro de conexão com banco de dados", 500
    sessao = con.cursor()
    try:
        inserir_order(sessao, pedido)
        inserir_order_details(sessao, order_details)
        con.commit()
        return "Pedido inserido com sucesso!", 200
    except Exception as e:
        con.rollback()
        return f"Erro ao inserir pedido: {e}", 400
    finally:
        sessao.close()
        con.close()
