import datetime
from flask import Blueprint, jsonify, request
from ..utils import get_uf_value

get_value_by_date = Blueprint('get_value_by_date', __name__)


@get_value_by_date.route('/api/date', methods=['GET', 'POST'])
def get_value():
    # Try to get the date parameter from the URL first
    date_string = request.args.get('date')

    # If the date parameter is not present in the URL, try to get it from the request body
    if not date_string:
        date_string = request.json.get('date')
    if not date_string:
        return jsonify({'error': 'DATE_MISSING', 'message': 'Date is a required parameter.'}), 400

    try:
        # Validate date format and check if it exists
        date = datetime.datetime.strptime(date_string, '%d-%m-%Y')
        if date.year < 2013 or date > datetime.datetime.now():
            return jsonify({'error': 'DATE_INVALID_RANGE',
                            'message': 'Date must be greater than 01-01-2013 and less than today.'}), 400
    except ValueError:
        return jsonify({'error': 'DATE_INVALID_FORMAT', 'message': 'Date format must be DD-MM-YYYY.'}), 400

    # get the uf value from the web page
    uf_value = get_uf_value(date)

    if isinstance(uf_value, dict):
        return jsonify(uf_value), 400

    return jsonify({'date': uf_value})
