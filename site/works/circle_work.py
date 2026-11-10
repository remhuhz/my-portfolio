from flask import Blueprint, render_template, request

from ._helpers import to_num

bp = Blueprint("circle", __name__)

WORK = {
    "order": 2,
    "href": "/works/area/circle",
    "title": "Area of a Circle",
    "desc": "Enter a radius to get the area.",
    "category": "Math",
}


@bp.route("/works/area/circle", methods=["GET", "POST"])
def acircle():
    result = None
    error = None

    if request.method == "POST":
        radius = to_num("radius")

        if radius is None or radius < 0:
            error = "Enter a radius of 0 or more."
        else:
            result = round(3.14 * radius * radius, 2)

    return render_template("circle.html", result=result, error=error)
