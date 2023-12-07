import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import *
from PIL import Image, ImageTk
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
from logic import HandClassifierHandler
import time


class MyApp:
    def __init__(self, root, hch, model):
        self.root = root
        self.root.title("POLSKI JĘZYK MIGOWY")

        self.task_list = self.get_task()
        self.detected_list = []

        self.frame = ttk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        self.flag_task = 1
        self.task_counter = 0
        self.task_list_len = 5
        self.create_widgets(hch, model)

        self.show_welcome_activity()

    def get_task(self):
        # TODO uzupełnić
        video_paths = ["res/dziendobry.mp4", "res/dowidzenia.mp4", "res/dziekuje.mp4", "res/przepraszam.mp4",
                       "res/prosze.mp4"]
        correct_answers = []
        exercises = ["DZIEŃ DOBRY", "DO WIDZENIA", "DZIĘKUJĘ", "PROSZĘ", "PRZEPRASZAM"]
        return [video_paths, correct_answers, exercises]

    def create_widgets(self, hch, model):
        # Welcome Activity #############################################################################################
        mess = "Proszę zapoznać się uważnie z każdnym z zaprezentowanych znaków a następnie powtórzyć je do kamery"
        self.label_welcome = ttk.Label(self.frame, text=mess)
        self.label_welcome.pack(pady=20)
        # TODO obrazek z instrukcją!!!

        self.btn_activity1 = ttk.Button(self.frame, text="START", command=self.show_image_activity)
        self.btn_activity1.pack()

        # Classify hands activity ######################################################################################
        self.label_image = ttk.Label(self.frame, text="Pokaż znak do kamery")
        self.label_image.pack(pady=20)

        self.label_counter = ttk.Label(self.frame, text="")
        self.label_counter.pack()

        self.btn_activity3 = ttk.Button(self.frame, text="DALEJ", command=self.run)
        self.btn_activity3.pack()

        self.image_label = ttk.Label(self.frame)
        self.image_label.pack(pady=20)

        self.video_label = ttk.Label(self.frame)
        self.video_label.pack(pady=20)

        self.counter = 12000

    def show_image_activity(self):

        self.label_welcome.pack_forget()
        self.btn_activity1.pack_forget()

        self.btn_activity3.pack()
        self.label_image.pack()
        self.label_counter.pack()

        self.run()

    def run(self):

        if self.task_counter < self.task_list_len:
            if self.flag_task == 1:
                print("polecenie")
                self.flag_task = 0
                self.image_label.pack_forget()
                self.video_label.pack()
                self.show_wideo()
            else:
                print("zadanie")
                self.flag_task = 1
                self.image_label.pack()
                self.video_label.pack_forget()
                self.capture_camera()

    def show_welcome_activity(self):
        self.label_welcome.pack()
        self.btn_activity1.pack()
        self.btn_activity3.pack_forget()
        self.label_image.pack_forget()
        self.image_label.pack_forget()
        self.label_counter.pack_forget()

    def capture_camera(self):
        self.cap = cv2.VideoCapture(0)
        start_time = time.time()
        result_R = []
        result_L = []
        movement_R = []
        movement_L = []

        def select_img():
            with mp_hands.Hands(
                    model_complexity=0,
                    max_num_hands=2,
                    min_detection_confidence=0.7,
                    min_tracking_confidence=0.5) as hands:
                _, img = self.cap.read()

                #                    self.run()

                img = cv2.resize(img, (600, 500))
                img.flags.writeable = False
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                results = hands.process(img)
                # Draw the hand annotations on the image:
                img.flags.writeable = True
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

                if results.multi_hand_landmarks:
                    message = results.multi_handedness
                    # obtain result from classificator:
                    result = hch.get_result(model=model, handlandmarks=results.multi_hand_landmarks[0],
                                            is_R=hch.is_right(message))

                    movement = 0
                    print(result)
                    result_name = hch.result_parser(result=result)

                    # check which hand:
                    if hch.is_right(message):
                        print('Right')
                        result_R.append(result)
                        movement_R.append(movement)
                    else:
                        print('Left')
                        result_L.append(result)
                        movement_L.append(movement)
                    # draw handlandmarks on image:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            img,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style())

                # Flip the image horizontally for a selfie-view display: cv2.flip(image, 1)
                # or leave for more video like effect
                imgPIL = Image.fromarray(cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB))
                imgtk = ImageTk.PhotoImage(imgPIL)

                if time.time() - start_time > 10:
                    self.cap.release()
                    self.image_label.pack_forget()
                    self.task_counter += 1
                else:
                    self.image_label.configure(image=imgtk)
                    self.image_label.image = imgtk
                    self.image_label.after(10, select_img)

        select_img()

    def show_wideo(self):
        cnt = self.task_counter
        task_text = self.task_list[2][cnt]
        self.label_image.config(text=task_text)
        task_path = self.task_list[0][cnt]

        self.cap = cv2.VideoCapture(task_path)

        def update_video():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                imgPIL = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(imgPIL)
                self.video_label.configure(image=imgtk)
                self.video_label.image = imgtk
                self.video_label.after(10, update_video)
            else:
                self.cap.release()
                self.video_label.pack_forget()

        update_video()


if __name__ == "__main__":
    hch = HandClassifierHandler.HandClassifierHandler()
    model = hch.load_model()

    root = tk.Tk()
    app = MyApp(root, hch, model)
    root.geometry("1200x800")
    root.mainloop()
