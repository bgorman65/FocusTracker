# Importing needed libraries

import pathlib
import cv2
import time
import customtkinter

# Initializing user time variable to 45

aspiredTime = 45

# Function to set the aspired time from the slider(Used by start Window)
def getInt(value):
    # Gaining user desired time from slider
    global aspiredTime
    aspiredTime = value

# Creating Starting UI and various customTKinter settting

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
startWindow = customtkinter.CTk()
startWindow.geometry("600x280")
startWindow.title("Study Tool")
startFrame = customtkinter.CTkFrame(master=startWindow)
startFrame.pack(pady=20, padx=20, fill="both", expand=True)
startLabel = customtkinter.CTkLabel(master=startFrame, text="Focus Tracker", font=("Roboto", 24))
startLabel.pack(pady=10, padx=10)
startBox = customtkinter.CTkTextbox(master=startFrame, width=530, height=70, font=("Roboto", 14))
startBox.insert("0.0", "This program tracks how many times you lose focus by timing how long you arent    looking at a screen. Set the time(in seconds) aspired below using the slider, it is          between 30 and 90 and defaults at 45. Then click next to begin.")
startBox.pack(pady=10, padx=10)
timeEntry = customtkinter.CTkSlider(master=startFrame, from_=3, to=90, command=getInt, width=300)
timeEntry.pack(padx=10, pady=10)
nextButton = customtkinter.CTkButton(master=startFrame, text="Next", command=startWindow.destroy)
nextButton.pack(padx=10, pady=10)
startWindow.mainloop()

# Getting path for frontal face images detection, Training the dataset, and reading the camera

cascade_path = pathlib.Path(cv2.__file__).parent.absolute() / "data/haarcascade_frontalface_default.xml"
clf = cv2.CascadeClassifier(str(cascade_path))
camera = cv2.VideoCapture(0)

# Initializing needed variables

startTime = 0
endTime = 0
focusCounter = 0
startStop = True

# Creating Beginning Running UI

runWindow = customtkinter.CTk()
runWindow.geometry("500x320")
runWindow.title("Study Tool")

# Function to start facial tracking

def start():
    # Changing global condition to True
    global startStop
    startStop = True

# Function to stop facial tracking

def stop():
    # Changing global copnditon to False
    global startStop
    startStop = False

# Function to track focus using opencv

def startTrack():
    # Checking global condition to detect faces
    if startStop:
        # Creating global variables needed
        global focusCounter
        global startTime
        global endTime
        # Gaining the frame from the camera
        _, frame = camera.read()
        # Converting camera to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detecting the faces
        faces = clf.detectMultiScale(gray, scaleFactor=1.1, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
        # Finding if there is a face in frame and setting the face flag and times
        if len(faces) == 1:
            startTime = time.time()
            faceFlag = True
        else:
            endTime = time.time()
            faceFlag = False
        # Checking if focus is lost for longer than fifteen seconds and resetting if needed
        if (endTime - startTime) > aspiredTime:
            startTime = time.time()
            focusCounter += 1
    # Making the Run Window refresh
    runWindow.after(100, startTrack)

# Finishing Running UI

runFrame = customtkinter.CTkFrame(master=runWindow)
runFrame.pack(pady=20, padx=20, fill="both", expand=True)
runLabel = customtkinter.CTkLabel(master=runFrame, text="Instructions", font=("Roboto", 24))
runLabel.pack(pady=10, padx=10)
runBox = customtkinter.CTkTextbox(master=runFrame, width=480, height=50, font=("Roboto", 14))
runBox.insert("0.0", "Click Pause to stop and Resume to begin tracking again. Click View    Reults to end.")
runBox.pack(pady=10, padx=10)
startButton = customtkinter.CTkButton(master=runFrame, text="Resume", command=start)
startButton.pack(padx=10, pady=10)
stopButton = customtkinter.CTkButton(master=runFrame, text="Pause", command=stop)
stopButton.pack(padx=10, pady=10)
resultsButton = customtkinter.CTkButton(master=runFrame, text="View Results", command=runWindow.destroy)
resultsButton.pack(padx=10, pady=10)
runWindow.after(100, startTrack)
runWindow.mainloop()

# Releasing the camera

camera.release()

# Creating Results/Exit UI

endWindow = customtkinter.CTk()
endWindow.geometry("200x120")
endWindow.title("Results")
results = customtkinter.CTkTextbox(master=endWindow, width=180, height=40, font=("Roboto", 14))
results.insert("0.0", " times.")
results.insert("0.0", focusCounter)
results.insert("0.0", "You lost focus ")
results.pack(padx=10, pady=10)
exitButton = customtkinter.CTkButton(master=endWindow, text="Exit", command=endWindow.destroy)
exitButton.pack(padx=10, pady=10)
endWindow.mainloop()
