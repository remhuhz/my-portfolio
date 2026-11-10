from flask import Blueprint, render_template, request

bp = Blueprint("queue", __name__)

WORK = {
    "order": 6,
    "href": "/works/queue",
    "title": "Queue Algorithm",
    "desc": "Implement a queue using Enqueue, Dequeue, Peek, and display operations.",
    "category": "Data Structure",
}


# ==================================================
# QUEUE IMPLEMENTATION - ENQUEUE AND DEQUEUE
# ==================================================

class QueueNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def enqueue(self, data):
        node = QueueNode(data)

        if self.rear is None:
            self.front = node
            self.rear = node
        else:
            self.rear.next = node
            self.rear = node

        self.size += 1

    def dequeue(self):
        if self.front is None:
            return None

        node = self.front
        self.front = self.front.next

        if self.front is None:
            self.rear = None

        node.next = None
        self.size -= 1

        return node.data

    def peek(self):
        if self.front is None:
            return None

        return self.front.data

    def to_list(self):
        elements = []
        current = self.front

        while current:
            elements.append(current.data)
            current = current.next

        return elements

    def is_empty(self):
        return self.front is None

    def clear(self):
        self.front = None
        self.rear = None
        self.size = 0


queue = Queue()


# ==================================================
# QUEUE PAGE - ENQUEUE AND DEQUEUE
# ==================================================

@bp.route("/works/queue", methods=["GET", "POST"])
def queue_page():
    msg = None

    if request.method == "POST":
        action = request.form.get("action")
        value = request.form.get("value", "").strip()

        if action == "enqueue":
            if not value:
                msg = "Enter a value to enqueue."
            else:
                queue.enqueue(value)
                msg = f"{value} enqueued at the rear."

        elif action == "dequeue":
            removed = queue.dequeue()

            if removed is None:
                msg = "Queue is empty. Nothing to dequeue."
            else:
                msg = f"Dequeued element: {removed}"

        elif action == "peek":
            front_value = queue.peek()

            if front_value is None:
                msg = "Queue is empty. No front element."
            else:
                msg = f"Front element: {front_value}"

        elif action == "clear":
            queue.clear()
            msg = "Queue cleared."

    return render_template("queue.html", elements=queue.to_list(), msg=msg)
