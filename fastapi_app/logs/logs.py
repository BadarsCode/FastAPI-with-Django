from fastapi import BackgroundTasks

def write_log(message: str):
    with open('./logs/logs.txt', 'a') as file:
        file.write(message + "\n")
