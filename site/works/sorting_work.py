import math
import re

from flask import Blueprint, render_template, request

bp = Blueprint("sorting", __name__)

WORK = {
    "order": 7,
    "href": "/works/sorting",
    "title": "Sorting Algorithm",
    "desc": "Bubble, Selection, Insertion, Merge and Quick sort, step by step.",
    "category": "Data Structure",
}

MAX_ITEMS = 20
DEFAULT_NUMBERS = "64, 25, 12, 22, 11, 90, 5"


# ==================================================
# SORTING IMPLEMENTATIONS
# Each function sorts a COPY of the list and returns:
#   sorted      -> the sorted list
#   steps       -> snapshots shown on the page
#   comparisons -> how many comparisons were made
#   moves       -> swaps / shifts / merged items
# ==================================================

def _start_step(data):
    return {"label": "Start: original list", "data": data[:], "marked": []}


def bubble_sort(values):
    a = list(values)
    n = len(a)
    comparisons = swaps = 0
    steps = [_start_step(a)]

    for i in range(n - 1):
        swapped = False

        for j in range(n - i - 1):
            comparisons += 1

            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True

        if swapped:
            label = f"Pass {i + 1}: the largest remaining value moved to index {n - i - 1}"
        else:
            label = f"Pass {i + 1}: no swaps needed, the list is already sorted"

        steps.append({
            "label": label,
            "data": a[:],
            "marked": list(range(n - i - 1, n)),
        })

        if not swapped:
            break

    return {"sorted": a, "steps": steps,
            "comparisons": comparisons, "moves": swaps}


def selection_sort(values):
    a = list(values)
    n = len(a)
    comparisons = swaps = 0
    steps = [_start_step(a)]

    for i in range(n - 1):
        smallest = i

        for j in range(i + 1, n):
            comparisons += 1

            if a[j] < a[smallest]:
                smallest = j

        if smallest != i:
            a[i], a[smallest] = a[smallest], a[i]
            swaps += 1

        steps.append({
            "label": f"Pass {i + 1}: smallest remaining value {a[i]} placed at index {i}",
            "data": a[:],
            "marked": list(range(0, i + 1)),
        })

    return {"sorted": a, "steps": steps,
            "comparisons": comparisons, "moves": swaps}


def insertion_sort(values):
    a = list(values)
    n = len(a)
    comparisons = shifts = 0
    steps = [_start_step(a)]

    for i in range(1, n):
        key = a[i]
        j = i - 1

        while j >= 0:
            comparisons += 1

            if a[j] > key:
                a[j + 1] = a[j]
                shifts += 1
                j -= 1
            else:
                break

        a[j + 1] = key

        steps.append({
            "label": f"Insert {key} into the sorted part (indices 0 to {i})",
            "data": a[:],
            "marked": list(range(0, i + 1)),
        })

    return {"sorted": a, "steps": steps,
            "comparisons": comparisons, "moves": shifts}


def merge_sort(values):
    a = list(values)
    comparisons = 0
    moves = 0
    steps = [_start_step(a)]

    def sort(low, high):
        """Sort a[low:high] (high is exclusive)."""
        nonlocal comparisons, moves

        if high - low <= 1:
            return

        mid = (low + high) // 2
        sort(low, mid)
        sort(mid, high)

        left = a[low:mid]
        right = a[mid:high]
        i = j = 0
        k = low

        while i < len(left) and j < len(right):
            comparisons += 1

            if left[i] <= right[j]:
                a[k] = left[i]
                i += 1
            else:
                a[k] = right[j]
                j += 1

            k += 1
            moves += 1

        while i < len(left):
            a[k] = left[i]
            i += 1
            k += 1
            moves += 1

        while j < len(right):
            a[k] = right[j]
            j += 1
            k += 1
            moves += 1

        steps.append({
            "label": f"Merge {left} and {right}",
            "data": a[:],
            "marked": list(range(low, high)),
        })

    sort(0, len(a))

    return {"sorted": a, "steps": steps,
            "comparisons": comparisons, "moves": moves}


def quick_sort(values):
    a = list(values)
    comparisons = swaps = 0
    steps = [_start_step(a)]

    def partition(low, high):
        """Lomuto partition: the last item is the pivot."""
        nonlocal comparisons, swaps

        pivot = a[high]
        i = low - 1

        for j in range(low, high):
            comparisons += 1

            if a[j] <= pivot:
                i += 1

                if i != j:
                    a[i], a[j] = a[j], a[i]
                    swaps += 1

        if i + 1 != high:
            a[i + 1], a[high] = a[high], a[i + 1]
            swaps += 1

        return i + 1

    def sort(low, high):
        """Sort a[low..high] (both ends inclusive)."""
        if low >= high:
            return

        pivot_index = partition(low, high)

        steps.append({
            "label": f"Pivot {a[pivot_index]} placed at index {pivot_index}",
            "data": a[:],
            "marked": [pivot_index],
        })

        sort(low, pivot_index - 1)
        sort(pivot_index + 1, high)

    sort(0, len(a) - 1)

    return {"sorted": a, "steps": steps,
            "comparisons": comparisons, "moves": swaps}


# ==================================================
# ALGORITHM INFO (shown in the tabs on the page)
# The code strings are clean teaching versions.
# ==================================================

ALGORITHMS = {
    "bubble": {
        "name": "Bubble Sort",
        "func": bubble_sort,
        "moves_label": "Swaps",
        "idea": (
            "Walk through the list again and again, comparing neighbours "
            "and swapping them when they are in the wrong order. After "
            "each pass the largest remaining value has bubbled to the end."
        ),
        "best": "O(n)", "average": "O(n²)", "worst": "O(n²)",
        "space": "O(1)", "stable": "Yes",
        "code": '''def bubble_sort(a):
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:      # already sorted
            break
    return a''',
    },
    "selection": {
        "name": "Selection Sort",
        "func": selection_sort,
        "moves_label": "Swaps",
        "idea": (
            "Find the smallest value in the unsorted part and swap it "
            "into the next position at the front. Repeat until the whole "
            "list is sorted."
        ),
        "best": "O(n²)", "average": "O(n²)", "worst": "O(n²)",
        "space": "O(1)", "stable": "No",
        "code": '''def selection_sort(a):
    n = len(a)
    for i in range(n - 1):
        smallest = i
        for j in range(i + 1, n):
            if a[j] < a[smallest]:
                smallest = j
        a[i], a[smallest] = a[smallest], a[i]
    return a''',
    },
    "insertion": {
        "name": "Insertion Sort",
        "func": insertion_sort,
        "moves_label": "Shifts",
        "idea": (
            "Build the sorted list one item at a time, like sorting "
            "playing cards in your hand: take the next value and slide it "
            "left until it sits in the right place."
        ),
        "best": "O(n)", "average": "O(n²)", "worst": "O(n²)",
        "space": "O(1)", "stable": "Yes",
        "code": '''def insertion_sort(a):
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]      # shift right
            j -= 1
        a[j + 1] = key
    return a''',
    },
    "merge": {
        "name": "Merge Sort",
        "func": merge_sort,
        "moves_label": "Items merged",
        "idea": (
            "Divide and conquer: split the list in half, sort each half "
            "recursively, then merge the two sorted halves into one "
            "sorted list."
        ),
        "best": "O(n log n)", "average": "O(n log n)", "worst": "O(n log n)",
        "space": "O(n)", "stable": "Yes",
        "code": '''def merge_sort(a):
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left = merge_sort(a[:mid])
    right = merge_sort(a[mid:])

    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged''',
    },
    "quick": {
        "name": "Quick Sort",
        "func": quick_sort,
        "moves_label": "Swaps",
        "idea": (
            "Pick a pivot, move smaller values to its left and larger "
            "values to its right, then sort the left and right parts "
            "recursively. The pivot ends up in its final position."
        ),
        "best": "O(n log n)", "average": "O(n log n)", "worst": "O(n²)",
        "space": "O(log n)", "stable": "No",
        "code": '''def quick_sort(a, low, high):
    if low < high:
        p = partition(a, low, high)
        quick_sort(a, low, p - 1)
        quick_sort(a, p + 1, high)
    return a


def partition(a, low, high):
    pivot = a[high]              # last item is the pivot
    i = low - 1
    for j in range(low, high):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[high] = a[high], a[i + 1]
    return i + 1''',
    },
}


# ==================================================
# INPUT PARSING
# ==================================================

def parse_numbers(raw):
    """Turn '5, 3 8' into [5, 3, 8]. Raises ValueError with a friendly message."""
    parts = [p for p in re.split(r"[,\s]+", raw.strip()) if p]

    if not parts:
        raise ValueError("Enter at least one number, separated by commas.")

    if len(parts) > MAX_ITEMS:
        raise ValueError(f"Please enter at most {MAX_ITEMS} numbers.")

    numbers = []

    for part in parts:
        try:
            value = float(part)
        except ValueError:
            raise ValueError(f"'{part}' is not a number.") from None

        if not math.isfinite(value) or abs(value) > 1_000_000_000:
            raise ValueError(f"'{part}' is out of range (use -1,000,000,000 to 1,000,000,000).")

        numbers.append(int(value) if value.is_integer() else value)

    return numbers


# ==================================================
# SORTING PAGE
# ==================================================

@bp.route("/works/sorting", methods=["GET", "POST"])
def sorting_page():
    raw = DEFAULT_NUMBERS
    error = None
    result = None
    comparison = None
    selected = None

    if request.method == "POST":
        raw = request.form.get("numbers", "").strip()
        action = request.form.get("action", "")

        try:
            numbers = parse_numbers(raw)

            if action == "compare":
                comparison = []

                for key, info in ALGORITHMS.items():
                    run = info["func"](numbers)
                    comparison.append({
                        "name": info["name"],
                        "comparisons": run["comparisons"],
                        "moves": run["moves"],
                        "moves_label": info["moves_label"],
                    })

                result = {
                    "sorted": sorted(numbers),
                    "name": "All five algorithms",
                    "original": numbers,
                }

            elif action in ALGORITHMS:
                info = ALGORITHMS[action]
                run = info["func"](numbers)
                selected = action

                result = {
                    "name": info["name"],
                    "original": numbers,
                    "moves_label": info["moves_label"],
                    **run,
                }

            else:
                error = "Choose a sorting algorithm."

        except ValueError as exc:
            error = str(exc)

    return render_template(
        "sorting.html",
        algorithms=ALGORITHMS,
        raw=raw,
        error=error,
        result=result,
        comparison=comparison,
        selected=selected,
        max_items=MAX_ITEMS,
    )
