from flask import Flask

app = Flask(__name__)


@app.route('/cart', methods=['GET', 'PUT'])
def cart():  # put application's code here
    return


@app.route('/cart/order', methods=['POST'])
def cart_order():  # put application's code here
    return


@app.route('/cart/add', methods=['POST'])
def cart_add():  # put application's code here
    return


@app.route('/user', methods=['GET', 'POST', 'DELETE'])
def user():  # put application's code here
    return


@app.route('/user/register', methods=['POST'])
def user_register():  # put application's code here
    return


@app.route('/user/sign_in', methods=['POST'])
def user_sign_in():  # put application's code here
    return


@app.route('/user/logout', methods=['POST'])
def user_logout():  # put application's code here
    return


@app.route('/user/restore', methods=['POST'])
def user_restore():  # put application's code here
    return


@app.route('/user/orders', methods=['GET'])
def user_orders_history():  # put application's code here
    return


@app.route('/user/orders/<order_id>', methods=['GET'])
def user_order(order_id: int):  # put application's code here
    return


@app.route('/user/address', methods=['GET', 'POST'])
def user_address_list():  # put application's code here
    return


@app.route('/user/address/<address_id>', methods=['GET', 'PUT', 'DELETE'])
def user_address(address_id: int):  # put application's code here
    return


@app.route('/menu', methods=['GET'])
def menu():  # put application's code here
    return


@app.route('/menu/<category_name>', methods=['GET'])
def menu_category(category_name: str):  # put application's code here
    return


@app.route('/menu/<category_name>/<dish_name>', methods=['GET'])
def menu_dish(category_name: str, dish_name: str):  # put application's code here
    return


@app.route('/menu/<category_name>/<dish_name>/review', methods=['POST'])
def menu_dish_review(category_name: str, dish_name: str):  # put application's code here
    return


@app.route('/menu/search', methods=['GET'])
def menu_search():  # put application's code here
    return


if __name__ == '__main__':
    app.run()
