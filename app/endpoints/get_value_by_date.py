import datetime
from flask import Blueprint, jsonify, request
from ..utils import get_uf_value

get_value_by_date = Blueprint('get_value_by_date', __name__)


@get_value_by_date.route('/api/date/<string:date_string>')
def get_value(date_string):
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

    return jsonify({'date': uf_value})
