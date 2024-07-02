import time
import os
import argparse
import signal

# Global variable to track if the timer has been interrupted
interrupted = False


# Pomodoro timer: set time for work and break
def pomodoro_timer(work_time, break_time):
    global interrupted
    print("Pomodoro timer started! (Work: " + str(work_time) +
          " min | Break: " + str(break_time) + " min)")
    # Work time
    print(f"~ Work for {work_time} minutes")
    countdown(work_time * 60)

    if interrupted:
        return

    notify("Pomodoro Timer", "Pomodoro Completed", "Time is up! Take a break.")

    # Break time
    if break_time != 0:
        print(f"~ Take a {break_time} minutes break")
        countdown(break_time * 60)
        if interrupted:
            return
        notify("Pomodoro Timer", "Break done!", "Time to get back to work.")


def countdown(seconds):
    global interrupted
    try:
        while seconds:
            mins, secs = divmod(seconds, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            print('\033[K' + timeformat, end='\r', flush=True)
            time.sleep(1)
            seconds -= 1
            if interrupted:
                return
        print("\033[K00:00", end='\r')
    except KeyboardInterrupt:
        interrupted = True
        print("Timer interrupted.")


def notify(title, subtitle, message):
    os.system(f"osascript -e 'display notification \"{message}\" \
            with title \"{title}\" subtitle \"{subtitle}\"\
            sound name \"Morse\"'")


def signal_handler(sig, frame):
    global interrupted
    print('You pressed Ctrl+C!')
    interrupted = True


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(description="Pomodoro Timer")
    parser.add_argument("--preset", "-p", choices=["short", "medium", "long"],
                        help="Choose preset time configuration")
    parser.add_argument("--work", "-w", dest="work_time", type=int,
                        help="Custom work time in minutes")
    parser.add_argument("--break", "-b", dest="break_time", type=int,
                        help="Custom break time in minutes")
    args = parser.parse_args()

    # Case where user uses presets or p
    if args.preset:
        presets = {
                "short": (5, 0),
                "medium": (25, 5),
                "long": (90, 10)
                }
        work_time, break_time = presets[args.preset]
    else:
        if args.work_time is None or args.break_time is None:
            parser.error("Please specify both work and break times.")
        work_time = args.work_time
        break_time = args.break_time
        if work_time < 0 or break_time < 0:
            parser.error("Time cannot be negative.")

    pomodoro_timer(work_time, break_time)
