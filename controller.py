from psycopg2 import Error
import model
import view
import datetime


class Controller:
    def __init__(self):
        self.v = view.View()
        self.m = model.Model()

    def print(self, table_name):
        t_name = self.v.valid.check_table_name(table_name)
        if t_name:
            if t_name == 'Drink':
                self.v.print_drink(self.m.print_drink())
            elif t_name == 'Category':
                self.v.print_category(self.m.print_category())
            elif t_name == 'Drink_category':
                self.v.print_drink_category(self.m.print_drink_category())
            elif t_name == 'Order':
                self.v.print_order(self.m.print_order())

    def delete(self, table_name, value):
        t_name = self.v.valid.check_table_name(table_name)
        if t_name:
            k_val = self.v.valid.check_pk(value)
            count = 0
            if t_name == 'Drink' and k_val:
                count = self.m.find_pk_drink(k_val)
            elif t_name == 'Category' and k_val:
                count = self.m.find_pk_category(k_val)
            elif t_name == 'Drink_category' and k_val:
                count = self.m.find_pk_drink_category(k_val)
            elif t_name == 'Order' and k_val:
                count = self.m.find_pk_order(k_val)

            if count:
                if t_name == 'Drink' or t_name == 'Category':
                    count_d_c = self.m.find_fk_drink_category(k_val, t_name)
                    if count_d_c:
                        self.v.cannot_delete()
                    else:
                        try:
                            if t_name == 'Drink':
                                self.m.delete_data_drink(k_val)
                            elif t_name == 'Category':
                                self.m.delete_data_category(k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)
                elif t_name == 'Drink_category':
                    count_o = self.m.find_fk_order(k_val)
                    if count_o:
                        self.v.cannot_delete()
                    else:
                        try:
                            self.m.delete_data_drink_category(k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)
                else:
                    try:
                        self.m.delete_data_order(k_val)
                    except (Exception, Error) as _ex:
                        self.v.sql_error(_ex)
            else:
                self.v.deletion_error()


    def update_order(self, key: str, drink_category_id: str, customer_name: str):
        if self.v.valid.check_possible_keys('Order', 'id', key):
            count_o = self.m.find_pk_order(int(key))
            o_val = self.v.valid.check_pk(key)
        if self.v.valid.check_possible_keys('Drink_category', 'id', drink_category_id):
            count_d_c = self.m.find_pk_drink_category(int(drink_category_id))
            d_c_val = self.v.valid.check_pk(drink_category_id)

        if count_d_c and count_o and \
                d_c_val and o_val:
            try:
                self.m.update_data_order(o_val, d_c_val, customer_name)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_drink_category(self, key: str, drink_id: str, category_id: str):
        if self.v.valid.check_possible_keys('Drink_category', 'id', key):
            count_d_c = self.m.find_pk_drink_category(int(key))
            d_c_val = self.v.valid.check_pk(key)
        if self.v.valid.check_possible_keys('Drink', 'id', drink_id):
            count_d = self.m.find_pk_drink(int(drink_id))
            d_val = self.v.valid.check_pk(drink_id)
        if self.v.valid.check_possible_keys('Category', 'id', category_id):
            count_c = self.m.find_pk_category(int(category_id))
            c_val = self.v.valid.check_pk(category_id)

        if count_d_c and count_d and count_c and \
                d_c_val and d_val and c_val:
            try:
                self.m.update_data_drink_category(d_c_val, d_val, c_val,)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_drink(self, key: str, name: str, price: int):
        if self.v.valid.check_possible_keys('Drink', 'id', key):
            count_d = self.m.find_pk_drink(int(key))
            d_val = self.v.valid.check_pk(key)

        if count_d and d_val:
            try:
                self.m.update_data_drink(d_val, name, price)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_category(self, key: str, name: str):
        if self.v.valid.check_possible_keys('Category', 'id', key):
            count_c = self.m.find_pk_category(int(key))
            c_val = self.v.valid.check_pk(key)

        if count_c and c_val:
            try:
                self.m.update_data_category(c_val, name)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def insert_order(self, key: str, drink_category_id: str, customer_name: str):
        if self.v.valid.check_possible_keys('Order', 'id', key):
            count_o = self.m.find_pk_order(int(key))
        if self.v.valid.check_possible_keys('Drink_category', 'id', drink_category_id):
            count_d_c = self.m.find_pk_drink_category(int(drink_category_id))
            d_c_val = self.v.valid.check_pk(drink_category_id)

        if (not count_o) and count_d_c and d_c_val and self.v.valid.check_possible_keys('Order', 'id', key):
            try:
                self.m.insert_data_order(int(key), d_c_val, customer_name)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_drink_category(self, key: str, drink_id: str, category_id: str):
        if self.v.valid.check_possible_keys('Drink_category', 'id', key):
            count_d_c = self.m.find_pk_drink_category(int(key))
        if self.v.valid.check_possible_keys('Drink', 'id', drink_id):
            count_d = self.m.find_pk_drink(int(drink_id))
            d_val = self.v.valid.check_pk(drink_id)
        if self.v.valid.check_possible_keys('Category', 'id', category_id):
            count_c = self.m.find_pk_category(int(category_id))
            c_val = self.v.valid.check_pk(category_id)

        if (not count_d_c) and count_d and count_c and d_val and c_val \
                and self.v.valid.check_possible_keys('Drink_category', 'id', key):
            try:
                self.m.insert_data_drink_category(int(key), d_val, c_val)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_drink(self, key: str, name: str, price: int):
        if self.v.valid.check_possible_keys('Drink', 'id', key):
            count_d = self.m.find_pk_drink(int(key))

        if (not count_d) and self.v.valid.check_possible_keys('Drink', 'id', key):
            try:
                self.m.insert_data_drink(int(key), name, price)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_category(self, key: str, name: str):
        if self.v.valid.check_possible_keys('Category', 'id', key):
            count_c = self.m.find_pk_category(int(key))

        if (not count_c) and self.v.valid.check_possible_keys('Category', 'id', key):
            try:
                self.m.insert_data_category(int(key), name)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def generate(self, table_name: str, n: int):
        t_name = self.v.valid.check_table_name(table_name)
        if t_name:
            if t_name == 'Order':
                self.m.order_data_generator(n)
            elif t_name == 'Drink_category':
                self.m.drink_category_data_generator(n)
            elif t_name == 'Drink':
                self.m.drink_data_generator(n)
            elif t_name == 'Category':
                self.m.category_data_generator(n)

    def search_two(self):
        result = self.m.search_data_two_tables()
        self.v.print_search(result)

    def search_three(self):
        result = self.m.search_data_three_tables()
        self.v.print_search(result)

    def search_all(self):
        result = self.m.search_data_all_tables()
        self.v.print_search(result)