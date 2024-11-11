from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import sqlite3
import os

app = Flask(__name__)

def get_stones():
    conn = sqlite3.connect('bd/data.bd')
    cursor = conn.cursor()
    cursor.execute("SELECT Nom FROM mineraux ORDER BY Nom ASC")
    stones = cursor.fetchall()
    conn.close()
    return stones

def get_stone_details(name):
    conn = sqlite3.connect('bd/data.bd')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mineraux WHERE Nom=?", (name,))
    stone = cursor.fetchone()
    conn.close()
    if stone:
        return {
            'Nom': stone[1],
            'Commentaires': stone[2],
            'Provenance': stone[3],
            'Date_acquisition': stone[4],
            'Prix_achat': stone[5],
            'cm_g': stone[6],
            'autres_infos': stone[7],
            'Boite': stone[8],
        }
    return None

@app.route('/')
def index():
    stones = get_stones()
    return render_template('index.html', stones=stones)

@app.route('/stone/<stone_name>')
def stone_detail(stone_name):
    stone = get_stone_details(stone_name)
    if not stone:
        return "Pierre non trouvée", 404

    image_path = os.path.join(app.root_path, 'static', 'images', f"{stone_name}.png")

    if not os.path.exists(image_path):
        image_path = url_for('static', filename='images/errorNoImage.png')
    else:
        image_path = url_for('static', filename=f'images/{stone_name}.png')

    return render_template('stone_detail.html', stone=stone, image_path=image_path)

@app.route('/error')
def error_page():
    return render_template('error.html', message="An error occurred: some form data was missing.")

@app.route('/formulaire', methods=['GET', 'POST'])
def add_stone():
    if request.method == 'POST':
        try:
            name = request.form['name']
            comments = request.form['comments']
            provenance = request.form['provenance']
            date_acquisition = request.form['date_acquisition']
            price = request.form['price']
            weight = request.form['weight']
            other_info = request.form['other_info']
            box = request.form['box']

        except KeyError as e:
            print(f"Error while collecting data {str(e)}. Please retry", "error")
            return redirect(url_for('error_page'))

        conn = sqlite3.connect('bd/data.bd')
        cursor = conn.cursor()
        cursor.execute(''' 
            INSERT INTO mineraux (Nom, Commentaires, Provenance, Date_acquisition, Prix_achat, cm_g, autres_infos, Boite) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?) 
        ''', (name, comments, provenance, date_acquisition, price, weight, other_info, box))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_stone.html')
if __name__ == '__main__':
    app.run(debug=True)
