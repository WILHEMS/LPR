#!/usr/bin/python
#  _     _                           ____  _       _         ____                            _ _   _
# | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
# | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
# | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
# |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
#                                                                                |___/
# (c) Shahar Gino, July-2017, sgino209@gmail.com

from math import atan, pi
from random import randint
from Preprocess import preprocess
from PossibleChar import PossibleChar
from Auxiliary import Colors, debug, info, sample_image
from numpy import zeros, float32, uint8, ones, median, sqrt
from cv2 import imwrite, drawContours, findContours, resize, threshold, cvtColor, rectangle, COLOR_BGR2HSV, mean, \
    THRESH_BINARY, THRESH_OTSU, RETR_LIST, CHAIN_APPROX_SIMPLE, COLOR_GRAY2BGR, morphologyEx, MORPH_OPEN, split

# ---------------------------------------------------------------------------------------------------------------
def detectCharsInPlates(listOfPossiblePlates, PreprocessGaussKernel, PreprocessThreshBlockSize, PreprocessThreshweight,
                        PreprocessMorphKernel, MinPixelWidth, MaxPixelWidth, MinPixelHeight, MaxPixelHeight,
                        MinAspectRatio, MaxAspectRatio, MinPixelArea, MaxPixelArea, MinDiagSizeMultipleAway, MaxDiagSizeMultipleAway,
                        MinNumberOfMatchingChars, MaxNumberOfMatchingChars, MinAngleBetweenChars, MaxAngleBetweenChars,
                        MinChangeInArea, MaxChangeInArea, MinChangeInWidth, MaxChangeInWidth, MinChangeInHeight,
                        MaxChangeInHeight, ResizedCharImageWidth, ResizedCharImageHeight, kNearest, kFactorKNN,
                        NoVerticalAlign, NoOcrTextualFixes, NoOcrKnnFixes, NoOcrDigitsOnly, blueMaxThrH, blueMinThrS, OpMode, DebugMode):
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
                                                                PreprocessMorphKernel,
                                                                OpMode, "charsDet")

        # Increase size of plate image for easier viewing and char detection
        possiblePlate.imgThresh = resize(imgThreshScene, (0, 0), fx=1.6, fy=1.6)

        # Threshold again to eliminate any gray areas:
        _, possiblePlate.imgThresh = threshold(possiblePlate.imgThresh, 0.0, 255.0, THRESH_BINARY | THRESH_OTSU)

        # Perform Opening again to eliminate characters that touch border:
        kernel = ones((3, 3), uint8)
        possiblePlate.imgThresh = morphologyEx(possiblePlate.imgThresh, MORPH_OPEN, kernel)

        # Find all possible chars in the plate (finds all contours that could be chars):
        listOfPossibleCharsInPlate = findPossibleCharsInImage(possiblePlate.imgThresh,
                                                              MinPixelWidth, MaxPixelWidth,
                                                              MinPixelHeight, MaxPixelHeight,
                                                              MinAspectRatio, MaxAspectRatio,
                                                              MinPixelArea, MaxPixelArea,
                                                              DebugMode)

        # Remove possibleChars that are "too blue" (filters garbage from the Israeli symbol):
        if OpMode != "police":
            RemoveTooBlueChars(listOfPossibleCharsInPlate, possiblePlate.imgPlate, blueMaxThrH, blueMinThrS, DebugMode)

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

            # Characters Vertical alignment:
            vertical_align_check_pass = True
            if NoVerticalAlign:
                vertical_align_check_pass = charactersVerticalAlignCheck(longestListOfMatchingCharsInPlate, 
                                                                         3.5,
                                                                         MaxChangeInHeight,
                                                                         DebugMode)
            else:
                charactersVerticalAlign(longestListOfMatchingCharsInPlate, 0.05, 0.1, DebugMode)

            # Characters recognition (OCR):
            if vertical_align_check_pass:
                possiblePlate.strChars = recognizeCharsInPlate(possiblePlate,
                                                               longestListOfMatchingCharsInPlate,
                                                               ResizedCharImageWidth,
                                                               ResizedCharImageHeight,
                                                               kNearest,
                                                               kFactorKNN,
                                                               NoOcrKnnFixes,
                                                               intPlateCounter,
                                                               DebugMode)

                if not NoOcrTextualFixes:
                    possiblePlate.strChars = OcrTextualCorrections(possiblePlate.strChars,
                                                                   OpMode,
                                                                   NoOcrDigitsOnly,
                                                                   DebugMode)

                if not NoOcrDigitsOnly and not possiblePlate.strChars.isdigit() and not OpMode=="police":
                    debug("Deleting invalid OCR result (%s), since it not digits only" % possiblePlate.strChars, DebugMode)
                    possiblePlate.strChars = ""

        # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
        if DebugMode:

            height, width, _ = possiblePlate.imgPlate.shape
            contours1 = []; imgContours1 = zeros((2*height, 2*width, 3), uint8)
            contours2 = []; imgContours2 = zeros((2*height, 2*width, 3), uint8)
            contours3 = []; imgContours3 = zeros((2*height, 2*width, 3), uint8)
            contours4 = []; imgContours4 = zeros((2*height, 2*width, 3), uint8)

            debug("#listOfPossibleCharsInPlate = %d" % len(listOfPossibleCharsInPlate), True)
            for possibleChar in listOfPossibleCharsInPlate:
                contours1.append(possibleChar.contour)
            drawContours(imgContours1, contours1, -1, Colors.white)

            debug("#listOfListsOfMatchingCharsInPlate = %d" % len(listOfListsOfMatchingCharsInPlate), True)
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
def findPossibleCharsInImage(imgBinary, MinPixelWidth, MaxPixelWidth, MinPixelHeight, MaxPixelHeight,
                             MinAspectRatio, MaxAspectRatio, MinPixelArea, MaxPixelArea, debugMode=False):
    """ Find all possible chars in the plate (finds all contours that could be chars) """

    # Initialization:
    listOfPossibleChars = []
    imgBinaryCopy = imgBinary.copy()

    # Find all contours in the image:
    _, contours, _ = findContours(imgBinaryCopy, RETR_LIST, CHAIN_APPROX_SIMPLE)

    # Foreach contour, check if it describes a possible character:
    height, width = imgBinaryCopy.shape
    imgContours = zeros((height, width, 3), uint8)
    intCountOfPossibleChars = 0
    for i in range(0, len(contours)):

        # Register the contour as a possible character (+calculate intrinsic metrics):
        possibleChar = PossibleChar(contours[i],
                                    MinPixelWidth, MaxPixelWidth,
                                    MinPixelHeight, MaxPixelHeight,
                                    MinAspectRatio, MaxAspectRatio,
                                    MinPixelArea, MaxPixelArea)

        # If contour is a possible char, increment count of possible chars and add to list of possible chars:
        if possibleChar.checkIfPossibleChar():
            intCountOfPossibleChars += 1
            listOfPossibleChars.append(possibleChar)

        if debugMode:
            drawContours(imgContours, contours, i, Colors.white)

    if debugMode:
        debug("Amount of detected contours: %d" % len(contours), True)
        debug("Amount of possible characters: %d" % intCountOfPossibleChars, True)
        imwrite("img_contours_all.jpg", imgContours)

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
def recognizeCharsInPlate(possiblePlate, listOfMatchingChars, ResizedCharImageWidth, ResizedCharImageHeight,
                          kNearest, kFactorKNN, NoOcrKnnFixes, intPlateCounter, debugMode):
    """ This is where we apply the actual char recognition """

    # Initialization:
    strChars = ""
    imgThresh = possiblePlate.imgThresh
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
        _, npaResults, _, _ = kNearest.findNearest(npaROIResized, k=kFactorKNN)
        npaResultAscii = chr(int(npaResults[0][0]))

        # KNN corrections:
        if not NoOcrKnnFixes:
            npaResultAscii = OcrKnnCorrections(npaResultAscii, imgROIResized, currentChar.fltAspectRatio, debugMode)

        # Get character from results, and append it to the full string:
        strCurrentChar = str(npaResultAscii)
        strChars = strChars + strCurrentChar

    if debugMode:
        imwrite("img_ocr_result_%d.jpg" % intPlateCounter, imgThreshColor)

    return strChars

# ---------------------------------------------------------------------------------------------------------------
def OcrTextualCorrections(strChars, mode, NoOcrDigitsOnly, debugMode):
    """ OCR textual corrections """

    strCharsFinal = strChars

    if mode == "police":
        strCharsPre = strCharsFinal
        strCharsFinal = strChars[:-1] + "@"
        debug("Textual OCR change (police): %s --> %s" % (strCharsPre, strCharsFinal), debugMode)

    if not NoOcrDigitsOnly:
        if 'A' in strCharsFinal:
            strCharsPre = strCharsFinal
            strCharsFinal = strCharsFinal.replace("A","4")
            debug("Textual OCR change: %s --> %s" % (strCharsPre, strCharsFinal), debugMode)

        if 'B' in strCharsFinal:
            strCharsPre = strCharsFinal
            strCharsFinal = strCharsFinal.replace("B","8")
            debug("Textual OCR change: %s --> %s" % (strCharsPre, strCharsFinal), debugMode)

        if 'Z' in strCharsFinal:
            strCharsPre = strCharsFinal
            strCharsFinal = strCharsFinal.replace("Z","4")
            debug("Textual OCR change: %s --> %s" % (strCharsPre, strCharsFinal), debugMode)

        if 'I' in strCharsFinal:
            strCharsPre = strCharsFinal
            strCharsFinal = strCharsFinal.replace("I","1")
            debug("Textual OCR change: %s --> %s" % (strCharsPre, strCharsFinal), debugMode)

        if 'J' in strCharsFinal:
            strCharsPre = strCharsFinal
            strCharsFinal = strCharsFinal.replace("J", "3")
            debug("Textual OCR change: %s --> %s" % (strCharsPre, strCharsFinal), debugMode)

    return strCharsFinal

# ---------------------------------------------------------------------------------------------------------------
def OcrKnnCorrections(npaResultAscii, npaROIResized, charAspectRatio, debugMode):
    """ OCR KNN corrections """

    npaResultAsciiFinal = npaResultAscii

    imgH, imgW = npaROIResized.shape

    #if debugMode:
    #    print_character(npaROIResized)
    #    print str(npaResultAscii)
    #    print charAspectRatio

    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    # '2' --> '7'/'1':
    if str(npaResultAscii) == "2":

        bottom_right_sum = sample_image(npaROIResized, [int(0.87 * imgH), imgW-4, 2, 4], 255)

        if charAspectRatio < 0.4 and bottom_right_sum < 0.8:
            npaResultAsciiFinal = 1
            debug("KNN OCR fix (%.2f,%.2f): 2 --> 1" % (bottom_right_sum, charAspectRatio), debugMode)

        if bottom_right_sum < 0.4:
            npaResultAsciiFinal = 7
            debug("KNN OCR fix (%.2f,%.2f): 2 --> 7" % (bottom_right_sum, charAspectRatio), debugMode)

    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    # '3' --> '6'/'1':
    if str(npaResultAscii) == "3":

        mid_left_sum = sample_image(npaROIResized, [int(0.47 * imgH), 0, 4, 2], 255)

        if mid_left_sum > 0.4:
            npaResultAsciiFinal = 6
            debug("KNN OCR fix (%.2f): 3 --> 6" % mid_left_sum, debugMode)
        
        if charAspectRatio < 0.4:
            npaResultAsciiFinal = 1
            debug("KNN OCR fix (%.2f,%.2f): 3 --> 1" % (mid_left_sum, charAspectRatio), debugMode)

    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    # '5'-->'6':
    elif str(npaResultAscii) == "5":

        top_left_sum = sample_image(npaROIResized, [1, 0, 4, 2], 255)

        mid_left_sum = sample_image(npaROIResized, [int(0.65 * imgH), 0, 4, 2], 255)

        if top_left_sum < 0.5 and mid_left_sum > 0.1:
            npaResultAsciiFinal = 6
            debug("KNN OCR fix (%.2f,%.2f): 5 --> 6" % (top_left_sum, mid_left_sum), debugMode)

    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    # '6'-->'8'/'5'/'4':
    elif str(npaResultAscii) == "6":

        top_right_sum = sample_image(npaROIResized, [int(0.35 * imgH), imgW-6, 4, 2], 255)
        
        mid_left_sum = sample_image(npaROIResized, [int(0.65 * imgH), 0, 4, 2], 255)

        bottom_left_sum = sample_image(npaROIResized, [imgH-4, 5, 2, 4], 255)

        if top_right_sum > 0.5:
            npaResultAsciiFinal = 8
            debug("KNN OCR fix (%.2f,%.2f,%.2f): 6 --> 8" % (top_right_sum, mid_left_sum, bottom_left_sum), debugMode)
        
        if mid_left_sum < 0.1:
            npaResultAsciiFinal = 5
            debug("KNN OCR fix (%.2f,%.2f,%.2f): 6 --> 5" % (top_right_sum, mid_left_sum, bottom_left_sum), debugMode)

        elif bottom_left_sum < 0.1:
                npaResultAsciiFinal = 4
                debug("KNN OCR fix (%.2f,%.2f,%.2f): 6 --> 4" % (top_right_sum, mid_left_sum, bottom_left_sum), debugMode)

    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    # '7' --> '1':
    elif str(npaResultAscii) == "7":

        bottom_left_sum = sample_image(npaROIResized, [int(0.85 * imgH), 0, 6, 2], 255)

        if bottom_left_sum < 0.25 and charAspectRatio < 0.45:
            npaResultAsciiFinal = 1
            debug("KNN OCR fix (%.2f,%.2f): 7 --> 1" % (bottom_left_sum, charAspectRatio), debugMode)

    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    # '8' --> '9'/'6'/'0':
    elif str(npaResultAscii) == "8":

        bottom_left_sum = sample_image(npaROIResized, [int(0.6 * imgH), 0, 4, 2], 255)

        top_right_sum = sample_image(npaROIResized, [int(0.35 * imgH), imgW-6, 4, 2], 255)

        mid_sum = sample_image(npaROIResized, [int(0.45 * imgH), int(0.5 * imgW), 4, 2], 255)

        if bottom_left_sum < 0.2:
            npaResultAsciiFinal = 9
            debug("KNN OCR fix (%.2f): 8 --> 9" % bottom_left_sum, debugMode)

        elif top_right_sum < 0.2:
            npaResultAsciiFinal = 6
            debug("KNN OCR fix (%.2f): 8 --> 6" % top_right_sum, debugMode)

        elif mid_sum < 0.2:
            npaResultAsciiFinal = 0
            debug("KNN OCR fix (%.2f): 8 --> 0" % mid_sum, debugMode)

    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    # 'B' --> '0'/'5'/'6':
    elif str(npaResultAscii) == "B":

        mid_sum = sample_image(npaROIResized, [int(0.5 * imgH), int(0.5 * imgW), 4, 2], 255)
        
        bottom_left_sum = sample_image(npaROIResized, [int(0.6 * imgH), 0, 4, 2], 255)
        
        top_right_sum = sample_image(npaROIResized, [int(0.35 * imgH), imgW-6, 4, 2], 255)

        if top_right_sum < 0.2:
          
            if bottom_left_sum < 0.2:
                npaResultAsciiFinal = '5'
                debug("KNN OCR fix (%.2f): B --> 5" % bottom_left_sum, top_right_sum, debugMode)
        
            else:
                npaResultAsciiFinal = 6
                debug("KNN OCR fix (%.2f): B --> 6" % top_right_sum, debugMode)
        
        elif mid_sum < 0.2:
            npaResultAsciiFinal = 0
            debug("KNN OCR fix (%.2f): B --> 0" % mid_sum, debugMode)
        
    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    # 'J' --> '5':
    if str(npaResultAscii) == "J":

        top_left_sum = sample_image(npaROIResized, [int(0.2 * imgH), 1, 2, 4], 255)

        if top_left_sum > 0.7:
            npaResultAsciiFinal = 5
            debug("KNN OCR fix (%.2f): J --> 5" % top_left_sum, debugMode)
    
    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    # 'Z' --> '2':
    if str(npaResultAscii) == "Z":

        top_left_sum = sample_image(npaROIResized, [1, 1, 2, 4], 255)

        if top_left_sum > 0.4:
            npaResultAsciiFinal = 2
            debug("KNN OCR fix (%.2f): Z --> 2" % top_left_sum, debugMode)

    return npaResultAsciiFinal

# ---------------------------------------------------------------------------------------------------------------
def charactersVerticalAlignCheck(listOfMatchingChars, errY_thr, errH_thr, DebugMode):
    """ Characters Vertical alignment check, i.e. check characters alignment along y-axis """

    res = True
    intBoundingRectY_list = []
    intBoundingRectHeight_list = []
    for matchingChar in listOfMatchingChars:
        intBoundingRectY_list.append(matchingChar.intBoundingRectY)
        intBoundingRectHeight_list.append(matchingChar.intBoundingRectHeight)

    medianY = median(intBoundingRectY_list)
    medianH = median(intBoundingRectHeight_list)

    errY = 0
    errH = 0
    for matchingChar in listOfMatchingChars:
        errY += (abs(matchingChar.intBoundingRectY - medianY) / medianY)
        errH += (abs(matchingChar.intBoundingRectHeight - medianH) / medianH)

    if (errY > errY_thr and errH > errH_thr):
        res = False;
        info("charactersVerticalAlignCheck failed!")

    debug("(errY, errH) = (%.2f,%.2f)" % (errY, errH), DebugMode)

    return res

# ---------------------------------------------------------------------------------------------------------------
def charactersVerticalAlign(listOfMatchingChars, errY_thr, errH_thr, DebugMode):
    """ Characters Vertical alignment, i.e. fix outlier characters along y-axis """

    intBoundingRectY_list = []
    intBoundingRectHeight_list = []
    for matchingChar in listOfMatchingChars:
        intBoundingRectY_list.append(matchingChar.intBoundingRectY)
        intBoundingRectHeight_list.append(matchingChar.intBoundingRectHeight)

    medianY = median(intBoundingRectY_list)
    medianH = median(intBoundingRectHeight_list)

    for matchingChar in listOfMatchingChars:
        errY = abs(matchingChar.intBoundingRectY - medianY) / medianY
        errH = abs(matchingChar.intBoundingRectHeight - medianH) / medianH

        if (errY > errY_thr and errH > errH_thr):
            debug("Vertical fix --> (y,w): (%d,%d)-->(%d,%d)" % \
                  (matchingChar.intBoundingRectY, matchingChar.intBoundingRectHeight, int(medianY), int(medianH)), DebugMode)

            matchingChar.intBoundingRectY = int(medianY)
            matchingChar.intBoundingRectHeight = int(medianH)

            matchingChar.boundingRect = [matchingChar.intBoundingRectX,
                                         matchingChar.intBoundingRectY,
                                         matchingChar.intBoundingRectWidth,
                                         matchingChar.intBoundingRectHeight]

            matchingChar.intBoundingRectArea = matchingChar.intBoundingRectWidth * matchingChar.intBoundingRectHeight

            matchingChar.intCenterY = (matchingChar.intBoundingRectY + matchingChar.intBoundingRectY + matchingChar.intBoundingRectHeight) / 2

            matchingChar.fltDiagonalSize = sqrt((matchingChar.intBoundingRectWidth ** 2) + (matchingChar.intBoundingRectHeight ** 2))

            matchingChar.fltAspectRatio = float(matchingChar.intBoundingRectWidth) / float(matchingChar.intBoundingRectHeight)

# ---------------------------------------------------------------------------------------------------------------
def RemoveTooBlueChars(listOfPossibleCharsInPlate, imgPlate, blueMaxThrH, blueMinThrS, debugMode):
    """ Remove possibleChars that are "too blue" (probably part of the Israeli symbol) """
    
    imgHSV = cvtColor(imgPlate, COLOR_BGR2HSV)
    imgHSV = resize(imgHSV, (0, 0), fx=1.6, fy=1.6)
    H, S, _ = split(imgHSV)
    for possibleChar in listOfPossibleCharsInPlate:
        height, width = H.shape
        mask = zeros((height, width), uint8)
        contours = []; 
        contours.append(possibleChar.contour)
        drawContours(mask, contours, -1, Colors.white, -1)
        tempValH = mean(H, mask)
        tempValS = mean(S, mask)
        myMAtMeanH = tempValH[0] 
        myMAtMeanS = tempValS[0]
        if ((myMAtMeanH > blueMaxThrH) and (myMAtMeanS < blueMinThrS)):
            debug("Possible char removed (too blue) --> (x,y,h,s)=(%d,%d,%.2f,%.2f)" % (possibleChar.intCenterX, possibleChar.intCenterY, myMAtMeanH, myMAtMeanS), debugMode)
            listOfPossibleCharsInPlate.remove(possibleChar)

# ---------------------------------------------------------------------------------------------------------------
def print_character(imgGray):
    """ Debug print image (useful for character OCR debug) """

    imgH, imgW = imgGray.shape

    for k1 in range(imgH):
        for k2 in range(imgW):
            print "%3d" % imgGray[k1][k2],
        print("")

    print "--------------------------------------------------------------------------"

