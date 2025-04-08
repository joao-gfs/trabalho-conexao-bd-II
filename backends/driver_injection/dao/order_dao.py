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
    sessao = con.cursor()

    try:
        sessao.execute(
            f"INSERT INTO northwind.orders (orderid, customerid, employeeid) VALUES ({pedido.orderid}, '{pedido.customerid}', {pedido.employeeid});"
        )
        con.commit()
        return "Pedido inserido com sucesso!"
    except Exception as e:
        return f"Erro ao inserir pedido: \n{e}"
    finally:
        sessao.close()
        con.close()