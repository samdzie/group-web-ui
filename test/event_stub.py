import json
from flask import Flask, jsonify


app = Flask(__name__)
events = {
    '1' : {
        'events' : [
            {
                'name' : 'Breakfast',
                'start_time' : '11/01/2020 09:00 AM',
                'end_time' : '11/01/2020 10:00 AM',
            },
            {
                'name' : 'Lunch',
                'start_time' : '11/01/2020 01:00 PM',
                'end_time' : '11/01/2020 02:00 PM',
            },
        ]
    },
}


@app.route('/group/<group_id>')
def group_events(group_id):
    group_events = events.get(group_id)
    return jsonify(group_events)


if __name__ == '__main__':
    app.run(port=5002)
