from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector

app = FastAPI()



def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        database="more",
        port=3306
    )

@app.get("/")
def home():
    return{"connected"}

# user
class User(BaseModel):
    id :int
    username :str
    mobile_number: int
    entry_date: str

@app.get("/user")
def view_user():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("select*from user")
    data =cursor.fetchall()
    cursor.close()
    db.close()
    return data

@app.post("/user")
def insert_user(user:User):
    db =get_db()
    cursor = db.cursor()

    sql ="insert into user (id,username,mobile_number,entry_date) values (%s,%s,%s,%s)"
    cursor.execute(sql,(user.id,user.username,user.mobile_number,user.entry_date))
    db.commit()

    cursor.close()
    db.close()
    return {"msg" : "student added"}

# unit
class Unit(BaseModel):
    id:int
    unit:str

@app.get("/unit")
def get_unit():
    db= get_db()
    cursor =db.cursor(dictionary=True)

    cursor.execute("select*from unit")
    data = cursor.fetchall()

    cursor.close()
    db.close()
    return data

@app.post("/unit")
def post_unit(unit:Unit):
    db = get_db()
    cursor = db.cursor()

    sql="insert into unit(id,unit) values (%s,%s,%s)"
    cursor.execute(sql,(unit.id,unit.unit))
    db.commit()

    cursor.close()
    db. close()
    return {'msg':'unit added'}

# product
class Product(BaseModel):
    id :int
    product_name : str
    unit_id: int
    per_price: int
    expiry_date: str

@app.post("/product")
def create_product(data: Product):

    db = get_db()
    cursor = db.cursor()

    sql = """
    insert into product
    (id,product_name, unit_id, per_price, expiry_date)values(%s,%s,%s,%s,%s)"""
    values = (
        data.id,
        data.product_name,
        data.unit_id,
        data.per_price,
        data.expiry_date
    )

    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()

    return {"message": "Product Inserted"}
@app.get("/product")
def get_product():

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("select * from product")

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return data

# order list
class OrderList(BaseModel):
    id:int
    user_id: int
    total_amount: int
    order_date: str
    order_status: str
@app.post("/order-list")
def create_order_list(data1: OrderList):

    db = get_db()
    cursor = db.cursor()
    sql = """
    insert into order_list
    (id,user_id, total_amount, order_date, order_status)values(%s,%s,%s,%s,%s)"""
    values = (
        data1.id,
        data1.user_id,
        data1.total_amount,
        data1.order_date,
        data1.order_status
    )

    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return {"message": "Order List Inserted"}

@app.get("/order-list")
def get_order_list():

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("select * from order_list")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data

# order items
class OrderItems(BaseModel):
    id:int
    order_list_id: int
    product_id: int
    qty: int
@app.post("/order-items")
def create_order_items(ot: OrderItems):

    db = get_db()
    cursor = db.cursor()

    query = """
    insert into order_items
    (id,order_list_id, product_id, qty)values(%s,%s,%s,%s)"""
    values = (
        ot.id,
        ot.order_list_id,
        ot.product_id,
        ot.qty
    )
    cursor.execute(query, values)
    db.commit()
    cursor.close()
    db.close()
    return {"message": "Order Items Inserted"}

@app.get("/order-items")
def get_order_items():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("select * from order_items")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data

@app.get("/final-orders")
def final_orders():

    db = get_db()
    cursor = db.cursor(dictionary=True)
    sql = """
    select order_list.id,user.username,user.mobile_number,product.product_name,
    order_items.qty,order_list.total_amount as total,order_list.order_date,
    order_list.order_status from order_items join order_list
    on order_items.order_list_id = order_list.id join user
    on order_list.user_id = user.id join product
    on order_items.product_id = product.id """
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data
