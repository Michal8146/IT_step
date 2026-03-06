from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
# A secret key is required to use 'session' safely
app.secret_key = 'super_secret_pizzeria_key'

# Mock menu data
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
        # Save user data to session so they don't have to re-enter it next time
        session['name'] = request.form.get('name')
        session['email'] = request.form.get('email')
        
        # In a real app, you would save the reservation details to a database here
        date = request.form.get('date')
        time = request.form.get('time')
        
        return render_template('reservation.html', success=True, date=date, time=time)
    
    return render_template('reservation.html', success=False)

@app.route('/profile')
def profile():
    # Check if the user has saved details in the session
    if 'name' not in session:
        return redirect(url_for('reservation')) # Redirect to make a reservation if no profile exists
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)