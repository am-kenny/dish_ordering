from functions import SQLiteDB
import sqlite3
from datetime import datetime


def add_to_cart(user_id: int, dish_id: str, quantity: int = 1):  # add new items to cart
    order_id = user_cart(user_id)
    with SQLiteDB("dish.db") as db:
        ordered = db.select_from("ordered_dish", ["*"], {"order_id": order_id, "dish_id": dish_id})
        if not ordered:
            try:
                db.insert_into("ordered_dish", {"order_id": order_id, "dish_id": dish_id, "dish_quantity": quantity})
            except sqlite3.IntegrityError:
                print("Insert Error")
    update_order(order_id)


def user_cart(user_id: int):  # return cart id or create cart and return id
    with SQLiteDB("dish.db") as db:
        cart = db.select_from("user_order", ["id"], {"order_status": "0", "user_id": user_id})
        if not cart:
            try:
                db.insert_into("user_order", {"user_id": user_id, "address_id": 1, "order_date": datetime.now()})
            except sqlite3.IntegrityError:
                print("Insert Error")
        return db.select_from("user_order", ["id"], {"order_status": "0", "user_id": user_id})[0].get("id")


def update_order(order_id: int):
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
