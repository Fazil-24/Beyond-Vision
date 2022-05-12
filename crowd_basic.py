import numpy as np
import cv2, imutils
from imutils.object_detection import non_max_suppression

def average(lst):
    if len(lst) == 0:
        return 0
    else:
        return sum(lst) / len(lst)

def detect(frame):
    (bounding_box_cordinates, weights) = HOGCV.detectMultiScale(frame, winStride = (4, 4), padding = (8, 8), scale = 1.03)

    # non-maxima suppression
    bounding_box_cordinates = np.array([[x, y, x + w, y + h] for (x, y, w, h) in bounding_box_cordinates])
    nms_box = non_max_suppression(bounding_box_cordinates, probs=None, overlapThresh=0.65)
    
    person = 1
    # calculate center of each box and draw the bounding boxes for people
    centers=[]
    widths=[]
    for (xA, yA, xB, yB) in nms_box:
        widths.append(xB-xA)
        xC=xA+int((xB-xA)/2)
        yC=yA+int((yB-yA)/2)
        centers.append((xC,yC))
        cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
        cv2.circle(frame, (xC,yC), 15, (120,0,0), 2)
        cv2.putText(frame, f'person {person}', (xA,yA-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        person += 1
        
    cv2.putText(frame, 'Status : Detecting', (5,25), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0,0,0), 3)
    cv2.putText(frame, 'Status : Detecting', (5,25), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255,255,255), 1)
    
    cv2.putText(frame, f'Total Person : {person-1}', (5,55), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0,0,0), 3)
    cv2.putText(frame, f'Total Person : {person-1}', (5,55), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0,200,0), 1)
    
    violations=[]
    averageWidths = average(widths)
    distance= averageWidths * 2
    print("Distance: ", distance)
    violation_counter = 0
    for i,p1 in enumerate(centers):
        for j,p2 in enumerate(centers[i+1:]): 
            if (np.linalg.norm(np.array(p2)-np.array(p1)))< distance:
                if abs(p1[1] - p2[1])< distance // 2: 
                    cv2.line(frame, p1, p2, (0, 0, 255), thickness=3, lineType=3)
                    violations.append((i,j+i+1))
                  
    # detect violations and draw red bounding boxes              
    for (i,j) in violations:
        (xA, yA, xB, yB) = nms_box[i]
        cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 0, 255), 2)
        (xA, yA, xB, yB) = nms_box[j]
        cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 0, 255), 2)
        violation_counter += 1
    
    cv2.putText(frame, f'Social distance violations : {violation_counter}', (5,85), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0,0,0), 3)
    cv2.putText(frame, f'Social distance violations : {violation_counter}', (5,85), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0,0,255 ), 1)
    
    cv2.imshow('output', frame)
    return frame

def detectByPathVideo(path):

    video = cv2.VideoCapture(path)
    check, frame = video.read()
    if check == False:
        print('Video Not Found. Please Enter a Valid Path (Full path of Video Should be Provided).')
        return

    print('Detecting people...')
    while video.isOpened():
        check, frame =  video.read()

        if check:
            frame = imutils.resize(frame , width=min(800,frame.shape[1]))
            frame = detect(frame)

            key = cv2.waitKey(1)
            if key== ord('q'):
                break
        else:
            break
    video.release()
    cv2.destroyAllWindows()


path = "video/test.mp4"
HOGCV = cv2.HOGDescriptor()
HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
detectByPathVideo(path)