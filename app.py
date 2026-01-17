from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Shared in-memory todo list
todos = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task = request.form.get("task")
        if task:
            todos.append({
                "id": len(todos),
                "task": task,
                "done": False
            })
        return redirect(url_for("index"))

    return render_template("index.html", todos=todos)

@app.route("/complete/<int:todo_id>")
def complete(todo_id):
    if 0 <= todo_id < len(todos):
        todos[todo_id]["done"] = True
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    if 0 <= todo_id < len(todos):
        todos.pop(todo_id)
    return redirect(url_for("index"))

@app.route("/health")
def health():
    return {"status": "UP"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
