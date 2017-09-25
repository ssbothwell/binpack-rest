from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
import binpack

app = FlaskAPI(__name__)
items = []

@app.route("/", methods=['GET','POST'])
def pack():
    """
    Takes a set of items and binpack settings
    Returns backed bins

    JSON Schema:
    {
        "items": [(int,int), (int,int)],
        "binmanager": {
            "width": int,
            "height": int,
            "bin_algo": string,
            "pack_algo": string,
            "heuristic": string,
            "sorting": bool,
            "rotation: bool,
        }
    }
    """
    if request.method == 'POST':
        new_items = request.data.get('items', '')
        for item in new_items:
            items.append(binpack.Item(*item))

        binmanager = request.data.get('binmanager', '')
        bwidth = binmanager['width']
        bheight = binmanager['height']
        bbin_algo = binmanager['bin_algo']
        bpack_algo = binmanager['pack_algo']
        bheuristic = binmanager['heuristic']
        bsorting = binmanager['sorting']
        brotation = binmanager['rotation']

        M = binpack.BinManager(bwidth,
                               bheight,
                               bbin_algo,
                               bpack_algo,
                               bheuristic,
                               bsorting,
                               brotation)
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
