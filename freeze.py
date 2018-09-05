from flask_frozen import Freezer
from app import app, get_avlocs, get_airport_csv

'''
DONT DEFINE THESE AGAIN HERE - 

from avlocs import get_avlocs
def get_airport_csv():
    airports = get_avlocs().reset_index()
    airports = airports.to_dict(orient='records')
    return airports

CAN GET IT FROM OUR app.py LIKE THIS
from app import app, get_avlocs, get_airport_csv
'''

freezer = Freezer(app)

@freezer.register_generator
def detail():
    for row in get_airport_csv():
        yield {'row_id': row['LOC_ID']}

if __name__ == '__main__':
    freezer.freeze()
