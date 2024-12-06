import itertools
from flask import Flask, render_template, request
import os

app = Flask(__name__, template_folder='/Users/clayelzinga/Desktop/Work_School/School/Lit_Review/24application/')

operations = ['+', '-', '*', '/']

def apply_op(a, b, op):
    if op == '/' and b == 0:
        return None
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        return a / b

def close_enough(val, target=24, eps=1e-9):
    return abs(val - target) < eps

def try_operations(a, b, c, d):
    results = []
    for ops in itertools.product(operations, repeat=3):
        op1, op2, op3 = ops

        # ((a op b) op c) op d
        r1 = apply_op(a, b, op1)
        if r1 is not None:
            r2 = apply_op(r1, c, op2)
            if r2 is not None:
                r3 = apply_op(r2, d, op3)
                if r3 is not None and close_enough(r3):
                    results.append(f'(({a} {op1} {b}) {op2} {c}) {op3} {d} = 24')

        # (a op (b op c)) op d
        r1 = apply_op(b, c, op2)
        if r1 is not None:
            r2 = apply_op(a, r1, op1)
            if r2 is not None:
                r3 = apply_op(r2, d, op3)
                if r3 is not None and close_enough(r3):
                    results.append(f'({a} {op1} ({b} {op2} {c})) {op3} {d} = 24')

        # (a op b) op (c op d)
        r1 = apply_op(a, b, op1)
        r2 = apply_op(c, d, op3)
        if r1 is not None and r2 is not None:
            r3 = apply_op(r1, r2, op2)
            if r3 is not None and close_enough(r3):
                results.append(f'({a} {op1} {b}) {op2} ({c} {op3} {d}) = 24')

        # a op ((b op c) op d)
        r1 = apply_op(b, c, op2)
        if r1 is not None:
            r2 = apply_op(r1, d, op3)
            if r2 is not None:
                r3 = apply_op(a, r2, op1)
                if r3 is not None and close_enough(r3):
                    results.append(f'{a} {op1} (({b} {op2} {c}) {op3} {d}) = 24')

        # a op (b op (c op d))
        r1 = apply_op(c, d, op3)
        if r1 is not None:
            r2 = apply_op(b, r1, op2)
            if r2 is not None:
                r3 = apply_op(a, r2, op1)
                if r3 is not None and close_enough(r3):
                    results.append(f'{a} {op1} ({b} {op2} ({c} {op3} {d})) = 24')

    return results

def find_solutions(numbers):
    found_expressions = set()
    for nums in itertools.permutations(numbers):
        a, b, c, d = nums
        valid_exprs = try_operations(a, b, c, d)
        for expr in valid_exprs:
            found_expressions.add(expr)
    return found_expressions

@app.route("/", methods=["GET", "POST"])
def home():
    solutions = None
    if request.method == "POST":
        try:
            # Get each number from the form
            num1 = int(request.form.get("num1"))
            num2 = int(request.form.get("num2"))
            num3 = int(request.form.get("num3"))
            num4 = int(request.form.get("num4"))

            numbers = [num1, num2, num3, num4]
            solutions = find_solutions(numbers)
            if not solutions:
                solutions = ["No solutions found."]
        except ValueError:
            solutions = ["Invalid input. Please enter four numbers."]
    return render_template("24application.html", solutions=solutions)

if __name__ == "__main__":
    app.run()
    




