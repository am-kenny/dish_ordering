from flask import Flask, request, session, render_template
import sqlite3
from functions import SQLiteDB

app = Flask(__name__)
app.secret_key = "my_secret_key"
app.static_folder = 'static'

# TODO TEMPLATES

# "order_status" in "user_orders" table:
# 0 - not placed (cart)
# 1 - placed
# 2 - ready for delivery
# 3 - delivered


@app.route('/cart', methods=['GET', 'POST'])  # TODO POST
def cart():
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    with SQLiteDB("dish.db") as db:
        cart_info = db.select_from("user_order", ["*"], {"user_id": session["user_id"], "order_status": "0"})
    return cart_info


@app.route('/cart/order', methods=['PUT'])  # TODO PUT
def cart_order():  # put application's code here
    return "cart-order"


@app.route('/cart/add', methods=['PUT'])  # TODO PUT
def cart_add():  # put application's code here
    return "cart-add"


@app.route('/user', methods=['GET', 'PUT', 'DELETE'])  # TODO PUT, DELETE
def user():
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    with SQLiteDB("dish.db") as db:
        user_info = db.select_from("user", ["email", "name", "phone", "telegram"], {"id": session["user_id"]})[0]
    return render_template("user_page.html", user=user_info)


@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if session.get("user_id") is not None:
        return app.redirect("/user")
    with SQLiteDB("dish.db") as db:
        if request.method == 'POST':
            data = request.form.to_dict()
            try:
                db.insert_into("user", data)
            except sqlite3.IntegrityError:
                print("Insert Error")
            current_user = \
                db.select_from("user", ["email", "password", "id", "user_type", "name"], {"email": data["email"]})[0]
            session["user_id"] = current_user["id"]
            session["user_name"] = current_user["name"]
            session["user_type"] = current_user["user_type"]
            return app.redirect('/menu', 302)
    return render_template("register.html")


@app.route('/user/sign_in', methods=['GET', 'POST'])  # TODO TRY/EXCEPT block
def user_sign_in():
    if session.get("user_id") is not None:
        return app.redirect("/user")
    with SQLiteDB("dish.db") as db:
        if request.method == 'POST':
            data = request.form.to_dict()
            current_user = \
                db.select_from("user", ["email", "password", "id", "user_type", "name"], {"email": data["email"]})[0]
            if current_user["password"] != data["password"]:
                return "Incorrect password"
            session["user_id"] = current_user["id"]
            session["user_name"] = current_user["name"]
            session["user_type"] = current_user["user_type"]
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
        return render_template("sign_in.html")
    return render_template("logout.html")


@app.route('/user/restore', methods=['GET', 'POST'])
def user_restore():
    if session.get("user_id") is not None:
        return app.redirect("/user")
    with SQLiteDB("dish.db") as db:
        if request.method == 'POST':
            data = request.form.to_dict()
            try:
                current_user = db.select_from("user", ["email", "password", "id"], {"email": data["email"]})
                if len(current_user) != 0:
                    print(f"Link sent for id {current_user[0]['id']}")
                    return "Link sent"
            except sqlite3.IntegrityError:
                print("Insert Error")
    return render_template("restore.html")


@app.route('/user/orders', methods=['GET'])
def user_orders_history():
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    with SQLiteDB("dish.db") as db:
        orders = db.select_from("user_order", ["id", "order_price", "order_kcal", "order_proteins", "order_fats",     "order_carbs", "order_date"], {"user_id": session["user_id"], "order_status": 3})
    return render_template("user_orders.html", orders=orders)


@app.route('/user/orders/<order_id>', methods=['GET'])
def user_order(order_id: int):
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    with SQLiteDB("dish.db") as db:
        order = db.select_from("user_order", ["id", "order_price", "order_kcal", "order_proteins", "order_fats",     "order_carbs", "order_date"], {"user_id": session["user_id"], "id": order_id})[0]
    return render_template("user_order.html", order=order)


@app.route('/user/address', methods=['GET', 'POST'])
def user_address_list():
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    with SQLiteDB("dish.db") as db:
        if request.method == 'POST':
            data = request.form.to_dict()
            data["user_id"] = str(session["user_id"])
            try:
                db.insert_into("address", data)
            except sqlite3.IntegrityError:
                print("Insert Error")
        addresses = db.select_from("address", ["*"], {"user_id": session["user_id"]})
    return render_template("addresses.html", addresses=addresses)


@app.route('/user/address/<address_id>', methods=['GET', 'PUT', 'DELETE'])  # TODO PUT, DELETE
def user_address(address_id: int):
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    with SQLiteDB("dish.db") as db:
        address_info = db.select_from("address", ["*"], {"user_id": session["user_id"], "id": address_id})
    return render_template("address.html", address=address_info)


@app.route('/menu', methods=['GET'])
def menu():
    with SQLiteDB("dish.db") as db:
        categories = db.select_from("category", ["*"])
        return render_template("menu.html", categories=categories)


@app.route('/menu/<category_name>', methods=['GET'])
def menu_category(category_name: str):
    with SQLiteDB("dish.db") as db:
        category = db.select_from("dish", ["dish_name", "category_name", "price", "kcal", "proteins", "fats", "carbs",
                                           "dish.id"], {"category_name": category_name, "is_available": "1"},
                                  "category", ("id", "category_id"))
    return render_template("category.html", category=category)


@app.route('/menu/<category_name>/<dish_id>', methods=['GET'])
def menu_dish(category_name: str, dish_id: str):
    with SQLiteDB("dish.db") as db:
        dish = db.select_from("dish", ["dish_name", "category_name", "price", "kcal", "proteins", "fats", "carbs",
                                       "dish.id"], {"category_name": category_name, "dish.id": dish_id}, "category",
                              ("id", "category_id"))[0]
    return render_template("dish.html", dish=dish)


@app.route('/menu/<category_name>/<dish_id>/review', methods=['GET', 'POST'])
def menu_dish_review(category_name: str, dish_id: str):
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    with SQLiteDB("dish.db") as db:
        if request.method == 'POST':
            data = request.form.to_dict()
            data["user_id"] = str(session["user_id"])
            data["dish_id"] = dish_id
            try:
                db.insert_into("dish_rate", data)
                return app.redirect("/menu")
            except sqlite3.IntegrityError:
                print("Insert Error")
        dish = db.select_from("dish", ["dish_name", "category_name", "price", "kcal", "proteins", "fats", "carbs",
                                       "dish.id"], {"category_name": category_name, "dish.id": dish_id}, "category",
                              ("id", "category_id"))[0]
    return render_template("review.html", dish=dish)


@app.route('/menu/search', methods=['GET'])  # TODO SEARCH
def menu_search():
    return "Menu search"


# Admin endpoints
@app.route('/admin', methods=['GET', 'PUT', 'DELETE'])  # TODO PUT DELETE
def admin_page():
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    if session.get("user_type") == 0:
        return app.redirect('/menu', 302)
    with SQLiteDB("dish.db") as db:
        admin_info = db.select_from("user", ["*"], {"id": session["user_id"]})[0]
    return render_template("admin.html", user=admin_info)


@app.route('/admin/dishes', methods=['GET', 'POST'])
def admin_dishes():
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    if session.get("user_type") == 0:
        return app.redirect('/menu', 302)
    with SQLiteDB("dish.db") as db:
        if request.method == 'POST':
            data = request.form.to_dict()
            data["id"] = "_".join(data["dish_name"].lower().split(" "))
            try:
                db.insert_into("dish", data)
            except sqlite3.IntegrityError:
                print("Insert Error")
        dishes = db.select_from("dish", ["*"])
    return render_template("admin_dishes.html", dishes=dishes)


@app.route('/admin/dishes/<dish_id>', methods=['GET', 'PUT', 'DELETE'])  # TODO PUT DELETE
def admin_dish(dish_id: str):
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    if session.get("user_type") == 0:
        return app.redirect('/menu', 302)
    with SQLiteDB("dish.db") as db:
        dish = db.select_from("dish", ["*"], {"id": dish_id})[0]
    return render_template("admin_dish.html", dish=dish)


@app.route('/admin/current_orders', methods=['GET'])
def admin_orders():
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    if session.get("user_type") == 0:
        return app.redirect('/menu', 302)
    with SQLiteDB("dish.db") as db:
        orders = db.select_from("user_order", ["*"], {"order_status": "1"})
    return render_template("current_orders.html", orders=orders)


@app.route('/admin/current_orders/<order_id>', methods=['GET', 'PUT'])  # TODO PUT
def admin_order(order_id: int):
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    if session.get("user_type") == 0:
        return app.redirect('/menu', 302)
    with SQLiteDB("dish.db") as db:
        order = db.select_from("user_order", ["*"], {"order_status": "1", "id": order_id})[0]
    return render_template("current_orders_order.html", order=order)


@app.route('/admin/categories', methods=['GET', 'POST'])
def admin_categories():
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    if session.get("user_type") == 0:
        return app.redirect('/menu', 302)
    with SQLiteDB("dish.db") as db:
        if request.method == 'POST':
            data = request.form.to_dict()
            try:
                db.insert_into("category", data)
            except sqlite3.IntegrityError:
                print("Insert Error")
        categories = db.select_from("category", ["*"])

    return render_template("admin_categories.html", categories=categories)


@app.route('/admin/categories/<category_name>', methods=['GET', 'POST', 'DELETE'])  # TODO DELETE
def admin_category(category_name: str):
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    if session.get("user_type") == 0:
        return app.redirect('/menu', 302)
    with SQLiteDB("dish.db") as db:
        if request.method == 'POST':
            data = request.form.to_dict()
            data["id"] = "_".join(data["dish_name"].lower().split(" "))
            data["category_id"] = db.select_from("category", ["id"], {"category_name": category_name})[0]["id"]
            try:
                db.insert_into("dish", data)
            except sqlite3.IntegrityError:
                print("Insert Error")
        category = db.select_from("dish",
                                  ["dish_name", "category_name", "price", "kcal", "proteins", "fats", "carbs",
                                   "dish.id"], {"category_name": category_name, "is_available": "1"},
                                  "category", ("id", "category_id"))
    return render_template("admin_category.html", category=category)


@app.route('/admin/search', methods=['GET'])  # TODO SEARCH
def admin_search():
    if session.get("user_id") is None:
        return app.redirect("/user/sign_in")
    if session.get("user_type") == 0:
        return app.redirect('/menu', 302)
    return "Admin search"


if __name__ == '__main__':
    app.run()
