import psycopg
import inspect as constructor
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.inspection import inspect

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