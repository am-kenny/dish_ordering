from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

import database
from database import Base


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    town = Column(String(50), nullable=False)
    street = Column(String(50), nullable=False)
    building = Column(String(10), nullable=False)
    apartment = Column(String(10))
    block = Column(Integer)
    floor = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

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
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    category_name = Column(String(50), unique=True, nullable=False)

    dish = relationship("Dish", back_populates="category")

    def __init__(self, category_name):
        self.category_name = category_name


class Dish(Base):
    __tablename__ = "dish"
    id = Column(String(120), primary_key=True, unique=True)
    dish_name = Column(String(50), unique=True, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String(255), nullable=False)
    is_available = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    photo = Column(String(120), nullable=False)
    kcal = Column(Integer, nullable=False)
    proteins = Column(Integer, nullable=False)
    fats = Column(Integer, nullable=False)
    carbs = Column(Integer, nullable=False)

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
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    dish_id = Column(String(120), ForeignKey("dish.id"), nullable=False)
    rate = Column(Integer, nullable=False)

    dish = relationship("Dish", back_populates="dish_rate")

    def __init__(self, user_id=None, dish_id=None, rate=None):
        self.user_id = user_id
        self.dish_id = dish_id
        self.rate = rate


class OrderedDish(Base):
    __tablename__ = "ordered_dish"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    dish_id = Column(String(120), ForeignKey("dish.id"), nullable=False)
    dish_quantity = Column(Integer, nullable=False)
    order_id = Column(Integer, ForeignKey("user_order.id"), nullable=False)

    dish = relationship("Dish", back_populates="ordered_dish")
    user_order = relationship("UserOrder", back_populates="ordered_dish")

    def __init__(self, dish_id=None, dish_quantity=1, order_id=None):
        self.dish_id = dish_id
        self.dish_quantity = dish_quantity
        self.order_id = order_id


class Status(Base):
    __tablename__ = "status"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    status_name = Column(String(50), nullable=False)

    user_order = relationship("UserOrder", back_populates="status")

    def __init__(self, status_name=None):
        self.status_name = status_name


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(50), nullable=False)
    phone = Column(Integer, unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)
    telegram = Column(String(120), unique=True)
    user_type = Column(Integer, ForeignKey("user_type.id"), nullable=False)
    is_verified = Column(Boolean, default=False)

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
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    address_id = Column(Integer, ForeignKey("address.id"), nullable=False)
    order_price = Column(Integer, nullable=False)
    order_kcal = Column(Integer, nullable=False)
    order_proteins = Column(Integer, nullable=False)
    order_fats = Column(Integer, nullable=False)
    order_carbs = Column(Integer, nullable=False)
    comment = Column(String(255))
    order_date = Column(String(120))
    order_rate = Column(Integer)
    order_status = Column(Integer, ForeignKey("status.id"), nullable=False)
    update_date = Column(DateTime)

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
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    type_name = Column(String(120), unique=True, nullable=False)

    user = relationship("User", back_populates="user_type_rel")

    def __init__(self, type_name=None):
        self.type_name = type_name


class EmailVerification(Base):
    __tablename__ = "email_verification"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    code = Column(String, unique=True, nullable=False)
    expire_at = Column(DateTime, nullable=False)

    def __init__(self, user_id=None, code=None, expire_at=None):
        self.user_id = user_id
        self.code = code
        self.expire_at = expire_at
