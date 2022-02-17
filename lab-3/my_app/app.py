from crypt import methods
import sqlite3
from flask import Flask, request
import uuid

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/', methods=['POST', 'DELETE', 'GET'])
def index():
    conn = get_db_connection()
    if request.method == 'POST':
        sample = request.get_json()
        try:
            conn = get_db_connection()
            sampleKey, sampleValue, sampleMessage = sample['key'], sample['value'], sample['message']
            conn.execute('REPLACE INTO samples (key, value, message) VALUES (?, ?, ?)',
                         (sampleKey, sampleValue, sampleMessage))
            conn.commit()
            conn.close()
            return {'sample': {
                'key': sample['key'],
                'value': sample['value'],
                'message': sample['message']
            }, 'output': 'Sample inserted with id: '+sampleKey }, 201
        except:
            return {'error': 'Invalid JSON Body', 'status': 400}, 400
    elif request.method == 'DELETE':
        sample = request.get_json()
        try:
            conn = get_db_connection()
            sampleKey = sample['key']
            conn.execute('DELETE FROM samples WHERE key=?', (sampleKey,))
            conn.commit()
            conn.close()
            return {'sample': {
                'key': sample['key']
            }, 'output': 'Sample deleted with id: '+sampleKey }, 200
        except:
            return {'error': 'Invalid key', 'status': 404}, 404

    else:
        samples = conn.execute('SELECT * FROM samples').fetchall()
        print('Type: ', samples)
        conn.close()
        sampleList = list()
        for sample in list(samples):
            sampleList.append({
                'key': sample['key'],
                'value': sample['value'],
                'message': sample['message']
            })
        return {'data': sampleList}, 200

@app.route('/<string:key>/', methods=['GET'])
def getByKey(key):
    conn = get_db_connection()
    sample = conn.execute('SELECT * FROM samples WHERE key = ?',
                        (key,)).fetchone()
    conn.close()
    if sample is None:
        return {'error': 'Invalid key', 'status': 404}, 404
    return {'sample': {
                'key': sample['key'],
                'value': sample['value'],
                'message': sample['message']
            }}, 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)