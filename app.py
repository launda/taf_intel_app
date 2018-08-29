from flask import Flask
from flask import render_template
import os

from avlocs import get_avlocs

cur_dir = os.path.dirname(__file__)

app = Flask(__name__)


def get_csv():
	airports = get_avlocs().reset_index()
	# get only those in VIC
	airports = airports.loc[airports['State'].str.contains('VIC'),]

    # convert DF .to_dict() as we can't pass pandas DF to jinja2 templates
	# 'records' works as it gets rid of row index values for each column

    # another option is convert DF .to_html()
    # But less html control as it converts as whole blocl to html
	with open(os.path.join(cur_dir,'templates', 'airports.html'), 'w') as ob:
		airports.to_html(ob,bold_rows=True,
            border=4, col_space=10,justify='right',escape=False)

	airports = airports.to_dict(orient='records')
	return airports


@app.route("/")
def index():
    template = 'index.html'
    airports = get_csv()
    return render_template(template, object_list=airports)

@app.route('/<row_id>/')
def detail(row_id):
    template = 'detail.html'
    object_list = get_csv()
    for row in object_list:
        if row['LOC_ID'] == row_id:
            return render_template(template, object=row)

if __name__ == '__main__':
    # Fire up the Flask test server
    app.run(debug=True, use_reloader=True)
