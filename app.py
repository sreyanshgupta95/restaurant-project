from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

MENU_ITEMS = {
    'Pizza': 300,
    'French Fries': 100,
    'Gulab Jamun': 80,
    'Burger': 150,
    'Cold Drink': 60
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        room = request.form.get('room')
        if room:
            session['room'] = room
            session['orders'] = []
        return redirect(url_for('menu'))
    
    room = session.get('room', 'Table-1')
    return render_template('menu.html', menu=MENU_ITEMS, room=room)

@app.route('/add_order', methods=['POST'])
def add_order():
    item = request.form.get('item')
    try:
        quantity = int(request.form.get('quantity', 1))
    except ValueError:
        quantity = 1

    if item in MENU_ITEMS:
        price_per_item = MENU_ITEMS[item]
        total_price = price_per_item * quantity

        if 'orders' not in session:
            session['orders'] = []

        session['orders'].append({
            'item': item,
            'quantity': quantity,
            'total_price': total_price
        })
        session.modified = True

    room = session.get('room', 'Table-1')
    orders = session.get('orders', [])

    return render_template('success.html', 
                           item=item, 
                           quantity=quantity, 
                           total_price=total_price, 
                           room=room, 
                           orders=orders)

@app.route('/order-complete', methods=['POST', 'GET'])
def order_complete():
    orders = session.get('orders', [])
    room = session.get('room', 'Table-1')
    return render_template('thankyou.html', orders=orders, room=room)

if __name__ == '__main__':
    app.run(debug=True)