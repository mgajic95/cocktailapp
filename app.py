from flask import Flask, render_template, request, session, redirect, flash
from datetime import datetime
from fuzzywuzzy import fuzz

app = Flask(__name__)
app.secret_key = "tajni_kljuc_brate"

# Definisanje liste koktela
cocktails = {
    "Mojito": ["Bacardi White Rum 60ml", "lime 4-5 wedges", "brown sugar 2tbsp", "mint 8-10pcs",
               "Sparkling water top-up"],
    "Pina Colada": ["Bacardi White Rum 60ml", "Coconut cream 120ml", "pineapple juice 120ml"],
    "Daiquiri": ["Bacardi White rum 50ml", "lime 30ml", "simple syrup 25ml"],
    "Woodford Old Fashioned": ["Woodford Reserved 60ml", "Martini rosso 15ml", "maple syrup 7ml",
                               "Angostura bitters 3dash",
                               "Orange bitters 3dash"],
    "Mai Tai": ["Havana 7 50ml", "Simple syrup 15ml", "pineapple juice 30ml", "almond syrup 15ml", "lime 30ml",
                "cinnamon 1dash"],
    "Perfect Margarita": ["Silver Tequila 25ml", "Gold tequila 25ml", "lime 30ml", "orange juice 30ml",
                          "agave syrup 30ml", "Cointreau 25ml"],
}

@app.route('/')
def index():
    user_name = session.get('user_name')
    greeting = flash('greeting')
    return render_template('index.html', user_name=user_name, greeting=greeting)



@app.route('/search', methods=['POST', 'GET'])
def search_cocktails():
    if request.method == 'POST':
        ingredient = request.form['ingredient'].strip().lower()

        # Pronađite sastojke koji se podudaraju sa korisničkim unosom koristeći fuzzy pretragu
        matching_cocktails = {cocktail: ingredients for cocktail, ingredients in cocktails.items() if
                              any(fuzz.partial_ratio(ingredient, i.lower()) >= 80 for i in ingredients)}

        return render_template('search_results.html', user_name=session.get('user_name'), cocktails=matching_cocktails)

    return render_template('search.html')


@app.route('/set_name', methods=['POST'])
def set_name():
    user_name = request.form['user_name']
    session['user_name'] = user_name
    current_time = datetime.now().hour
    if current_time < 12:
        greeting = f"Good Morning, {user_name}!"
    elif 12 <= current_time < 18:
        greeting = f"Good Day, {user_name}!"
    else:
        greeting = f"Good Evening, {user_name}!"
    flash(greeting)
    return redirect('/personalized')

@app.route('/personalized')
def personalized():
    user_name = session.get('user_name')
    greeting = flash('greeting')
    return render_template('personalized.html', user_name=user_name, greeting=greeting)

@app.route('/cocktail_list_all')
def show_all_cocktails():
    user_name = session.get('user_name')
    return render_template('cocktail_list_all.html', user_name=user_name, cocktails=cocktails)

@app.route('/mojito')
def mojito():
    return render_template('mojito.html', cocktail=cocktails['Mojito'])

@app.route('/daiquiry')
def daiquiry():
    return render_template('daiquiry.html')

@app.route('/margarita')
def margarita():
    return render_template('margarita.html')

@app.route('/woodford')
def woodford():
    return render_template('woodford.html')

@app.route('/pinacolada')
def pinacolada():
    return render_template('/pinacolada.html')
@app.route('/maitai')
def maitai():
    return render_template('/maitai.html')

if __name__ == "__main__":
    app.run(debug=True)
