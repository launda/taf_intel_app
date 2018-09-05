from flask_frozen import Freezer
from app import app
from flask import abort
import os
from avlocs import get_avlocs
freezer = Freezer(app)

def get_airport_csv():
    airports = get_avlocs().reset_index()
    airports = airports.to_dict(orient='records')
    return airports

@freezer.register_generator
def detail():
    for row in get_airport_csv():
        yield {'row_id': row['LOC_ID']}

if __name__ == '__main__':
    freezer.freeze()
