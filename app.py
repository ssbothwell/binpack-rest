from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
import binpack

app = FlaskAPI(__name__)

@app.route("/", methods=['GET','POST'])
def pack():
    """
    Takes a set of items and binpack settings
    Returns backed bins

    JSON Schema:
    {
        "items": [(int,int), (int,int)],
        "binmanager": {
            "bin_width": int,
            "bin_height": int,
            "bin_algo": string,
            "pack_algo": string,
            "heuristic": string,
            "sorting": bool,
            "rotation: bool,
        }
    }
    """
    if request.method == 'POST':
        items = [binpack.Item(*item) for item in request.data.get('items', '')]
        binargs= request.data.get('binmanager', '')
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
