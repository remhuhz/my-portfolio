from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ---- Linked list (in memory) ----
class Node:
    def __init__(self, data):
        self.data, self.next = data, None

class LinkedList:
    def __init__(self):
        self.head = None
    def to_list(self):
        out, cur = [], self.head
        while cur:
            out.append(cur.data); cur = cur.next
        return out
    def insert_head(self, d):
        n = Node(d); n.next = self.head; self.head = n
    def insert_tail(self, d):
        n = Node(d)
        if not self.head: self.head = n; return
        cur = self.head
        while cur.next: cur = cur.next
        cur.next = n
    def delete(self, d):
        cur, prev = self.head, None
        while cur:
            if cur.data == d:
                if prev: prev.next = cur.next
                else: self.head = cur.next
                return True
            prev, cur = cur, cur.next
        return False
    def search(self, d):
        for i, v in enumerate(self.to_list()):
            if v == d: return i
        return -1
    def reverse(self):
        prev, cur = None, self.head
        while cur:
            cur.next, prev, cur = prev, cur, cur.next
        self.head = prev

ll = LinkedList()
for v in ("Jett", "Sage", "Omen"):
    ll.insert_tail(v)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/works')
def works():
    return render_template('works.html')

@app.route('/works/uppercase', methods=['GET', 'POST'])
def uppercase():
    result = None
    if request.method == 'POST':
        result = request.form.get('inputString', '').upper()
    return render_template('touppercase.html', result=result)

def to_num(name):
    try:
        return float(request.form.get(name, ''))
    except ValueError:
        return None

@app.route('/works/area/circle', methods=['GET', 'POST'])
def acircle():
    result = error = None
    if request.method == 'POST':
        r = to_num('radius')
        if r is None or r < 0: error = "Enter a radius of 0 or more."
        else: result = round(3.14 * r * r, 2)
    return render_template('circle.html', result=result, error=error)

@app.route('/works/area/triangle', methods=['GET', 'POST'])
def atriangle():
    result = error = None
    if request.method == 'POST':
        b, h = to_num('base'), to_num('height')
        if b is None or h is None or b < 0 or h < 0: error = "Enter a base and height of 0 or more."
        else: result = round(0.5 * b * h, 2)
    return render_template('triangle.html', result=result, error=error)

@app.route('/works/linkedlist', methods=['GET', 'POST'])
def linkedlist():
    msg = None
    if request.method == 'POST':
        act = request.form.get('action')
        val = request.form.get('value', '').strip()
        if act == 'reverse':
            ll.reverse(); msg = "List reversed."
        elif not val:
            msg = "Enter a value first."
        elif act == 'head': ll.insert_head(val); msg = f"{val} added to head."
        elif act == 'tail': ll.insert_tail(val); msg = f"{val} added to tail."
        elif act == 'delete':
            msg = f"{val} removed." if ll.delete(val) else f"{val} not found."
        elif act == 'search':
            i = ll.search(val)
            msg = f"{val} found at index {i}." if i >= 0 else f"{val} not found."
    return render_template('linkedlist.html', nodes=ll.to_list(), msg=msg)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)
