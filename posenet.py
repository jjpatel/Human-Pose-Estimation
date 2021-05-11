# -*- coding: utf-8 -*-
"""
@author: JATAN
"""


# Importing all he necessary modules
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2 as cv
from math import sqrt
import random
import keyboard
from pynput.keyboard import Key, Controller

# Creating and Initialising all the parameters and variables
keyboard1 = Controller()

net = cv.dnn.readNetFromTensorflow(r"C:\Users\SUSHANT\Jupyter_Projects\PoseNet\graph_opt.pb") ## weights

inWidth = 368
inHeight = 368
thr = 0.1

BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
               "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
               "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
               "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
               ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
               ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
               ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
               ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]

frame_1 = None
lmain = None
button2 = None

r_eye_to_nose = 0
r_ee_to_l_eye = 0
leftcorner= (0,0)
rightcorner= (0,0)
thickness = 2
txt = "Time to know your EYES' BEAUTY SCORE !!"
c = [(252, 142, 105), (23, 109, 252), (34, 214, 255), (16, 238, 158), (15, 241, 47), (252, 51, 183)]
k = 0
c_r = random.choice(c)
c_t = random.choice(c)
txt_1 = ""
alpha = ["A", "B", "C"]
part_game = {"Nose": "", "LEye": "", "REye": "", "LEar": "", "REar": ""};
start = 0


part_list = []
part_A = None
part_B = None
part_C = None
A= None
B = None
C = None
submit_button = None
game_label = None
game_score = None
ans = {}
frame = None
cap = cv.VideoCapture(1)

if not cap.isOpened():
    cap = cv.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Cannot open webcam.")
    
# Creating the GUI Main window
window = Tk()
window.title("PoseNet Implementation")
window.geometry('1200x650')

#window.configure(image = bg)
bgr = Image.open(r"C:\Users\SUSHANT\Downloads\bgr.jpg") 
bgr = bgr.resize((1200, 650))
bg = ImageTk.PhotoImage(bgr)
canvas1 = Canvas(window, width = 1200, height = 650)
canvas1.pack(fill = "both", expand = True)
canvas1.create_image( 0, 0, anchor = "nw",image = bg)


def calc_distance(p1, p2): # simple function to calculate the distance between two points
    return sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2) # Pythagorean theorem


# Function for Kids Game
def select_A(x):
    global ans
    global part_A
    global part_B
    ans[part_list[part_A.current()]] = "A"
    part_list.pop(part_A.current())
    part_B['values'] = part_list
    part_B.focus_set()

def select_B(x):
    global ans
    global part_C
    global part_B
    ans[part_list[part_B.current()]] = "B"
    part_list.pop(part_B.current())
    part_C['values'] = part_list
    part_C.focus_set()
    
def select_C(x): 
    global ans
    global part_C
    global part_B
    ans[part_list[part_C.current()]] = "C"
    submit_button.focus_set()
    

# Functions for checking the answers in the Kids game
def check_ans():
    global ans
    global part_game
    global part_list
    global game_score
    part_list = ['Nose', 'Ears', 'Eyes']
    
    score = 0
    if (ans['Nose'] == part_game['Nose']):
        score = score + 1
    
    if (ans['Ears'] == part_game['LEar']):
        score = score + 1
        
    if (ans['Eyes'] == part_game['LEye']):
        score = score + 1
    game_score = Label(window, text="Your score is "+str(score)+".", bg="grey", font = ("Times New Roman", 15, "bold"))
    canvas1.create_window(900, 425, window=game_score)


# Function to create the GUI components for Kids Game
def create_game():
    global part_list
    global part_A
    global part_B
    global part_C
    global game_label
    global A
    global B
    global C
    global submit_button
    part_list = ['Nose', 'Ears', 'Eyes']
    A = Label(window, text="A    : ", bg="grey", font = ("Times New Roman", 15, "bold"))

    B = Label(window, text="B    : ", bg="grey", font = ("Times New Roman", 15, "bold"))
    
    C = Label(window, text="C    : ", bg="grey", font = ("Times New Roman", 15, "bold"))
    submit_button = Button(window, text = "Submit", command = check_ans)
    game_label = Label(window, text="Match the letters with the correct body parts: ", bg="grey", font = ("Times New Roman", 15, "bold"))
    
    part_A = ttk.Combobox(window, width = 27, 
                                textvariable = StringVar())
    
    part_B = ttk.Combobox(window, width = 27, 
                                textvariable = StringVar())
    
    part_C = ttk.Combobox(window, width = 27, 
                                textvariable = StringVar())
    part_A.bind("<<ComboboxSelected>>", select_A)
    part_B.bind("<<ComboboxSelected>>", select_B)
    part_C.bind("<<ComboboxSelected>>", select_C)
    canvas1.create_window(1000, 225, window=part_A)
    canvas1.create_window(1000, 275, window=part_B)
    canvas1.create_window(1000, 325, window=part_C)
    canvas1.create_window(1000, 375, window=submit_button)
    canvas1.create_window(800, 325, window=C)
    canvas1.create_window(800, 225, window=A)
    canvas1.create_window(800, 275, window=B)
    canvas1.create_window(900, 175, window=game_label)
    part_A["values"] = part_list
    part_A.focus_set()

# Functions for destroying GUI components of Kids Game
def destroy_game():
    global A
    global B
    global C
    global part_A
    global part_B
    global part_C
    global game_label
    global game_score
    global submit_button
    A.destroy()
    B.destroy()
    C.destroy()
    part_A.destroy()
    part_B.destroy()
    part_C.destroy()
    game_label.destroy()
    game_score.destroy()
    submit_button.destroy()

# Function to create a section for live cam feed on the GUI
def addFrame():
    global frame_1
    global lmain
    frame_1 = Frame(window, bg = "white", height = 400, width = 600)
    lmain = Label(frame_1, bg = "white")
    lmain.grid()
    canvas1.create_window(350, 300, window = frame_1)
    
# Function for the EYE FILTER Section
def eye_filter():
    global frame
    hasFrame, frame = cap.read()
    global k
    global leftcorner
    global rightcorner
    global r_eye_to_nose
    global r_eye_to_l_eye
    global txt
    global c_r
    global c_t
    global txt_1
    k = k + 1
    if not hasFrame:
        cap.release()
        cv.destroyAllWindows()
        return
        
    
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]    
    net.setInput(cv.dnn.blobFromImage(frame, 1.0, (inWidth, inHeight), (127.5,127.5,127.5), swapRB = True, crop = False))
    out = net.forward()
    out = out[:, :19, :, :]  # MobileNet output [1, 57, -1, -1], we only need the first 19 elements

    assert(len(BODY_PARTS) == out.shape[1])

    points = []
    for i in range(len(BODY_PARTS)):
        # Slice heatmap of corresponging body's part.
        heatMap = out[0, i, :, :]

        # Originally, we try to find all the local maximums. To simplify a sample
        # we just find a global one. However only a single pose at the same time
        # could be detected this way.
        _, conf, _, point = cv.minMaxLoc(heatMap)
        x = (frameWidth * point[0]) / out.shape[3]
        y = (frameHeight * point[1]) / out.shape[2]
        # Add a point if it's confidence is higher than threshold.
        points.append((int(x), int(y)) if conf > thr else None)
    if not((points[BODY_PARTS['REye']] is None) or (points[BODY_PARTS['LEye']] is None) or (points[BODY_PARTS['Nose']] is None)):
                                                                                                 r_eye_to_nose = calc_distance(points[BODY_PARTS['REye']], points[BODY_PARTS['Nose']])
                                                                                                 r_eye_to_l_eye = calc_distance(points[BODY_PARTS['REye']], points[BODY_PARTS['LEye']])
                                                                                                 leftcorner = (int(points[BODY_PARTS['REye']][0] - (r_eye_to_nose/2)),int(points[BODY_PARTS['REye']][1] - (r_eye_to_nose/2)))
                                                                                                 rightcorner = (int(leftcorner[0] + (1.5*r_eye_to_nose)+r_eye_to_l_eye), int(leftcorner[1] + (r_eye_to_nose)))
    global thickness                                                                
    if (thickness == 2):
        thickness = -1
    elif thickness == -1:
        thickness = 2
        
    if k <= 25:
        c_r = random.choice(c)
        c_t = random.choice(c)
    else: 
        thickness = 3
        c_t_1 = random.choice(c)
    
    if (k == 25):
        rno = random.randint(1, 101)
        txt_1 = str(rno) + "%"
        if rno > 90:
            txt = "You have Magnificient Eyes !!!"
        elif rno> 75:
            txt = "You have Beautiful Eyes !!"
        elif rno> 60:
            txt = "You have Pretty Eyes !!"
        elif rno> 30:
            txt = "You have okay eyes."
        else:
            txt = "You have dark circles."  
    
    cv.rectangle(frame, leftcorner, rightcorner, c_r, thickness)
    
    cv.putText(frame, txt, (50,75), cv.FONT_HERSHEY_SIMPLEX, 0.8, c_t, 4)
    if (k > 25):
        cv.putText(frame, txt_1, (75,200), cv.FONT_HERSHEY_SIMPLEX, 2, c_t_1, 4)
    
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    img_1 = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img_1)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    

    if keyboard.is_pressed("esc"):
        cap.release()
        cv.destroyAllWindows()
        frame_1.destroy()
        button2.destroy()
        k = 0
        return
    
    lmain.after(2, eye_filter)

# Function for PoseNet Skeleton demonstration and basics of other features    
def poseNet():
    global frame
    hasFrame, frame = cap.read()
    if not hasFrame:
        cap.release()
        cv.destroyAllWindows()
        return
    
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]    
    net.setInput(cv.dnn.blobFromImage(frame, 1.0, (inWidth, inHeight), (127.5,127.5,127.5), swapRB = True, crop = False))
    out = net.forward()
    out = out[:, :19, :, :]  # MobileNet output [1, 57, -1, -1], we only need the first 19 elements

    assert(len(BODY_PARTS) == out.shape[1])

    points = []
    for i in range(len(BODY_PARTS)):
        # Slice heatmap of corresponging body's part.
        heatMap = out[0, i, :, :]

        # Originally, we try to find all the local maximums. To simplify a sample
        # we just find a global one. However only a single pose at the same time
        # could be detected this way.
        _, conf, _, point = cv.minMaxLoc(heatMap)
        x = (frameWidth * point[0]) / out.shape[3]
        y = (frameHeight * point[1]) / out.shape[2]
        # Add a point if it's confidence is higher than threshold.
        points.append((int(x), int(y)) if conf > thr else None)
    
    
    for pair in POSE_PAIRS:
        partFrom = pair[0]
        partTo = pair[1]
        assert(partFrom in BODY_PARTS)
        assert(partTo in BODY_PARTS)

        idFrom = BODY_PARTS[partFrom]
        idTo = BODY_PARTS[partTo]

        if points[idFrom] and points[idTo]:
            cv.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
            cv.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)
            cv.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)
    
    
    
    
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    img_1 = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img_1)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    
    if keyboard.is_pressed("esc"):
        cap.release()
        cv.destroyAllWindows()
        frame_1.destroy()
        button2.destroy()
        
        return
    
    lmain.after(2, poseNet)

# Function for the KID'S GAME section using PoseNet    
def game():
    global frame
    hasFrame, frame = cap.read()
    if not hasFrame:
        cap.release()
        cv.destroyAllWindows()
        return
    
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]    
    net.setInput(cv.dnn.blobFromImage(frame, 1.0, (inWidth, inHeight), (127.5,127.5,127.5), swapRB = True, crop = False))
    out = net.forward()
    out = out[:, :19, :, :]  # MobileNet output [1, 57, -1, -1], we only need the first 19 elements

    assert(len(BODY_PARTS) == out.shape[1])

    points = []
    for i in range(len(BODY_PARTS)):
        # Slice heatmap of corresponging body's part.
        heatMap = out[0, i, :, :]

        # Originally, we try to find all the local maximums. To simplify a sample
        # we just find a global one. However only a single pose at the same time
        # could be detected this way.
        _, conf, _, point = cv.minMaxLoc(heatMap)
        x = (frameWidth * point[0]) / out.shape[3]
        y = (frameHeight * point[1]) / out.shape[2]
        # Add a point if it's confidence is higher than threshold.
        points.append((int(x), int(y)) if conf > thr else None)
    
    global alpha
    global part_game
    global start
    if (start == 1):
        random.shuffle(alpha)
        part_game['Nose'] = alpha[0]
        part_game['LEye'] = alpha[1]
        part_game['REye'] = alpha[1]
        part_game['LEar'] = alpha[2]
        part_game['REar'] = alpha[2]
        start = 0
        
    cv.putText(frame, part_game['Nose'], points[BODY_PARTS['Nose']], cv.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 4)
    cv.putText(frame, part_game['LEye'], points[BODY_PARTS['LEye']], cv.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 4)
    cv.putText(frame, part_game['REye'], points[BODY_PARTS['REye']], cv.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 4)
    cv.putText(frame, part_game['LEar'], points[BODY_PARTS['REar']], cv.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 4)
    cv.putText(frame, part_game['REar'], points[BODY_PARTS['REar']], cv.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 4)
    
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    img_1 = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img_1)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    
    if keyboard.is_pressed("esc"):
        cap.release()
        cv.destroyAllWindows()
        destroy_game()
        frame_1.destroy()
        return
    
    lmain.after(2, game)

# Function for the button click event and starting the EYE Filter Section    
def start_cam():
    global cap
    global k
    global txt
    txt = "Time to know your EYES' BEAUTY SCORE !!"
    k = 0
    if not cap.isOpened():
        cap = cv.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam.")
    addFrame()
    global button2
    button2 = Button(window, text = "CAPTURE", command = click_image)
    canvas1.create_window(900, 300, window = button2)
    eye_filter()

# Function for the button click event and starting the basic PoseNet section    
def start_poseNet():
    global cap
    global k
    k = 0
    if not cap.isOpened():
        cap = cv.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam.")
    addFrame()
    keyboard1.press(Key.esc)
    keyboard1.release(Key.esc)
    global button2
    button2 = Button(window, text = "CAPTURE", command = click_image)
    canvas1.create_window(900, 300, window = button2)
    poseNet()

# Function for the button click event and starting the KID's GAME section
def start_game():
    global cap
    global start
    create_game()
    start = 1
    if not cap.isOpened():
        cap = cv.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam.")
    addFrame()
    game()

# Function for clicking and saving the image
e = 0
def click_image():
    global frame
    global e
    e = e+1
    cv.imwrite(r"C:\Users\jatan\Downloads\File"+str(e)+".jpg", cv.cvtColor(frame, cv.COLOR_BGR2RGB))

button1 = Button(window, text = "Eye Filter", command = start_cam) 
canvas1.create_window(300, 600, window = button1)
button3 = Button(window, text = "PoseNet Skeleton", command = start_poseNet)
canvas1.create_window(200, 600, window = button3)
button4 = Button(window, text = "Game for Kids", command = start_game)
canvas1.create_window(400, 600, window = button4)
window.mainloop()
