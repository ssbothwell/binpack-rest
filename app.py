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
    Returns backed bins

    JSON Schema:
    """
    if request.method == 'POST':
        data = request.data
        schema.validate(data)
        items = [binpack.Item(*item) for item in data['items']]
        binargs= request.data['binmanager']
        M = binpack.BinManager(**binargs)
        M.add_items(*items)
        M.execute()
        return {'items': [{'width': i.x,
                           'height': i.y,
                           'cornerPoint': i.CornerPoint}
                           for i in M.items]}
    # request.method == 'GET'
    return {}


if __name__ == "__main__":
    app.run(debug=True)
