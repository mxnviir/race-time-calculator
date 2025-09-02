import numpy as np
import pandas as pd

# === LOAD DATA ===
df = pd.read_csv(co2_thrust_data.csv)

# Expect thrust and mass columns in the CSV
t = df['time (s)'].astype(float).values
F_thrust = df['force (N)'].astype(float).values
m_sheet = df['mass (kg)'].astype(float).values   # mass column from spreadsheet

# Add 21 g (0.021 kg) base mass to spreadsheet values
m_car = 0.021 + m_sheet   # array, kg

# === INPUTS ===
Cd = float(input("Enter drag coefficient Cd: "))
A = float(input("Enter frontal area (m^2): "))
rho = 1.225  # kg/m^3 (air density at sea level)
mu = float(input("Enter rolling friction coefficient: "))

# wheel parameters
N_wheels = 4
I_wheel = float(input("Enter entire wheel MOI (kg·m^2): "))
r_wheel = 0.015  # m (wheel radius)

# === EFFECTIVE MASS WITH WHEEL MOI ===
m_eq = N_wheels * I_wheel / (r_wheel**2)
m_eff = m_car + m_eq   # kg

print("Example effective mass values (g):", (m_eff[:5]*1000))

# === SIMULATION ===
v = np.zeros(len(t))
x = np.zeros(len(t))

for i in range(1, len(t)):
    dt = t[i] - t[i-1]

    # friction at this timestamp
    F_fric = mu * m_car[i-1] * 9.81

    # drag at this velocity
    F_drag = 0.5 * rho * Cd * A * v[i-1]**2

    # net force
    F_net = F_thrust[i-1] - F_drag - F_fric
    a = F_net / m_eff[i-1]

    v[i] = v[i-1] + a * dt
    if v[i] < 0:
        v[i] = 0.0
    x[i] = x[i-1] + v[i-1]*dt + 0.5*a*dt*dt

# === FIND FINISH TIME (20 m) ===
idx = np.where(x >= 20.0)[0]
if len(idx) == 0:
    print("Car did not reach 20 m within thrust duration.")
else:
    i = idx[0]
    finish_time = t[i-1] + (20.0 - x[i-1])*(t[i]-t[i-1])/(x[i]-x[i-1])
    print(f"Finish time: {finish_time:.6f} s")
    