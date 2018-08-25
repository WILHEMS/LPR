#!/usr/bin/python
#  _     _                           ____  _       _         ____                            _ _   _
# | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
# | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
# | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
# |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
#                                                                                |___/
# (c) Shahar Gino, July-2017, sgino209@gmail.com

from random import randint
from numpy import linspace, dstack
from onvif_capture import onvif_camera
from cv2 import resize, imshow, line, boxPoints, putText, getTextSize, FONT_HERSHEY_SIMPLEX, getRectSubPix,\
    COLOR_BGR2GRAY, cvtColor, Canny, matchTemplate, minMaxLoc, rectangle, TM_CCORR_NORMED, imread, imwrite

# ---------------------------------------------------------------------------------------------------------------
# Python structuring way:
class Struct:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

# ---------------------------------------------------------------------------------------------------------------
# Color vectors:
Colors = Struct(
    white=(255.0, 255.0, 255.0),
    green=(0.0, 255.0, 0.0),
    red=(0.0, 0.0, 255.0),
    yellow=(0.0, 255.0, 255.0)
)

# ---------------------------------------------------------------------------------------------------------------
def imshow_scaled(figure, img, dimensions):
    """ downscale + imshow """
    if img.shape[0] > dimensions[0] or img.shape[0] > dimensions[1]:
        img = resize(img, (img.shape[1] / 2, img.shape[0] / 2))
    imshow(figure, img)


# ---------------------------------------------------------------------------------------------------------------
def debug(message, debugMode):
    """ Auxiliary function for a conditional debug printout """

    if debugMode:
        print "DEBUG: %s" % message

# ---------------------------------------------------------------------------------------------------------------
def info(message):
    """ Auxiliary function for a info printout """

    print "INFO: %s" % message

# ---------------------------------------------------------------------------------------------------------------
def error(message):
    """ Auxiliary function for a error printout """

    print "ERROR: %s" % message

# ---------------------------------------------------------------------------------------------------------------
def drawRedRectangleAroundPlate(imgOriginalScene, licPlate, color):
    """ Mark a given license-plate (licPlate) with a colored rectangle """

    # Get 4 vertices of rotated rectangle:
    if licPlate.rrLocationOfPlateInSceneGbl is not None:
        p2fRectPoints = boxPoints(licPlate.rrLocationOfPlateInSceneGbl)
    else:
        p2fRectPoints = boxPoints(licPlate.rrLocationOfPlateInScene)

    # Draw 4 red lines:
    line(imgOriginalScene, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), color, 2)
    line(imgOriginalScene, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), color, 2)
    line(imgOriginalScene, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), color, 2)
    line(imgOriginalScene, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), color, 2)

# ---------------------------------------------------------------------------------------------------------------
def writeLicensePlateCharsOnImage(imgOriginalScene, licPlate, color):
    """ Write the given license-plate characters (licPlate.strChars) the provided image (imgOriginalScene) """

    # Retrieve basic geometric metrics:
    sceneHeight = imgOriginalScene.shape[0]
    plateHeight = licPlate.imgPlate.shape[0]

    # Font styling (type, scale, thickness):
    intFontFace = FONT_HERSHEY_SIMPLEX
    fltFontScale = float(plateHeight) / 30.0
    intFontThickness = int(round(fltFontScale * 1.5))
    textSize = getTextSize(licPlate.strChars, intFontFace, fltFontScale, intFontThickness)[0]

    # Retrieve license-plate centroid:
    if licPlate.rrLocationOfPlateInSceneGbl is not None:
        ((intPlateCenterX, intPlateCenterY), (_, _), _) = licPlate.rrLocationOfPlateInSceneGbl
    else:
        ((intPlateCenterX, intPlateCenterY), (_, _), _) = licPlate.rrLocationOfPlateInScene

    # The horizontal location of the text area is the same as the plate:
    ptCenterOfTextAreaX = int(intPlateCenterX)

    # The vertical location of the test area depends on the license-plate location in the scene image::
    if intPlateCenterY < (sceneHeight * 0.75):
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) + int(round(plateHeight * 1.6))  # chars below the plate
    else:
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) - int(round(plateHeight * 1.6))  # chars above the plate

    # Calculate the lower left origin of the text area based on the text area center, width, and height:
    ptLowerLeftTextOriginX = int(ptCenterOfTextAreaX - (textSize[0] / 2))
    ptLowerLeftTextOriginY = int(ptCenterOfTextAreaY + (textSize[1] / 2))

    # Write the text on the image:
    putText(imgOriginalScene, licPlate.strChars, (ptLowerLeftTextOriginX, ptLowerLeftTextOriginY), intFontFace, fltFontScale, color, intFontThickness)

# ---------------------------------------------------------------------------------------------------------------
def ROI_adjust(ROI, imgOriginalScene, W, H):
    """ ROI adjustments """

    imgH, imgW, _ = imgOriginalScene.shape

    if len(ROI) == 2 and ROI[0] == -1 and ROI[1] == -1:

        adjROI = (int(imgW * W[0]/100.0), int(imgH * H[0]/100.0),  int(imgW * W[1]/100.0), int(imgH * H[1]/100.0))
        autoRoiMode = True

        if sum(W) != 100 or sum(H) != 100:
            error('Invalid autoROI settings, doesnt converge to 100 percent: W=%s, H=%s' % (W, H))

    elif len(ROI) == 2 and ROI[0] == 0 and ROI[1] == 0:

        adjROI = (0, 0,  imgW, imgH)
        autoRoiMode = False

    else:
        adjROI = ROI
        autoRoiMode = False

    return adjROI, autoRoiMode

# ---------------------------------------------------------------------------------------------------------------
def crop_roi_from_image(imgOriginalScene, ROI, autoRoiMode):
    """ Crop a given ROI from a given Image; ROI=(startX,startY,W,H) """

    if ROI[2] == -1 or ROI[3] == -1:
        imgH, imgW, _ = imgOriginalScene.shape
        roiW = imgW
        roiH = imgH
    else:
        roiW = ROI[2]
        roiH = ROI[3]

    roiCx = ROI[0] + roiW / 2.0
    roiCy = ROI[1] + roiH / 2.0

    imgCropped = getRectSubPix(imgOriginalScene, (roiW, roiH), (roiCx, roiCy))

    info("ROI size: (Cx,Cy)=(%.2f,%.2f), WxH=%dx%d, autoROI=%d" % (roiCx, roiCy, roiW, roiH, int(autoRoiMode)))

    return imgCropped

# ---------------------------------------------------------------------------------------------------------------
def load_input_scene_image(ImageFile, ImType='Image', onvif_ip="", onvif_port=0, onvif_user="", onvif_passwd=""):
    """ Load input scene image (exit if fails) """

    if ImageFile == "onvif":
        mycam = onvif_camera(onvif_ip, onvif_port, onvif_user, onvif_passwd)
        imgOriginalScene = mycam.snaphot_capture()
    else:
        imgOriginalScene = imread(ImageFile)

    if imgOriginalScene is None:
        error("%s not read from file" % ImType)
        return None

    imgH, imgW, _ = imgOriginalScene.shape

    info("%s size: WxH=%dx%d" % (ImType, imgW, imgH))

    return imgOriginalScene

# ---------------------------------------------------------------------------------------------------------------
def isTemplateFound(imgOriginal, template, template_name, template_thr, debugMode):
    """ Seeking for police symbol in a multi-Scale template-matching fashion """

    # Convert original image to gray, and move to edge representation (boot + more accurate TM):
    gray = cvtColor(imgOriginal, COLOR_BGR2GRAY)
    edged_gray = Canny(gray, 50, 200)
    clone = dstack([edged_gray, edged_gray, edged_gray])

    # Convert template to gray:
    template_gray = cvtColor(template, COLOR_BGR2GRAY)

    # Loop over the scales of the template:
    found = None
    for scale in linspace(0.15, 1.0, 20)[::-1]:

        # Resize the template according to the scale, and keep track of the ratio of the resizing:
        resized = resize(template_gray, (0,0), fx=scale, fy=scale)
        (tH, tW) = resized.shape[:2]

        # Detect edges in the resized template, and apply template matching to find it in the edged image:
        edged_template = Canny(resized, 50, 200)
        result = matchTemplate(edged_gray, edged_template, TM_CCORR_NORMED)
        (_, maxVal, _, maxLoc) = minMaxLoc(result)

        # Check to see if the iteration should be visualized:
        if debugMode:

            # Draw a bounding box around the detected region
            intRandomBlue = randint(0, 255)
            intRandomGreen = randint(0, 255)
            intRandomRed = randint(0, 255)
            randColor = (intRandomBlue, intRandomGreen, intRandomRed)
            putText(clone, "maxVal=%.2f" % maxVal, (maxLoc[0], maxLoc[1]-20), FONT_HERSHEY_SIMPLEX, 1, randColor, 2)
            rectangle(clone, (maxLoc[0], maxLoc[1]), (maxLoc[0] + tW, maxLoc[1] + tH), randColor, 2)
            debug("maxVal=%.3f, tH=%d, tW=%d" % (maxVal, tH, tW), True)

        # If we have found a new maximum correlation value, then update the book-keeping variable:
        if found is None or maxVal > found[0]:
            found = (maxVal, maxLoc, tH, tW)

    if debugMode:
        imwrite("TemplateMatching_%s.jpg" % template_name, clone)

    if found is None:

        is_found = False
        loc = (None, None)

    else:

        # Unpack the book-keeping varaible and compute the (x, y) coordinates of the bounding box based on the resized ratio:
        (maxVal, maxLoc, tH, tW) = found
        (startX, startY) = (int(maxLoc[0]), int(maxLoc[1]))
        (endX, endY) = (int((maxLoc[0] + tW)), int((maxLoc[1] + tH)))
        loc = (maxLoc[0]+tW/2, maxLoc[1]+tH/2)
        avg_color = imgOriginal[startY:startY+tH, startX:startX+tW, :].mean()

        # draw a bounding box around the detected result and display the image
        is_found = maxVal >= template_thr[0] and avg_color > template_thr[1]

        if is_found:

            info("%s vehicle detected! (val1=%.2f, val2=%.2f)" % (template_name, found[0], avg_color))

            if debugMode:

                imgOriginalCopy = imgOriginal.copy()
                rectangle(imgOriginalCopy, (startX, startY), (endX, endY), (0, 255, 0), 2)
                putText(imgOriginalCopy, "maxVal=%.2f, avgRed=%.2f" % (maxVal, avg_color), (10, 30), FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                imwrite("img_%s_symbol.jpg" % template_name, imgOriginalCopy)

    return (is_found, loc)

# ---------------------------------------------------------------------------------------------------------------
def sample_image(imgGray, sampleRect, maxVal):
    """ Sample image in a given rectangle, represented as [x0,y0,w,h], where x0,y0 is the top-left coordinates of the sampling region """

    y0, x0, w, h = sampleRect

    sampleSum = 0
    for y in range(h):
        for x in range(w):
            sampleSum += imgGray[y0+y][x0+x]

    sample = float(sampleSum) / (w * h * maxVal)

    return sample
