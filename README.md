# 🏠 Smart Home Simulation with AI Environment Adaptation

This project simulates a smart home environment where an intelligent agent autonomously navigates between rooms and dynamically adjusts temperature, lighting, and music based on changing external conditions. It features real-time visualization using Tkinter and Matplotlib and simulates the logic using SimPy.

---

## 🔧 Features

- 🚶 Intelligent agent moves between predefined rooms
- 🌡️ Auto-adjusts internal temperature, lighting, and music genre
- 📊 Real-time plots of environmental conditions
- 🖼️ Interactive GUI with room layout and current status
- 🎶 Supports multiple music genres mapped to conditions

---

## 🗃️ File Structure

```
├── smart_home_simulation.py     # Main simulation script
├── smart_home_mappings.csv      # Data mapping external to internal conditions
├── README.md                    # Project documentation
```

---

## 📦 Requirements

Install dependencies using pip:

```bash
pip install simpy matplotlib numpy pandas
```

> `tkinter` usually comes preinstalled with Python. If not, install it via your OS's package manager.

---

## 🚀 How to Run

1. Make sure `smart_home_mappings.csv` is in the project folder.
2. Run the simulation:

```bash
python smart_home_simulation.py
```

3. A GUI window will launch showing:
   - Room layout with agent's current location
   - Temperature, lighting, and music graphs
   - External and internal condition display
   - A Play/Pause button

---

## 📄 CSV File Format

The simulation depends on a CSV file (`smart_home_mappings.csv`) structured like:

| Room         | External_Temperature | External_Lighting | External_Noise | Internal_Temperature | Internal_Lighting | Internal_Music |
|--------------|----------------------|--------------------|----------------|-----------------------|-------------------|----------------|
| Living Room  | high                 | medium             | low            | 23                    | 70                | 2              |

Each row maps a combination of external factors to internal environment settings.

---

## 🎵 Music Genre Mapping

| Code | Genre        |
|------|--------------|
| 1    | Calm         |
| 2    | Jazz         |
| 3    | Acoustic     |
| 4    | Chillstep    |
| 5    | Ambient      |
| 6    | Pop          |
| 7    | Rock         |
| 8    | EDM          |
| 9    | Dubstep      |
| 10   | Heavy Metal  |

---

## 📈 Visualization Overview

- **Top Left:** User location in the home
- **Top Right:** Temperature graph (15–30°C)
- **Bottom Left:** Lighting graph (0–100%)
- **Bottom Right:** Music genre progression

---

## 📌 Future Improvements

- Add support for user preferences & learning behavior
- Integrate with real-world data (e.g., weather APIs)
- Enable control over smart devices (AC, lights)
- Export logs or analysis reports

---

## 📝 License

MIT License – feel free to use and adapt!

---

## 👤 Author

**[ProgrammerTabish](https://github.com/ProgrammerTabish)**  
Built with 💡 for smart automation systems.
