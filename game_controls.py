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
        if keyboard.is_pressed('a'):
            pyautogui.press("left")
        if keyboard.is_pressed('s'):
            pyautogui.press("down")
        if keyboard.is_pressed('d'):
            pyautogui.press("right")


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
            thresholdX = 40
            thresholdy = 60
            if absDiffX > thresholdX and (absDiffX > absDiffY) :
                if diffX < 0  and last_dir != "right":
                    pyautogui.press("right")
                    last_dir = "right"
                    print("right")
                if diffX > 0 and last_dir != "left":
                    pyautogui.press("left")
                    last_dir = "left"
                    print("left")
            if absDiffY > thresholdy and (absDiffY > absDiffX):
                if diffY > 0 and last_dir != "up":
                    pyautogui.press("up")
                    last_dir = "up"
                    print("up")
                
                if diffY < 0 and last_dir != "down":
                    pyautogui.press("down")
                    last_dir = "down"
                    print("down")

                
            
               


            """
            Version 1:
            if absDiffX or absDiffY > 50: #need to check threshold
                if diffX > diffY:
                    if absDiffX < 50:
                        pyautogui.press("right")
                        last_dir = "right"
                        print("right")
                        
                    else:
                        pyautogui.press("left")
                        last_dir = "left"
                        print("left")

                        
                else:
                    if absDiffY < 0:
                        pyautogui.press("down")
                        last_dir = "down"
                        print("down")
                    else:
                        pyautogui.press("up")
                        last_dir = "up"
                        print("up")

            """
            """
            #variation 2
            if absDiffX > 30:
                if diffX > diffY :
                    if diffX < 100 and (last_dir != "right" or "left"):
                        pyautogui.press("right")
                        last_dir = "right"

                        print("right")

                        
                    else:
                        pyautogui.press("left")
                        last_dir = "left"
                        print("left")
            
            if absDiffY > 50 and (last_dir != "down" or "up"):
                if diffY < 100:
                        pyautogui.press("down")
                        last_dir= "down"
                        print("down")
                else:
                        pyautogui.press("up")
                        last_dir = "up"
                        print("up")

            """

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
    colorLower = None
    colorUpper = None

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
        # your code here
        continue
        



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
