import numpy as np
import matplotlib.pyplot as plt
R = 0.055 
r = 0.045 
e = 0.010 
total_length = 0.040 
h = 0.020 
a = 0.045 
Phi = 0.2 
#Input operating conditions
P_inlet = float(input("Enter inlet pressure (Pa): "))
P_outlet = float(input("Enter outlet pressure (Pa): "))
RPM = float(input("Enter compressor speed (RPM): "))
# Convert RPM into angular velocity
omega = 2*np.pi*RPM/60
#Exposed vane length
def L(Theta):
    return e*np.cos(Theta) + np.sqrt(R**2 - (e*np.sin(Theta))**2) - r

#Pressure functions
def P1(Theta):
    return (P_inlet + P_outlet)/2 + (P_outlet-P_inlet)/2*np.sin(Theta)
def P2(Theta):
    return (P_inlet + P_outlet)/2 + (P_outlet-P_inlet)/2*np.sin(Theta + delta)
def P3(Theta):
    return (P_inlet + P_outlet)/2 + (P_outlet-P_inlet)/2*np.sin(Theta + 2*delta)
def P4(Theta):
    return (P_inlet + P_outlet)/2 + (P_outlet-P_inlet)/2*np.sin(Theta + 3*delta)
def P5(Theta):
    return (P_inlet + P_outlet)/2 + (P_outlet-P_inlet)/2*np.sin(Theta + 4*delta)
#Angles
Theta = np.linspace(0, 2*np.pi, 1000)
pressures = [P1, P2, P3, P4, P5]

#Angular separation
delta = 72*np.pi/180
#Torque Equations
Tr = np.zeros_like(Theta)
for i in range(5):
    alpha = i*delta
    next_pressure = (i+1) % 5
    Fp = L(Theta+alpha)*h*(pressures[next_pressure](Theta)-pressures[i](Theta))
    Tr += Fp*(a-(L(Theta+alpha)/2)-e*np.cos(Phi+alpha))
#Calc Power Reqs
Power = Tr * omega
Average_power = np.mean(np.abs(Power))
Maximum_power = np.max(np.abs(Power))
#Calculate required volume reduction for pressure ratio
n = 1.4
volume_ratio = (P_inlet / P_outlet)**(1/n)
volume_reduction = (1 - volume_ratio) * 100
#Plot graphs, and display figures
plt.plot(Theta, Tr)
plt.xlabel('Theta (rad)')
plt.ylabel('Torque (Nm)')
plt.title('Torque Against Theta')
plt.grid()

plt.plot(Theta, L(Theta))
plt.xlabel('Theta (rad)')
plt.ylabel('Exposed Vane Length (m)')
plt.title('Exposed Vane Length Against Theta')
plt.grid()

plt.plot(Theta, Power)
plt.xlabel('Theta (rad)')
plt.ylabel('Power (W)')
plt.title('Power Against Theta')
plt.grid()
plt.show()
print(f"Polytropic exponent: {n}")
print(f"Final volume: {volume_ratio*100:.2f}% of initial volume")
print(f"Volume reduction required: {volume_reduction:.2f}%")
print(f"Angular velocity: {omega:.2f} rad/s")
print(f"Time per revolution: {60/RPM:.4f} seconds")
print(f"Average power requirement: {Average_power:.2f} W")
print(f"Maximum power requirement: {Maximum_power:.2f} W")