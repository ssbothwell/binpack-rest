from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS
from schema import Schema
import greedypacker

app = FlaskAPI(__name__)
CORS(app)

schema = Schema({
    "items": [[int,int], [int,int]],
    "binmanager": {
        "bin_width": int,
        "bin_height": int,
        "bin_algo": str,
        "pack_algo": str,
        "heuristic": str,
        "sorting": bool,
        "sorting_heuristic": str,
        "rotation": bool,
        "wastemap": bool,
        "rectangle_merge": bool
    }
})

@app.route("/", methods=['GET','POST'])
def pack():
    """
    Takes a set of items and greedypacker settings
    Returns packed bins
    """
    if request.method == 'POST':
        data = request.data
        schema.validate(data)
        items = [greedypacker.Item(*item) for item in data['items']]
        binargs= request.data['binmanager']
        M = greedypacker.BinManager(**binargs)
        M.add_items(*items)
        M.execute()
        unpacked_items= [[ unpackItem(i) for i in b.items] for b in M.bins]
        print(unpacked_items)

        return {'bin_width': M.bin_width, 'bin_height': M.bin_height, 'sheets': unpacked_items}

    # request.method == 'GET'
    return {}

def unpackItem(item: greedypacker.Item):
    return { 'width': item.width, 'height': item.height, 'x': item.x, 'y': item.y}

if __name__ == "__main__":
    app.run(debug=True)
