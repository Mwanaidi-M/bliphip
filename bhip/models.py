import bcrypt
import secrets

from bhip import my_db,my_login
from flask_login import UserMixin


# PRODUCT UNIQUE CODE GENERATOR
def generate_code():
    return secrets.token_hex(6)


# PRODUCTS TABLE
class Products(my_db.Model):
    product_id = my_db.Column(my_db.Integer, primary_key=True)
    product_name = my_db.Column(my_db.String(length=40), unique=True, nullable=False)
    product_desc = my_db.Column(my_db.Text, nullable=False)
    product_code = my_db.Column(my_db.String(length=12), unique=True, nullable=False, default=generate_code)
    product_price = my_db.Column(my_db.Integer, nullable=False)
    product_owner_id = my_db.Column(my_db.Integer, my_db.ForeignKey('users.user_id'))

    # PRODUCTS CONSTRUCTOR
    def __init__(self, p_name, p_desc, p_price):
        self.product_name = p_name
        self.product_desc = p_desc
        self.product_price = p_price

    # NEAT WAY DISPLAY PRODUCTS INSTANCE OBJECTS
    def __repr__(self):
        return f'Product:{self.product_name}'

    # METHOD FOR PURCHASING A PRODUCT
    def purchase_product(self, customer):
        self.product_owner_id = customer.user_id
        customer.user_budget -= self.product_price
        my_db.session.commit()

    # METHOD TO PUT PRODUCT BACK ON MARKET
    def remove_product(self, customer):
        self.product_owner_id = None
        customer.user_budget += self.product_price
        my_db.session.commit()


class Users(UserMixin, my_db.Model):
    user_id = my_db.Column(my_db.Integer, primary_key=True)
    user_fname = my_db.Column(my_db.String(length=30), nullable=False)
    user_lname = my_db.Column(my_db.String(length=30), nullable=False)
    user_email = my_db.Column(my_db.String(length=64), unique=True, nullable=False)
    user_pwd = my_db.Column(my_db.String(length=128), nullable=False)
    user_role = my_db.Column(my_db.String(length=12), nullable=False, default='customer')
    user_budget = my_db.Column(my_db.Integer, nullable=False)
    user_products = my_db.relationship('Products', backref='owned_product', lazy=True)

    # USERS CONSTRUCTOR FOR USERS
    # TO CREATE ADMIN ACCOUNT USE CLI flask shell TO SET ROLE.
    def __init__(self, u_fname, u_lname, u_email, u_pwd, u_budget):
        self.user_fname = u_fname
        self.user_lname = u_lname
        self.user_email = u_email
        self.user_pwd = u_pwd
        self.user_budget = u_budget

    # NEAT WAY DISPLAY USERS INSTANCE OBJECTS
    def __repr__(self):
        return f'User:{self.user_fname}'

    # PASSWORD HASHER

    def hash_pwd(self, password):
        self.user_pwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt(6))

    # PASSWORD CHECKER
    def check_pwd(self, password):
        return bcrypt.checkpw(password.encode(), self.user_pwd.encode())

    # CHECK IF USER HAS ENOUGH FUNDS TO MAKE PURCHASE
    def user_purchase(self, product):
        return self.user_budget >= product.product_price

    # CHECK IF USER OWNS ITEM THEY WANT TO PUT BACK ON MARKET
    def user_remove(self, product):
        return product in self.user_products

    # FUNDS DISPLAY FORMAT
    @property
    def display_budget_format(self):
        return f'{self.user_budget:,}$'

    # METHOD TO SET USER BUDGET; IF USER IS ADMIN THEY GET 0 AS THEY CAN ONLY ADD PRODUCTS TO THE SHOP;
    # NOT PURCHASE THEM
    def set_budget(self, amount):
        if self.user_role == 'admin':
            self.user_budget = 0
        else:
            self.user_budget = amount

    # METHOD FROM UserMixin Class
    def get_id(self):
        return self.user_id


#  user_loader callback used to reload the user object from the user ID stored in the session.
@my_login.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
