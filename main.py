import numpy as np
import pandas as pd

# === LOAD DATA ===
df = pd.read_csv("co2_thrust_data.csv")

# Expect thrust and mass columns in the CSV
t = df['time (s)'].astype(float).values
F_thrust = df['force (N)'].astype(float).values
m_sheet = df['mass (kg)'].astype(float).values   # mass column from spreadsheet

# Add 21 g (0.021 kg) base mass to spreadsheet values
m_car = 0.021 + m_sheet  - 0.048  # array, kg
m_car = m_car + (float(input("Weight of car (g): ")) / 1000.0)

# === INPUTS ===
Cd = float(input("Enter drag coefficient Cd: "))
A = float(input("Enter frontal area (mm^2): ")) / 1000000
rho = 1.225  # kg/m^3 (air density at sea level)
mu = float(input("Enter rolling friction coefficient: "))

# wheel parameters
N_wheels = 4
I_wheel = float(input("Enter wheel MOI (g·mm^2): ")) / 1000000000  # e.g. 1.71545e-7
r_wheel = 0.015  # m (wheel radius)

# === SIMULATION ===
v = np.zeros(len(t) * 10)  # allow space for coasting
x = np.zeros(len(t) * 10)
time = np.zeros(len(t) * 10)

# storage for wheel forces
F_wheel_arr = np.zeros(len(v))
tau_arr = np.zeros(len(v))
alpha_arr = np.zeros(len(v))

v[0] = 0.0
x[0] = 0.0
time[0] = t[0]

i_max = len(t) - 1
dt_default = np.mean(np.diff(t))  # use avg step for coasting

i = 1
while True:
    if i <= i_max:
        dt = t[i] - t[i-1]
        Fth = F_thrust[i-1]
        mass_car = m_car[i-1]
    else:
        dt = dt_default
        Fth = 0.0
        mass_car = m_car[-1]

    # resistive forces
    F_fric = mu * mass_car * 9.81
    F_drag = 0.5 * rho * Cd * A * v[i-1]**2

    # wheel angular acceleration from velocity difference
    omega_prev = v[i-1] / r_wheel
    omega_now = v[i-1] / r_wheel  # will update after velocity step
    if i > 1:
        omega_prev = v[i-2] / r_wheel
        omega_now = v[i-1] / r_wheel
    alpha = (omega_now - omega_prev) / dt
    tau = I_wheel * alpha
    F_wheel = (tau / r_wheel) * N_wheels

    # net force available for linear acceleration
    F_net = Fth - F_drag - F_fric - F_wheel
    a = F_net / mass_car

    # integrate motion
    v[i] = max(0.0, v[i-1] + a * dt)
    x[i] = x[i-1] + v[i-1]*dt + 0.5*a*dt*dt
    time[i] = time[i-1] + dt

    # store wheel dynamics
    alpha_arr[i] = alpha
    tau_arr[i] = tau
    F_wheel_arr[i] = F_wheel

    # stop conditions
    if x[i] >= 20:
        finish_time = time[i-1] + (20 - x[i-1]) * (time[i]-time[i-1]) / (x[i]-x[i-1])
        print(f"Finish time: {finish_time*0.76 :.4f} s")
        break
    if v[i] <= 0.0 and i > i_max:
        print("Car stopped before reaching 20 m.")
        break

    i += 1
    