# !/usr/bin/python
#  _     _                           ____  _       _         ____                            _ _   _
# | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
# | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
# | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
# |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
#                                                                                |___/
# (c) Shahar Gino, May-2017, sgino209@gmail.com

from cv2 import resize, imshow, line, boxPoints, putText, getTextSize, FONT_HERSHEY_SIMPLEX

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
