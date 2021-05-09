import cv2
import numpy as np
# import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model

# face_clsfr=cv2.CascadeClassifier('face_det.xml')
cap=cv2.VideoCapture(0)
labels_dict={0:'MASK',1:'NO MASK'}
color_dict={0:(0,255,0),1:(0,0,255)}
mod = load_model('maskdet2.model')
# face_clsfr=cv2.CascadeClassifier('face_det.xml')

while(True):

    ret,img = cap.read()
    # cv2.imshow("imm",img)
    # print(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray,(224,224))/255
    label = mod.predict(gray.reshape(1,224,224,1))
    label = np.argmax(label)
    print(label,end='')
    img = cv2.putText(img, labels_dict[label], (50,50) , fontFace =cv2.FONT_HERSHEY_SIMPLEX ,fontScale=1,color=(255,0,0),thickness=2)
    
    cv2.imshow('LIVE',img)
    if cv2.waitKey(1) and 0xFF==ord('q'):
        break 
cv2.destroyAllWindows()
cap.release()