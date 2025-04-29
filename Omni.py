import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
import cv2
import threading

# -------------------- Voice Engine Setup --------------------
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# -------------------- Greeting --------------------
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

# -------------------- Command Listener --------------------
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception:
        print("Didn't catch that, please say again...")
        return "none"
    return query.lower()

# -------------------- Camera Control --------------------
camera_active = False

def startCamera():
    global camera_active
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("Camera not detected.")
        speak("Camera not detected.")
        return  # Exit the function if camera cannot be opened

    speak("Camera started. Say 'click photo' to take a selfie or 'stop camera' to close it.")
    camera_active = True

    while camera_active:
        ret, frame = cam.read()
        if not ret:
            speak("Failed to grab frame from camera.")
            break

        cv2.imshow("Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Check for command
        query = takeCommand()

        if "click photo" in query:
            filename = "selfie.jpg"
            cv2.imwrite(filename, frame)
            speak("Selfie clicked and saved.")
            print("Saved as", filename)

        elif "stop camera" in query:
            speak("Stopping the camera.")
            camera_active = False
            break

    cam.release()
    cv2.destroyAllWindows()

# -------------------- Assistant Brain --------------------
def assistantCommands():
    wishMe()
    while True:
        query = takeCommand()

        if "open youtube" in query:
            webbrowser.open("https://youtube.com")

        elif "open instagram" in query:
            webbrowser.open("https://instagram.com")

        elif "open spotify" in query:
            webbrowser.open("https://spotify.com")

        elif "start camera" in query:
            cam_thread = threading.Thread(target=startCamera)
            cam_thread.start()

        elif "stop listening" in query:
            speak("Okay, shutting down.")
            break

# -------------------- Main --------------------
if __name__ == "__main__":
    assistantCommands()