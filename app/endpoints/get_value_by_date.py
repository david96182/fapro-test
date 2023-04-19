from flask import Blueprint, jsonify

get_date_by_date = Blueprint('get_date_by_date', __name__)


@get_date_by_date.route('/api/date')
def date1():
    return jsonify({'date': '123'})
