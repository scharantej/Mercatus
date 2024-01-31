
# Import necessary modules
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy

# Create a Flask app
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecomm.db'
app.config['SECRET_KEY'] = 'mysecretkey'

# Initialize the database
db = SQLAlchemy(app)

# Define the Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'

# Define the CartItem model
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<CartItem {self.product.name}>'

# Define the Order model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    shipping_address = db.Column(db.String(255), nullable=False)
    billing_address = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Order {self.id}>'

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Create the database tables
db.create_all()

# Define the home route
@app.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

# Define the product details route
@app.route('/product/<product_id>')
def product_details(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_details.html', product=product)

# Define the cart route
@app.route('/cart')
def cart():
    cart_items = CartItem.query.all()
    total_amount = 0
    for item in cart_items:
        total_amount += item.product.price * item.quantity
    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)

# Define the checkout route
@app.route('/checkout')
def checkout():
    cart_items = CartItem.query.all()
    total_amount = 0
    for item in cart_items:
        total_amount += item.product.price * item.quantity
    return render_template('checkout.html', cart_items=cart_items, total_amount=total_amount)

# Define the place order route
@app.route('/place_order', methods=['POST'])
def place_order():
    user_id = 1  # TODO: Get the user ID from the session
    shipping_address = request.form['shipping_address']
    billing_address = request.form['billing_address']
    cart_items = CartItem.query.all()
    total_amount = 0
    for item in cart_items:
        total_amount += item.product.price * item.quantity
    order = Order(user_id=user_id, total_amount=total_amount, shipping_address=shipping_address, billing_address=billing_address, status='Processing')
    db.session.add(order)
    db.session.commit()
    flash('Your order has been placed successfully.')
    return redirect(url_for('confirmation'))

# Define the confirmation route
@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
