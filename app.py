from flask import Flask
import sqlite3

app = Flask(__name__)

# Temp
user_id = 1
admin_id = 2
# "order_status" in "user_orders" table:
# 0 - not placed (cart)
# 1 - placed
# 2 - ready for delivery
# 3 - delivered


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    con = sqlite3.connect("dish.db")
    cursor = con.cursor()
    res = cursor.execute(f"SELECT * "
                         f"FROM user_order "
                         f"WHERE user_id = {user_id} AND order_status = 0")
    results = res.fetchall()
    return results


@app.route('/cart/order', methods=['PUT'])
def cart_order():  # put application's code here
    return "cart-order"


@app.route('/cart/add', methods=['PUT'])
def cart_add():  # put application's code here
    return "cart-add"


@app.route('/user', methods=['GET', 'POST', 'DELETE'])
def user():
    con = sqlite3.connect("dish.db")
    cursor = con.cursor()
    res = cursor.execute(f"SELECT * "
                         f"FROM user "
                         f"WHERE id = {user_id}")
    results = res.fetchall()
    return results


@app.route('/user/register', methods=['POST'])
def user_register():  # put application's code here
    return "user-register"


@app.route('/user/sign_in', methods=['POST'])
def user_sign_in():  # put application's code here
    return "user-sign_in"


@app.route('/user/logout', methods=['POST'])
def user_logout():  # put application's code here
    return "user-logout"


@app.route('/user/restore', methods=['POST'])
def user_restore():  # put application's code here
    return "user-restore"


@app.route('/user/orders', methods=['GET'])
def user_orders_history():
    con = sqlite3.connect("dish.db")
    cursor = con.cursor()
    res = cursor.execute(f"SELECT * "
                         f"FROM user_order "
                         f"WHERE user_id = {user_id} AND order_status <> 0")
    results = res.fetchall()
    return results


@app.route('/user/orders/<order_id>', methods=['GET'])
def user_order(order_id: int):
    con = sqlite3.connect("dish.db")
    cursor = con.cursor()
    res = cursor.execute(f"SELECT * "
                         f"FROM user_order "
                         f"WHERE user_id = {user_id} AND id = {order_id}")
    results = res.fetchall()
    return results


@app.route('/user/address', methods=['GET', 'POST'])
def user_address_list():
    con = sqlite3.connect("dish.db")
    cursor = con.cursor()
    res = cursor.execute(f"SELECT * "
                         f"FROM address "
                         f"WHERE user_id = {user_id}")
    results = res.fetchall()
    return results


@app.route('/user/address/<address_id>', methods=['GET', 'PUT', 'DELETE'])
def user_address(address_id: int):
    con = sqlite3.connect("dish.db")
    cursor = con.cursor()
    res = cursor.execute(f"SELECT * "
                         f"FROM address "
                         f"WHERE user_id = {user_id} AND id = {address_id}")
    results = res.fetchall()
    return results


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    con = sqlite3.connect("dish.db")
    cursor = con.cursor()
    res = cursor.execute("SELECT * "
                         "FROM dish")
    results = res.fetchall()
    return results


@app.route('/menu/<category_name>', methods=['GET'])
def menu_category(category_name: str):
    con = sqlite3.connect("dish.db")
    cursor = con.cursor()
    res = cursor.execute(f"SELECT * "
                         f"FROM dish "
                         f"JOIN category c on c.id = dish.category_id "
                         f"WHERE category_name = '{category_name}'")
    results = res.fetchall()
    return results


@app.route('/menu/<category_name>/<dish_id>', methods=['GET'])
def menu_dish(category_name: str, dish_id: str):
    con = sqlite3.connect("dish.db")
    cursor = con.cursor()
    res = cursor.execute(f"SELECT * "
                         f"FROM dish "
                         f"JOIN category c on c.id = dish.category_id "
                         f"WHERE category_name = '{category_name}' AND dish.id = '{dish_id}'")
    results = res.fetchall()
    return results


@app.route('/menu/<category_name>/<dish_name>/review', methods=['POST'])
def menu_dish_review(category_name: str, dish_name: str):  # put application's code here
    return "Dish review"


@app.route('/menu/search', methods=['GET'])
def menu_search():  # put application's code here
    return "Menu search"


# Admin endpoints
@app.route('/admin', methods=['GET', 'PUT', 'DELETE'])
def admin_page():  # put application's code here
    con = sqlite3.connect("dish.db")
    cursor = con.cursor()
    res = cursor.execute(f"SELECT * "
                         f"FROM user "
                         f"WHERE id = {admin_id}")
    results = res.fetchall()
    return results


@app.route('/admin/dishes', methods=['GET', 'POST'])
def admin_dishes():  # put application's code here
    con = sqlite3.connect("dish.db")
    cursor = con.cursor()
    res = cursor.execute("SELECT * "
                         "FROM dish")
    results = res.fetchall()
    return results


@app.route('/admin/dishes/<dish_id>', methods=['GET', 'PUT', 'DELETE'])
def admin_dish(dish_id: str):  # put application's code here
    con = sqlite3.connect("dish.db")
    cursor = con.cursor()
    res = cursor.execute(f"SELECT * "
                         f"FROM dish "
                         f"WHERE dish.id = '{dish_id}'")
    results = res.fetchall()
    return results


@app.route('/admin/current_orders', methods=['GET'])
def admin_orders():  # put application's code here
    con = sqlite3.connect("dish.db")
    cursor = con.cursor()
    res = cursor.execute(f"SELECT * "
                         f"FROM user_order "
                         f"WHERE order_status = 1")
    results = res.fetchall()
    return results


@app.route('/admin/current_orders/<order_id>', methods=['GET', 'PUT'])
def admin_order(order_id: int):  # put application's code here
    con = sqlite3.connect("dish.db")
    cursor = con.cursor()
    res = cursor.execute(f"SELECT * "
                         f"FROM user_order "
                         f"WHERE order_status = 1 AND id = {order_id}")
    results = res.fetchall()
    return results


@app.route('/admin/categories', methods=['GET', 'POST'])
def admin_categories():  # put application's code here
    con = sqlite3.connect("dish.db")
    cursor = con.cursor()
    res = cursor.execute("SELECT * "
                         "FROM category")
    results = res.fetchall()
    return results


@app.route('/admin/categories/<category_name>', methods=['GET', 'POST', 'DELETE'])
def admin_category(category_name: str):  # put application's code here
    con = sqlite3.connect("dish.db")
    cursor = con.cursor()
    res = cursor.execute(f"SELECT * "
                         f"FROM dish "
                         f"JOIN category c on c.id = dish.category_id "
                         f"WHERE category_name = '{category_name}'")
    results = res.fetchall()
    return results


@app.route('/admin/search', methods=['GET'])
def admin():  # put application's code here
    return "Admin search"


if __name__ == '__main__':
    app.run()
