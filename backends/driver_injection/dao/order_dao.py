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

def buscar_pedido(orderid, con):
    con = conectar_bd()
    if con is None:
        return "Erro de conexão com banco de dados", 500
    sessao = con.cursor()

    query = f"""
        select o.orderid, o.orderdate, c.companyname, e.firstname, e.lastname, p.productname, od.quantity, od.unitprice, od.quantity * od.unitprice as total 
        from northwind.orders o join northwind.order_details od on o.orderid = od.orderid 
        join northwind.customers c on o.customerid = c.customerid join northwind.employees e on o.employeeid = e.employeeid join northwind.products p on od.productid = p.productid where o.orderid = {orderid}
    """
    
    try:
        sessao.execute(query)
        rows = sessao.fetchall()

        if not rows:
            return None
        
        pedido = {
            "orderId": rows[0][0],
            "orderDate": rows[0][1].isoformat(),
            "customerName": rows[0][2],
            "employeeName": f"{rows[0][3]} {rows[0][4]}",
            "itens": []
        }

        for row in rows:
            pedido["itens"].append({
                "productName": row[5],
                "quantity": row[6],
                "unitPrice": float(row[7]),
                "total": float(row[8])
            })

        return pedido
    except Exception as e:
        print("Erro ao buscar pedido:", e)
        return None
    finally:
        sessao.close()
        con.close()
