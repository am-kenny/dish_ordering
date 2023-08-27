from flask import Flask, request, session, render_template
import order
from models import *
import database

app = Flask(__name__)
app.secret_key = "my_secret_key"
app.static_folder = 'static'


@app.route('/cart', methods=['GET', 'POST'])  # TODO Alchemy
def cart():
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    database.init_db()
    if request.method == 'POST':  # Change quantity, 0 = delete from order
        data = request.form.to_dict()
        order.change_quantity(session.get("cart_id"), data.get("ordered_id"), data.get("quantity"))
    dishes = (database.db_session.query(OrderedDish).join(Dish)
              .where(OrderedDish.order_id == session.get("cart_id")).all())
    cart_info = database.db_session.query(UserOrder).where(UserOrder.id == session.get("cart_id")).one()
    return render_template("cart.html", cart_info=cart_info, dishes=dishes)


@app.route('/cart/order', methods=['POST'])  # TODO Alchemy
def cart_order():  # put application's code here
    if request.method == 'POST':
        comment = request.form.to_dict().get("comment")
        order.post_order(session.get("cart_id"), comment)
        session["cart_id"] = order.user_cart(session["user_id"])
    return app.redirect("/user")


@app.route('/cart/add', methods=['POST'])  # TODO Alchemy
def cart_add():
    data = request.form.to_dict()
    order.add_to_cart(session.get("cart_id"), data.get("dish_id"))
    return app.redirect("/menu")


@app.route('/user', methods=['GET', 'PUT', 'DELETE'])  # TODO PUT, DELETE
def user():  # Alchemy
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    database.init_db()
    user_info = database.db_session.query(User).where(User.id == session.get("user_id")).one()
    return render_template("user_page.html", user=user_info)


@app.route('/user/register', methods=['GET', 'POST'])
def user_register():  # Alchemy
    if session.get("user_id") is not None:
        return app.redirect("/user")
    if request.method == 'POST':
        data = request.form.to_dict()
        try:
            new_user = User(**data)
            database.db_session.add(new_user)
            database.db_session.commit()
        except Exception as ex:
            database.db_session.rollback()
            print("Insert Error ")
            print(ex)
        current_user = database.db_session.query(User).where(User.email == data["email"]).one()
        session["user_id"] = current_user.id
        session["user_name"] = current_user.name
        session["user_type"] = current_user.user_type
        session["cart_id"] = order.user_cart(session["user_id"])
        return app.redirect('/menu', 302)
    return render_template("register.html")


@app.route('/user/sign_in', methods=['GET', 'POST'])
def user_sign_in():  # Alchemy
    if session.get("user_id") is not None:
        return app.redirect("/user")
    if request.method == 'POST':
        data = request.form.to_dict()
        current_user = database.db_session.query(User).where(User.email == data["email"]).one()
        if current_user.password != data["password"]:
            return "Incorrect password"
        else:
            session["user_id"] = current_user.id
            session["user_name"] = current_user.name
            session["user_type"] = current_user.user_type
            session["cart_id"] = order.user_cart(session["user_id"])
            return app.redirect('/menu', 302)
    return render_template("sign_in.html")


@app.route('/user/logout', methods=['GET', 'POST'])
def user_logout():
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    if request.method == 'POST':
        session.pop("user_id", default=None)
        session.pop("user_name", default=None)
        session.pop("user_type", default=None)
        session.pop("cart_id", default=None)
        return render_template("sign_in.html")
    return render_template("logout.html")


@app.route('/user/restore', methods=['GET', 'POST'])
def user_restore():  # Alchemy
    if session.get("user_id") is not None:
        return app.redirect("/user")
    if request.method == 'POST':
        data = request.form.to_dict()
        database.init_db()
        try:
            current_user = database.db_session.query(User.email, User.id).where(User.email == data["email"]).one()
            if current_user:
                print(f"Link sent for id {current_user[1]}")
                return f"Link sent for {current_user[0]}"
        except Exception as ex:
            print("Insert Error ")
            print(ex)
    return render_template("restore.html")


@app.route('/user/orders', methods=['GET'])
def user_orders_history():  # Alchemy
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    database.init_db()
    orders = database.db_session.query(UserOrder).where(UserOrder.user_id == session.get("user_id"),
                                                        UserOrder.order_status == 3)
    return render_template("user_orders.html", orders=orders)


@app.route('/user/orders/<order_id>', methods=['GET'])
def user_order(order_id: int):  # Alchemy
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    database.init_db()
    this_order = database.db_session.query(UserOrder).where(UserOrder.user_id == session.get("user_id"),
                                                            UserOrder.id == order_id)[0]
    return render_template("user_order.html", order=this_order)


@app.route('/user/address', methods=['GET', 'POST'])
def user_address_list():  # Alchemy
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    database.init_db()
    if request.method == 'POST':
        data = request.form.to_dict()
        data["user_id"] = str(session["user_id"])
        try:
            address = Address(**data)
            database.db_session.add(address)
            database.db_session.commit()
        except Exception as ex:
            database.db_session.rollback()
            print("Insert Error ")
            print(ex)
    addresses = database.db_session.query(Address).where(Address.user_id == session.get("user_id"))
    return render_template("addresses.html", addresses=addresses)


@app.route('/user/address/<address_id>', methods=['GET', 'PUT', 'DELETE'])  # TODO PUT, DELETE
def user_address(address_id: int):  # Alchemy
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    database.init_db()
    address_info = database.db_session.query(Address).where(Address.user_id == session.get("user_id"),
                                                            Address.id == address_id)[0]
    return render_template("address.html", address=address_info)


@app.route('/menu', methods=['GET'])
def menu():  # Alchemy
    database.init_db()
    categories = database.db_session.query(Category).all()
    return render_template("menu.html", categories=categories)


@app.route('/menu/<category_name>', methods=['GET'])
def menu_category(category_name: str):  # Alchemy
    database.init_db()
    category = database.db_session.query(Dish).join(Category).where(Category.category_name == category_name,
                                                                    Dish.is_available == 1).all()
    if category:
        return render_template("category.html", category=category)
    else:
        return app.redirect("/menu")


@app.route('/menu/<category_name>/<dish_id>', methods=['GET'])
def menu_dish(category_name: str, dish_id: str):  # Alchemy
    database.init_db()
    dish = database.db_session.query(Dish).join(Category).where(Category.category_name == category_name,
                                                                Dish.is_available == 1,
                                                                Dish.id == dish_id).all()[0]

    return render_template("dish.html", dish=dish)


@app.route('/menu/<category_name>/<dish_id>/review', methods=['GET', 'POST'])
def menu_dish_review(category_name: str, dish_id: str):  # Alchemy
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    database.init_db()
    if request.method == 'POST':
        data = request.form.to_dict()
        data["user_id"] = str(session["user_id"])
        data["dish_id"] = dish_id
        try:
            dish_review = DishRate(**data)
            database.db_session.add(dish_review)
            database.db_session.commit()
        except Exception as ex:
            database.db_session.rollback()
            print("Insert Error ")
            print(ex)
    dish = database.db_session.query(Dish).join(Category).where(Category.category_name == category_name,
                                                                Dish.is_available == 1,
                                                                Dish.id == dish_id).all()[0]
    return render_template("review.html", dish=dish)


@app.route('/menu/search', methods=['GET'])  # TODO SEARCH
def menu_search():
    return "Menu search"


# Admin endpoints
@app.route('/admin', methods=['GET', 'PUT', 'DELETE'])  # TODO PUT DELETE
def admin_page():  # Alchemy
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    if session.get("user_type") == 0:
        return app.redirect('/menu', 302)
    database.init_db()
    admin_info = database.db_session.query(User).where(User.id == session.get("user_id")).all()[0]
    return render_template("admin.html", user=admin_info)


@app.route('/admin/dishes', methods=['GET', 'POST'])
def admin_dishes():  # Alchemy
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    if session.get("user_type") == 0:
        return app.redirect('/menu', 302)
    database.init_db()
    if request.method == 'POST':
        data = request.form.to_dict()
        try:
            dish = Dish(**data)
            database.db_session.add(dish)
            database.db_session.commit()
        except Exception as ex:
            database.db_session.rollback()
            print("Insert Error ")
            print(ex)
    dishes = database.db_session.query(Dish)
    return render_template("admin_dishes.html", dishes=dishes)


@app.route('/admin/dishes/<dish_id>', methods=['GET', 'PUT', 'DELETE'])  # TODO PUT DELETE
def admin_dish(dish_id: str):  # Alchemy
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    if session.get("user_type") == 0:
        return app.redirect('/menu', 302)
    database.init_db()
    dish = database.db_session.query(Dish).where(Dish.id == dish_id)[0]
    return render_template("admin_dish.html", dish=dish)


@app.route('/admin/current_orders', methods=['GET'])
def admin_orders():  # Alchemy
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    if session.get("user_type") == 0:
        return app.redirect('/menu', 302)
    database.init_db()
    orders = database.db_session.query(UserOrder).where(UserOrder.order_status == 1)
    return render_template("current_orders.html", orders=orders)


@app.route('/admin/current_orders/<order_id>', methods=['GET', 'PUT'])  # TODO PUT
def admin_order(order_id: int):  # Alchemy
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    if session.get("user_type") == 0:
        return app.redirect('/menu', 302)
    database.init_db()
    this_order = database.db_session.query(UserOrder).where(UserOrder.order_status == 1, UserOrder.id == order_id).all()
    if this_order:
        return render_template("current_orders_order.html", order=this_order[0])
    else:
        return app.redirect("/admin/current_orders")


@app.route('/admin/categories', methods=['GET', 'POST'])
def admin_categories():  # Alchemy
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    if session.get("user_type") == 0:
        return app.redirect('/menu', 302)
    database.init_db()
    if request.method == 'POST':
        data = request.form.to_dict()
        try:
            category = Category(**data)
            database.db_session.add(category)
            database.db_session.commit()
        except Exception as ex:
            database.db_session.rollback()
            print("Insert Error ")
            print(ex)
    categories = database.db_session.query(Category)
    return render_template("admin_categories.html", categories=categories)


@app.route('/admin/categories/<category_name>', methods=['GET', 'POST', 'DELETE'])  # TODO DELETE
def admin_category(category_name: str):  # Alchemy
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    if session.get("user_type") == 0:
        return app.redirect('/menu', 302)
    database.init_db()
    if request.method == 'POST':
        data = request.form.to_dict()
        data["category_id"] = database.db_session.query(Category.id).where(Category.category_name == category_name)
        try:
            dish = Dish(**data)
            database.db_session.add(dish)
            database.db_session.commit()
        except Exception as ex:
            database.db_session.rollback()
            print("Insert Error ")
            print(ex)
    dishes = database.db_session.query(Dish).join(Category).where(Category.category_name == category_name)
    return render_template("admin_category.html", category=dishes, category_name=category_name)


@app.route('/admin/search', methods=['GET'])  # TODO SEARCH
def admin_search():
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    if session.get("user_type") == 0:
        return app.redirect('/menu', 302)
    return "Admin search"


if __name__ == '__main__':
    app.run()
