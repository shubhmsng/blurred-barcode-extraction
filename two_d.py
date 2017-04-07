import numpy as np
import cv2
from PIL import Image
import zbar

def two_d(image):

    kernel_sharpen = np.array([[-1,-1,-1,-1,-1],
                                 [-1,2,2,2,-1],
                                 [-1,2,8,2,-1],
                                 [-1,2,2,2,-1],
                                 [-1,-1,-1,-1,-1]]) / 8.0


    ##############################################
    # step 1: read image that contains barcode   #
    ##############################################

    image = cv2.imread(str(image))

    #################################################
    # step 2: convert image in to gray scale  format#
    #################################################

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ##############################################
    # step 3: find x gradient and y gradient     #
    ##############################################

    gradX = cv2.convertScaleAbs(cv2.Sobel(src= gray, ddepth=cv2.CV_64F, dx=1, dy=0,ksize=3))

    gradY = cv2.convertScaleAbs(cv2.Sobel(src=gray, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=3))

    ##############################################
    # step 4: subtract x gradient and y gradient #
    ##############################################

    gradient = cv2.subtract(gradX, gradY)

    ##########################################################
    # step 5: find threshold image using binary thresholding #
    ##########################################################

    ret, threshold = cv2.threshold(gradient, 187,255, cv2.THRESH_BINARY)

    #########################################################
    # step: 6  Morphological operation                      #
    #########################################################

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18,15))
    closed = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)

    #################################################
    # step 7: perform dilation on thresholded image #
    #################################################

    dilate = cv2.dilate(closed, None, iterations=5)

    ####################################################
    # step 8: perform erode operation on dilated image #
    ####################################################

    closed = cv2.erode(dilate, None, iterations=10)

    ##############################################
    # step 9: find contours on the image         #
    ##############################################

    contours, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    ###################################################
    # step 10: sort all contours on the basis of area #
    ###################################################

    c = sorted(contours, key=cv2.contourArea, reverse=True)[0]

    ###########################################################################
    # step 11: find the barcode contour and get the pixel location of contour #
    ###########################################################################

    rect = cv2.minAreaRect(c)

    box = np.int0(cv2.cv.BoxPoints(rect))

    a = np.asarray(box)

    max_x = 1
    min_x = 99999999999

    max_y = 1
    min_y = 99999999999

    for i in range(len(a)):
        if(a[i][0]<min_x ):
            min_x = a[i][0]
        if(a[i][1] < min_y ):
            min_y = a[i][1]


    for i in range(len(a)):
        if(a[i][0]>max_x):
            max_x = a[i][0]
        if(a[i][1] > max_y):
            max_y = a[i][1]

    x = min_x-15
    y = min_y-15
    w = max_x-min_x+15
    h = max_y-min_y+15

    if(x < 1):
        x = 1
    if(y < 1):
        y = 1

    #####################################################
    # step 12: crop the barcode from the original image #
    #####################################################

    cr_img = image[y:y+h+50, x:x+w+50]

    #####################################################
    # step 13: find the width and height of the barcode #
    #####################################################

    width = len(cr_img[0])
    height = len(cr_img)

    #######################################
    # step 14: zoom the barcode 1.5 times #
    #######################################

    cr_img = cv2.resize(cr_img, (width+ width/2, height +height/2))

    ############################################
    # step 15: smooth the barcode on the edges #
    ############################################

    cr_img = cv2.filter2D(cr_img, -1, kernel_sharpen)

    #######################################
    # step 16: display barcode            #
    #######################################

    cv2.imshow("gray", cr_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    #######################################
    # step 17: create a reader            #
    #######################################

    scanner = zbar.ImageScanner()

    #######################################
    # step 18: configure the reader       #
    #######################################

    scanner.parse_config('enable')

    #######################################
    # step 19: obtain image data          #
    #######################################

    cr_img = Image.fromarray(cr_img)
    cr_img = cr_img.convert('L')
    width, height = cr_img.size
    raw = cr_img.tobytes()

    #######################################
    # step 20: wrap image data            #
    #######################################

    image = zbar.Image(width, height, 'Y800', raw)

    ########################################
    # step 21: scan the image for barcode  #
    ########################################

    scanner.scan(image)

    #######################################
    # step 22: extract results            #
    #######################################

    result = ""
    for symbol in image:
        result += 'decoded ' + str(symbol.type) + ' symbol ' + '"%s"' % symbol.data + "\n"
    if result == "":
        return "unable to read barcode"
    else:
        return result