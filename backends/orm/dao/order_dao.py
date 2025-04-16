import sys
sys.path.append('../')
import psycopg
import inspect as constructor
from sqlalchemy import create_engine, func
from datetime import datetime
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.inspection import inspect
from model.models import Orders, OrderDetails, Customers, Employees, Products

def conectar_bd():
    try:
        engine = create_engine("postgresql+psycopg://postgres:pgsql456@localhost/northwind")
        return engine
    except Exception as e:
        print(e)
        return None

def criar_sessao():
    engine = conectar_bd()
    if engine is None:
        raise Exception("Erro de conexão com o banco de dados")
    try:
        Session = sessionmaker(bind=engine)
        return Session()
    except Exception as e:
        raise Exception("Erro ao criar sessão no banco de dados")


def inserir_order(sessao, pedido):
    sessao.add(pedido)

def inserir_order_details(sessao, order_details):
    sessao.add_all(order_details)

def inserir_pedido(pedido):
    sessao = criar_sessao()
    try:
        inserir_order(sessao, pedido)
        inserir_order_details(sessao, pedido.order_details)
        sessao.commit()
        return "Pedido inserido com sucesso!", 200
    except Exception as e:
        sessao.rollback()
        return f"Erro ao inserir pedido: {e}", 400
    finally:
        sessao.close()

def buscar_pedido(orderid):
    sessao: Session = criar_sessao()

    try:
        pedido = sessao.query(Orders).filter(Orders.orderid == orderid).first()

        if not pedido:
            return None

        cliente = sessao.query(Customers).filter(Customers.customerid == pedido.customerid).first()
        funcionario = sessao.query(Employees).filter(Employees.employeeid == pedido.employeeid).first()

        itens = sessao.query(OrderDetails, Products) \
        .join(Products, OrderDetails.productid == Products.productid) \
        .filter(OrderDetails.orderid == orderid).all()

        resultado = {
            "orderid": pedido.orderid,
            "orderDate": pedido.orderdate.isoformat() if pedido.orderdate else "Não informado",
            "customerName": cliente.companyname if cliente else "Desconhecido",
            "employeeName": f"{funcionario.firstname} {funcionario.lastname}" if funcionario else "Desconhecido",
            "itens": []
        }

        for orderdetails, produto in itens: 
            total = float(orderdetails.unitprice) * orderdetails.quantity
            resultado["itens"].append({
                "productName": produto.productname,
                "quantity": orderdetails.quantity,
                "unitPrice": float(orderdetails.unitprice),
                "total": total
            })

        return resultado
    
    except Exception as e:
        print("Erro ao buscar relatório de pedidos:", e)
        return None
    finally:
        sessao.close()

def buscar_ranking(start, end):
    sessao: Session = criar_sessao()

    try:
        startDate = datetime.strptime(start, "%Y-%m-%d").date()  
        endDate = datetime.strptime(end, "%Y-%m-%d").date()

        resultados = sessao.query(
            Employees.firstname,
            func.count(Orders.orderid).label("total_vendas"),
            func.sum(OrderDetails.unitprice * OrderDetails.quantity).label("total_vendido")
        ).join(Orders, Employees.employeeid == Orders.employeeid) \
        .join(OrderDetails, Orders.orderid == OrderDetails.orderid) \
        .filter(Orders.orderdate.between(startDate, endDate)) \
        .group_by(Employees.firstname) \
        .order_by(func.sum(OrderDetails.unitprice * OrderDetails.quantity).desc()) \
        .all()

        ranking = []
        for row in resultados:
            ranking.append({
                "firstname": row.firstname,
                "total_vendas": row.total_vendas,
                "total_vendido": float(row.total_vendido)
            })

        return ranking

    except Exception as e:
        print("Erro ao buscar relatório de ranking dos funcionários:", e)
        return None
    finally:
        sessao.close()

