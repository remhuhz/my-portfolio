from flask import Flask, render_template

from works import register_works

app = Flask(__name__)

# Every work lives in its own file inside the works/ folder.
# register_works() finds each *_work.py file, registers its routes,
# and returns the cards shown on the /works page.
WORKS = register_works(app)


# ==================================================
# HOME, PROFILE, WORKS, AND CONTACT
# ==================================================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/works", endpoint="works")
def works_page():
    return render_template("works.html", items=WORKS)


@app.route("/contact")
def contact():
    return render_template("contact.html")


# ==================================================
# RUN APPLICATION
# ==================================================

if __name__ == "__main__":
    app.run(debug=True)
