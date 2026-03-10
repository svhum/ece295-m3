# This is a simple script to acquire a waveform from an oscilloscope channel and plot it.
# SVH 2026

import pyvisa
import numpy as np

import matplotlib
matplotlib.use("QtAgg")

import matplotlib.pyplot as plt

rm = pyvisa.ResourceManager()

# List instruments to find your scope
print(rm.list_resources())

# Resource string
scope = rm.open_resource('TCPIP0::192.168.0.253::hislip0::INSTR')
#scope = rm.open_resource('USB0::0x2A8D::0x1797::CN59176194::0::INSTR')

# Identify instrument
print(scope.query("*IDN?"))

# Stop acquisition so waveform doesn't change during transfer
scope.write(":STOP")

# Select waveform source
scope.write(":WAV:SOUR CHAN1")
#scope.write(":WAV:SOUR MATH")  # instead of CHAN1

# Set waveform format
scope.write(":WAV:FORM BYTE")

# Set waveform mode
scope.write(":WAV:MODE NORM")

# Query scaling parameters
x_increment = float(scope.query(":WAV:XINC?"))
x_origin = float(scope.query(":WAV:XOR?"))
y_increment = float(scope.query(":WAV:YINC?"))
y_origin = float(scope.query(":WAV:YOR?"))
y_reference = float(scope.query(":WAV:YREF?"))

# Request waveform data
raw = scope.query_binary_values(":WAV:DATA?", datatype='B', container=np.array)

# Convert to voltages
voltage = (raw - y_reference) * y_increment + y_origin

# Generate time axis
time = np.arange(len(voltage)) * x_increment + x_origin
print(time)
# Plot

#plt.figure(figsize=(5,5))   # width, height in inches
plt.figure(figsize=(8,5), constrained_layout=True)
#plt.tight_layout()
#plt.plot(time*1e6, voltage)
plt.plot(time, voltage)
plt.xlabel("Time (us)")
plt.ylabel("Voltage (V)")
#plt.title("Oscilloscope Trace")
plt.show()

scope.close()
