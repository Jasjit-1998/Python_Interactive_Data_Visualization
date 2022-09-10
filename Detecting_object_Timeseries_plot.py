# Continue from Code Detecting_moving_object
# Aim - Storin the time csv file when the object enter or leave the frame.



import cv2, time, pandas
from datetime import datetime

video = cv2.VideoCapture(0)

# Checking how many frames being generated
# Cheating a variable outsid the while loop
# Initialization section

first_frame = None
status_list = [None, None]      # Adding the 2 items into the list otherwise the errorn will occur
times = []
# Initializing dandas frame to read the date and the columns
df = pandas.DataFrame(columns = ["Start", "End"])

while True:

    check, frame = video.read()
    status = 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Removing the noise from the immge by blurring it with GaussianBlue
    # gray=cv2.GaussianBlur(gray,size of gaussain blur,standard deviation)
    gray=cv2.GaussianBlur(gray,(21,21),0)
# Link - https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html

    if first_frame is None:
        first_frame = gray         # We will get the first frame in the numpy array
        continue

        # When the object appear in the frame then above if condition will be false
        # Comparing the diffrence between the current frame and the delta frames
    delta_frame = cv2.absdiff(first_frame,gray)
    # <SYNTAX>.thresh_delta = cv2.threshold(delta_frame, diffrence between frames , 255, cv.THRESH_BINARY)
    thresh_delta = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]     # Accesing second item of the tuple as we are using the threshold binary
    thresh_frame = cv2.dilate(thresh_delta, None, iterations = 2)   # Smoothning of the threshold

# Finding the Countour   (Soring the countour in the Tupil)
# Checking the Area of the countour
    # <SYNTAX> = (cnts,_) = cv2.findCountours(thresh_frame.copy(), cv2.RETR_EXTERNAL (external Countour retrival), cv2.CHAIN_APPROX_SIMPLE(approximation method used by the open cv))
    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue

        status =1     # If the window is greater than 10000 we will chage the status to 1

   # If countour is greater than 1000 pixel then we have to draw the rectangle arounf that frame
   # Perameters defining the rectangle
        (x, y, w, h) = cv2.boundingRect(contour) # Creating the rectagle
        cv2.rectangle(frame, (x,y), (x+w, y+w), (0,255,0), 3)  # Drawing the rectangle on the frame

    status_list.append(status)    # Printing the status list outside the while loop

# Checking the last 2 items of the list [0,1]   Status changes from 0 to 1 or 1 to 0

# Recording the time whien the status change from 1 to 0
    if status_list[-1] ==1 and status_list[-2] ==0:
        times.append(datetime.now())
        # We need to record the date and time of the event in the list

# When the status change from p to 1
    if status_list[-1] ==0 and status_list[-2] ==1:
        times.append(datetime.now())

    cv2.imshow("Gray Frame", gray)
    cv2.imshow("DeltaFrame", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key=cv2.waitKey(1)
    #print(gray)

    if key == ord('q'):

        if status ==1:
            times.append(datetime.now())   # when the sttaus is 1 and the window is closed then it will record the time of the window
        break

print(status_list)   # Printing status list outside the while loop
print(times)

for i in range(0,len(times),2):
    df = df.append({"Start": times[i], "End":times[i+1]}, ignore_index = True)
        #cv2.imshow("delta_frame",delta_frame)

df.to_csv("Times.csv")
    #time.sleep(3)    # Holding the script for 3 seconds



# If statement will break the while loop when 'q' key is pressed
video.release()
cv2.detroyAllWindows()


# Creating the frame object which will read video of that Object
