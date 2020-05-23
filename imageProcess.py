
#car plate detection function
import numpy as np
import cv2
import pytesseract
import imutils
import logging

def processPlate(plate, filename):
    #read image
    image = cv2.imread(plate)

    #resize image
    image = imutils.resize(image, width=500)

    #RGB to Gray Scale converstion
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #noise removal 
    gray = cv2.bilateralFilter(gray,11,17,17)

    #find edges of the grayscale image
    edged = cv2.Canny(gray, 170,200)

    #Find contours based on Edges
    _,cnts, new  = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    #Create copy of original image to draw all contours
    img1 = image.copy()
    cv2.drawContours(img1, cnts, -1, (0,255,0), 3)

    #sort contours based on their area keeping minimum required area as '30' (anything smaller than this will not be considered)
    cnts=sorted(cnts, key = cv2.contourArea, reverse = True)[:30]
    NumberPlateCnt = None #we currently have no Number plate contour

    #Top 30 Contours
    img2 = image.copy()
    cv2.drawContours(img2, cnts, -1, (0,255,0), 3)

    #loop over our contours to find the best possible approximate contour of number plate
    idx=filename
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # print ("approx = ",approx)
        if len(approx) == 4:  # Select the contour with 4 corners
            NumberPlateCnt = approx #This is our approx Number Plate Contour

            # Crop those contours and store it in Cropped Images folder
            x, y, w, h = cv2.boundingRect(c) #This will find out co-ord for plate
            new_img = gray[y:y + h, x:x + w] #Create new image
            cv2.imwrite('upload/' + 'cropped_' + str(idx), new_img) #Store new image
            #idx+=1

            break

    #Drawing the selected contour on the original image
    #print(NumberPlateCnt)
    cv2.drawContours(image, [NumberPlateCnt], -1, (0,255,0), 3)
    #cv2.imshow("Final Image With Number Plate Detected", image)
    #cv2.waitKey(0)

    Cropped_img_loc = 'upload/' + 'cropped_' + str(idx)#'cropped_images/8.png'

    #Use tesseract to covert image into string
    text = pytesseract.image_to_string(Cropped_img_loc, lang='eng')
    text = text.replace('.', '')
    text = text.replace(' ','')
    return text
    


#processPlate('car_images/3.jpg')

#import cv2
#import pytesseract
#import imutils

#def processPlate(image):
#    img = cv2.imread(image)
#    #use tesseract to convert image into strinf
#    text = pytesseract.image_to_string(img, lang='eng')
#    return text