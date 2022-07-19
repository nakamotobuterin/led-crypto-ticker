## Requirements
Adafruit MatrixPortal M4: https://www.adafruit.com/product/4745
Adafruit 64x32 RGB LED Matrix: https://www.adafruit.com/product/2278

## Instructions
- Assemble MatrixPortal and LED Matrix (https://learn.adafruit.com/matrix-portal-new-guide-scroller/prep-the-matrixportal)
- Install CircuitPython on the MatrixPortal (https://learn.adafruit.com/matrix-portal-new-guide-scroller/install-circuitpython)
- Copy the content of this repository to the CIRCUITPY drive of the MatrixPortal (all required Adafruit libs are already included)
- Open secrets.py and enter your WiFi credentials
- The MatrixPortal should retart automatically and if your WiFi credentials are valid it should show and update prices on the LED Matrix periodically
- Optional: Modify code.py at will e.g. to add other pairs, change timings, price API URL, ...