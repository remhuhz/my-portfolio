Put your images in this folder (static/images).

Use them in a template like this:
<img src="{{ url_for('static', filename='images/yourfile.png') }}" alt="description">

The profile page looks for: static/images/profile.jpg
