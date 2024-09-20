from microbit import *
import music
import random

# Initialization
# - test configuration and rules
signals_made = 0
correct_reactions = 0
start_time = 0
signal_time = 0
test_duration = 60000  # 1 minute in milliseconds
reaction_time_limit = 3000  # 3 seconds in milliseconds

# Random number of signals (1, 2, or 3)
total_signals = random.randint(1, 3)

# Random intervals between signals (between 10 and 20 seconds)
signal_play_intervals = [random.randint(10000, 20000) for _ in range(total_signals)]

# Make it quiet, simulating the effect of a delicate buzz
set_volume(16)

# Start test when button A is pressed
# - a long beep indicates the start of the test
while True:
    if button_a.is_pressed():
        start_time = running_time()
        music.pitch(440, duration=1000)
        break

# Set initial last signal time to the game start time
last_signal_time = start_time

# Main test loop
# - keeps running while test_duration is up
while running_time() - start_time < test_duration:
    if signals_made < total_signals:
        
        # Check if it's time to make the next signal
        if running_time() - last_signal_time >= signal_play_intervals[signals_made]:
            # Make a signal
            display.show(Image.SURPRISED)
            for _ in range(3):
                music.pitch(440, duration=100)
                sleep(100)
            display.clear()

            # Update test state
            last_signal_time = running_time()
            signals_made += 1

            # Wait for response
            # - check if response is made within the allowed time limit
            while running_time() - last_signal_time < reaction_time_limit:
                if button_b.is_pressed():
                    correct_reactions += 1
                    break
        else:
            # Short sleep to let the processor chill
            sleep(100)

# Test evaluation, check if the user responded to all signals
if correct_reactions == total_signals:
    # "you managed to keep up with the group"
    display.show(Image.HAPPY)
    music.pitch(640, duration=1000)
else:
    # "you are lost in the forest, forever"
    display.show(Image.SAD)
    music.pitch(240, duration=1000)

# Keep showing the result
while True:
    sleep(1000)
