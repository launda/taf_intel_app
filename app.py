from flask import Flask
from flask import abort
from flask import render_template
import os

from avlocs import get_avlocs

cur_dir = os.path.dirname(__file__)

app = Flask(__name__)


def get_csv():
    airports = get_avlocs().reset_index()
    # get only those in VIC
    # airports = airports.loc[airports['State'].str.contains('VIC'),]
    # convert DF .to_dict() as we can't pass pandas DF to jinja2 templates
    # 'records' works as it gets rid of row index values for each column

    # another option is convert DF .to_html()
    # But less html control as it converts as whole block to html
    with open(os.path.join(cur_dir,'templates', 'airports.html'), 'w') as ob:
        airports.to_html(ob,bold_rows=True,
            border=4, col_space=10,justify='right',escape=False)

    '''
    df.to_dict() converts df into dict, so columns like 'Location', 'Area'
    are translated into “keys” on dictionary objects 
    that you can access like airports['Location'].
    '''
    airports = airports.to_dict(orient='records')
    return airports

'''
The @app.route() decorator used to connect index() function 
with the root URL of our site, "/"

We use Jinja to sculpt the data in index.html to create 
an HTML table that lists all airport details
'''

@app.route("/")
def index():
    template = 'index.html'  # html page to render
    airports = get_csv()     # get airport data as a dict obj
    return render_template(template, object_list=airports)



'''
create a unique “detail” page dedicated to each airport
both the URL route and function accept an argument, named row_id. 
Our goal is for the airport taf code e.g 'YMML' string
passed into the URL to go into the function where it can be used 
to pull the record with the corresponding id from the dict.
When we find a match, pass that row out to the template for 
rendering with the name object on its own unique page.
'''
@app.route('/<string:row_id>/')
def detail(row_id):
    template = 'detail.html'  # the html page to render content to 
    object_list = get_csv()   # get data as list of records
    for row in object_list:   # find record/row for given airport code 
        if row['LOC_ID'] == row_id:
            return render_template(template, object=row)
    abort(404)  # Display MSG if no page found
    #Not Found : The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.

if __name__ == '__main__':
    # Fire up the Flask test server
    app.run(debug=True, use_reloader=True)
