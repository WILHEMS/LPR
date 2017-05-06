# !/usr/bin/python
#  _     _                           ____  _       _         ____                            _ _   _
# | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
# | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
# | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
# |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
#                                                                                |___/
# (c) Shahar Gino, May-2017, sgino209@gmail.com

from math import atan, pi
from random import randint
from Preprocess import preprocess
from Auxiliary import Colors, debug
from PossibleChar import PossibleChar
from numpy import zeros, float32, uint8
from cv2 import imwrite, drawContours, findContours, resize, threshold, cvtColor, rectangle, \
    THRESH_BINARY, THRESH_OTSU, RETR_LIST, CHAIN_APPROX_SIMPLE, COLOR_GRAY2BGR

# ---------------------------------------------------------------------------------------------------------------
def detectCharsInPlates(listOfPossiblePlates, PreprocessGaussKernel, PreprocessThreshBlockSize, PreprocessThreshweight,
                        PreprocessMorphKernel, MinPixelWidth, MaxPixelWidth, MinPixelHeight, MaxPixelHeight,
                        MinAspectRatio, MaxAspectRatio, MinPixelArea, MaxPixelArea, MinDiagSizeMultipleAway, MaxDiagSizeMultipleAway,
                        MinNumberOfMatchingChars, MaxNumberOfMatchingChars, MinAngleBetweenChars, MaxAngleBetweenChars,
                        MinChangeInArea, MaxChangeInArea, MinChangeInWidth, MaxChangeInWidth, MinChangeInHeight,
                        MaxChangeInHeight, ResizedCharImageWidth, ResizedCharImageHeight, kNearest, DebugMode):
    """ Detect characters in the pre-detected plate (OCR analysis, over KNN engine) """

    # Early break condition (empty input):
    if len(listOfPossiblePlates) == 0:
        return listOfPossiblePlates

    # For each possible plate --> preprocess, find all characters, try to group them, remove overlaps and perform OCR:
    intPlateCounter = 0
    longestListOfMatchingCharsInPlate = []
    for possiblePlate in listOfPossiblePlates:

        # Pre-processing (CSC --> contrast --> blur --> threshold):
        possiblePlate.imgGrayscale, imgThreshScene = preprocess(possiblePlate.imgPlate,
                                                                PreprocessGaussKernel,
                                                                PreprocessThreshBlockSize,
                                                                PreprocessThreshweight,
                                                                PreprocessMorphKernel)

        # Increase size of plate image for easier viewing and char detection
        possiblePlate.imgThresh = resize(imgThreshScene, (0, 0), fx=1.6, fy=1.6)

        # Threshold again to eliminate any gray areas:
        _, possiblePlate.imgThresh = threshold(possiblePlate.imgThresh, 0.0, 255.0, THRESH_BINARY | THRESH_OTSU)

        # Find all possible chars in the plate (finds all contours that could be chars):
        listOfPossibleCharsInPlate = findPossibleCharsInPlate(possiblePlate.imgThresh,
                                                              MinPixelWidth, MaxPixelWidth,
                                                              MinPixelHeight, MaxPixelHeight,
                                                              MinAspectRatio, MaxAspectRatio,
                                                              MinPixelArea, MaxPixelArea)

        # Given a list of all possible chars, find groups of matching chars within the plate:
        listOfListsOfMatchingCharsInPlate = findListOfListsOfMatchingChars(listOfPossibleCharsInPlate,
                                                                           MinNumberOfMatchingChars, MaxNumberOfMatchingChars,
                                                                           MinAngleBetweenChars, MaxAngleBetweenChars,
                                                                           MinChangeInArea, MaxChangeInArea,
                                                                           MinChangeInWidth, MaxChangeInWidth,
                                                                           MinChangeInHeight, MaxChangeInHeight,
                                                                           MaxDiagSizeMultipleAway)

        # If groups of matching chars were found in the plate:
        if len(listOfListsOfMatchingCharsInPlate) > 0:

            # Within each list of matching chars, sort chars from left to right and remove inner overlapping chars:
            for i in range(0, len(listOfListsOfMatchingCharsInPlate)):
                listOfListsOfMatchingCharsInPlate[i].sort(key=lambda tmpMatchingChar: tmpMatchingChar.intCenterX)
                listOfListsOfMatchingCharsInPlate[i] = removeInnerOverlappingChars(listOfListsOfMatchingCharsInPlate[i],
                                                                                   MinDiagSizeMultipleAway)

            # Within each possible plate, loop through all the vectors of matching chars, get the index of the one with the most chars:
            intLenOfLongestListOfChars = 0
            intIndexOfLongestListOfChars = 0
            for i in range(0, len(listOfListsOfMatchingCharsInPlate)):
                if len(listOfListsOfMatchingCharsInPlate[i]) > intLenOfLongestListOfChars:
                    intLenOfLongestListOfChars = len(listOfListsOfMatchingCharsInPlate[i])
                    intIndexOfLongestListOfChars = i

            # Suppose that the longest list of matching chars within the plate is the actual list of chars:
            longestListOfMatchingCharsInPlate = listOfListsOfMatchingCharsInPlate[intIndexOfLongestListOfChars]

            # Characters recognition (OCR):
            possiblePlate.strChars = recognizeCharsInPlate(possiblePlate.imgThresh,
                                                           longestListOfMatchingCharsInPlate,
                                                           ResizedCharImageWidth,
                                                           ResizedCharImageHeight,
                                                           kNearest,
                                                           intPlateCounter,
                                                           DebugMode)

        # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
        if DebugMode:

            height, width, _ = possiblePlate.imgPlate.shape
            contours1 = []; imgContours1 = zeros((height, width, 3), uint8)
            contours2 = []; imgContours2 = zeros((height, width, 3), uint8)
            contours3 = []; imgContours3 = zeros((height, width, 3), uint8)
            contours4 = []; imgContours4 = zeros((height, width, 3), uint8)

            for possibleChar in listOfPossibleCharsInPlate:
                contours1.append(possibleChar.contour)
            drawContours(imgContours1, contours1, -1, Colors.white)

            if len(listOfListsOfMatchingCharsInPlate) > 0:

                for listOfMatchingChars in listOfListsOfMatchingCharsInPlate:
                    intRandomBlue = randint(0, 255)
                    intRandomGreen = randint(0, 255)
                    intRandomRed = randint(0, 255)
                    for matchingChar in listOfMatchingChars:
                        contours2.append(matchingChar.contour)
                    drawContours(imgContours2, contours2, -1, (intRandomBlue, intRandomGreen, intRandomRed))

                for listOfMatchingChars in listOfListsOfMatchingCharsInPlate:
                    intRandomBlue = randint(0, 255)
                    intRandomGreen = randint(0, 255)
                    intRandomRed = randint(0, 255)
                    for matchingChar in listOfMatchingChars:
                        contours3.append(matchingChar.contour)
                    drawContours(imgContours3, contours3, -1, (intRandomBlue, intRandomGreen, intRandomRed))

                for matchingChar in longestListOfMatchingCharsInPlate:
                    contours4.append(matchingChar.contour)
                drawContours(imgContours4, contours4, -1, Colors.white)

            imwrite("img_possible_plate_%d.jpg" % intPlateCounter, possiblePlate.imgPlate)
            imwrite("img_possible_plate_gray_%d.jpg" % intPlateCounter, possiblePlate.imgGrayscale)
            imwrite("img_possible_plate_threshold_scene_%d.jpg" % intPlateCounter, imgThreshScene)
            imwrite("img_possible_plate_threshold_%d.jpg" % intPlateCounter, possiblePlate.imgThresh)
            imwrite("img_possible_plate_contours1_%d.jpg" % intPlateCounter, imgContours1)
            if len(listOfListsOfMatchingCharsInPlate) > 0:
                imwrite("img_possible_plate_contours2_%d.jpg" % intPlateCounter, imgContours2)
                imwrite("img_possible_plate_contours3_%d.jpg" % intPlateCounter, imgContours3)
                imwrite("img_possible_plate_contours4_%d.jpg" % intPlateCounter, imgContours4)

            if len(listOfListsOfMatchingCharsInPlate) > 0:
                debug("Characters found in plate number #%d = %s" % (intPlateCounter, possiblePlate.strChars), True)
                intPlateCounter = intPlateCounter + 1
            else:
                debug("Characters found in plate number #%d = (none)" % intPlateCounter, True)
                intPlateCounter = intPlateCounter + 1

        # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
        # If no groups of matching chars were found in the plate, continue for next plate candidate:
        if len(listOfListsOfMatchingCharsInPlate) == 0:

            possiblePlate.strChars = ""
            continue

    if DebugMode:
        debug("Characters detection complete", True)

    return listOfPossiblePlates

# ---------------------------------------------------------------------------------------------------------------
def findPossibleCharsInPlate(imgBinary, MinPixelWidth, MaxPixelWidth, MinPixelHeight, MaxPixelHeight,
                             MinAspectRatio, MaxAspectRatio, MinPixelArea, MaxPixelArea):
    """ Find all possible chars in the plate (finds all contours that could be chars) """

    # Initialization:
    listOfPossibleChars = []
    imgBinaryCopy = imgBinary.copy()

    # Find all contours in plate:
    _, contours, _ = findContours(imgBinaryCopy, RETR_LIST, CHAIN_APPROX_SIMPLE)

    # check if it might be representing a possible character:
    # For each contour, create a PossibleChar object, which packs contour intrinsic geometrical metrics (for a later analysis):
    for contour in contours:
        possibleChar = PossibleChar(contour,
                                    MinPixelWidth, MaxPixelWidth,
                                    MinPixelHeight, MaxPixelHeight,
                                    MinAspectRatio, MaxAspectRatio,
                                    MinPixelArea, MaxPixelArea)

        # Add contour to list of possible characters (if found):
        if possibleChar.checkIfPossibleChar():
            listOfPossibleChars.append(possibleChar)

    return listOfPossibleChars

# ---------------------------------------------------------------------------------------------------------------
def findListOfListsOfMatchingChars(listOfPossibleChars, MinNumberOfMatchingChars, MaxNumberOfMatchingChars,
                                   MinAngleBetweenChars, MaxAngleBetweenChars, MinChangeInArea, MaxChangeInArea,
                                   MinChangeInWidth, MaxChangeInWidth, MinChangeInHeight, MaxChangeInHeight, MaxDiagSizeMultipleAway):
    """ Re-arrange the one big list of characters (listOfPossibleChars) into a list of lists of matching characters (listOfListsOfMatchingChars)
        Note: characters that are not found to be in a group of matches do not need to be considered further """

    # For each possible character in the one big list of characters, do:
    listOfListsOfMatchingChars = []
    for possibleChar in listOfPossibleChars:

        # Find all characters in the big list that match the current character (+ add the current character):
        listOfMatchingChars = findListOfMatchingChars(possibleChar,
                                                      listOfPossibleChars,
                                                      MaxDiagSizeMultipleAway,
                                                      MinAngleBetweenChars, MaxAngleBetweenChars,
                                                      MinChangeInArea, MaxChangeInArea,
                                                      MinChangeInWidth, MaxChangeInWidth,
                                                      MinChangeInHeight, MaxChangeInHeight)
        listOfMatchingChars.append(possibleChar)

        # If current list not too short and not too long, then it may be a valid plate candidate:
        if MinNumberOfMatchingChars <= len(listOfMatchingChars) <= MaxNumberOfMatchingChars:

            # Add the cluster of characters to the list of lists of matching characters:
            listOfListsOfMatchingChars.append(listOfMatchingChars)

            # Remove the current list of matching characters from the big list, for not using same characters twice:
            listOfPossibleCharsWithCurrentMatchesRemoved = list(set(listOfPossibleChars) - set(listOfMatchingChars))

            # Recursive call:
            recursiveListOfListsOfMatchingChars = findListOfListsOfMatchingChars(listOfPossibleCharsWithCurrentMatchesRemoved,
                                                                                 MinNumberOfMatchingChars, MaxNumberOfMatchingChars,
                                                                                 MinAngleBetweenChars, MaxAngleBetweenChars,
                                                                                 MinChangeInArea, MaxChangeInArea,
                                                                                 MinChangeInWidth, MaxChangeInWidth,
                                                                                 MinChangeInHeight, MaxChangeInHeight,
                                                                                 MaxDiagSizeMultipleAway)

            # For each list of matching characters found by recursive call, add to the list of lists of matching chars:
            for recursiveListOfMatchingChars in recursiveListOfListsOfMatchingChars:
                listOfListsOfMatchingChars.append(recursiveListOfMatchingChars)

            break

    return listOfListsOfMatchingChars

# ---------------------------------------------------------------------------------------------------------------
def findListOfMatchingChars(possibleChar, listOfChars, MaxDiagSizeMultipleAway, MinAngleBetweenChars, MaxAngleBetweenChars,
                            MinChangeInArea, MaxChangeInArea, MinChangeInWidth, MaxChangeInWidth, MinChangeInHeight, MaxChangeInHeight):
    """ Find all characters in the big list of possible characters, that match a single possible character, 
        and return those matching chars as a list """

    # For each character in big list, do:
    listOfMatchingChars = []
    for possibleMatchingChar in listOfChars:

        # Bypass self matches, to avoid double insertions of current char:
        if possibleMatchingChar == possibleChar:
            continue

        # Compute intrinsic metrics for characters match-up:
        fltDistanceBetweenChars = possibleChar - possibleMatchingChar
        fltAngleBetweenChars = angleBetweenChars(possibleChar, possibleMatchingChar)
        fltChangeInArea = float(abs(possibleMatchingChar.intBoundingRectArea - possibleChar.intBoundingRectArea)) / float(possibleChar.intBoundingRectArea)
        fltChangeInWidth = float(abs(possibleMatchingChar.intBoundingRectWidth - possibleChar.intBoundingRectWidth)) / float(possibleChar.intBoundingRectWidth)
        fltChangeInHeight = float(abs(possibleMatchingChar.intBoundingRectHeight - possibleChar.intBoundingRectHeight)) / float(possibleChar.intBoundingRectHeight)

        # Check if characters match, and add the current character to list of matching characters if so:
        if (fltDistanceBetweenChars < (possibleChar.fltDiagonalSize * MaxDiagSizeMultipleAway) and
            MinAngleBetweenChars <= fltAngleBetweenChars < MaxAngleBetweenChars and
            MinChangeInArea <= fltChangeInArea < MaxChangeInArea and
            MinChangeInWidth <= fltChangeInWidth < MaxChangeInWidth and
            MinChangeInHeight <= fltChangeInHeight < MaxChangeInHeight):

            listOfMatchingChars.append(possibleMatchingChar)

    return listOfMatchingChars

# ---------------------------------------------------------------------------------------------------------------
def angleBetweenChars(firstChar, secondChar):
    """ Use basic trigonometry (SOH, CAH, TOA) to calculate angle between two given characters """

    fltAdj = float(abs(firstChar.intCenterX - secondChar.intCenterX))
    fltOpp = float(abs(firstChar.intCenterY - secondChar.intCenterY))

    if fltAdj != 0.0:
        fltAngleInRad = atan(fltOpp / fltAdj)
    else:
        fltAngleInRad = 1.5708   # 90 degrees case:

    # Calculate angle in degrees:
    fltAngleInDeg = fltAngleInRad * (180.0 / pi)

    return fltAngleInDeg

# ---------------------------------------------------------------------------------------------------------------
def removeInnerOverlappingChars(listOfMatchingChars, MinDiagSizeMultipleAway):
    """ If we have two characters overlapping or to close to each other to possibly be separate chars, remove the inner (smaller) character.
        This is to prevent including the same character twice if two contours are found for the same character.
        For example, for the letter 'O', both the inner ring and the outer ring may be found as contours, but we should only include the character once """

    listOfMatchingCharsWithInnerCharRemoved = list(listOfMatchingChars)
    for currentChar in listOfMatchingChars:
        for otherChar in listOfMatchingChars:

            # If current char and other char are not the same character:
            if currentChar != otherChar:

                # If current character and other character have center points at almost the same location:
                if (currentChar - otherChar) < (currentChar.fltDiagonalSize * MinDiagSizeMultipleAway):

                    # Overlapping characters handling: identify which character is smaller and remove it (if not already removed on a previous pass)
                    if currentChar.intBoundingRectArea < otherChar.intBoundingRectArea:
                        if currentChar in listOfMatchingCharsWithInnerCharRemoved:
                            listOfMatchingCharsWithInnerCharRemoved.remove(currentChar)
                    else:
                        if otherChar in listOfMatchingCharsWithInnerCharRemoved:
                            listOfMatchingCharsWithInnerCharRemoved.remove(otherChar)

    return listOfMatchingCharsWithInnerCharRemoved

# ---------------------------------------------------------------------------------------------------------------
def recognizeCharsInPlate(imgThresh, listOfMatchingChars, ResizedCharImageWidth, ResizedCharImageHeight, kNearest, intPlateCounter, debugMode):
    """ This is where we apply the actual char recognition """

    # Initialization:
    strChars = ""
    height, width = imgThresh.shape
    imgThreshColor = zeros((height, width, 3), uint8)

    # Sort characters from left to right:
    listOfMatchingChars.sort(key=lambda matchingChar: matchingChar.intCenterX)

    # Make Color Version of Threshold image, for drawing contours in color on it:
    cvtColor(imgThresh, COLOR_GRAY2BGR, imgThreshColor)

    # For each character in the plate
    for currentChar in listOfMatchingChars:

        # Draw a green box around the character:
        pt1 = (currentChar.intBoundingRectX, currentChar.intBoundingRectY)
        pt2 = ((currentChar.intBoundingRectX + currentChar.intBoundingRectWidth), (currentChar.intBoundingRectY + currentChar.intBoundingRectHeight))
        rectangle(imgThreshColor, pt1, pt2, Colors.green, 2)

        # Crop the characters out of threshold image:
        imgROI = imgThresh[currentChar.intBoundingRectY: currentChar.intBoundingRectY + currentChar.intBoundingRectHeight,
                           currentChar.intBoundingRectX: currentChar.intBoundingRectX + currentChar.intBoundingRectWidth]

        # Resize the image (necessary for later OCR):
        imgROIResized = resize(imgROI, (ResizedCharImageWidth, ResizedCharImageHeight))

        # Flatten the resized image into 1d numpy array:
        npaROIResized = imgROIResized.reshape((1, ResizedCharImageWidth * ResizedCharImageHeight))

        # Convert from 1d numpy array of ints to 1d numpy array of floats:
        npaROIResized = float32(npaROIResized)

        # OCR, by calling findNearest (KNN):
        _, npaResults, _, _ = kNearest.findNearest(npaROIResized, k=1)

        # Get character from results, and append it to the full string:
        strCurrentChar = str(chr(int(npaResults[0][0])))
        strChars = strChars + strCurrentChar

    if debugMode:
        imwrite("img_ocr_result_%d.jpg" % intPlateCounter, imgThreshColor)

    return strChars
