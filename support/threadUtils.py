import threading, time

def repeated_function_call(func, interval):
    next_call = time.time()  # Start time

    while True:
        now = time.time()
        if now >= next_call:
            func()  # Call the passed function
            next_call += interval  # Schedule next call

        # Sleep for a short time to avoid high CPU usage
        time.sleep(0.001)

# Create a thread that runs the repeated_function_call function
def start_background_task(func, interval):
    thread = threading.Thread(target=repeated_function_call, args=(func, interval), daemon=True)
    thread.start()