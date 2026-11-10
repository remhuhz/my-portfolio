from flask import Blueprint, render_template, request

bp = Blueprint("linkedlist", __name__)

WORK = {
    "order": 4,
    "href": "/works/linkedlist",
    "title": "Linked List",
    "desc": "Add, remove, search and reverse nodes.",
    "category": "Data Structure",
}


# ==================================================
# LINKED LIST IMPLEMENTATION
# ==================================================

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def to_list(self):
        result = []
        current = self.head

        while current:
            result.append(current.data)
            current = current.next

        return result

    def insert_head(self, data):
        node = Node(data)
        node.next = self.head
        self.head = node

    def insert_tail(self, data):
        node = Node(data)

        if self.head is None:
            self.head = node
            return

        current = self.head

        while current.next:
            current = current.next

        current.next = node

    def delete(self, data):
        current = self.head
        previous = None

        while current:
            if current.data == data:
                if previous:
                    previous.next = current.next
                else:
                    self.head = current.next

                return True

            previous = current
            current = current.next

        return False

    def search(self, data):
        for index, value in enumerate(self.to_list()):
            if value == data:
                return index

        return -1

    def reverse(self):
        previous = None
        current = self.head

        while current:
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node

        self.head = previous


ll = LinkedList()

for value in ("Jett", "Sage", "Omen"):
    ll.insert_tail(value)


# ==================================================
# LINKED LIST PAGE
# ==================================================

@bp.route("/works/linkedlist", methods=["GET", "POST"])
def linkedlist():
    msg = None

    if request.method == "POST":
        action = request.form.get("action")
        value = request.form.get("value", "").strip()

        if action == "reverse":
            ll.reverse()
            msg = "List reversed."

        elif not value:
            msg = "Enter a value first."

        elif action == "head":
            ll.insert_head(value)
            msg = f"{value} added to head."

        elif action == "tail":
            ll.insert_tail(value)
            msg = f"{value} added to tail."

        elif action == "delete":
            if ll.delete(value):
                msg = f"{value} removed."
            else:
                msg = f"{value} not found."

        elif action == "search":
            index = ll.search(value)

            if index >= 0:
                msg = f"{value} found at index {index}."
            else:
                msg = f"{value} not found."

    return render_template("linkedlist.html", nodes=ll.to_list(), msg=msg)
