class Order:
    def __init__(self, orderid: int, customerid: str, employeeid: int):
        self.orderid = orderid
        self.customerid = customerid
        self.employeeid = employeeid
        self.products = []

    def to_dict(self):
        return {
            "orderid": self.orderid,
            "customerid": self.customerid,
            "employeeid": self.employeeid
        }
    
    def inserir_produto(self, details):
        self.products.append(details)
    
class Order_Details:
    def __init__(self, orderid: int,  productid: int, unitprice: float, quantity: int):
        self.orderid = orderid
        self.productid = productid
        self.unitprice = unitprice
        self.quantity = quantity

    def to_dict(self):
        return {
            "orderid": self.orderid,
            "productid": self.productid,
            "unitprice": self.unitprice,
            "quantity": self.quantity
        }