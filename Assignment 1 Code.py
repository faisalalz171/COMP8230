# Time module is imported so we can track duration of pours
import time

# This function simulates a Hall effect sensor by asking the user to enter 1 (tap open) or 0 (tap closed).
def read_tap_sensor():
    return int(input("Enter tap state (1=open, 0=closed): "))

# This variable remembers if the tap is currently open or not,
# so the program can tell when the tap changes from closed to open or open to closed.
# This helps us measure the start and end of each pour.
tap_is_open = False

# These variables save the time in seconds when the tap is opened and when it is closed.
# We use these times to calculate how long each pour lasts.
tap_open_time = 0
tap_close_time = 0

# These variables help us check if the bartender is pulling the tap too many times in a short time.
# 'event_count' counts how many times the tap is opened,
# and 'event_window_start' remembers the time when we started counting.
event_count = 0
event_window_start = 0

# This list will store all pouring events with timing and classification
event_log = []

# This loop runs forever, which mimics how a real sensor would continuously monitor the tap in real time.
while True:
    tap_state = read_tap_sensor()          # Get sensor input (1 = open, 0 = closed)
    current_time = time.time()             # Get the current time in seconds

    # When the tap just opened
    if tap_state == 1 and not tap_is_open:
        # This records when the tap was opened
        tap_open_time = current_time

        # And this marks the tap as open       
        tap_is_open = True                 

        # This part tracks how many times the tap was opened in under 12 seconds
        if event_window_start == 0 or (current_time - event_window_start > 12):
            event_window_start = current_time
            
            # Start new count
            event_count = 1                
        else:
            # We're still in 12-second window, we keep counting
            event_count += 1              

    # This part detects when the tap just closed
    if tap_state == 0 and tap_is_open:
        # Record when the tap was closed
        tap_close_time = current_time 

        # Mark the tap as closed
        tap_is_open = False                

        # This calculates how long the tap was open
        pour_duration = tap_close_time - tap_open_time
        timestamp = time.strftime('%H:%M:%S', time.localtime(tap_close_time))

        # Here, we match the pour time to the possible classification table
        if pour_duration < 3:
            result = "❌ Too short – Possible waste or wrong order"
        elif 3 <= pour_duration < 6:
            result = "❌ Short pour – Not a full drink, possible waste"
        elif 6 <= pour_duration < 9:
            result = "✅ Standard schooner pour"
        elif 9 <= pour_duration < 12:
            result = "✅ Standard pint pour"
        elif pour_duration > 12:
            result = "❌ Excessive pour – Tap may have been left open"

        print(f"{result} (⏱ {pour_duration:.1f} sec at {timestamp})")

        # Add the pour details to the event log
        event_log.append({
            "Start": time.strftime('%H:%M:%S', time.localtime(tap_open_time)),
            "End": timestamp,
            "Duration": round(pour_duration, 1),
            "Result": result
        })

    # This checks if the bartender opened the tap 3 or more times in less than 12 seconds
    # A behavior that happens when foaming happens due to improper pour
    if event_count >= 3 and (current_time - event_window_start <= 12):
        timestamp = time.strftime('%H:%M:%S', time.localtime(current_time))
        print(f"❌ Irregular pouring – too many pulls in short time ({timestamp})")

        # Log the irregular pour event
        event_log.append({
            "Time": timestamp,
            "Result": "❌ Irregular pouring – too many pulls"
        })

        event_count = 0
        event_window_start = 0

    # Slight delay so the system doesn't run too fast
    time.sleep(0.2)

# When you stop the program (e.g., with Ctrl+C), print all recorded events
    print("\n=== Event Log Summary ===")
    for i, event in enumerate(event_log, 1):
        print(f"{i}. {event}")
