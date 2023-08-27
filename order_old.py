from sqlalchemy import func

import database
from functions import SQLiteDB
import sqlite3
from datetime import datetime
from models import *


def add_to_cart(user_id: int, dish_id: str, quantity: int = 1):  # add new items to cart
    order_id = user_cart(user_id)
    database.init_db()
    ordered = database.db_session.query(OrderedDish).where(OrderedDish.order_id == order_id,
                                                           OrderedDish.dish_id == dish_id).all()
    if not ordered:
        try:
            new_item = OrderedDish(order_id=order_id,
                                   dish_id=dish_id,
                                   dish_quantity=quantity)
            database.db_session.add(new_item)
            database.db_session.commit()
        except Exception as ex:
            database.db_session.rollback()
            print("Insert Error ")
            print(ex)
    update_order(order_id)


def user_cart(user_id: int):  # return cart id or create cart and return id
    database.init_db()
    cart_id = database.db_session.query(UserOrder).where(UserOrder.order_status == 0, UserOrder.user_id == user_id).all()
    if not cart_id:
        try:
            new_cart = UserOrder(user_id=user_id, address_id=1, order_date=datetime.now())
            database.db_session.add(new_cart)
            database.db_session.commit()
        except Exception as ex:
            database.db_session.rollback()
            print("Insert Error ")
            print(ex)
    cart_object = database.db_session.query(UserOrder).where(UserOrder.id == cart_id).one()
    return cart_object
    # return (database.db_session.query(UserOrder.id)
    #         .where(UserOrder.order_status == 0, UserOrder.user_id == user_id).scalar())


def update_order(order_id: int):
    database.init_db()
    # dish_data = database.db_session.query(Dish).join(OrderedDish).where(OrderedDish.order_id == order_id).all()
    sums = database.db_session.query(func.sum(Dish.carbs).label("total_carbs"),
                                     func.sum(Dish.kcal).label("total_kcal"),
                                     func.sum(Dish.proteins).label("total_proteins"),
                                     func.sum(Dish.fats).label("total_fats"),
                                     func.sum(Dish.price).label("total_price"),
                                     ).join(OrderedDish).where(OrderedDish.order_id == order_id).one()



    with SQLiteDB("dish.db") as db:
        dish_data = db.select_from("dish", ["price", "kcal", "proteins", "fats", "carbs", "dish_quantity"],
                                   {"order_id": order_id}, "ordered_dish", ("dish_id", "id"))
        sums = {}
        for dish in dish_data:  # create dict with counted values
            quantity = dish.pop("dish_quantity")
            for key, value in dish.items():
                sums[key] = sums.get(key, 0) + value * quantity
        insert_sums = {"order_price": sums.get("price"),  # prepare dict for insert
                       "order_kcal": sums.get("kcal"),
                       "order_proteins": sums.get("proteins"),
                       "order_fats": sums.get("fats"),
                       "order_carbs": sums.get("carbs")}
        try:
            db.update_data("user_order", insert_sums, {"id": order_id})
        except sqlite3.IntegrityError:
            print("Update Error")


def post_order(user_id: int, comment: str):  # change order status to 1 if there are items in cart
    order_id = user_cart(user_id)
    with SQLiteDB("dish.db") as db:
        ordered = db.select_from("ordered_dish", ["*"], {"order_id": order_id})
        if ordered:
            db.update_data("user_order", {"order_status": 1, "comment": comment, "order_date": datetime.now()},
                           {"id": order_id})
        else:
            print("no items in cart")


def change_quantity(user_id: int, ordered_id, quantity):
    order_id = user_cart(user_id)
    if quantity == "0":
        delete_from_cart(order_id, ordered_id)
    else:
        with SQLiteDB("dish.db") as db:
            db.update_data("ordered_dish", {"dish_quantity": quantity}, {"id": ordered_id})
    update_order(order_id)


def delete_from_cart(order_id: int, ordered_id):
    with SQLiteDB("dish.db") as db:
        db.delete_from("ordered_dish", {"id": ordered_id})
    update_order(order_id)
