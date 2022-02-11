from crypt import methods
import sqlite3
from flask import Flask, request
import uuid

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    if request.method == 'POST':
        cat = request.get_json()
        try:
            conn = get_db_connection()
            newCatId = str(uuid.uuid4())
            catName, catColor, catBreed = cat['catName'], cat['catColor'], cat['catBreed']
            conn.execute('INSERT INTO cats (id, catName, catColor, catBreed) VALUES (?, ?, ?, ?)',
                         (newCatId, catName, catColor, catBreed))
            conn.commit()
            conn.close()
            return {'cat': {
                'id': newCatId,
                'catName': cat['catName'],
                'catColor': cat['catColor'],
                'catBreed': cat['catBreed']
            }, 'message': 'Cat inserted with id: '+newCatId }, 201
        except:
            return {'error': 'Invalid JSON Body', 'status': 400}, 400
    else:
        cats = conn.execute('SELECT * FROM cats').fetchall()
        print('Type: ', cats)
        conn.close()
        catList = list()
        for cat in list(cats):
            catList.append({
                'id': cat['id'],
                'catName': cat['catName'],
                'catColor': cat['catColor'],
                'catBreed': cat['catBreed']
            })
        return {'data': catList}, 200

@app.route('/<string:id>/', methods=['GET'])
def getById(id):
    conn = get_db_connection()
    cat = conn.execute('SELECT * FROM cats WHERE id = ?',
                        (id,)).fetchone()
    conn.close()
    if cat is None:
        return {'error': 'Invalid ID', 'status': 400}, 400
    return {'cat': {
                'id': cat['id'],
                'catName': cat['catName'],
                'catColor': cat['catColor'],
                'catBreed': cat['catBreed']
            }}, 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)