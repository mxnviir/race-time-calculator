# Race Time Calculator

A physics-based simulator for CO2-powered dragster cars (Doesn't have to be STEM Racing!) that predicts 20-metre track time using thrust, drag, rolling friction, and wheel rotational inertia.

Works perfectly with our [OpenFOAM Auto-CFD](github.com/mxnviir/openfoam-for-stem) program. 

## Overview

The simulator integrates Newton's second law over time using CO2 thrust data from a CSV file. At each timestep it accounts for:

- **Thrust** — from the CO2 canister (see note below)
- **Aerodynamic drag** — scaled from a user-supplied drag force at 20 m/s
- **Rolling friction** — proportional to normal force via a user-supplied coefficient
- **Wheel inertia** — torque required to angularly accelerate the wheels

## Important: Simulated CO2 Thrust Data

> **The thrust values in `co2_thrust_data.csv` are simulated / modelled data, not measured real-world values.**
> They are intended as a reasonable approximation of a CO2 canister discharge curve for educational and design purposes only.

Because the data is simulated, predicted track times will likely differ from actual times on the day. To account for this, a **time coefficient** is applied:

```
actual_time ≈ predicted_time × coefficient
```

After running your car on a real track, divide your measured time by the simulator's predicted time to get your coefficient. Apply this to future predictions to bring them in line with reality. Typical values sit between **0.85 and 1.1** depending on the canisters, track conditions and sample size.

## Requirements

- Python 3.10+
- `numpy`
- `pandas`

Install dependencies:

```bash
pip install numpy pandas
# or, if using uv:
uv sync
```

## Usage

```bash
python main.py
```

You will be prompted for three inputs:

| Prompt | Description | Typical value |
|--------|-------------|---------------|
| Drag force at 20 m/s (N) | Measured or estimated drag force on your car at a reference speed of 20 m/s Shameless plug, go use [this](github.com/mxnviir/openfoam-for-stem)| 0.15 - 0.25 N |
| Rolling friction coefficient | Between wheels and track surface | 0.01 – 0.05 (0.3 is a nice middle-ground for proffesional class cars)|
| Wheel MOI (g·mm²) | Moment of inertia of one wheel | 150 – 300 g·mm² |

The simulator prints the interpolated finish time once the car crosses 20 m, or reports if the car stops short.

## File Structure

```
├── main.py                # Simulation script
├── co2_thrust_data.csv    # Simulated CO2 thrust / mass discharge curve
└── README.md
```

## Notes

- Car base mass includes a 21 g empty canister weight (`m_car = 0.0212 + m_sheet`).
- The drag model uses quadratic scaling: `F_drag = F_drag_20 × (v / 20)²`, where `F_drag_20` is the drag force at the 20 m/s reference speed. The input is a force (N) rather than a drag coefficient (Cd) — since drag force is `½ρCdA·v²`, the frontal surface area (A) and air density (ρ) terms are already baked into the measured reference force and cancel out when scaling to other speeds, so Cd and A are not needed separately.
- The track distance target is 20 metres.
