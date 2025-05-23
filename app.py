from flask import Flask, render_template, request, redirect, url_for, Response
from prometheus_client import Counter, generate_latest, Summary

app = Flask(__name__)

# Updated product structure with code, description, and price
products = {
    1: {'description': 'Apple', 'price': 0.5},
    2: {'description': 'Banana', 'price': 0.3},
    3: {'description': 'Orange', 'price': 0.4},
    4: {'description': 'Mango', 'price': 1.0}
}

view_metric = Counter('views_by_product', 'Product views', ['product'])
view_duration = Summary('checkout_duration', 'Time spent in products checkout')
sales_history = []

@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/calculate', methods=['POST'])
def calculate():
    product_code = int(request.form['product'])
    product_info = products.get(product_code)

    if product_info is None:
        return "Invalid product", 400

    view_metric.labels(product=product_info['description']).inc()

    quantity = int(request.form['quantity'])
    total = quantity * product_info['price']
    sales_history.append({
        'product': product_info['description'],
        'quantity': quantity,
        'total': total
    })
    return render_template('result.html', product=product_info['description'], quantity=quantity, total=total)

@app.route('/sales')
@view_duration.time()
def sales():
    return render_template('sales.html', sales=sales_history)

@app.route('/back')
def back():
    return redirect(url_for('index'))

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)
