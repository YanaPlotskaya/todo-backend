from flask import Flask, request
from resources import EntryManager, Entry

app = Flask(__name__)

FOLDER = "C:\\Users\\yanap\\PycharmProjects\\json_files"


@app.route("/")
def hello_world():
    return "<p>Hello, World</p>"


@app.route("/api/entries/")
def get_entries():
    em = EntryManager(FOLDER)
    em.load()
    result = []
    for entry in em.entries:
        result.append(entry.json())
    return result


@app.route("/api/save_entries/", methods=['POST'])
def save_entries():
    entry_manager = EntryManager(FOLDER)
    for i in request.get_json():
        entry = Entry.from_json(i)
        entry_manager.entries.append(entry)
    entry_manager.save()
    return {'status': 'success'}


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
