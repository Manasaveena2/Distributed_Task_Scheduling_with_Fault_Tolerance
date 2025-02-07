# from flask import Flask, render_template
# from flask_socketio import SocketIO
# import queue
# import threading
# import time
# import random

# # Initialize Flask app and SocketIO
# app = Flask(__name__)
# socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# # Task queue and order tracking
# task_queue = queue.PriorityQueue()
# workers = {}
# order_status = {}
# completed_tasks = {}
# dependency_graph = {}
# lock = threading.Lock()

# # Configuration
# CHECK_INTERVAL = 5
# MAX_WORKERS = 5
# MIN_WORKERS = 2
# RETRY_LIMIT = 3
# WORKER_TIMEOUT = 10

# @app.route('/')
# def index():
#     return render_template('dashboard.html')

# def emit_update(update_data):
#     """Emit updates to the WebSocket."""
#     socketio.emit('update', update_data)

# def process_order(order_id, worker_id):
#     """Processes an order through payment, packing, and shipping with fault tolerance."""
#     stages = ["payment", "packing", "shipping"]
    
#     for stage in stages:
#         with lock:
#             if order_id not in order_status:
#                 return
#             order_status[order_id][stage] = f"Processing by {worker_id}"
#             order_status[order_id][f"worker_{stage}"] = worker_id
#         socketio.emit("update", {order_id: order_status[order_id]})

#         time.sleep(2)  # Simulate processing time
        
#         if stage == "payment" and not process_payment(order_id, worker_id):  # Retry logic for payment
#             with lock:
#                 order_status[order_id]["payment"] = f"Failed by {worker_id}"
#                 order_status[order_id]["overall"] = "Failed ❌"
#             socketio.emit("update", {order_id: order_status[order_id]})
#             return

#         with lock:
#             order_status[order_id][stage] = f"Completed by {worker_id}"
#             if stage == "shipping":
#                 order_status[order_id]["overall"] = "Completed ✅"
#         socketio.emit("update", {order_id: order_status[order_id]})

# def process_payment(order_id, worker_id):
#     """Simulates payment processing with retries and logs failures."""
#     attempts = 0
#     while attempts < RETRY_LIMIT:
#         time.sleep(2)  # Simulate processing time
#         if random.random() > 0.3:  # 70% success rate
#             return True
        
#         attempts += 1
#         with lock:
#             order_status[order_id]["retries"] = attempts  # Track retry attempts
#             log_message = f"🔄 Payment retry {attempts} for Order {order_id} by Worker {worker_id}"
#             if "logs" not in order_status[order_id]:
#                 order_status[order_id]["logs"] = []
#             order_status[order_id]["logs"].append(log_message)

#         # Emit update to the dashboard
#         socketio.emit("update", {order_id: order_status[order_id]})

#     # If all retries fail, log the failure
#     with lock:
#         log_message = f"❌ Payment failed for Order {order_id} after {RETRY_LIMIT} retries."
#         order_status[order_id]["logs"].append(log_message)
    
#     socketio.emit("update", {order_id: order_status[order_id]})
#     return False



# def worker(name):
#     """Worker function to process tasks from the queue with fault tolerance."""
#     while True:
#         try:
#             priority, order_id, task_name = task_queue.get(timeout=CHECK_INTERVAL)
#         except queue.Empty:
#             with lock:
#                 if name in workers:
#                     del workers[name]
#             return
        
#         workers[name] = time.time()
#         process_order(order_id, name)
#         with lock:
#             if name in workers:
#                 del workers[name]

# def monitor_workers():
#     """Monitors and adjusts worker threads based on queue size and detects failures."""
#     while True:
#         time.sleep(CHECK_INTERVAL)
#         queue_size = task_queue.qsize()

#         with lock:
#             num_workers = len(workers)
#             if queue_size > num_workers and num_workers < MAX_WORKERS:
#                 t_name = f"Worker-{num_workers+1}"
#                 t = threading.Thread(target=worker, args=(t_name,), daemon=True)
#                 t.start()
#                 workers[t_name] = time.time()

#             # Detect crashed workers
#             now = time.time()
#             inactive_workers = [w for w, last_seen in workers.items() if now - last_seen > WORKER_TIMEOUT]
#             for w in inactive_workers:
#                 del workers[w]
#                 reassign_tasks(w)


# def reassign_tasks(worker_id):
#     """Reassigns unfinished tasks if a worker fails and logs the event."""
#     with lock:
#         for order_id, status in order_status.items():
#             for stage in ["payment", "packing", "shipping"]:
#                 if status.get(f"worker_{stage}") == worker_id and "Completed" not in status[stage]:
#                     task_queue.put((1, order_id, stage))
#                     status[stage] = "Reassigned"
#                     status[f"worker_{stage}"] = None

#                     log_message = f"⚠️ Worker {worker_id} crashed. Task {stage} for Order {order_id} reassigned."
#                     if "logs" not in order_status[order_id]:
#                         order_status[order_id]["logs"] = []
#                     order_status[order_id]["logs"].append(log_message)

#         socketio.emit("update", order_status)


# def add_order(order_id):
#     """Adds a new order to the task queue and maintains task dependencies."""
#     dependency_graph[order_id] = ["payment", "packing", "shipping"]
#     task_queue.put((1, order_id, "payment"))
#     with lock:
#         order_status[order_id] = {
#             "payment": "Awaiting Payment",
#             "packing": "Pending",
#             "shipping": "Pending",
#             "overall": "Processing",
#             "worker_payment": None,
#             "worker_packing": None,
#             "worker_shipping": None,
#         }
#     socketio.emit('update', order_status)

# def start_system():
#     """Starts the initial workers and monitoring thread."""
#     for i in range(MIN_WORKERS):
#         t_name = f"Worker-{i+1}"
#         t = threading.Thread(target=worker, args=(t_name,), daemon=True)
#         t.start()
#         workers[t_name] = time.time()

#     monitor_thread = threading.Thread(target=monitor_workers, daemon=True)
#     monitor_thread.start()

#     time.sleep(1)
#     add_order(101)
#     time.sleep(2)
#     add_order(102)
#     time.sleep(2)
#     add_order(103)
#     add_order(104)
#     add_order(105)

# if __name__ == "__main__":
#     threading.Thread(target=start_system, daemon=True).start()
#     socketio.run(app, debug=True)


from flask import Flask, render_template
from flask_socketio import SocketIO
import queue
import threading
import time
import random

# Initialize Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# Task queue and order tracking
task_queue = queue.PriorityQueue()
workers = {}
order_status = {}
completed_tasks = {}
dependency_graph = {}
lock = threading.Lock()

# Configuration
CHECK_INTERVAL = 10
MAX_WORKERS = 5
MIN_WORKERS = 2
RETRY_LIMIT = 3
WORKER_TIMEOUT = 10

@app.route('/')
def index():
    return render_template('dashboard.html')

@socketio.on("connect")
def handle_connect():
    """Send current order status to newly connected clients."""
    with lock:
        socketio.emit("update", order_status)  # Send full existing data

def emit_update(update_data):
    """Emit updates to the WebSocket."""
    socketio.emit('update', update_data)

def process_order(order_id, worker_id):
    """Processes an order through payment, packing, and shipping with fault tolerance."""
    stages = ["payment", "packing", "shipping"]
    
    for stage in stages:
        with lock:
            if order_id not in order_status:
                return
            order_status[order_id][stage] = f"Processing by {worker_id}"
            order_status[order_id][f"worker_{stage}"] = worker_id
        socketio.emit("update", {order_id: order_status[order_id]})

        time.sleep(2)  # Simulate processing time
        
        if stage == "payment" and not process_payment(order_id, worker_id):  # Retry logic for payment
            with lock:
                order_status[order_id]["payment"] = f"Failed by {worker_id}"
                order_status[order_id]["overall"] = "Failed ❌"
            socketio.emit("update", {order_id: order_status[order_id]})
            return

        with lock:
            order_status[order_id][stage] = f"Completed by {worker_id}"
            if stage == "shipping":
                order_status[order_id]["overall"] = "Completed ✅"
        socketio.emit("update", {order_id: order_status[order_id]})

def process_payment(order_id, worker_id):
    """Simulates payment processing with retries and logs failures."""
    attempts = 0
    while attempts < RETRY_LIMIT:
        time.sleep(2)  # Simulate processing time
        if random.random() > 0.3:  # 70% success rate
            return True
        
        attempts += 1
        with lock:
            order_status[order_id]["retries"] = attempts  # Track retry attempts
            log_message = f"🔄 Payment retry {attempts} for Order {order_id} by Worker {worker_id}"
            if "logs" not in order_status[order_id]:
                order_status[order_id]["logs"] = []
            order_status[order_id]["logs"].append(log_message)

        # Emit update to the dashboard
        socketio.emit("update", {order_id: order_status[order_id]})

    # If all retries fail, log the failure
    with lock:
        log_message = f"❌ Payment failed for Order {order_id} after {RETRY_LIMIT} retries."
        order_status[order_id]["logs"].append(log_message)
    
    socketio.emit("update", {order_id: order_status[order_id]})
    return False

def worker(name):
    """Worker function to process tasks from the queue with fault tolerance."""
    while True:
        try:
            priority, order_id, task_name = task_queue.get(timeout=CHECK_INTERVAL)
        except queue.Empty:
            with lock:
                if name in workers:
                    del workers[name]
            return
        
        workers[name] = time.time()
        process_order(order_id, name)
        with lock:
            if name in workers:
                del workers[name]

def monitor_workers():
    """Monitors and adjusts worker threads based on queue size and detects failures."""
    while True:
        time.sleep(CHECK_INTERVAL)
        queue_size = task_queue.qsize()

        with lock:
            num_workers = len(workers)
            if queue_size > num_workers and num_workers < MAX_WORKERS:
                t_name = f"Worker-{num_workers+1}"
                t = threading.Thread(target=worker, args=(t_name,), daemon=True)
                t.start()
                workers[t_name] = time.time()

            # Detect crashed workers
            now = time.time()
            inactive_workers = [w for w, last_seen in workers.items() if now - last_seen > WORKER_TIMEOUT]
            for w in inactive_workers:
                del workers[w]
                reassign_tasks(w)

def reassign_tasks(worker_id):
    """Reassigns unfinished tasks if a worker fails and logs the event."""
    with lock:
        for order_id, status in order_status.items():
            for stage in ["payment", "packing", "shipping"]:
                if status.get(f"worker_{stage}") == worker_id and "Completed" not in status[stage]:
                    task_queue.put((1, order_id, stage))
                    status[stage] = "Reassigned"
                    status[f"worker_{stage}"] = None

                    log_message = f"⚠️ Worker {worker_id} crashed. Task {stage} for Order {order_id} reassigned."
                    if "logs" not in order_status[order_id]:
                        order_status[order_id]["logs"] = []
                    order_status[order_id]["logs"].append(log_message)

        socketio.emit("update", order_status)

def add_order(order_id):
    """Adds a new order to the task queue and maintains task dependencies."""
    dependency_graph[order_id] = ["payment", "packing", "shipping"]
    task_queue.put((1, order_id, "payment"))
    with lock:
        order_status[order_id] = {
            "payment": "Awaiting Payment",
            "packing": "Pending",
            "shipping": "Pending",
            "overall": "Processing",
            "worker_payment": None,
            "worker_packing": None,
            "worker_shipping": None,
        }
    socketio.emit('update', order_status)

def start_system():
    """Starts the initial workers and monitoring thread."""
    for i in range(MIN_WORKERS):
        t_name = f"Worker-{i+1}"
        t = threading.Thread(target=worker, args=(t_name,), daemon=True)
        t.start()
        workers[t_name] = time.time()

    monitor_thread = threading.Thread(target=monitor_workers, daemon=True)
    monitor_thread.start()

    time.sleep(1)
    add_order(101)
    time.sleep(2)
    add_order(102)
    time.sleep(2)
    add_order(103)
    add_order(104)
    add_order(105)

if __name__ == "__main__":
    threading.Thread(target=start_system, daemon=True).start()
    socketio.run(app, debug=True)
