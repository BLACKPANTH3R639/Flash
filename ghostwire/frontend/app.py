
from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)
API_URL = "http://localhost:8000/api"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/agents")
def agents():
    return render_template("agents.html")

@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    if request.method == "POST":
        agent_id = request.form["agent_id"]
        command = request.form["command"]
        requests.post(f"{API_URL}/tasks/{agent_id}/add", json={
            "task_id": "web-task",
            "command": command
        })
        return redirect("/tasks")
    return render_template("tasks.html")

@app.route("/results")
def results():
    r = requests.get(f"{API_URL}/results")
    return render_template("results.html", results=r.json())

if __name__ == "__main__":
    app.run(debug=True)
