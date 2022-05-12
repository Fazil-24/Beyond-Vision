# import the necessary packages
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2
import h5py
import _pickle as cPickle
import pickle
import face_recognition
from subprocess import call
import datetime
import os
from PIL import Image, ImageDraw
import sys


import speech_recognition as sr
import pyttsx3 

ctime = datetime.datetime.now()

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice','voices[0].id')

def speak(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            statement = r.recognize_google(audio, language='en-in')
            print(f"user said:{statement}\n")

        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement



"""# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
args = vars(ap.parse_args())"""


i = 0
with open("trained_knn_model.clf", 'rb') as f:
 	knn_clf = pickle.load(f)

# if a video path was not supplied, grab the reference to the webcam
#if not args.get("video", False):
	
camera = cv2.VideoCapture(0)
 
# otherwise, grab a reference to the video file
#else:
	#camera = cv2.VideoCapture(args["video"])

while True:	

	# grab the current frame
	(grabbed, image1) = camera.read()
	# if we are viewing a video and we did not grab a
	# frame, then we have reached the end of the video
	"""if args.get("video") and not grabbed:
		break"""
	if grabbed:
		image = image1[:, :, ::-1]
	else:
		break
	#image=image1 
	#(w,h,d)=image.shape
	#print("w: {},h: {},d: {}",format(w,h))

	X_face_locations = face_recognition.face_locations(image)

	# If no faces are found in the image, return an empty result.
	if len(X_face_locations) != 0:
		
		# Find encodings for faces in the test iamge
		faces_encodings = face_recognition.face_encodings(image, known_face_locations=X_face_locations)

		# Use the KNN model to find the best matches for the test face
		#print(np.array(faces_encodings).shape)
		closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
		are_matches = [closest_distances[0][i][0] <= 0.4 for i in range(len(X_face_locations))]

		#draw = ImageDraw.Draw(image)

		# Predict classes and remove classifications that aren't within the threshold
		predictions = [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]
		
		for name, (top, right, bottom, left) in predictions:
			# Draw a box around the face using the Pillow module
			#draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
		
			# There's a bug in Pillow where it blows up with non-UTF-8 text
			# when using the default bitmap font
			#name = name.encode("UTF-8")
			#rect = (left,top,right,bottom)
			#(x, y, w, h) = face_utils.rect_to_bb(rect)
			cv2.rectangle(image1, (left,bottom),(right,top), (0, 255, 0), 2)
            
			# show the face number
            
			cv2.putText(image1, "{}".format(name), (left-10, top-10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
			
              
			# Draw a label with a name below the face
			#text_width, text_height = draw.textsize(name)
			#draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
			#draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))
			print (name)
            
            
			
			
			
			


				#import face_generate.py....to call face generate
				# call(["python","face_generate.py"])....other way to call face generate 
				
				
				
		
	#print(predictions)
	#cv2.imshow("output", image)	
	cv2.imshow("output image",image1)	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

camera.release()
cv2.destroyAllWindows()


speak('Hi')
speak(name)
speak('Welcome to apolo hospital')


while True:
    
    statement = takeCommand().lower()
    if statement == 0:
        continue

    if "thank you" in statement or "stop" in statement:
        speak('Happy to help you , bye')
        print('Happy to help you , bye ')
        break

#Appointment
    if 'fix an appointment' in statement:
        
        speak('What is the doctor name ')
        uname=takeCommand()
        speak('What is purpose of meeting')
        pur=takeCommand()
        speak('Ok Thank you ')
        speak('your appointment has been succesfully booked')
        file1 = open("Hosp-Appointment.txt","w")
        file1.write("Appointment details \n")

        with open('Hosp-Appointment.txt','a',encoding='utf-8') as f:
            file1.write("Name :")
            file1.write(uname)
            file1.write(" \n")
            file1.write("Appointment fixed with: ")
            file1.write("Dr.Sandeep")
            file1.write(" \n")
            file1.write("purpose of meeting: ")
            file1.write(pur)
            file1.write(" \n")
            file1.write("time: ")
            file1.write(str(ctime))
            file1.write(" \n")
            #file1.writelines(L)
            file1.close()
            