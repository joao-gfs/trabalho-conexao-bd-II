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
        f"INSERT INTO northwind.orders (orderid, customerid, employeeid) VALUES ({pedido.orderid}, '{pedido.customerid}', {pedido.employeeid});"
    )

def inserir_order_details(sessao, order_details):
    for detail in order_details:
        sessao.execute(
            f"INSERT INTO northwind.order_details (orderid, productid, unitprice, quantity) VALUES ({detail.orderid}, {detail.productid}, {detail.unitprice}, {detail.quantity});"
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

def buscar_pedido(orderid):
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
        
        if not rows[0][1]:
            order_date = "Não informado"
        else:
            order_date = rows[0][1].isoformat()

        pedido = {
            "orderId": rows[0][0],
            "orderDate": order_date,
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

def buscar_ranking(start, end):
    con = conectar_bd()
    if con is None:
        return "Erro de conexão com banco de dados", 500
    sessao = con.cursor()

    query = f"""
        select e.firstname, count(o.orderid) as total_vendas, sum(od.unitprice * od.quantity) as total_vendido
        from northwind.orders o join northwind.employees e on o.employeeid = e.employeeid
        join northwind.order_details od on o.orderid = od.orderid
        where o.orderdate between '{start}' and '{end}'
        group by e.firstname order by total_vendido desc
    """

    try:
        sessao.execute(query)
        rows = sessao.fetchall()

        if not rows:
            return None

        ranking = []
        for row in rows:
            ranking.append({
                "firstname": row[0],
                "total_vendas": row[1],
                "total_vendido": float(row[2])
            })

        return ranking
    except Exception as e:
        print("Erro ao buscar ranking:", e)
        return None
    finally:
        sessao.close()
        con.close()
        

        