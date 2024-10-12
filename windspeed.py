import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(34,GPIO.IN)

# Anamometer vane diameter (set to the value for your cup-to-cup in cm)
vane_diameter = float(14)

# Calculate vane circumference in km
vane_circ = float (vane_diameter/100000)*3.1415

# Set an anamometer factor to account for inefficiency (value is a guess)
afactor = float(2.5)

# Start measuring wind speed and let us know things are happening!
print('Measuring wind speed...')

# Define variables rotations and trigger (trigger = 1 if sensor triggered)
rotations = float(0)
trigger = 0

# Define variable endtime to be current time in seconds plus 10 seconds
endtime = time.time() + 10

# Get initial state of sensor
sensorstart = GPIO.input(34)

# Measurement loop to run for 10 seconds
while time.time() < endtime:
	if GPIO.input(34)==1 and trigger==0:
		rotations = rotations + 1
		trigger=1
	if GPIO.input(34)==0:
		trigger = 0
	# We seem to need to a little delay to make things work reliably...
	time.sleep(0.001)

# Loop has now finished. But if sensor triggered at start and did not move,
# rotations value will be 1, which is probably wrong, so . . .
if rotations==1 and sensorstart==1:
	rotations = 0


