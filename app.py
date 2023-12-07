import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk

class MultiActivityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Activity App")

        self.current_activity = None

        self.create_widgets()

    def create_widgets(self):
        self.label_title = ttk.Label(self.root, text="Welcome to the Multi-Activity App!")
        self.label_title.pack(pady=20)

        self.btn_show_film = ttk.Button(self.root, text="Show Film", command=self.show_film_activity)
        self.btn_show_film.pack()

        self.btn_capture_camera = ttk.Button(self.root, text="Capture Camera", command=self.capture_camera_activity)
        self.btn_capture_camera.pack()

        self.btn_show_film.pack()

    def show_film_activity(self):
        self.clear_frame()

        self.label_title = ttk.Label(self.root, text="Film Activity")
        self.label_title.pack(pady=20)

        # Video player
        self.video_frame = ttk.Frame(self.root)
        self.video_frame.pack()

        self.cap = cv2.VideoCapture("res/dziendobry.mp4")  # Replace with your video file path

        _, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        self.photo = ImageTk.PhotoImage(image=frame)
        self.video_label = ttk.Label(self.video_frame, image=self.photo)
        self.video_label.pack()

        self.btn_back = ttk.Button(self.root, text="Back to Welcome", command=self.show_welcome_activity)
        self.btn_back.pack()

        self.current_activity = "film"

    def capture_camera_activity(self):
        self.clear_frame()

        self.label_title = ttk.Label(self.root, text="Camera Capture Activity")
        self.label_title.pack(pady=20)

        # Camera preview
        self.video_frame = ttk.Frame(self.root)
        self.video_frame.pack()

        self.cap = cv2.VideoCapture(0)  # 0 corresponds to the default camera (you can change it if you have multiple cameras)

        _, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        self.photo = ImageTk.PhotoImage(image=frame)
        self.video_label = ttk.Label(self.video_frame, image=self.photo)
        self.video_label.pack()

        self.btn_back = ttk.Button(self.root, text="Back to Welcome", command=self.show_welcome_activity)
        self.btn_back.pack()

        self.current_activity = "camera"

    def show_welcome_activity(self):
        self.clear_frame()

        self.label_title = ttk.Label(self.root, text="Welcome to the Multi-Activity App!")
        self.label_title.pack(pady=20)

        self.btn_show_film.pack()
        self.btn_capture_camera.pack()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        if self.cap:
            self.cap.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiActivityApp(root)
    root.geometry("800x600")
    root.mainloop()