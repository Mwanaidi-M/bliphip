from bhip import my_app, my_db
from .models import Users, Products
from .forms import RegisterForm, LogInForm, ProductAdd, BuyProduct, SellProduct

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user


# HOME PAGE
@my_app.route('/')
@my_app.route('/home/')
def home():
    msg = 'WELCOME HOME'
    return render_template('index.html', message=msg)


# ABOUT PAGE
@my_app.route('/about/')
def about():
    return render_template('about.html')


# MARKET PAGE
@my_app.route('/market/', methods=['GET', 'POST'])
def market():
    purchase_product_form = BuyProduct()

    if purchase_product_form.validate_on_submit():
        prd_name = request.form.get('purchased_item')
        prd_object = Products.query.filter_by(product_name=prd_name).first()

        if prd_object is not None:
            if current_user.is_authenticated:
                if current_user.user_purchase(prd_object):
                    prd_object.product_owner_id = current_user.user_id
                    prd_object.purchase_product(current_user)

                    flash(message='Product Purchased Successfully', category='success')
                else:
                    flash(message='You have insufficient funds to make this purchase.', category='warning')
            else:
                flash(message='You need to have an account to purchase this product.', category='danger')
                return redirect(url_for('market'))

    # geting the value of the page URL parameter using the request.args object and its get() method
    m_page = request.args.get('page', 1, int)

    all_products = Products.query.filter_by(product_owner_id=None).paginate(page=m_page, per_page=3)
    return render_template('market.html', products=all_products, buy_pr=purchase_product_form)


# ACCOUNT PAGE
@my_app.route('/account/', methods=['GET', 'POST'])
@login_required
def account():
    sell_product_form = SellProduct()

    if sell_product_form.validate_on_submit():
        owned_prd = request.form.get('owned_item')
        owned_prd_obj = Products.query.filter_by(product_name=owned_prd).first()

        if owned_prd_obj is not None:
            if current_user.user_remove(owned_prd_obj):
                owned_prd_obj.remove_product(current_user)
                flash(message='Product removed successfully.', category='success')

            else:
                flash(message='Sorry, you do not own this product.', category='info')
            return redirect(url_for('market'))
        return redirect(url_for('account'))

    client_products = Products.query.filter_by(product_owner_id=current_user.user_id).all()
    return render_template('account.html', my_prd=client_products, sell_pr=sell_product_form)


@my_app.route('/account/register/', methods=['GET', 'POST'])
def account_register():
    reg_form = RegisterForm()
    if reg_form.validate_on_submit():
        cust_fname = reg_form.first_name.data
        cust_lname = reg_form.last_name.data
        cust_email = reg_form.email_addr.data
        cust_pwd = reg_form.password.data
        cust_budget = reg_form.acc_budget.data

        customer_exist = Users.query.filter_by(user_email=cust_email).first()
        if customer_exist is not None:
            flash(message='Email already exists. Please enter a different email address', category='dange')
            return redirect(url_for('account_register'))

        new_customer = Users(cust_fname, cust_lname, cust_email, cust_pwd, cust_budget)
        new_customer.hash_pwd(cust_pwd)
        new_customer.set_budget(cust_budget)

        my_db.session.add(new_customer)
        my_db.session.commit()

        login_user(new_customer)
        flash(message='Account created successfully.', category='success')
        return redirect(url_for('account'))
    return render_template('register.html', s_up=reg_form)


@my_app.route('/account/login/', methods=['GET', 'POST'])
def account_login():
    # check if user is already logged
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # Bypass if user is not logged in, they fill in the form
    login_form = LogInForm()
    if login_form.validate_on_submit():
        customer_acc = Users.query.filter_by(user_email=login_form.email_addr.data).first()
        if customer_acc is None:
            flash(message='Account does not exist.', category='danger')
            return redirect(url_for('account_login'))
        elif not customer_acc.check_pwd(login_form.password.data):
            flash(message='Invalid password.', category='danger')
            return redirect(url_for('account_login'))

        login_user(customer_acc)

        # check for next, which is a parameter stored in the query string of the current user.
        # If the user attempted to access the app before logging in, next would equal the page they had
        # tried to reach: this allows wall-offing the app from unauthorized users, and then drop users off
        # at the page they tried to reach before they logged in.
        next_page = request.args.get('next')

        flash(message='Login Successful', category='success')
        return redirect(url_for('account') or next_page)
    return render_template('login.html', s_in=login_form)


@my_app.route('/account/logout/')
def account_logout():
    logout_user()
    flash(message='You are now logged out.', category='info')
    return redirect(url_for('home'))


@my_app.route('/new-product/', methods=['GET', 'POST'])
@login_required
def add_product():
    new_product_form = ProductAdd()
    if new_product_form.validate_on_submit():
        prd_name = new_product_form.name_product.data
        prd_desc = new_product_form.desc_product.data
        prd_price = new_product_form.price_product.data

        product_check = Products.query.filter_by(product_name=prd_name).first()

        if product_check is None:
            new_product = Products(prd_name, prd_desc, prd_price)
            my_db.session.add(new_product)
            my_db.session.commit()

            flash(message=f'Product: {new_product.product_name} added successfully.', category='success')
            return redirect(url_for('account'))
        else:
            flash(message='This product already exists. Please add a different product.')
            return redirect(url_for('add_product'))
    return render_template('add-product.html', prd_form=new_product_form)
