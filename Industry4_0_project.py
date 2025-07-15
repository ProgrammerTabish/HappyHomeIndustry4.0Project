import simpy, random, tkinter as tk, matplotlib.pyplot as plt, matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np, threading, time, pandas as pd

ROOMS = ['Living Room', 'Bedroom', 'Kitchen', 'Bathroom', 'Workout Area']
POS = {'Living Room': (1,1), 'Bedroom': (5,1), 'Kitchen': (1,5), 'Bathroom': (5,5), 'Workout Area': (3,3)}
TRAIL, WIN = [], 10
music_labels = {1: 'Calm', 2: 'Jazz', 3: 'Acoustic', 4: 'Chillstep', 5: 'Ambient',
                6: 'Pop', 7: 'Rock', 8: 'EDM', 9: 'Dubstep', 10: 'Heavy Metal'}

df = pd.read_csv('smart_home_mappings.csv')
temp, light, music = [], [], []

class SmartHome:
    def __init__(self, env):
        self.env, self.loc, self.pos, self.resting = env, 'Living Room', list(POS['Living Room']), False
        self.target, self._path = self._new_target(), None
        self.temp = self.light = self.music = 0
        self.ext_temp = self.ext_light = self.ext_noise = ''
        self._make_path()
        env.process(self.run())

    def _new_target(self): return random.choice([r for r in ROOMS if r != self.loc])
    def _make_path(self):
        a, b = np.array(self.pos), np.array(POS[self.target])
        ctrl = (a + b)/2 + np.random.uniform(-1,1,2)
        self.t = 0; self._path = lambda t: (1 - t)**2 * a + 2*(1 - t)*t * ctrl + t**2 * b

    def _update_env(self):
        self.ext_temp = random.choice(['low','medium','high'])
        self.ext_light = random.choice(['low','medium','high'])
        self.ext_noise = random.choice(['low','medium','high'])

        row = df.query(
            f"Room == '{self.loc}' and "
            f"External_Temperature == '{self.ext_temp}' and "
            f"External_Lighting == '{self.ext_light}' and "
            f"External_Noise == '{self.ext_noise}'"
        ).iloc[0]

        self.temp, self.light, self.music = row['Internal_Temperature'], row['Internal_Lighting'], row['Internal_Music']

    def run(self):
        self._update_env()
        while True:
            TRAIL.append(tuple(self.pos)); TRAIL[:] = TRAIL[-500:]
            temp.append(self.temp); light.append(self.light); music.append(self.music)
            temp[:], light[:], music[:] = temp[-WIN:], light[-WIN:], music[-WIN:]

            if self.resting:
                for _ in range(20): yield self.env.timeout(0.2); TRAIL.append(tuple(self.pos))
            else:
                self.t += 0.01
                self.pos = list(POS[self.target]) if self.t >= 1 else list(self._path(self.t))
                self.resting = self.t >= 1
                yield self.env.timeout(0.2)

            if self.resting:
                self.loc = self.target
                self._update_env()
                self.target = self._new_target()
                self._make_path()
                self.resting = False

class SmartHomeGUI:
    def __init__(self, root, home):
        self.home = home
        fig, ax = plt.subplots(2,2, figsize=(8,6))
        fig.subplots_adjust(hspace=0.5, wspace=0.4)
        self.ax_main, self.ax_temp, self.ax_light, self.ax_music = ax.flatten()
        self.canvas = FigureCanvasTkAgg(fig, master=root); self.canvas.get_tk_widget().pack()
        self.status = tk.Label(root, font=("Arial", 12)); self.status.pack()
        self.ext_status = tk.Label(root, font=("Arial", 10), fg='gray')
        self.ext_status.pack(pady=(5,10))
        tk.Button(root, text="Play/Pause", command=self.toggle).pack()
        self.ani = animation.FuncAnimation(fig, self.update_plot, interval=1000, cache_frame_data=False)

    def toggle(self): pause_event.set() if not pause_event.is_set() else pause_event.clear()

    def update_plot(self, _):
        ax = self.ax_main
        ax.clear(); ax.set_xlim(0,6); ax.set_ylim(0,6)
        for room, pos in POS.items():
            ax.add_patch(plt.Rectangle((pos[0]-0.4, pos[1]-0.4), 0.8, 0.8, color='lightgrey'))
            ax.text(pos[0], pos[1], room, fontsize=8, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.7))
        if TRAIL:
            xs, ys = zip(*TRAIL)
            ax.plot(xs, ys, 'b-', alpha=0.5)
            ax.plot(xs[-1], ys[-1], 'ro', markersize=8)
        ax.set_title("User Location")

        self.status.config(
            text=f"Room: {self.home.loc} | Temp: {self.home.temp}°C | Light: {self.home.light}% | Music: {music_labels.get(self.home.music, self.home.music)}"
        )

        self.ext_status.config(
            text=f"External → Temperature: {self.home.ext_temp.capitalize()} | "
                 f"Lighting: {self.home.ext_light.capitalize()} | "
                 f"Noise: {self.home.ext_noise.capitalize()}  ||  "
                 f"Internal → Temperature: {self.home.temp}°C | Lighting: {self.home.light}% | "
                 f"Music: {music_labels.get(self.home.music, self.home.music)}"
        )

        def draw_line(ax, data, color, title, ylim, yticks=None, labels=None):
            ax.clear(); ax.plot(data, color=color); ax.set_title(title); ax.set_ylim(*ylim)
            if yticks and labels: ax.set_yticks(yticks); ax.set_yticklabels(labels)

        draw_line(self.ax_temp, temp, 'g', "Temperature", (15,30))
        draw_line(self.ax_light, light, 'y', "Lighting", (0,100))
        draw_line(self.ax_music, music, 'purple', "Music Genre", (1,10),
                  list(music_labels.keys()), list(music_labels.values()))
        self.canvas.draw()

def sim_thread(env):
    while True:
        if pause_event.is_set(): time.sleep(0.1); continue
        try: env.step(); time.sleep(0.1)
        except: break

env = simpy.Environment(); home = SmartHome(env)
pause_event = threading.Event(); pause_event.set()
root = tk.Tk(); root.title("Smart Home Simulation")
gui = SmartHomeGUI(root, home)
threading.Thread(target=sim_thread, args=(env,), daemon=True).start()
root.mainloop()
