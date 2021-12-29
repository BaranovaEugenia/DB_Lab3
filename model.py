import datetime
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, select, and_
from sqlalchemy.orm import relationship
from db import Orders, Session, engine


def recreate_database():
    Orders.metadata.drop_all(engine)
    Orders.metadata.create_all(engine)


class Category(Orders):
    __tablename__ = 'Category'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, key, name):
        self.id = key
        self.name = name

    def __repr__(self):
        return "{:>10}{:>15}" \
            .format(self.id, self.name)


class Drink(Orders):
    __tablename__ = 'Drink'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

    def __init__(self, key, name, price):
        self.id = key
        self.name = name
        self.price = price

    def __repr__(self):
        return "{:>10}{:>15}{:>10}" \
            .format(self.id, self.name, self.price)


class Drink_category(Orders):
    __tablename__ = 'Drink_category'
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('Category.id'))
    drink_id = Column(Integer, ForeignKey('Drink.id'))
    categories = relationship("Category")
    drinks = relationship("Drink")

    def __init__(self, key, category_id, drink_id):
        self.id = key
        self.category_id = category_id
        self.drink_id = drink_id

    def __repr__(self):
        return "{:>10}{:>10}{:>10}" \
            .format(self.id, self.category_id, self.drink_id)


class Order(Orders):
    __tablename__ = 'Order'
    id = Column(Integer, primary_key=True)
    drink_category_id = Column(Integer, ForeignKey('Drink_category.id'))
    customer_name = Column(String)
    drink_categories = relationship("Drink_category")

    def __init__(self, key, drink_category_id, customer_name):
        self.id = key
        self.drink_category_id = drink_category_id
        self.customer_name = customer_name

    def __repr__(self):
        return "{:>10}{:>10}{:>15}" \
            .format(self.id, self.drink_category_id, self.customer_name)

class Model:
    def __init__(self):
        self.session = Session()
        self.connection = engine.connect()

    def find_pk_drink_category(self, key_value: int):
        return self.session.query(Drink_category).filter_by(id=key_value).first()

    def find_fk_drink_category(self, key_value: int, table_name: str):
        if table_name == "Drink":
            return self.session.query(Drink_category).filter_by(drink_id=key_value).first()
        elif table_name == "Category":
            return self.session.query(Drink_category).filter_by(category_id=key_value).first()

    def find_pk_order(self, key_value: int):
        return self.session.query(Order).filter_by(id=key_value).first()

    def find_fk_order(self, key_value: int):
        return self.session.query(Order).filter_by(drink_category_id=key_value).first()

    def find_pk_drink(self, key_value: int):
        return self.session.query(Drink).filter_by(id=key_value).first()

    def find_pk_category(self, key_value: int):
        return self.session.query(Category).filter_by(id=key_value).first()

    def print_drink_category(self):
        return self.session.query(Drink_category).order_by(Drink_category.id.asc()).all()

    def print_order(self):
        return self.session.query(Order).order_by(Order.id.asc()).all()

    def print_drink(self):
        return self.session.query(Drink).order_by(Drink.id.asc()).all()

    def print_category(self):
        return self.session.query(Category).order_by(Category.id.asc()).all()

    def delete_data_drink_category(self, key) -> None:
        self.session.query(Drink_category).filter_by(id=key).delete()
        self.session.commit()

    def delete_data_order(self, key) -> None:
        self.session.query(Order).filter_by(id=key).delete()
        self.session.commit()

    def delete_data_drink(self, key) -> None:
        self.session.query(Drink).filter_by(id=key).delete()
        self.session.commit()

    def delete_data_category(self, key) -> None:
        self.session.query(Category).filter_by(id=key).delete()
        self.session.commit()

    def update_data_drink_category(self, key: int, drink_id: int, category_id: int) -> None:
        self.session.query(Drink_category).filter_by(id=key) \
            .update({Drink_category.drink_id: drink_id, Drink_category.category_id: category_id})
        self.session.commit()

    def update_data_order(self, key: int, drink_category_id: str, customer_name: str) -> None:
        self.session.query(Order).filter_by(id=key) \
            .update({Order.drink_category_id: drink_category_id, Order.customer_name: customer_name})
        self.session.commit()

    def update_data_drink(self, key: int, name: str, price: int) -> None:
        self.session.query(Drink).filter_by(id=key) \
            .update({Drink.name: name, Drink.price: price})
        self.session.commit()

    def update_data_category(self, key: int, name: str) -> None:
        self.session.query(Category).filter_by(id=key) \
            .update({Category.name: name})
        self.session.commit()

    def insert_data_drink_category(self, key: int, drink_id: int, category_id: int) -> None:
        drink_category = Drink_category(key=key, drink_id=drink_id, category_id=category_id)
        self.session.add(drink_category)
        self.session.commit()

    def insert_data_order(self, key: int, drink_category_id: str, customer_name: str) -> None:
        order = Order(key=key, drink_category_id=drink_category_id, customer_name=customer_name)
        self.session.add(order)
        self.session.commit()

    def insert_data_drink(self, key: int, name: str, price: int) -> None:
        drink = Drink(key=key, name=name, price=price)
        self.session.add(drink)
        self.session.commit()

    def insert_data_category(self, key: int, name: str) -> None:
        category = Category(key=key, name=name)
        self.session.add(category)
        self.session.commit()

    def drink_category_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute("insert into public.\"Drink_category\" "
                         "select (SELECT (MAX(id)+1) FROM public.\"Drink_category\"), "
                         "(SELECT id FROM public.\"Drink\" LIMIT 1 OFFSET "
                         "(round(random() *((SELECT COUNT(id) FROM public.\"Drink\")-1)))), "
                         "(SELECT id FROM public.\"Category\" LIMIT 1 OFFSET "
                         "(round(random() *((SELECT COUNT(id) FROM public.\"Category\")-1))));")

    def order_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute("insert into public.\"Order\" select (SELECT MAX(id)+1 FROM public.\"Order\"), "
                         "(SELECT id FROM public.\"Drink_category\" LIMIT 1 OFFSET "
                         "(round(random() *((SELECT COUNT(id) FROM public.\"Drink_category\")-1)))), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(15-5)+5):: integer)), '');")

    def drink_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute(
                "insert into public.\"Drink\""
                         "select (SELECT MAX(id)+1 FROM public.\"Drink\"), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) \
                         FROM generate_series(1, FLOOR(RANDOM()*(10-4)+4):: integer)), ''), "
                         "FLOOR(RANDOM()*(100000-1)+1);")

    def category_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute("insert into public.\"Category\""
                         "select (SELECT MAX(id)+1 FROM public.\"Category\"), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) \
                         FROM generate_series(1, FLOOR(RANDOM()*(10-4)+4):: integer)), '');")

    def search_data_two_tables(self):
        return self.session.query(Drink) \
            .select_from(Drink_category) \
            .filter(and_(
            Drink.price <= 20,
            Drink_category.id <= 4,
            Drink_category.category_id <= 3,
            )) \
            .all()

    def search_data_three_tables(self):
        return self.session.query(Drink) \
            .select_from(Drink_category, Order) \
            .filter(and_(
            Drink.price <= 25,
            Drink_category.id <= 3,
            Order.drink_category_id <= 9,
        )) \
            .all()

    def search_data_all_tables(self):
        return self.session.query(Drink) \
            .select_from(Category, Drink_category, Order) \
            .filter(and_(
            Drink.price == 30,
            Category.name.ilike('With_sugar_Hot'),
            Drink_category.category_id <= 10,
            Order.id <= 5,
        )) \
            .all()