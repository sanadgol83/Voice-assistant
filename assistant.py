from media import *
#ketabkhane tanzime nor
import screen_brightness_control as sbc

from contextlib import redirect_stdout
#ketabkhane fasele sang shahr code
from geopy.geocoders import Nominatim
#ketabkhane fasele sang shahr fasele
from geopy.distance import geodesic

from ctypes import cast, POINTER

from comtypes import CLSCTX_ALL
#ketabkhane pakhsh faile soti
from playsound import playsound
#ketabkhane seda be neveshte
import speech_recognition as sr

from tkinter import messagebox

from threading import Thread

import pycaw.pycaw as pycaw
#ketabkhane pillow va majol screenshot
from PIL import ImageGrab
#ketabkhane wikipedia
import wikipedia as wiki

from tkinter import ttk
#ketabkhane tashkhis noghat kelidi dast
import mediapipe as mp

import tkinter as tk
#ketabkhane pillow va majol namayesh aks
from PIL import Image

import numpy as np
#majol modiriat os *
import subprocess
#ketabkhane modiriat keyboard
import pyautogui
#majol zaman *
import datetime
#ketabkhane matn be seda
import pyttsx3
#majol entekhab etefaghi *
import random
#majol modiriat zaman *
import time

import sys
#ketabkhane opencv pardazesh tasvir
import cv2

import io
#majol modiriat os *
import os

#tanzimat pyttsx3
engine = pyttsx3.init()
#sorat goftar
rate = engine.getProperty('rate')
engine.setProperty('rate',130)
#hagme seda
volume = engine.getProperty('volume')
engine.setProperty('volume',1.0)
#seday goyande
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

engine.say("hello i am alen your voice assistant")
engine.runAndWait()

#kalame shenasay
wakeUpCall = 'آلن'
#kalame khorog
exit_commands = ['خروج','خاموش','تموم','پايان','خداحافظ','بدرود']
#kalame pakhsh tavaghof
play_commands = ['پخش','پلی']
stop_commands= ['متوقف','قطع','استاپ']
#kalame ghably bady
prev_commands = ['قبلی','قبلیه']
next_commands = ['بعدی','بعديه']
#kalame tanzimat seda
sound_commands = ['صدا',]
sound_mute_commands = ['ببند','ميوت']
sound_unmute_commands = ['باز']
sound_vol_down = ['کم','کاهش']
sound_vol_up = ['زياد','افزایش']
#kalame tanzimat nor
bright_commands = ['نور','روشنایی']
bright_vol_down = ['کم','کاهش']
bright_vol_up = ['زیاد','افزايش']
#kalame control taswiri
display_command = ['تصویری','تصوير','کنترل']
#kalame screenshot
screen_command = ['عکس','صفحه']
#kalame wikipedia
wiki_command = ['ویکی']
#kalame bazi
game_command = ['بازی','گيم']
#kalame narm afzar ha
app_commands = ['برنامه','اپ']
expelor_command = ['فايرفاکس','اکسپلور']
vscode_command = ['اديتور','کد']
#kalame mashin hesab
calculator_command = ['حساب','ماشين']
#kalame fasele sang
distancemeter_command = ['فاصله','مسافت','هوایی']
#kalame zaman goya
time_commands = ['زمان','ساعت']
running = False
recognizer = None
microphone = None

def start_assistant():
    global running, r, microphone
    r = sr.Recognizer()
    r.pause_threshold = 0.9
    r.energy_threshold = 300
    microphone = sr.Microphone(device_index=1)
    while running:
        try:
            with microphone as source:
                #tabe kahesh noize mohit  
                r.adjust_for_ambient_noise(source , duration = 5)
                print('...بفرماييد...')
                audio = r.listen(source)
                #daryaft farman
                command = r.recognize_google(audio , language='fa-IR').lower()
                #etminan az goftan kalame shenasay
                if wakeUpCall in command:
                    #farman khamosh
                    if any(item in command for item in exit_commands):
                        print('...🔌 آلن خاموش شد...')
                        print('    ...🗿 بدرود...')
                        engine.say("Alan shut down, goodbye")
                        engine.runAndWait()
                        running = False
                        break
                    #farman pakhsh 
                    elif any(item in command for item in play_commands):
                        play()
                        continue
                    #farman tavaghof
                    elif any(item in command for item in stop_commands):
                        stop()
                        continue
                    #farman ghably
                    elif any(item in command for item in prev_commands):
                        gl()
                        continue
                    #farman bady
                    elif any(item in command for item in next_commands):
                        bl()
                        continue
                    #farman tanzimat seda
                    elif any(item in command for item in sound_commands):
                        #farman bi seda kardan
                        if any(item in command for item in sound_mute_commands):
                            mute()
                            continue
                        #farman ba seda kardan
                        elif any(item in command for item in sound_unmute_commands):
                            unmute()
                            continue
                        #farman seda kam kardan
                        elif any(item in command for item in sound_vol_down):
                            kam()
                            continue
                        #farman seda ziad kardan
                        elif any(item in command for item in sound_vol_up):
                            ziad()
                            continue
                    #farman tanzimat nor
                    elif any(item in command for item in bright_commands):
                        #farman nor kam kardan
                        if any(item in command for item in bright_vol_down):
                            n_kam()
                            continue
                        #farman nor ziad kardan
                        elif any(item in command for item in bright_vol_up):
                            n_ziad()
                            continue
                    elif any(item in command for item in display_command):
                        # تنظیمات صدا
                        devices = pycaw.AudioUtilities.GetSpeakers()
                        interface = devices.Activate(pycaw.IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                        volume = cast(interface, POINTER(pycaw.IAudioEndpointVolume))

                        mp_hands = mp.solutions.hands
                        hands = mp_hands.Hands()
                        mp_drawing = mp.solutions.drawing_utils

                        cap = cv2.VideoCapture(0)

                        cv2.namedWindow("Webcam", cv2.WND_PROP_FULLSCREEN)
                        cv2.setWindowProperty("Webcam", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

                        brightness = 50  # مقدار اولیه روشنایی
                        volume_level = 50  # مقدار اولیه صدا

                        while cap.isOpened():
                            success, image = cap.read()
                            if not success:
                                break

                            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                            results = hands.process(image)

                            if results.multi_hand_landmarks:
                                for hand_landmarks in results.multi_hand_landmarks:
                                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                                    
                                    # تشخیص دست راست و چپ
                                    handedness = results.multi_handedness[0].classification[0].label
                                    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                                    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                                    distance = np.sqrt((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)

                                    if handedness == 'Right':
                                        # تنظیم نور صفحه با دست راست
                                        brightness = int(distance * 200)
                                        brightness = max(0, min(brightness, 100))
                                        sbc.set_brightness(brightness)
                                    elif handedness == 'Left':
                                        # تنظیم صدا با دست چپ
                                        volume_level = distance * 200
                                        volume_level = max(0, min(volume_level, 100))
                                        volume.SetMasterVolumeLevelScalar(volume_level / 100, None)

                            # نمایش درصدهای نور و صدا روی تصویر
                            cv2.putText(image, f'Brightness: {brightness}%', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
                            cv2.putText(image, f'Volume: {int(volume_level)}%', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (128, 0, 128), 2, cv2.LINE_AA)

                            cv2.imshow("Webcam", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
                            if cv2.waitKey(5) & 0xFF == 27:  # کلید ESC برای خروج
                                break

                        cap.release()
                        cv2.destroyAllWindows()

                    #farman screenshot
                    elif any(item in command for item in screen_command):
                        screenshot = ImageGrab.grab()
                        screenshot.show()
                        screenshot.save("screenshot.png")
                        print('...📷اسکرین شات گرفتم...')
                        engine.say("i took a screenshot")
                        engine.runAndWait()
                        continue
                    #farman wikipedia
                    elif any(item in command for item in wiki_command):
                        print('...📚ویکی پدیا باز کردم...')
                        engine.say("wikipedia is opened, what information do you need?")
                        engine.runAndWait()
                        def search_wikipedia():
                            keyword = entry_keyword.get()
                            LANG = 'fa'
                            wiki.set_lang(LANG)
                            try:
                                summary = wiki.summary(keyword, sentences=5)
                                text_display.config(state=tk.NORMAL)
                                text_display.delete(1.0, tk.END)
                                text_display.insert(tk.END, summary)
                                text_display.config(state=tk.DISABLED)
                            except wiki.exceptions.DisambiguationError as e:
                                text_display.config(state=tk.NORMAL)
                                text_display.delete(1.0, tk.END)
                                text_display.insert(tk.END, "Disambiguation error: " + str(e.options))
                                text_display.config(state=tk.DISABLED)
                            except wiki.exceptions.PageError:
                                text_display.config(state=tk.NORMAL)
                                text_display.delete(1.0, tk.END)
                                text_display.insert(tk.END, "Page not found.")
                                text_display.config(state=tk.DISABLED)

                        def reset_fields():
                            entry_keyword.delete(0, tk.END)
                            text_display.config(state=tk.NORMAL)
                            text_display.delete(1.0, tk.END)
                            text_display.config(state=tk.DISABLED)

                        def quit_wikipedia():
                            engine.say("thanks for using wikipedia")
                            engine.runAndWait()
                            print('...📝بخاطر استفاده از ویکی پدیا ممنون...')
                            root.destroy()
                            

                        root = tk.Tk()
                        root.title("آلن پديا")

                        label_keyword = tk.Label(root, text="موضوع خود را وارد کنید:")
                        label_keyword.pack()

                        entry_keyword = tk.Entry(root)
                        entry_keyword.pack()

                        button_search = tk.Button(root, text="بررسی", command=search_wikipedia)
                        button_search.pack()

                        button_reset = tk.Button(root, text="ریست", command=reset_fields)
                        button_reset.pack()

                        button_exit = tk.Button(root, text="خروج", command=quit_wikipedia)
                        button_exit.pack()

                        text_display = tk.Text(root, state=tk.DISABLED, wrap=tk.WORD)
                        text_display.pack()

                        root.mainloop()
                    #farman narm afzar ha
                    elif any(item in command for item in app_commands):
                        #farman expelor baz kardan
                        if any(item in command for item in expelor_command):
                            subprocess.Popen(["C:\\Program Files\\Mozilla Firefox\\firefox.exe"])
                            print('...💻اینترنت اکسپلور باز کردم...')
                            engine.say("i opened the internet expelor")
                            engine.runAndWait()
                        #farman vs code baz kardan
                        elif any(item in command for item in vscode_command):
                            subprocess.Popen(["C:\\Users\\azadshahrnews\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"])
                            print('...⌨ویژوال استودیو کد باز کردم...')
                            engine.say("i opened the visual studio code editor")
                            engine.runAndWait()
                    #farman mashin hesab baz kardan
                    elif any(item in command for item in calculator_command):
                        print('...🧮ماشین حساب باز کردم...')
                        engine.say("i opened the calculator")
                        engine.runAndWait()
                        def on_click(button_text):
                            if button_text == "=":
                                try:
                                    result = eval(entry.get())
                                    entry.delete(0, tk.END)
                                    entry.insert(tk.END, str(result))
                                except Exception as e:
                                    entry.delete(0, tk.END)
                                    entry.insert(tk.END, "Error")
                            elif button_text == "C":
                                entry.delete(0, tk.END)
                            else:
                                entry.insert(tk.END, button_text)

                        # Create the main window
                        root = tk.Tk()
                        root.title("آلن حساب")

                        # Create the label for the welcome message
                        welcome_label = ttk.Label(root, text="سلام به ماشين حساب آلن خوش آمديد", font=("Helvetica", 20))
                        welcome_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

                        # Create the entry widget for displaying the input and result
                        entry = ttk.Entry(root, font=("Helvetica", 26), justify=tk.LEFT)
                        entry.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

                        # Create buttons for the calculator
                        buttons = [
                            "7", "8", "9", "/",
                            "4", "5", "6", "*",
                            "1", "2", "3", "-",
                            "0", ".", "=", "+",
                            "C"
                        ]

                        row_num = 2
                        col_num = 0

                        for button_text in buttons:
                            ttk.Button(root, text=button_text, command=lambda text=button_text: on_click(text)).grid(row=row_num, column=col_num, padx=5, pady=5)
                            col_num += 1

                            if col_num > 3:
                                col_num = 0
                                row_num += 1
                        def calculator_exit():
                            engine.say("thanks for using calculator")
                            engine.runAndWait()
                            print('...📈بخاطر استفاده از ماشین حساب ممنون...')
                            root.destroy()
                        # Add the exit button
                        exit_button = ttk.Button(root, text="خروج", command=calculator_exit)
                        exit_button.grid(row=row_num, column=col_num, padx=5, pady=5)

                        # Start the main event loop
                        root.mainloop()
                    #farman fasele sang baz kardan
                    elif any(item in command for item in distancemeter_command):
                        print("...📏فاصله سنج را باز کردم...")
                        engine.say("i opened the distancemeter")
                        engine.runAndWait()
                        def get_coordinates(city_name):
                            geolocator = Nominatim(user_agent="city_distance_calculator")
                            location = geolocator.geocode(city_name)
                            return (location.latitude, location.longitude)

                        def calculate_distance():
                            city1_name = entry_city1.get()
                            city2_name = entry_city2.get()
                            try:
                                city1_coords = get_coordinates(city1_name)
                                city2_coords = get_coordinates(city2_name)
                                distance = geodesic(city1_coords, city2_coords).kilometers
                                result_label.config(text=f"فاصله هوايي بين دو شهر برابر است با: {distance:.2f} کیلومتر")
                                engine.say(f"The distance between {city1_name} and {city2_name} is {distance:.2f} kilometers")
                                engine.runAndWait()
                            except Exception as e:
                                messagebox.showerror("Error", "Could not calculate distance. Please check the city names and try again.")

                        def reset_fields():
                            entry_city1.delete(0, tk.END)
                            entry_city2.delete(0, tk.END)
                            result_label.config(text="")

                        def exit_program():
                            engine.say("Thanks for using distance meter")
                            engine.runAndWait()
                            root.destroy()

                        root = tk.Tk()
                        root.title("Distance Meter")

                        tk.Label(root, text="لطفا نام شهر اول را وارد کن:").grid(row=0, column=0)
                        entry_city1 = tk.Entry(root)
                        entry_city1.grid(row=0, column=1)

                        tk.Label(root, text="لطفا نام شهر دوم را وارد کن:").grid(row=1, column=0)
                        entry_city2 = tk.Entry(root)
                        entry_city2.grid(row=1, column=1)

                        tk.Button(root, text="محاسبه", command=calculate_distance).grid(row=0, column=3)
                        tk.Button(root, text="ریست", command=reset_fields).grid(row=1, column=3)
                        tk.Button(root, text="خروج", command=exit_program).grid(row=2, column=3)

                        result_label = tk.Label(root, text="")
                        result_label.grid(row=2, columnspan=3)

                        root.mainloop()
                    #farman bazi sang kaghaz ghaychi baz kardan
                    elif any(item in command for item in game_command):
                        #pakhsh mosighi
                        sound_file = 'music/Stage_Clear.mp3'
                        playsound(sound_file)
                        #namayesh aks
                        image = Image.open('images/Picture 2.jpeg')
                        image.show()
                    
                        words = ["ROCK","SCISSORS","PAPER"]
                        artificial_win = 0
                        user_win = 0
                        draw = 0
                        #tanzimat mediapipe
                        mp_hands = mp.solutions.hands
                        mp_drawing = mp.solutions.drawing_utils
                        while True:
                            #shoroe daryaft video
                            cap = cv2.VideoCapture(0)
                            #tanzimat full screen
                            cv2.namedWindow("Webcam" ,cv2.WND_PROP_FULLSCREEN)
                            cv2.setWindowProperty("Webcam" ,cv2.WND_PROP_FULLSCREEN ,cv2.WINDOW_FULLSCREEN)

                            open_fingers_count = 0
                            #tanzimat hasasiat tashkhis angoshtan baz 
                            with mp_hands.Hands(min_detection_confidence=0.9, min_tracking_confidence=0.9) as hands:
                                start_time = time.time()
                                while cap.isOpened():
                                    ret, frame = cap.read()
                                    if not ret:
                                        break

                                    #tabdil tasvir be RGB
                                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                    results = hands.process(frame_rgb)
                                    #barresy natayeg
                                    if results.multi_hand_landmarks:
                                        for hand_landmarks in results.multi_hand_landmarks:
                                            #rasm noghat va etsalat 
                                            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                                            #shomaresh angoshtan baz 
                                            finger_tips = [hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],
                                                        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
                                                        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]]
                                            finger_pips = [hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP],
                                                        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP],
                                                        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]]

                                            count = 0
                                            for tip, pip in zip(finger_tips, finger_pips):
                                                if tip.y < pip.y:
                                                    count += 1
                                            if count == 0:
                                                count = "ROCK"
                                            if count == 1:
                                                count = "FINISH"
                                            if count == 2:
                                                count = "SCISSORS"
                                            if count == 3:
                                                count = "PAPER" 
                                            cv2.putText(frame, f'{user_win}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                                            cv2.putText(frame, f'{draw}', (75, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                                            cv2.putText(frame, f'{artificial_win}', (140, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                                            #bastan bazi
                                            if count == "FINISH":
                                                cv2.putText(frame, 'FINISH', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                                            else:
                                                #namayesh entekhab
                                                cv2.putText(frame, f'{count}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                                            #zakhire entekhab
                                            open_fingers_count = count

                                    #namayeshe tasvir
                                    cv2.imshow('Webcam', frame)

                                    #bastan bazi bad az 3 sanie
                                    if time.time() - start_time > 3:
                                        break
                                    #bastan bazi ba q
                                    if cv2.waitKey(1) & 0xFF == ord("q"):
                                        break

                            cap.release()
                            cv2.destroyAllWindows()

                            #namayesh entekhab
                            print(f'YOUR CHOICE : {open_fingers_count}')

                            if (open_fingers_count == "FINISH"): break

                            random_artificial = random.choice(words)

                            print("ARTIFICIAL CHOICE :",random_artificial)
                            
                            if (open_fingers_count == "ROCK" and random_artificial == "SCISSORS") or (open_fingers_count == "PAPER" and random_artificial == "ROCK") or (open_fingers_count == "SCISSORS" and random_artificial == "PAPER"):
                                user_win += 1
                                print("YOU WIN!")

                                if user_win >= 5:
                                    sound_file = 'music/Act_Complete.mp3'
                                    playsound(sound_file)

                                else:
                                    sound_file = 'music/flag_up.mp3'
                                    playsound(sound_file)

                            elif (random_artificial == "ROCK" and open_fingers_count == "SCISSORS") or (random_artificial == "PAPER" and open_fingers_count == "ROCK") or (random_artificial == "SCISSORS" and open_fingers_count == "PAPER"):
                                artificial_win += 1
                                print("ARTIFICIAL WIN!")

                                if user_win >= 5:
                                    sound_file = 'music/mario_over.mp3'
                                    playsound(sound_file)

                                else:
                                    sound_file = 'music/finito_game_2.mp3'
                                    playsound(sound_file)

                            elif (open_fingers_count == random_artificial):
                                sound_file = 'music/finito_game_1.mp3'
                                playsound(sound_file)
                                print("BOTH ARE THE SAME!")

                                draw += 1
                            
                        print("YOU : ",user_win)
                        print("ARTIFICIAL : ",artificial_win)
                    #zaman goya
                    elif any(item in command for item in time_commands):
                        time=datetime.datetime.now().strftime("%H:%M")
                        print(time)
                        engine.say(str(time))
                        engine.runAndWait()
                                                    
                    else:
                        print(command)
                        print('...😉 عزیزم متوجه نشدم...')
        except Exception as e:
            print(e)
            r = sr.Recognizer()
            continue
engine.runAndWait()
def on_start():
    global running
    running = True
    thread = Thread(target=start_assistant)
    thread.start()
    print("...شروع...")

def on_stop():
    global running
    running = False
    print("آلن متوقف شد")

def on_exit():
    global running
    running = False
    root.destroy()
    sys.exit()

class StdoutRedirector(io.StringIO):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def write(self, s):
        if self.text_widget.winfo_exists():
            self.text_widget.config(state=tk.NORMAL)
            self.text_widget.insert(tk.END, s)
            self.text_widget.config(state=tk.DISABLED)
            self.text_widget.see(tk.END)

# ایجاد پنجره اصلی
root = tk.Tk()
root.title("دستیار صوتی آلن")

# تنظیمات پنجره مستطیلی
root.geometry("400x300")

# ایجاد فریم برای دکمه‌ها
button_frame = tk.Frame(root)
button_frame.pack(side=tk.TOP, pady=10)

# ایجاد دکمه‌ها
start_button = tk.Button(button_frame, text="شروع", command=on_start)
start_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(button_frame, text="توقف", command=on_stop)
stop_button.pack(side=tk.LEFT, padx=5)

exit_button = tk.Button(button_frame, text="خروج", command=on_exit)
exit_button.pack(side=tk.LEFT, padx=5)

# ایجاد پنجره نمایش پرینت‌ها
print_display = tk.Text(root, height=10, width=50, state=tk.DISABLED, bg="white", fg="blue", font=("Arial", 12), wrap=tk.WORD)
print_display.pack(pady=10)

# تغییر مسیر stdout به ویجت Text
sys.stdout = StdoutRedirector(print_display)

# اجرای حلقه اصلی
root.mainloop()
