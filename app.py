from flask import Flask
from flask import render_template
import os

from avlocs import get_avlocs

cur_dir = os.path.dirname(__file__)

app = Flask(__name__)

@app.route("/")
def index():
    template = 'index.html'
    airports = get_avlocs().reset_index()
    # get only those in VIC
    airports = airports.loc[airports['State'].str.contains('VIC'),]

    '''Now we can't pass a dataframe to jinja2 template '''
    # 1st Solution - convert to html - but little control over display
    '''
    pd.set_option('display.max_columns', None)
    with open(os.path.join(cur_dir,'templates', 'airports.html'), 'w') as ob:
        airports.to_html(ob,bold_rows=True,
            border=4, col_space=10,justify='right',escape=False)
    '''
    
    # 2nd solutin - Convert the DataFrame to a dictionary.
    '''
    DataFrame.to_dict(orient='dict', into=<class 'dict'>)[source]
    orient : str {‘dict’, ‘list’, ‘series’, ‘split’, ‘records’, ‘index’}
    Determines the type of the values of the dictionary.
    ‘dict’ (default) : dict like {column -> {index -> value}}
    ‘list’ : dict like {column -> [values]}
    ‘series’ : dict like {column -> Series(values)}  <--closest
    ‘records’ : list like [{column -> value}, … , {column -> value}]
    '''
    # 'records' works as it gets rid of row index values for each column
    airports = airports.to_dict(orient='records')


    return render_template(template, object_list=airports)

if __name__ == '__main__':
    # Fire up the Flask test server
    app.run(debug=True, use_reloader=True)
