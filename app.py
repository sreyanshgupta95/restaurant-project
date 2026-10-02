from flask import Flask, render_template, request, session, redirect, url_for
import os
import qrcode

app = Flask(__name__)
app.secret_key = 'restaurant_secret_key'

# Menu Items with IDs and Categories
MENU_ITEMS = {
    'starters': [
        {'id': 1, 'name': 'Soup', 'price': 100},
        {'id': 2, 'name': 'Paneer Tikka', 'price': 200}
    ],
    'dinner': [
        {'id': 3, 'name': 'Dal Makhani', 'price': 250},
        {'id': 4, 'name': 'Butter Naan', 'price': 40}
    ],
    'beverages': [
        {'id': 5, 'name': 'Cold Drink', 'price': 60},
        {'id': 6, 'name': 'Juice', 'price': 90}
    ],
    'dessert': [
        {'id': 7, 'name': 'Ice Cream', 'price': 120},
        {'id': 8, 'name': 'Gulab Jamun', 'price': 80}
    ]
}

@app.route('/')
def home():
    room = request.args.get('room', 'Table-1')
    session['room'] = room
    
    # Generate QR code for the table
    if not os.path.exists('static'):
        os.makedirs('static')
    current_url = f"http://10.2.0.2:5000/?room={room}"
    qr = qrcode.make(current_url)
    qr_path = os.path.join('static', 'qr_code.png')
    qr.save(qr_path)
    
    return render_template('index.html', room=room, qr_code='static/qr_code.png')

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        session['name'] = request.form.get('name')
        session['people'] = request.form.get('people')
        if request.form.get('room'):
            session['room'] = request.form.get('room')
            
    room = session.get('room', 'Table-1')
    return render_template('menu.html', room=room, menu=MENU_ITEMS)

@app.route('/place_order', methods=['POST'])
def place_order():
    selected_items = request.form.getlist('items')
    room = session.get('room', 'Table-1')
    name = session.get('name', 'Guest')
    return render_template('success.html', name=name, room=room, items=selected_items)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)