from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample products
products = {
    'Apple': 0.5,
    'Banana': 0.3,
    'Orange': 0.4,
    'Mango': 1.0
}

sales_history = []

@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/calculate', methods=['POST'])
def calculate():
    product = request.form['product']
    quantity = int(request.form['quantity'])
    price = products[product]
    total = quantity * price
    sales_history.append({'product': product, 'quantity': quantity, 'total': total})
    return render_template('result.html', product=product, quantity=quantity, total=total)

@app.route('/sales')
def sales():
    return render_template('sales.html', sales=sales_history)

@app.route('/back')
def back():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
