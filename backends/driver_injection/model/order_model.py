class Order:
    def __init__(self, orderid: int, customerid: str, employeeid: int):
        self.orderid = orderid
        self.customerid = customerid
        self.employeeid = employeeid

    def to_dict(self):
        return {
            "orderid": self.orderid,
            "customerid": self.customerid,
            "employeeid": self.employeeid
        }