from flask import Blueprint, render_template, request

from ._helpers import to_num

bp = Blueprint("triangle", __name__)

WORK = {
    "order": 3,
    "href": "/works/area/triangle",
    "title": "Area of a Triangle",
    "desc": "Enter a base and height to get the area.",
    "category": "Math",
}


@bp.route("/works/area/triangle", methods=["GET", "POST"])
def atriangle():
    result = None
    error = None

    if request.method == "POST":
        base = to_num("base")
        height = to_num("height")

        if base is None or height is None or base < 0 or height < 0:
            error = "Enter a base and height of 0 or more."
        else:
            result = round(0.5 * base * height, 2)

    return render_template("triangle.html", result=result, error=error)
