# Distributed Task Scheduling System with Fault Tolerance

##  What is Distributed Task Scheduling with Fault Tolerance?

A **Distributed Task Scheduling System** is a system that dynamically assigns and manages tasks across multiple worker nodes in a distributed environment. It ensures efficient task execution by balancing the load and maintaining task dependencies.

**Fault tolerance** is a critical feature of such a system, ensuring that if a worker node fails or crashes, the system automatically detects the failure and reassigns the uncompleted tasks to another available worker.

### Key Components of Distributed Task Scheduling:
- **Task Scheduling:** Assigns tasks dynamically to available worker nodes.
- **Task Dependencies:** Ensures that some tasks (e.g., shipping) run only after their prerequisite tasks (e.g., packing) are completed.
- **Fault Tolerance:** Automatically detects worker failures and reassigns tasks.
- **Scalability:** Allows the system to handle more tasks by adding worker nodes dynamically.
- **Optimized Scheduling:** Ensures tasks are completed in the shortest time while balancing the load.
- **Monitoring Dashboard:** Provides real-time tracking of tasks, worker health, retries, and failures.

---

##  How This System Suits an E-Commerce Application

This system is specifically designed to handle the **order processing workflow of an e-commerce platform**, ensuring efficient execution of orders while handling failures dynamically.

### Order Processing Workflow:
1. **Payment Processing** → Payment must be completed before moving to the next step.
2. **Packing Order** → Once payment is successful, the order is packed.
3. **Shipping Order** → After packing, the order is shipped to the customer.

🔹 Each order follows the above sequence, ensuring correctness and efficiency. If any step fails, the system **retries the task up to 3 times** before marking it as failed. If a worker crashes, the pending task is reassigned to another available worker.

---

## Features Implemented in This Project

✅ **Task Dependencies Handling:**
- Payment → Packing → Shipping order enforced correctly.
- Tasks execute in the correct sequence.

✅ **Fault Tolerance:**
- Worker failures detected.
- Tasks are reassigned to a new worker if a worker crashes.
- System logs failures and reassignments.

✅ **Retry Mechanism:**
- Each task retries up to **3 times** before marking it as failed.
- Retries are logged in the system.

✅ **Dynamic Worker Management:**
- New worker nodes can be added dynamically.
- Load is redistributed if a worker crashes or is removed.

✅ **Real-Time Dashboard:**
- Shows **order progress**, **worker failures**, **task retries**, and **reassignments**.
- Logs failures, reassignments, and retries in a persistent log system.


##  Tech Stack Used & Purpose

| Technology | Purpose |
|------------|---------|
| **Python (Standard Library)** | Core implementation of task scheduling, fault tolerance, and retries. |
| **Flask** | Provides the web server for the real-time dashboard. |
| **Flask-SocketIO** | Enables real-time updates between the backend and dashboard. |
| **Threading & Multiprocessing** | Handles concurrent task execution and worker management. |
| **Logging** | Maintains system logs for debugging and monitoring. |
| **HTML + JavaScript (Socket.IO)** | Implements the real-time dashboard UI. |
| **CSS** | Enhances dashboard appearance. |

---

##  How the System Works

1. Order Created → Added to the queue.
2. **Task Assignment** → Consistent hashing assigns tasks to workers.
3. **Task Execution** → Workers process payment, packing, and shipping sequentially.
4. **Failure Detection** → If a worker fails, tasks are reassigned.
5. **Retries** → If a task fails, it retries up to 3 times before marking it as failed.
6. **Dashboard Updates** → UI updates in real-time with logs, task progress, and failures.

---

This project effectively demonstrates a **fault-tolerant distributed task scheduling system** designed for **e-commerce order processing** while ensuring **efficiency, fault tolerance, and real-time monitoring**. 🚀

**
