import inspect
import textwrap

from flask import Blueprint, render_template, request

bp = Blueprint("binary_tree", __name__)

WORK = {
    "order": 8,
    "href": "/works/binarytree",
    "title": "Binary Tree",
    "desc": "Insert, search, delete nodes and view the post-order traversal.",
    "category": "Data Structure",
}

MAX_NODES = 31
SAMPLE_KEYS = (50, 30, 70, 20, 40, 60, 80)


# ==================================================
# BINARY (SEARCH) TREE IMPLEMENTATION
# ==================================================

class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self):
        self.root = None

    # ---------- insert (needed so the tree can be built) ----------

    def insert(self, root, key):
        """Insert key into the subtree at root. Returns the subtree's root."""
        if root is None:
            return TreeNode(key)

        if key < root.key:
            root.left = self.insert(root.left, key)
        elif key > root.key:
            root.right = self.insert(root.right, key)

        return root

    # ---------- required method 1: search ----------

    def search(self, root, key):
        """Return the node that holds key, or None if it is not in the tree."""
        if root is None or root.key == key:
            return root

        if key < root.key:
            return self.search(root.left, key)

        return self.search(root.right, key)

    # ---------- required method 2: post_traversal ----------

    def post_traversal(self, start, traversal):
        """Post-order: Left -> Right -> Root. `traversal` is a list that
        collects the keys; the filled list is returned."""
        if start:
            traversal = self.post_traversal(start.left, traversal)
            traversal = self.post_traversal(start.right, traversal)
            traversal.append(start.key)

        return traversal

    # ---------- required method 3: delete_node ----------

    def delete_node(self, root, key):
        """Delete key from the subtree at root. Returns the new subtree root."""
        if root is None:
            return root

        if key < root.key:
            root.left = self.delete_node(root.left, key)

        elif key > root.key:
            root.right = self.delete_node(root.right, key)

        else:
            # Case 1 and 2: no child, or only one child
            if root.left is None:
                return root.right

            if root.right is None:
                return root.left

            # Case 3: two children -> copy the in-order successor
            # (smallest key in the right subtree), then delete it there.
            successor = self.min_node(root.right)
            root.key = successor.key
            root.right = self.delete_node(root.right, successor.key)

        return root

    # ---------- helpers used by the page ----------

    def min_node(self, node):
        while node.left:
            node = node.left

        return node

    def count(self, root):
        if root is None:
            return 0

        return 1 + self.count(root.left) + self.count(root.right)

    def height(self, root):
        if root is None:
            return 0

        return 1 + max(self.height(root.left), self.height(root.right))

    def search_path(self, key):
        """Keys visited while looking for key (to show the search route)."""
        path = []
        node = self.root

        while node:
            path.append(node.key)

            if key == node.key:
                break

            node = node.left if key < node.key else node.right

        return path

    def layout(self, highlight=None):
        """Pixel positions for drawing the tree as an SVG."""
        x_gap, y_gap, pad, radius = 56, 72, 36, 22
        nodes = []
        edges = []
        next_x = [0]

        def place(node, depth):
            if node is None:
                return None

            left = place(node.left, depth + 1)
            x = pad + next_x[0] * x_gap      # in-order position = x
            next_x[0] += 1
            y = pad + depth * y_gap
            right = place(node.right, depth + 1)

            entry = {"key": node.key, "x": x, "y": y,
                     "hit": node.key == highlight}
            nodes.append(entry)

            for child in (left, right):
                if child:
                    edges.append({"x1": x, "y1": y,
                                  "x2": child["x"], "y2": child["y"]})

            return entry

        place(self.root, 0)

        return {
            "nodes": nodes,
            "edges": edges,
            "width": pad * 2 + max(next_x[0] - 1, 0) * x_gap,
            "height": pad * 2 + max(self.height(self.root) - 1, 0) * y_gap,
            "radius": radius,
        }


def build_sample_tree():
    tree = BinaryTree()

    for key in SAMPLE_KEYS:
        tree.root = tree.insert(tree.root, key)

    return tree


tree = build_sample_tree()


def method_source(method):
    """Real source of a method, shown on the page so it always matches."""
    return textwrap.dedent(inspect.getsource(method))


# ==================================================
# BINARY TREE PAGE
# ==================================================

@bp.route("/works/binarytree", methods=["GET", "POST"])
def binary_tree_page():
    global tree

    msg = None
    traversal = None
    highlight = None

    if request.method == "POST":
        action = request.form.get("action")
        raw = request.form.get("value", "").strip()

        if action == "reset":
            tree = build_sample_tree()
            msg = "Tree reset to the sample tree."

        elif action == "clear":
            tree = BinaryTree()
            msg = "Tree cleared."

        elif action == "postorder":
            if tree.root is None:
                msg = "The tree is empty. Insert a number first."
            else:
                traversal = tree.post_traversal(tree.root, [])
                msg = "Post-order traversal (Left, Right, Root) complete."

        else:
            try:
                key = int(raw)
            except ValueError:
                key = None

            if key is None:
                msg = "Enter a whole number first."

            elif action == "insert":
                if tree.search(tree.root, key):
                    msg = f"{key} is already in the tree."
                elif tree.count(tree.root) >= MAX_NODES:
                    msg = f"The tree can hold at most {MAX_NODES} nodes on this page."
                else:
                    tree.root = tree.insert(tree.root, key)
                    highlight = key
                    msg = f"{key} inserted."

            elif action == "search":
                node = tree.search(tree.root, key)
                path = " → ".join(str(k) for k in tree.search_path(key))

                if node:
                    highlight = key
                    msg = f"{key} found. Path: {path}"
                elif path:
                    msg = f"{key} not found. Path checked: {path}"
                else:
                    msg = f"{key} not found. The tree is empty."

            elif action == "delete":
                if tree.search(tree.root, key) is None:
                    msg = f"{key} not found, nothing deleted."
                else:
                    tree.root = tree.delete_node(tree.root, key)
                    msg = f"{key} deleted."

    return render_template(
        "binary_tree.html",
        layout=tree.layout(highlight),
        size=tree.count(tree.root),
        height=tree.height(tree.root),
        traversal=traversal,
        msg=msg,
        code={
            "search": method_source(BinaryTree.search),
            "post_traversal": method_source(BinaryTree.post_traversal),
            "delete_node": method_source(BinaryTree.delete_node),
        },
    )
