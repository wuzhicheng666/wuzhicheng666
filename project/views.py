from flask import Blueprint, jsonify

from project.utils import get_time, get_date, get_china, get_lj, get_xz

bp = Blueprint("bp", __name__)


def init_views(app):
    app.register_blueprint(blueprint=bp)


@bp.route('/time/', methods=['GET', 'POST'])
def time():
    time = get_time()
    date = get_date()
    data = {
        "status": 0,
        "msg": "ok",
        "data": {
            "time": time,
            "confirm": date[0],
            "suspect": date[1],
            "heal": date[2],
            "dead": date[3]
        }
    }
    return jsonify(data)


@bp.route('/china/', methods=['GET', 'POST'])
def china():
    res = []
    for tup in get_china():
        res.append({"name": tup[0], "value": int(tup[1])})
    return jsonify({"data": res})


@bp.route('/lj/', methods=['GET', 'POST'])
def lj():
    data = get_lj()
    day, confirm, suspect, heal, dead = [], [], [], [], []
    for a, b, c, d, e in data[7:]:
        day.append(a.strftime("%m-%d"))
        confirm.append(b)
        suspect.append(c)
        heal.append(d)
        dead.append(e)
    return jsonify({"day": day, "confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead})


@bp.route('/xz/', methods=['GET', 'POST'])
def xz():
    data = get_xz()
    day, confirm_add, suspect_add = [], [], []
    for a, b, c in data[7:]:
        day.append(a.strftime("%m-%d"))
        confirm_add.append(b)
        suspect_add.append(c)

    return jsonify({"day": day, "confirm_add": confirm_add, "suspect_add": suspect_add})
