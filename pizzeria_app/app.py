from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'super_secret_pizzeria_key'

MENU = [
    {"name": "Margherita", "desc": "Classic tomato sauce, fresh mozzarella, and basil.", "price": "$12.00"},
    {"name": "Pepperoni", "desc": "Tomato sauce, mozzarella, and spicy pepperoni cups.", "price": "$14.00"},
    {"name": "Truffle Mushroom", "desc": "White base, roasted mushrooms, mozzarella, truffle oil.", "price": "$16.00"},
    {"name": "Spicy Diavola", "desc": "Tomato sauce, mozzarella, spicy salami, chili flakes.", "price": "$15.00"}
]

@app.route('/')
def home():
    return render_template('index.html', menu=MENU)

@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        session['name'] = request.form.get('name')
        session['email'] = request.form.get('email')
        
        date = request.form.get('date')
        time = request.form.get('time')
        
        return render_template('reservation.html', success=True, date=date, time=time)
    
    return render_template('reservation.html', success=False)

@app.route('/profile')
def profile():
    # We no longer redirect here; the logic is handled in the HTML template
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)