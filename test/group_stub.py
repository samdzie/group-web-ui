import json
from flask import Flask, jsonify


app = Flask(__name__)
groups = {
    '1' : {
        'name' : 'Group A',
        'welcome' : 'Welcome to Group A!',
    }
}


@app.route('/group/<group_id>')
def group(group_id):
    group_info = groups.get(group_id)
    return jsonify(group_info)


if __name__ == '__main__':
    app.run(port=5001)
