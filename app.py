from flask import Flask, render_template, request, redirect, url_for
import redis

app = Flask(__name__)

# Redis connection (Docker service name = redis)
r = redis.Redis(host="redis", port=6379, decode_responses=True)

TASK_LIST = "todos"          # list of task IDs (order)
TASK_COUNTER = "todo_counter"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task = request.form.get("task")

        if task:
            # ATOMIC counter increment (concurrency-safe)
            task_id = r.incr(TASK_COUNTER)

            # store task data WITH index
            r.hset(
                f"todo:{task_id}",
                mapping={
                    "task": task,
                    "done": "0",
                    "index": task_id
                }
            )

            # maintain order
            r.rpush(TASK_LIST, task_id)

        return redirect(url_for("index"))

    # fetch all tasks
    todos = []
    task_ids = r.lrange(TASK_LIST, 0, -1)

    for tid in task_ids:
        data = r.hgetall(f"todo:{tid}")
        todos.append({
            "id": int(tid),
            "index": int(data.get("index", tid)),  # fallback safe
            "task": data.get("task"),
            "done": data.get("done") == "1"
        })

    return render_template("index.html", todos=todos)


@app.route("/complete/<int:todo_id>")
def complete(todo_id):
    r.hset(f"todo:{todo_id}", "done", "1")
    return redirect(url_for("index"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    r.delete(f"todo:{todo_id}")
    r.lrem(TASK_LIST, 0, todo_id)
    return redirect(url_for("index"))


@app.route("/health")
def health():
    return {"status": "UP"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
