from cv2 import FONT_HERSHEY_SIMPLEX
import pyautogui

last_position = (None,None)
last_dir = ''

def keypress()->None:
    ''' 
    @keypress
    @purpose: Control the game using the keys 'w','a','s', and 'd' as input
    @parameters: None
    @return: None
    '''
    import keyboard

    forever = True
    while forever is True:
        if keyboard.is_pressed('w'):
            pyautogui.press("up")
            print("up")
        if keyboard.is_pressed('a'):
            pyautogui.press("left")
            print("left")
        if keyboard.is_pressed('s'):
            pyautogui.press("down")
            print("down")
        if keyboard.is_pressed('d'):
            pyautogui.press("right")
            print("right")


def trackpad_mouse():
    ''' 
    @trackpad_mouse
    @purpose: Control the game by moving the mouse/finger 
    on trackpad left, right, up, or down. 
    @parameters: None
    @return: None
    '''

    from pynput import mouse

    def on_move(x, y):
        global last_position
        global last_dir
        if last_position == (None, None):
            last_position = (x ,y )
        else:
            diffX = last_position[0] - x
            diffY = last_position[1] - y
            absDiffX = abs(last_position[0] - x)
            absDiffY = abs(last_position[1] - y)
            thresholdX = 100
            thresholdy = 100
            if absDiffX > thresholdX and (absDiffX > absDiffY) :
                if diffX < 0  and last_dir != "right":
                    pyautogui.press("right")
                    last_position = (x ,y )
                    last_dir = "right"
                    print("right")
                if diffX > 0 and last_dir != "left":
                    pyautogui.press("left")
                    last_position = (x ,y )
                    last_dir = "left"
                    print("left")
            if absDiffY > thresholdy and (absDiffY > absDiffX):
                if diffY > 0 and last_dir != "up":
                    pyautogui.press("up")
                    last_position = (x ,y )
                    last_dir = "up"
                    print("up")
                
                if diffY < 0 and last_dir != "down":
                    pyautogui.press("down")
                    last_position = (x ,y )
                    last_dir = "down"
                    print("down")

    with mouse.Listener(on_move=on_move) as listener:
        listener.join() 

def color_tracker():
    """
    @color_tracker
    @purpose: Control the game by identifying the movement of a specific color in the camera.
    @parameters: None
    @return: None
    """
    import cv2
    import imutils
    import numpy as np
    from collections import deque
    import time
    import multithreaded_webcam as mw
    # You need to define HSV colour range MAKE CHANGE HERE
    colorLower = (255,36,36)
    colorUpper = (255,36 ,144)

    # set the limit for the number of frames to store and the number that have seen direction change
    buffer = 20
    pts = deque(maxlen = buffer)

    # store the direction and number of frames with direction change
    num_frames = 0
    (dX, dY) = (0, 0)
    direction = ''
    global last_dir
    global last_position
    threshold = 20
    #Sleep for 2 seconds to let camera initialize properly
    time.sleep(2)
    #Start video capture
    vs = mw.WebcamVideoStream().start()
    for i in range(5):
        print("This works so far")
    


    while True:
        frame = vs.read()

        #flip and resize frame
        flipped = cv2.flip(frame,1)
        resize = imutils.resize(flipped, width = 600)

        #reduce noise and convert to HSV
        blur = cv2.GaussianBlur(resize, (5,5), 0) 
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        #creates MASK
        mask = cv2.inRange(hsv, colorLower, colorUpper)
        noiseEraser = cv2.erode(mask, None, iterations = 2)
        dilate = cv2.dilate(noiseEraser, None, iterations = 2)
        #creates object of the found color differentiation 
        foundObj = cv2.findContours(dilate.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #is a list of contour points
        objCenter = None
        for i in range(len(foundObj)):
            print(foundObj[i])

        
        if len(foundObj[0]) > 0:
            maxContour = max(foundObj, key = cv2.contourArea) #max contour errors
            radius= cv2.minEnclosingCircle(maxContour) #returns center and raidus so use [1]
            M = cv2.moments(maxContour)
            objCenter = (int(M['m10']/ M['m00']), int(M['m01']/M['m00']))
            if radius[1] > 10:
                pts.appendleft(objCenter)
            if len(pts) > 10 and num_frames >10:
                #compares the dx and dy differences of x and y between the first and last in the 1 and 10 in the list
                diffX = pts[0][0] - pts[9][0]
                diffY= pts[0][1] - pts[9][1] #in the document it says first (1) and (10)
                absDiffX = abs(diffX)
                absDiffY = abs(diffY)
                (dX,dY) = (diffX,diffY) #stores the difference between the two points
                cv2.putText(resize, direction, (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1 , (0,0,255), 3) #not sure where this goes rn
                    
            if absDiffX > threshold and (absDiffX > absDiffY):
                if diffX > 0  and last_dir != "right":
                    pyautogui.press("right")
                    last_position = (dX ,dY )
                    last_dir = "right"
                    print("right")
                if diffX < 0 and last_dir != "left":
                    pyautogui.press("left")
                    print("left")
                    last_position = (dX ,dY )
                    last_dir = "left"
                    print("left")
            if absDiffY > threshold and (absDiffY > absDiffX):
                if diffY > 0 and last_dir != "up":
                    pyautogui.press("up")
                    last_position = (dX ,dY )
                    last_dir = "up"
                    print("up")
                
                if diffY < 0 and last_dir != "down":
                    pyautogui.press("down")
                    last_position = (dX ,dY)
                    last_dir = "down"
                    print("down")

            cv2.imshow('Game Control Window', flipped)
            cv2.waitKey(1)
            num_frames += 1



        
     



def finger_tracking()->None:
    import cv2
    import imutils
    import numpy as np
    import time
    import multithreaded_webcam as mw
    import mediapipe as mp

    ##Sleep for 2 seconds to let camera initialize properly
    time.sleep(2)
    #Start video capture
    vs = mw.WebcamVideoStream().start()

    right_hand = mp.solutions.hands
    right_hand.Hands(static_image_mode=False, max_num_hands = 1, min_detection_confidence = 0.5, min_tracking_conference = 0)
    draw = mp.solutions.drawing_utils
    global last_dir
    upFingers = 0
    while True:
        frame = vs.read()
         
        #flip and resize frame
        flipped_frame = cv2.flip(frame,1) #I assigned flipped frame to cv2.flip differnet from above.
        imutils.resize(flipped_frame, width = 600)
        cv2.COLOR_BGR2RGB
        hands.process(flipped_frame) #what is hands
        #if multi
        #for i in range(multi_hand_landmarks):









def unique_control()->None:
    """
    @unique_control
    @purpose: Control the game through up and down scrolls 
    mixed with left/right clicks (mouse needed)
    @parameters: None
    @return: None
    """
    from pynput import mouse 
    from tkinter import Tk 
    #initializes variables to hold the last direction of scrolls and clicks 
    last_scroll = None
    last_click = None 

    #detects in what direction you are scrolling and inputs up/down directionality 
    def on_scroll(x,y,dx,dy)->None:
        if dy>0 and last_scroll != "down":
            pyautogui.press("down")
            print("down")
        elif dy<0 and last_scroll != "up":
            pyautogui.press("up")
            print("up")
        else:
            pass

    #detects left or right click and changes direction 
    def on_click(x, y, button, pressed)->None:
        click = button.name 
        if click == "left" and last_click != "left":
            if pressed:
                pyautogui.press("left")
                print("left")
        elif click == "right" and last_click != "right":
            if pressed:
                pyautogui.press("right")
                print("right")
        else:
            pass

    #establishes continous event listener
    with mouse.Listener(on_scroll = on_scroll, on_click = on_click) as listener:
        listener.join()

    """
    ATTENTION: ^^^code all works we just need to find out a way
    to disable the right click menus in order 
    for this method to make any sense
    """
   
    


def main():
    control_mode = input("How would you like to control the game? ")
    if control_mode == '1':
        keypress()
    elif control_mode == '2':
        trackpad_mouse()
    elif control_mode == '3':
        color_tracker()
    elif control_mode == '4':
        finger_tracking()
    elif control_mode == '5':
        unique_control()

if __name__ == '__main__':
	main()
