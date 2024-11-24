# ABOUT: This file contains the gunicorn hooks, which perform special 
#  functionality outside of the normal flask runtime

import os
from pathlib import Path


# Runs once when the master Gunicorn process starts. Useful for setting up 
#  resources needed across all workers.
# def on_starting(server): 
#     pass

# Runs after each worker is forked. Good for creating per-worker instances of 
#  resources.
def post_fork(server, worker): 
    Path(f"img_file{worker.pid}.jpg").touch(exist_ok=True)

    # print(f"worker!! {worker}")
    # print(type(worker))
    # print(vars(worker))


# # Runs when a worker exits. Useful for cleanup.
def worker_exit(server, worker): 
    os.remove(f"img_file{worker.pid}.jpg")
    # print(f"worker exit!! {worker}")



# # Runs when the master process is shutting down. Useful for global cleanup
# def on_exit(server): 
#     pass



# NOTE: I think there can also be hooks that trigger on signals, like int, etc.