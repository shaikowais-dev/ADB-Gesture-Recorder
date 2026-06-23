import subprocess
import threading
import tkinter as tk
from tkinter import filedialog
import time
import math

def hex_to_dec(h):
    return int(h, 16)

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

class ADBRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("ADB Advanced Gesture Recorder")

        self.text = tk.Text(root, height=25, width=90)
        self.text.pack()

        tk.Button(root, text="Start Recording", command=self.start_recording).pack()
        tk.Button(root, text="Stop Recording", command=self.stop_recording).pack()
        tk.Button(root, text="Export Script", command=self.export).pack()

        self.recording = False
        self.steps = []

        self.x = None
        self.y = None

        self.points = []
        self.touch_start_time = None

    # ------------------
    def start_recording(self):
        self.recording = True
        threading.Thread(target=self.listen, daemon=True).start()

    def stop_recording(self):
        self.recording = False

    # ------------------
    def listen(self):
        process = subprocess.Popen(
            ["adb", "shell", "getevent", "-l"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        for line in process.stdout:
            if not self.recording:
                process.kill()
                break

            self.text.insert(tk.END, line)
            self.text.see(tk.END)

            # Capture coordinates
            if "ABS_MT_POSITION_X" in line:
                self.x = hex_to_dec(line.split()[-1])

            elif "ABS_MT_POSITION_Y" in line:
                self.y = hex_to_dec(line.split()[-1])

            # Touch START
            elif "BTN_TOUCH            DOWN" in line:
                self.points = []
                self.touch_start_time = time.time()

                if self.x and self.y:
                    self.points.append((self.x, self.y))

            # Movement
            elif "BTN_TOUCH" not in line and self.x and self.y:
                if len(self.points) == 0 or distance(self.points[-1], (self.x, self.y)) > 5:
                    self.points.append((self.x, self.y))

            # Touch END
            elif "BTN_TOUCH            UP" in line:
                self.process_gesture()

    # ------------------
    def process_gesture(self):
        if not self.points:
            return

        duration = int((time.time() - self.touch_start_time) * 1000)

        start = self.points[0]
        end = self.points[-1]

        move_dist = distance(start, end)

        # ---- Threshold tuning ----
        TAP_MOVE_THRESHOLD = 10
        LONG_PRESS_TIME = 500  # ms

        if move_dist < TAP_MOVE_THRESHOLD:
            if duration > LONG_PRESS_TIME:
                cmd = f"adb shell input swipe {start[0]} {start[1]} {start[0]} {start[1]} {duration}"
                gesture = "LONG PRESS"
            else:
                cmd = f"adb shell input tap {start[0]} {start[1]}"
                gesture = "TAP"
        else:
            cmd = f"adb shell input swipe {start[0]} {start[1]} {end[0]} {end[1]} {duration}"
            gesture = "SWIPE"

        self.steps.append(cmd)

        self.text.insert(tk.END, f"\n✅ {gesture}: {cmd}\n\n")

        self.points = []

    # ------------------
    def export(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".sh")

        with open(file_path, "w") as f:
            for step in self.steps:
                f.write(step + "\n")

        self.text.insert(tk.END, f"\n📁 Exported to {file_path}\n")


# Run GUI
root = tk.Tk()
app = ADBRecorder(root)
root.mainloop()