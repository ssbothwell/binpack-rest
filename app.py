from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from schema import Schema
import binpack

app = FlaskAPI(__name__)

schema = Schema({
    "items": [[int,int], [int,int]],
    "binmanager": {
        "bin_width": int,
        "bin_height": int,
        "bin_algo": str,
        "pack_algo": str,
        "heuristic": str,
        "sorting": bool,
        "rotation": bool,
    }
})

@app.route("/", methods=['GET','POST'])
def pack():
    """
    Takes a set of items and binpack settings
    Returns packed bins
    """
    if request.method == 'POST':
        data = request.data
        schema.validate(data)
        items = [binpack.Item(*item) for item in data['items']]
        binargs= request.data['binmanager']
        M = binpack.BinManager(**binargs)
        M.add_items(*items)
        M.execute()
        unpacked = [[ unpackItem(i) for i in b.items] for b in M.bins]
        return { i: el for i,el in enumerate(unpacked)}
        return {'items': [{'width': i.x,
                           'height': i.y,
                           'cornerPoint': i.CornerPoint}
                           for i in M.items]}
    # request.method == 'GET'
    return {}

def unpackItem(item: binpack.Item):
    return [item.x, item.y, [item.CornerPoint[0], item.CornerPoint[1]]]

if __name__ == "__main__":
    app.run(debug=True)
