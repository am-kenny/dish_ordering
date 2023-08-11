from flask import Flask, request
import sqlite3
from functions import SQLiteDB

app = Flask(__name__)

# Temp
user_id = None

# "order_status" in "user_orders" table:
# 0 - not placed (cart)
# 1 - placed
# 2 - ready for delivery
# 3 - delivered


@app.route('/cart', methods=['GET', 'POST'])  # TODO POST
def cart():
    if user_id is None:
        return app.redirect("/user/sign_in")
    with SQLiteDB("dish.db") as db:
        cart_info = db.select_from("user_order", ["*"], {"user_id": user_id, "order_status": "0"})
    return cart_info


@app.route('/cart/order', methods=['PUT'])  # TODO PUT
def cart_order():  # put application's code here
    return "cart-order"


@app.route('/cart/add', methods=['PUT'])  # TODO PUT
def cart_add():  # put application's code here
    return "cart-add"


@app.route('/user', methods=['GET', 'PUT', 'DELETE'])  # TODO PUT, DELETE
def user():
    if user_id is None:
        return app.redirect("/user/sign_in")
    with SQLiteDB("dish.db") as db:
        user_info = db.select_from("user", ["*"], {"id": user_id})
    return user_info


@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    with SQLiteDB("dish.db") as db:
        if request.method == 'POST':
            data = request.form.to_dict()
            try:
                db.insert_into("user", data)
                global user_id
                user_id = db.select_from("user", ["id"], data)[0]["id"]
            except sqlite3.IntegrityError:
                print("Insert Error")
    html_form = f"""
    <form method = "POST">
        <input type="text" name="name" placeholder="Name">
        <input type="text" name="phone" placeholder="Phone">
        <input type="text" name="email" placeholder="E-Mail">
        <input type="text" name="password" placeholder="Password">
        <input type="text" name="telegram" placeholder="Telegram">
        <input type = submit>
    </form>
    """
    return html_form


@app.route('/user/sign_in', methods=['GET', 'POST'])
def user_sign_in():
    with SQLiteDB("dish.db") as db:
        if request.method == 'POST':
            data = request.form.to_dict()
            try:
                current_user = db.select_from("user", ["email", "password", "id"], {"email": data["email"]})
                if current_user[0]["password"] != data["password"]:
                    return "Incorrect password"
                global user_id
                user_id = current_user[0]["id"]
                return "Success"
            except sqlite3.IntegrityError:
                print("Insert Error")
    html_form = f"""
    <form method = "POST">
        <input type="text" name="email" placeholder="E-Mail">
        <input type="text" name="password" placeholder="Password">
        <input type = submit>
    </form>
    """
    return html_form


@app.route('/user/logout', methods=['GET', 'POST'])
def user_logout():
    global user_id
    if user_id is None:
        return app.redirect("/user/sign_in")
    if request.method == 'POST':
        user_id = None
        return "You have logged out"
    html_form = f"""
    Do you want to log out?
    <form method = "POST">
        <input type = submit>
    </form>
    """
    return html_form


@app.route('/user/restore', methods=['GET', 'POST'])
def user_restore():  # put application's code here
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
    html_form = f"""
    <form method = "POST">
        Enter email to get link
        <input type="text" name="email" placeholder="E-Mail">
        <input type = submit>
    </form>
    """
    return html_form


@app.route('/user/orders', methods=['GET'])
def user_orders_history():
    if user_id is None:
        return app.redirect("/user/sign_in")
    with SQLiteDB("dish.db") as db:
        orders = db.select_from("user_order", ["*"], {"user_id": user_id, "order_status": 3})
    return " <br> ".join([str(i) for i in orders])


@app.route('/user/orders/<order_id>', methods=['GET'])
def user_order(order_id: int):
    if user_id is None:
        return app.redirect("/user/sign_in")
    with SQLiteDB("dish.db") as db:
        order = db.select_from("user_order", ["*"], {"user_id": user_id, "id": order_id})
    return order


@app.route('/user/address', methods=['GET', 'POST'])
def user_address_list():
    if user_id is None:
        return app.redirect("/user/sign_in")
    with SQLiteDB("dish.db") as db:
        if request.method == 'POST':
            data = request.form.to_dict()
            data["user_id"] = str(user_id)
            try:
                db.insert_into("address", data)
            except sqlite3.IntegrityError:
                print("Insert Error")
        addresses = db.select_from("address", ["*"], {"user_id": user_id})
    html_form = f"""
    <form method = "POST">
        <input type="text" name="town" placeholder="Town">
        <input type="text" name="street" placeholder="Street">
        <input type="text" name="building" placeholder="Building">
        <input type="text" name="apartment" placeholder="Apartment">
        <input type="text" name="block" placeholder="Block">
        <input type="text" name="floor" placeholder="Floor">
        <input type = submit>
    </form>
    <br> 
    {" <br> ".join([str(i) for i in addresses])}
    """
    return html_form


@app.route('/user/address/<address_id>', methods=['GET', 'PUT', 'DELETE'])  # TODO PUT, DELETE
def user_address(address_id: int):
    if user_id is None:
        return app.redirect("/user/sign_in")
    with SQLiteDB("dish.db") as db:
        address_info = db.select_from("address", ["*"], {"user_id": user_id, "id": address_id})
    return address_info


@app.route('/menu', methods=['GET'])
def menu():
    with SQLiteDB("dish.db") as db:
        data = db.select_from("dish", ["*"])
        return data


@app.route('/menu/<category_name>', methods=['GET'])
def menu_category(category_name: str):
    with SQLiteDB("dish.db") as db:
        category = db.select_from("dish", ["*"], {"category_name": category_name}, "category", ("id", "category_id"))
    return category


@app.route('/menu/<category_name>/<dish_id>', methods=['GET'])
def menu_dish(category_name: str, dish_id: str):
    with SQLiteDB("dish.db") as db:
        dish = db.select_from("dish", ["*"], {"category_name": category_name, "dish.id": dish_id}, "category", ("id", "category_id"))
    return dish


@app.route('/menu/<category_name>/<dish_id>/review', methods=['GET', 'POST'])
def menu_dish_review(category_name: str, dish_id: str):
    if user_id is None:
        return app.redirect("/user/sign_in")
    with SQLiteDB("dish.db") as db:
        if request.method == 'POST':
            data = request.form.to_dict()
            data["user_id"] = str(user_id)
            data["dish_id"] = dish_id
            try:
                db.insert_into("dish_rate", data)
                return "Success"
            except sqlite3.IntegrityError:
                print("Insert Error")
        dish = db.select_from("dish", ["*"], {"category_name": category_name, "dish.id": dish_id}, "category", ("id", "category_id"))
    html_form = f"""
        <form method = "POST">
            Please, rate this dish
            <input type="text" name="rate" placeholder="Rate">
            <input type = submit>
        </form>
        <br> 
        {dish}
        """
    return html_form


@app.route('/menu/search', methods=['GET'])  # TODO SEARCH
def menu_search():
    return "Menu search"


# Admin endpoints
@app.route('/admin', methods=['GET', 'PUT', 'DELETE'])  # TODO PUT DELETE
def admin_page():
    if user_id is None:
        return app.redirect("/user/sign_in")
    with SQLiteDB("dish.db") as db:
        admin_info = db.select_from("user", ["*"], {"id": user_id})
        print(admin_info)
        if admin_info[0]["user_type"] != 1:
            return app.redirect('/menu', 302)
    return admin_info


@app.route('/admin/dishes', methods=['GET', 'POST'])
def admin_dishes():
    if user_id is None:
        return app.redirect("/user/sign_in")
    with SQLiteDB("dish.db") as db:
        admin_info = db.select_from("user", ["*"], {"id": user_id})
        if admin_info[0]["user_type"] != 1:
            return app.redirect('/menu', 302)
        if request.method == 'POST':
            data = request.form.to_dict()
            data["id"] = "_".join(data["dish_name"].lower().split(" "))
            try:
                db.insert_into("dish", data)
            except sqlite3.IntegrityError:
                print("Insert Error")
        dishes = db.select_from("dish", ["*"])
    html_form = f"""
    <form method = "POST">
        <input type="text" name="dish_name" placeholder="Dish name">
        <input type="text" name="price" placeholder="Price">
        <input type="text" name="description" placeholder="Description">
        <input type="text" name="category_id" placeholder="Category id">
        <input type="text" name="photo" placeholder="Photo">
        <input type="text" name="ccal" placeholder="Ccal">
        <input type="text" name="proteins" placeholder="Proteins">
        <input type="text" name="fats" placeholder="Fats">
        <input type="text" name="carbs" placeholder="Carbs">
        <input type = submit>
    </form>
    <br> 
    {" <br> ".join([str(i) for i in dishes])}
    """
    return html_form


@app.route('/admin/dishes/<dish_id>', methods=['GET', 'PUT', 'DELETE'])  # TODO PUT DELETE
def admin_dish(dish_id: str):
    if user_id is None:
        return app.redirect("/user/sign_in")
    with SQLiteDB("dish.db") as db:
        admin_info = db.select_from("user", ["*"], {"id": user_id})
        if admin_info[0]["user_type"] != 1:
            return app.redirect('/menu', 302)
        dish = db.select_from("dish", ["*"], {"id": dish_id})
    return dish


@app.route('/admin/current_orders', methods=['GET'])
def admin_orders():
    if user_id is None:
        return app.redirect("/user/sign_in")
    with SQLiteDB("dish.db") as db:
        admin_info = db.select_from("user", ["*"], {"id": user_id})
        if admin_info[0]["user_type"] != 1:
            return app.redirect('/menu', 302)
        orders = db.select_from("user_order", ["*"], {"order_status": "1"})
    return orders


@app.route('/admin/current_orders/<order_id>', methods=['GET', 'PUT'])  # TODO PUT
def admin_order(order_id: int):
    if user_id is None:
        return app.redirect("/user/sign_in")
    with SQLiteDB("dish.db") as db:
        admin_info = db.select_from("user", ["*"], {"id": user_id})
        if admin_info[0]["user_type"] != 1:
            return app.redirect('/menu', 302)
        order = db.select_from("user_order", ["*"], {"order_status": "1", "id": order_id})
    return order


@app.route('/admin/categories', methods=['GET', 'POST'])
def admin_categories():
    if user_id is None:
        return app.redirect("/user/sign_in")
    with SQLiteDB("dish.db") as db:
        admin_info = db.select_from("user", ["*"], {"id": user_id})
        if admin_info[0]["user_type"] != 1:
            return app.redirect('/menu', 302)
        if request.method == 'POST':
            data = request.form.to_dict()
            try:
                db.insert_into("category", data)
            except sqlite3.IntegrityError:
                print("Insert Error")
        categories = db.select_from("category", ["*"])
    html_form = f"""
    <form method = "POST">
        <input type="text" name="category_name" placeholder="Category name">
        <input type = submit>
    </form>
    <br> 
    {" <br> ".join([str(i) for i in categories])}
    """
    return html_form


@app.route('/admin/categories/<category_name>', methods=['GET', 'POST', 'DELETE'])  # TODO DELETE
def admin_category(category_name: str):
    if user_id is None:
        return app.redirect("/user/sign_in")
    with SQLiteDB("dish.db") as db:
        admin_info = db.select_from("user", ["*"], {"id": user_id})
        if admin_info[0]["user_type"] != 1:
            return app.redirect('/menu', 302)
        if request.method == 'POST':
            data = request.form.to_dict()
            data["id"] = "_".join(data["dish_name"].lower().split(" "))
            data["category_id"] = db.select_from("category", ["id"], {"category_name": category_name})[0]["id"]
            try:
                db.insert_into("dish", data)
            except sqlite3.IntegrityError:
                print("Insert Error")
        category_dishes = db.select_from("dish", ["*"], {"category_name": category_name}, "category",
                                         ("id", "category_id"))
    html_form = f"""
    <form method = "POST">
        <input type="text" name="dish_name" placeholder="Dish name">
        <input type="text" name="price" placeholder="Price">
        <input type="text" name="description" placeholder="Description">
        <input type="text" name="photo" placeholder="Photo">
        <input type="text" name="ccal" placeholder="Ccal">
        <input type="text" name="proteins" placeholder="Proteins">
        <input type="text" name="fats" placeholder="Fats">
        <input type="text" name="carbs" placeholder="Carbs">
        <input type = submit>
    </form>
    <br> 
    {" <br> ".join([str(i) for i in category_dishes])}
    """
    return html_form


@app.route('/admin/search', methods=['GET'])  # TODO SEARCH
def admin():  # put application's code here
    return "Admin search"


if __name__ == '__main__':
    app.run()
