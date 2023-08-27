from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

import database
from database import Base


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    town = Column(String(50))
    street = Column(String(50))
    building = Column(String(10))
    apartment = Column(String(10))
    block = Column(Integer)
    floor = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship("User", back_populates="address")
    user_order = relationship("UserOrder", back_populates="address")

    def __init__(self, town=None, street=None, building=None, apartment=None, block=None, floor=None, user_id=None):
        self.town = town
        self.street = street
        self.building = building
        self.apartment = apartment
        self.block = block
        self.floor = floor
        self.user_id = user_id


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    category_name = Column(String(50), unique=True)

    dish = relationship("Dish", back_populates="category")

    def __init__(self, category_name):
        self.category_name = category_name


class Dish(Base):
    __tablename__ = "dish"
    id = Column(String(120), primary_key=True, unique=True)
    dish_name = Column(String(50), unique=True)
    price = Column(Integer)
    description = Column(String(255))
    is_available = Column(Integer)
    category_id = Column(Integer, ForeignKey("category.id"))
    photo = Column(String(120))
    kcal = Column(Integer)
    proteins = Column(Integer)
    fats = Column(Integer)
    carbs = Column(Integer)

    category = relationship("Category", back_populates="dish")
    dish_rate = relationship("DishRate", back_populates="dish")
    ordered_dish = relationship("OrderedDish", back_populates="dish")

    def __init__(self, dish_name, price, description, category_id, photo,kcal, proteins, fats, carbs):
        self.dish_name = dish_name
        self.id = dish_name.replace(" ", "_")
        self.price = price
        self.description = description
        self.category_id = category_id
        self.photo = photo
        self.kcal = kcal
        self.proteins = proteins
        self.fats = fats
        self.carbs = carbs
        self.is_available = 0


class DishRate(Base):
    __tablename__ = "dish_rate"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    dish_id = Column(String(120), ForeignKey("dish.id"))
    rate = Column(Integer)

    dish = relationship("Dish", back_populates="dish_rate")

    def __init__(self, user_id=None, dish_id=None, rate=None):
        self.user_id = user_id
        self.dish_id = dish_id
        self.rate = rate


class OrderedDish(Base):
    __tablename__ = "ordered_dish"
    id = Column(Integer, primary_key=True)
    dish_id = Column(String(120), ForeignKey("dish.id"))
    dish_quantity = Column(Integer)
    order_id = Column(Integer, ForeignKey("user_order.id"))

    dish = relationship("Dish", back_populates="ordered_dish")
    user_order = relationship("UserOrder", back_populates="ordered_dish")

    def __init__(self, dish_id=None, dish_quantity=1, order_id=None):
        self.dish_id = dish_id
        self.dish_quantity = dish_quantity
        self.order_id = order_id


class Status(Base):
    __tablename__ = "status"
    id = Column(Integer, primary_key=True)
    status_name = Column(String(50))
    user_order = relationship("UserOrder", back_populates="status")

    def __init__(self, status_name=None):
        self.status_name = status_name


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    phone = Column(Integer, unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(120))
    telegram = Column(String(120), unique=True)
    user_type = Column(Integer, ForeignKey("user_type.id"))

    address = relationship("Address", back_populates="user")
    user_order = relationship("UserOrder", back_populates="user")
    user_type_rel = relationship("UserType", back_populates="user")

    def __init__(self, name=None, phone=None, email=None, password=None, telegram=None):
        self.name = name
        self.phone = phone
        self.email = email
        self.password = password
        self.telegram = telegram
        self.user_type = 0


class UserOrder(Base):
    __tablename__ = "user_order"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    address_id = Column(Integer, ForeignKey("address.id"))
    order_price = Column(Integer)
    order_kcal = Column(Integer)
    order_proteins = Column(Integer)
    order_fats = Column(Integer)
    order_carbs = Column(Integer)
    comment = Column(String(255))
    order_date = Column(String(120))
    order_rate = Column(Integer)
    order_status = Column(Integer, ForeignKey("status.id"))

    address = relationship("Address", back_populates="user_order")
    user = relationship("User", back_populates="user_order")
    ordered_dish = relationship("OrderedDish", back_populates="user_order")
    status = relationship("Status", back_populates="user_order")

    def __init__(self, user_id=None, address_id=None, order_price=0, order_kcal=0, order_proteins=0,
                 order_fats=0, order_carbs=0, comment=None, order_date=None, order_rate=None, order_status=0):
        self.user_id = user_id
        self.address_id = address_id
        self.order_price = order_price
        self.order_kcal = order_kcal
        self.order_proteins = order_proteins
        self.order_fats = order_fats
        self.order_carbs = order_carbs
        self.comment = comment
        self.order_date = order_date
        self.order_rate = order_rate
        self.order_status = order_status

    def __repr__(self):
        return f"UserOrder(id={self.id}, user_id={self.user_id}, order_date={self.order_date}"


class UserType(Base):
    __tablename__ = "user_type"
    id = Column(Integer, primary_key=True)
    type_name = Column(String(120), unique=True)
    user = relationship("User", back_populates="user_type_rel")

    def __init__(self, type_name=None):
        self.type_name = type_name
