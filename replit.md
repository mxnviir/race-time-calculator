# Replit MD

## Overview

This is a CO2 car physics simulation project written in Python. It models the motion of a CO2-powered car by reading thrust data from a CSV file and simulating the vehicle's velocity and position over time. The simulation accounts for aerodynamic drag, rolling friction, wheel rotational inertia, and time-varying thrust and mass (as CO2 is expelled). It's designed as a tool for engineering students or hobbyists working on CO2 dragster cars.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Project Structure
This is a single-file Python script (`main.py`) with no web framework, no backend server, and no frontend. It runs as a command-line application.

- **`main.py`** — The entire simulation logic: data loading, user input collection, and physics calculations.
- **`co2_thrust_data.csv`** — Input data file containing time-series thrust and mass data for the CO2 cartridge.

### Core Design Decisions

**Data-Driven Thrust Model**
- The thrust curve and mass depletion over time come from a CSV file rather than being hard-coded or analytically modeled. This allows easy swapping of different cartridge profiles.
- The CSV is expected to have columns: `time (s)`, `force (N)`, and `mass (kg)`.

**Interactive User Inputs**
- Several parameters are collected at runtime via `input()` calls: car weight, drag force at 1 m/s, rolling friction coefficient, and wheel moment of inertia.
- This makes the simulation flexible without needing config files.

**Physics Model**
- Drag force scales with velocity squared: `F_drag = Fd_input * v^2` (where `Fd_input` is the drag at 1 m/s).
- Rolling friction uses a simple coefficient model.
- Wheel rotational inertia is accounted for using moment of inertia (MOI) for 4 wheels.
- Mass varies over time as CO2 is expelled, with a 21g base mass offset applied to the spreadsheet values.

**Numerical Integration**
- Uses a time-stepping approach with arrays pre-allocated at 10x the thrust data length to allow for coasting simulation after thrust ends.
- Time steps during the thrust phase come from the CSV data spacing; a default average step size is used for coasting.

### Technologies
- **Python 3** — Core language
- **NumPy** — Numerical arrays and math operations
- **Pandas** — CSV data loading and manipulation

## External Dependencies

### Python Packages
- **numpy** — Array operations and numerical computation
- **pandas** — Reading and parsing the CSV thrust data file

### Data Files
- **`co2_thrust_data.csv`** — Required input file with columns `time (s)`, `force (N)`, `mass (kg)`. Must be present in the project root directory.

### No External Services
There are no databases, APIs, authentication systems, or third-party service integrations. This is a purely local, offline simulation tool.