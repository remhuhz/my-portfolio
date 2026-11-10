from flask import Blueprint, render_template, request

bp = Blueprint("stack", __name__)

WORK = {
    "order": 5,
    "href": "/works/stack",
    "title": "Stack Algorithm",
    "desc": "Implement a stack using Push, Pop, Peek, and display operations.",
    "category": "Data Structure",
}


# ==================================================
# STACK IMPLEMENTATION - LAB EXERCISE #5
# ==================================================

class StackNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:
    def __init__(self):
        self.top = None

    def push(self, data):
        node = StackNode(data)
        node.next = self.top
        self.top = node

    def pop(self):
        if self.top is None:
            return None

        node = self.top
        self.top = self.top.next
        node.next = None

        return node.data

    def peek(self):
        if self.top is None:
            return None

        return self.top.data

    def to_list(self):
        elements = []
        current = self.top

        while current:
            elements.append(current.data)
            current = current.next

        return elements

    def is_empty(self):
        return self.top is None

    def clear(self):
        self.top = None


stack = Stack()


# ==================================================
# STACK PAGE - LAB EXERCISE #5
# ==================================================

@bp.route("/works/stack", methods=["GET", "POST"])
def stack_page():
    msg = None

    if request.method == "POST":
        action = request.form.get("action")
        value = request.form.get("value", "").strip()

        if action == "push":
            if not value:
                msg = "Enter a value to push."
            else:
                stack.push(value)
                msg = f"{value} pushed onto the stack."

        elif action == "pop":
            popped = stack.pop()

            if popped is None:
                msg = "Stack is empty. Nothing to pop."
            else:
                msg = f"Popped element: {popped}"

        elif action == "peek":
            top_value = stack.peek()

            if top_value is None:
                msg = "Stack is empty. No top element."
            else:
                msg = f"Top element: {top_value}"

        elif action == "clear":
            stack.clear()
            msg = "Stack cleared."

    return render_template(
        "stack.html",
        elements=stack.to_list(),
        top=stack.peek(),
        msg=msg,
    )
