1. Install Python if you haven't already.
2. Go to your working directory.
3. (Recommended) Create a virtual environment:
    python3 -m venv venv
    source venv/bin/activate

    .venv/Scripts/activate.ps1 -- for windows


4. Install Flask:
    pip3 install flask
5. Run the app:
    
python app.py


ADDING A NEW WORK
Each work lives in its own file inside the works/ folder, named <something>_work.py.
The file defines a Blueprint called bp and a WORK dict (order, href, title, desc, category).
Put its page in templates/. app.py finds and registers every *_work.py file automatically.
