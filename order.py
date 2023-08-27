from sqlalchemy import func
import database
from datetime import datetime
from models import *


def add_to_cart(cart_id: int, dish_id: str, quantity: int = 1):  # add new items to cart
    database.init_db()
    ordered = database.db_session.query(OrderedDish).where(OrderedDish.order_id == cart_id,
                                                           OrderedDish.dish_id == dish_id).all()
    if not ordered:
        try:
            new_item = OrderedDish(order_id=cart_id,
                                   dish_id=dish_id,
                                   dish_quantity=quantity)
            database.db_session.add(new_item)
            database.db_session.commit()
        except Exception as ex:
            database.db_session.rollback()
            print("Insert Error ")
            print(ex)
    update_order(cart_id)


def user_cart(user_id: int):  # return cart id or create cart and return id
    database.init_db()
    has_cart = (database.db_session.query(UserOrder)
                .where(UserOrder.order_status == 0, UserOrder.user_id == user_id).all())
    if not has_cart:
        try:
            new_cart = UserOrder(user_id=user_id, address_id=1, order_date=datetime.now())
            database.db_session.add(new_cart)
            database.db_session.commit()
        except Exception as ex:
            database.db_session.rollback()
            print("Insert Error ")
            print(ex)
    cart_id = (database.db_session.query(UserOrder.id)
               .where(UserOrder.order_status == 0, UserOrder.user_id == user_id).scalar())
    return cart_id


def update_order(cart_id: int):
    database.init_db()
    cart = database.db_session.query(UserOrder).where(UserOrder.id == cart_id).one()
    sums = database.db_session.query(func.sum(Dish.carbs * OrderedDish.dish_quantity).label("total_carbs"),
                                     func.sum(Dish.kcal * OrderedDish.dish_quantity).label("total_kcal"),
                                     func.sum(Dish.proteins * OrderedDish.dish_quantity).label("total_proteins"),
                                     func.sum(Dish.fats * OrderedDish.dish_quantity).label("total_fats"),
                                     func.sum(Dish.price * OrderedDish.dish_quantity).label("total_price"),
                                     ).join(OrderedDish).filter(OrderedDish.order_id == cart.id).one()
    cart.order_carbs = sums.total_carbs
    cart.order_kcal = sums.total_kcal
    cart.order_proteins = sums.total_proteins
    cart.order_fats = sums.total_fats
    cart.order_price = sums.total_price
    database.db_session.commit()


def post_order(cart_id: int, comment: str = None):  # change order status to 1 if there are items in cart
    database.init_db()
    cart = database.db_session.query(UserOrder).where(UserOrder.id == cart_id).one()
    ordered = database.db_session.query(OrderedDish).where(OrderedDish.order_id == cart.id).all()
    if ordered:
        cart.order_status = 1
        cart.comment = comment
        database.db_session.commit()
    else:
        print("no items in cart")


def change_quantity(cart_id: int, ordered_id, quantity):
    cart = database.db_session.query(UserOrder).where(UserOrder.id == cart_id).one()
    database.init_db()
    ordered_dish = database.db_session.query(OrderedDish).where(OrderedDish.id == ordered_id).one()
    if quantity == "0":
        delete_from_cart(cart_id, ordered_dish)
    else:
        ordered_dish.dish_quantity = quantity
        database.db_session.commit()
        update_order(cart_id)


def delete_from_cart(cart_id: int, ordered_dish: OrderedDish):
    database.init_db()
    database.db_session.delete(ordered_dish)
    database.db_session.commit()
    update_order(cart_id)
