import screen_brightness_control as sbc
import pyautogui
import pyttsx3
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
def play():
    pyautogui.press('playpause')
    print('...▶ پخش کردم...')
    engine.say("i started the case")
    engine.runAndWait()
def stop():
    pyautogui.press('playpause')
    print('...⏸ قطع کردم...')
    engine.say("i stepped on it")
    engine.runAndWait()
def gl():
    pyautogui.press('prevtrack')
    print('...⏮ زدم قبلی...')
    engine.say("i clicked on the previous item")
    engine.runAndWait()
def bl():
    pyautogui.press('nexttrack')
    print('...⏭ زدم بعدی...')
    engine.say("i clicked to go to next item")
    engine.runAndWait()
def unmute():
    pyautogui.press('volumemute')
    print('...🎶صدا باز کردم...')
    engine.say("i opened the volume")
    engine.runAndWait()
def mute():
    pyautogui.press('volumemute')
    print('...🔈 صدا قطع کردم...')
    engine.say("i mute the volume")
    engine.runAndWait()
def kam():
    for _ in range(5):
        pyautogui.press('volumedown')
    print('...🔉 صدا کم کردم...')
    engine.say("i turned down the volume")
    engine.runAndWait()
def ziad():
    for _ in range(5):
        pyautogui.press('volumeup')
    print('...🔊 صدا زیاد کردم...')
    engine.say("i turned up the volume")
    engine.runAndWait()
def n_kam():
    sbc.set_brightness(40)
    print('...🔆 روشنایی کم کردم...')
    engine.say("i dimmed the brightness")
    engine.runAndWait()
def n_ziad():
    sbc.set_brightness(90)
    print('...🌟روشنایی زیاد کردم...')
    engine.say("i increased the brightness")
    engine.runAndWait()
