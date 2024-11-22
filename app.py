from flask import Flask, render_template, request, redirect, url_for, jsonify
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
    stones_with_paths = []

    for stone in stones:
        image_name = stone[0].replace(" ", "_") + ".png"
        original_image_path = os.path.join('static/images', image_name)
        thumbnail_image_path = os.path.join('static/thumbnail', image_name)

        if os.path.exists(thumbnail_image_path):
            thumbnail_path = url_for('static', filename=f'thumbnail/{image_name}')
        elif os.path.exists(original_image_path):
            thumbnail_path = url_for('static', filename=f'images/{image_name}')
        else:
            thumbnail_path = url_for('static', filename='images/imageNotFound.png')

        stones_with_paths.append({
            "Nom": stone[0],
            "ImagePathLowRes": thumbnail_path
        })

    return render_template('index.html', stones=stones_with_paths)

@app.route('/stone/<stone_name>')
def stone_detail(stone_name):
    stone = get_stone_details(stone_name)
    if not stone:
        return render_template('error.html', message="Stone Not Found")

    image_path = os.path.join(app.root_path, 'static', 'images', f"{stone_name}.png")

    if not os.path.exists(image_path):
        image_path = url_for('static', filename='images/imageNotFound.png')
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

@app.route('/edit_stone/<stone_name>', methods=['GET', 'POST'])
def edit_stone(stone_name):
    stone = get_stone_details(stone_name)
    if not stone:
        return render_template('error.html', message="Stone Not Found")

    if request.method == 'POST':
        try:
            new_name = request.form['name']
            comments = request.form['comments']
            provenance = request.form['provenance']
            date_acquisition = request.form['date_acquisition']
            price = request.form['price']
            weight = request.form['weight']
            other_info = request.form['other_info']
            box = request.form['box']
        except KeyError as e:
            message="Error while collecting data"
            return render_template('error.html', message=message)

        conn = sqlite3.connect('bd/data.bd')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE mineraux
            SET Nom = ?, Commentaires = ?, Provenance = ?, Date_acquisition = ?, Prix_achat = ?, cm_g = ?, autres_infos = ?, Boite = ?
            WHERE Nom = ?
        ''', (new_name, comments, provenance, date_acquisition, price, weight, other_info, box, stone_name))
        conn.commit()
        conn.close()

        return redirect(url_for('stone_detail', stone_name=new_name))

    return render_template('edit_stone.html', stone=stone)

@app.route('/stone/<stone_name>/delete', methods=['POST'])
def delete_stone(stone_name):
    conn = sqlite3.connect('bd/data.bd')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mineraux WHERE Nom = ?", (stone_name,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


def get_country_coordinates(country_name):
    coordinates_map = {
        "Canada": [56.1304, -106.3468],
        "France": [46.603354, 1.888334],
        "USA": [37.09024, -95.712891],
        "Germany": [51.1657, 10.4515],
        "Italy": [41.87194, 12.56738],
    }
    return coordinates_map.get(country_name, [0, 0])


@app.route('/api/map-data')
def map_data():
    conn = sqlite3.connect('bd/data.bd')
    cursor = conn.cursor()

    cursor.execute("SELECT Provenance, COUNT(*), GROUP_CONCAT(Nom) FROM mineraux GROUP BY Provenance")
    stones_by_country = cursor.fetchall()
    conn.close()

    result = []
    for country, count, stones in stones_by_country:
        if country:
            coordinates = get_country_coordinates(country)
            stone_list = stones.split(",") if stones else []
            result.append({
                "country": country,
                "coordinates": coordinates,
                "stones": stone_list,
                "count": count
            })

    return jsonify(result)


@app.route('/map')
def map_view():
    return render_template('map.html')


if __name__ == '__main__':
    app.run(debug=True)
