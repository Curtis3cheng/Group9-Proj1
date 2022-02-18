import pyautogui

last_position = (None,None)
last_dir = ''

def keypress():
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
    Control the game by moving the mouse/finger on trackpad left, right, up, or down. 
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
    import cv2
    import imutils
    import numpy as np
    from collections import deque
    import time
    import multithreaded_webcam as mw

    # You need to define HSV colour range MAKE CHANGE HERE
    colorLower = (0,106,255)
    colorUpper = (59, 0 , 255)

    # set the limit for the number of frames to store and the number that have seen direction change
    buffer = 20
    pts = deque(maxlen = buffer)

    # store the direction and number of frames with direction change
    num_frames = 0
    (dX, dY) = (0, 0)
    direction = ''
    global last_dir

    #Sleep for 2 seconds to let camera initialize properly
    time.sleep(2)
    #Start video capture
    vs = mw.WebcamVideoStream().start()


    while True:
        frame = vs.read()
         
        #flip and resize frame
        cv2.flip(frame,1)
        imutils.resize(frame, width = 600)

        #reduce noise and convert to HSV
        cv2.GaussianBlur(frame, (5,5), 0) 
        cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #creates MASK
        mask = cv2.inRange(frame, colorLower, colorUpper)
        cv2.erode(mask, None, iterations = 2)
        cv2.dilate(mask, None, iterations = 2)

        #creates object of the found color differentiation 
        foundObj = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        objCenter = None
        
        if len(foundObj) != 0:

        



def finger_tracking():
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

    # put your code here


def unique_control():
    # put your code here
    pass

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
