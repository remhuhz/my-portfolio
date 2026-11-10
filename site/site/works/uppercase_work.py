from flask import Blueprint, render_template, request

bp = Blueprint("uppercase", __name__)

WORK = {
    "order": 1,
    "href": "/works/uppercase",
    "title": "To Upper Case",
    "desc": "Turn any text into capital letters.",
    "category": "Strings",
}


@bp.route("/works/uppercase", methods=["GET", "POST"])
def uppercase():
    result = None

    if request.method == "POST":
        result = request.form.get("inputString", "").upper()

    return render_template("touppercase.html", result=result)
