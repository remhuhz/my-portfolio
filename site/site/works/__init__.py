"""
Works package
=============
Every file in this folder whose name ends in ``_work.py`` is one "work"
(one page of the portfolio). Each work file must define:

    bp    -> a Flask Blueprint with the work's route(s)
    WORK  -> a dict used for the card on the /works page:
             {"order": 7, "href": "/works/example", "title": "...",
              "desc": "...", "category": "..."}

app.py calls register_works(app) once, which finds and registers every
work automatically. To add a new work, just drop a new ``*_work.py`` file
in this folder (and its template in templates/) - app.py never changes.
"""

import importlib
import pkgutil


def register_works(app):
    """Import every *_work module, register its blueprint, return the cards."""
    cards = []

    for info in pkgutil.iter_modules(__path__):
        if not info.name.endswith("_work"):
            continue

        module = importlib.import_module(f"{__name__}.{info.name}")
        app.register_blueprint(module.bp)
        cards.append(module.WORK)

    cards.sort(key=lambda card: card["order"])
    return cards
