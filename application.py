import threading
import time
import os
import schedule
import psutil
from app import create_app, socketio
from app.tasks import job1

app = create_app()

def kill_existing_scheduler_processes():
    current_pid = os.getpid()
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
        try:
            if proc.info['pid'] != current_pid and 'python' in proc.info['name']:
                cmdline = ' '.join(proc.info['cmdline'])
                if 'application.py' in cmdline:  # Adjust to match your script name
                    print(f"Killing existing process {proc.info['pid']} running: {cmdline}")
                    proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

# Test task
def my_task():
    job1()
    print("Task executed! " + str(int(time.time())))

def setup_testing_scheduler():
    schedule.every(10).seconds.do(my_task)

def setup_real_scheduler():
    schedule.every(6).hours.do(my_task)

# Run the scheduler
def run_scheduler(sleep_time, stop_event_flag):
    while not stop_event_flag.is_set():  # Run until the stop event is triggered
        schedule.run_pending()  # Executes tasks that are due
        print(f"Scheduler sleeping for {sleep_time} seconds... {int(time.time())}")
        stop_event_flag.wait(timeout=sleep_time)  # Sleep with the ability to stop early

if __name__ == '__main__':
    kill_existing_scheduler_processes()

    # setup_testing_scheduler()  # Testing scheduler
    setup_real_scheduler()  # Real scheduler

    stop_event = threading.Event()
    # scheduler_thread = threading.Thread(target=run_scheduler, args=(2, stop_event), daemon=True) # Testing scheduler
    scheduler_thread = threading.Thread(target=run_scheduler, args=(7200, stop_event), daemon=True)  # Real scheduler
    scheduler_thread.start()

    try:
        port = int(os.getenv('PORT', 5001))
        socketio.run(app, debug=True, host='0.0.0.0', port=port, use_reloader=False)
    except KeyboardInterrupt:
        print("\nGracefully shutting down...")

        # Signal the scheduler thread to stop
        stop_event.set()
        scheduler_thread.join()  # Wait for the scheduler thread to finish

        print("Shutdown complete.")