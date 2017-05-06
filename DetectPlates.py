# !/usr/bin/python
#  _     _                           ____  _       _         ____                            _ _   _
# | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
# | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
# | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
# |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
#                                                                                |___/
# (c) Shahar Gino, May-2017, sgino209@gmail.com

from math import asin, pi
from random import randint
from numpy import zeros, uint8
from Preprocess import preprocess
from PossibleChar import PossibleChar
from PossiblePlate import PossiblePlate
from Auxiliary import info, debug, Colors
from DetectChars import findListOfListsOfMatchingChars
from cv2 import line, boxPoints, warpAffine, drawContours, findContours, getRectSubPix, \
    getRotationMatrix2D, imwrite, RETR_LIST, CHAIN_APPROX_SIMPLE

# ---------------------------------------------------------------------------------------------------------------
def detectPlatesInScene(imgOriginalScene,
                        PreprocessGaussKernel, PreprocessThreshBlockSize, PreprocessThreshweight, PreprocessMorphKernel,
                        PlateWidthPaddingFactor, PlateHeightPaddingFactor,
                        MinPixelWidth, MaxPixelWidth, MinPixelHeight, MaxPixelHeight, MinAspectRatio, MaxAspectRatio, MinPixelArea, MaxPixelArea,
                        MaxDiagSizeMultipleAway, MinNumberOfMatchingChars, MaxNumberOfMatchingChars, MinAngleBetweenChars, MaxAngleBetweenChars,
                        MinChangeInArea, MaxChangeInArea, MinChangeInWidth, MaxChangeInWidth, MinChangeInHeight, MaxChangeInHeight, debugMode):
    """ License Plate Detection in a given input image scene, using geometrical analysis techniques """

    # Pre-processing (CSC --> contrast --> blur --> threshold):
    imgGrayscaleScene, imgThreshScene = preprocess(imgOriginalScene,
                                                   PreprocessGaussKernel,
                                                   PreprocessThreshBlockSize,
                                                   PreprocessThreshweight,
                                                   PreprocessMorphKernel)

    # Find all possible characters in the scene (finds all contours that could be characters, w/o OCR yet):
    listOfPossibleCharsInScene = findPossibleCharsInScene(imgThreshScene,
                                                          MinPixelWidth, MaxPixelWidth,
                                                          MinPixelHeight, MaxPixelHeight,
                                                          MinAspectRatio, MaxAspectRatio,
                                                          MinPixelArea, MaxPixelArea,
                                                          debugMode)

    # Given a list of all possible chars, find groups of matching characters (later on, each group will attempt to be recognized as a plate):
    listOfListsOfMatchingCharsInScene = findListOfListsOfMatchingChars(listOfPossibleCharsInScene,
                                                                       MinNumberOfMatchingChars,
                                                                       MaxNumberOfMatchingChars,
                                                                       MinAngleBetweenChars, MaxAngleBetweenChars,
                                                                       MinChangeInArea, MaxChangeInArea,
                                                                       MinChangeInWidth, MaxChangeInWidth,
                                                                       MinChangeInHeight, MaxChangeInHeight,
                                                                       MaxDiagSizeMultipleAway)

    # For each group of matching chars, attempt to extract plate:
    listOfPossiblePlates = []
    for listOfMatchingChars in listOfListsOfMatchingCharsInScene:

        possiblePlate = extractPlate(imgOriginalScene, listOfMatchingChars,  PlateWidthPaddingFactor, PlateHeightPaddingFactor)

        # Add plate to list of possible plates (if found):
        if possiblePlate.imgPlate is not None:
            listOfPossiblePlates.append(possiblePlate)

    info("%d possible plates found" % len(listOfPossiblePlates))

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
    if debugMode:

        height, width, _ = imgOriginalScene.shape

        # Original image:
        imwrite("img_original.jpg", imgOriginalScene)

        # Pre-processing images:
        imwrite("img_gray.jpg", imgGrayscaleScene)
        imwrite("img_threshold.jpg", imgThreshScene)

        # Possible characters in image:
        imgContours = zeros((height, width, 3), uint8)
        contours = []
        for possibleChar in listOfPossibleCharsInScene:
            contours.append(possibleChar.contour)
        drawContours(imgContours, contours, -1, Colors.white)
        imwrite("img_contours_possible_chars.jpg", imgContours)

        # Matching characters:
        imgContours = zeros((height, width, 3), uint8)
        for listOfMatchingChars in listOfListsOfMatchingCharsInScene:
            intRandomBlue = randint(0, 255)
            intRandomGreen = randint(0, 255)
            intRandomRed = randint(0, 255)
            contours = []
            for matchingChar in listOfMatchingChars:
                contours.append(matchingChar.contour)
            drawContours(imgContours, contours, -1, (intRandomBlue, intRandomGreen, intRandomRed))
            imwrite("img_contours_matching_chars.jpg", imgContours)

        # Possible license-plates:
        for i in range(0, len(listOfPossiblePlates)):
            p2fRectPoints = boxPoints(listOfPossiblePlates[i].rrLocationOfPlateInScene)
            line(imgContours, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), Colors.red, 2)
            line(imgContours, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), Colors.red, 2)
            line(imgContours, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), Colors.red, 2)
            line(imgContours, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), Colors.red, 2)
            imwrite("img_contours_possible_plates_%d.jpg" % i, imgContours)
            imwrite("img_plate_%d.jpg" % i, listOfPossiblePlates[i].imgPlate)

        debug("Plate detection complete", True)

    return listOfPossiblePlates

# ---------------------------------------------------------------------------------------------------------------
def findPossibleCharsInScene(binaryImage, MinPixelWidth, MaxPixelWidth, MinPixelHeight, MaxPixelHeight,
                             MinAspectRatio, MaxAspectRatio, MinPixelArea, MaxPixelArea, debugMode):
    """ Find all possible characters in the scene (finds all contours that could be characters, w/o OCR yet) """

    # Find all contours in the image:
    binaryImageCopy = binaryImage.copy()
    _, contours, _ = findContours(binaryImageCopy, RETR_LIST, CHAIN_APPROX_SIMPLE)

    # Foreach contour, check if it describes a possible character:
    height, width = binaryImage.shape
    imgContours = zeros((height, width, 3), uint8)
    intCountOfPossibleChars = 0
    listOfPossibleChars = []
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

    return listOfPossibleChars

# ---------------------------------------------------------------------------------------------------------------
def extractPlate(imgOriginal, listOfMatchingChars, PlateWidthPaddingFactor, PlateHeightPaddingFactor):
    """ Extract license-plate in the provided image, based on given contours group that corresponds for matching characters """

    # Sort characters from left to right based on x position:
    listOfMatchingChars.sort(key=lambda matchingChar_: matchingChar_.intCenterX)

    # Calculate the plate centroid (average of leftmost and righhtmost characters):
    fltPlateCenterX = (listOfMatchingChars[0].intCenterX + listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterX) / 2.0
    fltPlateCenterY = (listOfMatchingChars[0].intCenterY + listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterY) / 2.0
    ptPlateCenter = fltPlateCenterX, fltPlateCenterY

    # Calculate plate width (rightmost - leftmost characters):
    intPlateWidth = int(PlateWidthPaddingFactor * (listOfMatchingChars[len(listOfMatchingChars) - 1].intBoundingRectX +
                                                   listOfMatchingChars[len(listOfMatchingChars) - 1].intBoundingRectWidth -
                                                   listOfMatchingChars[0].intBoundingRectX))

    # Calculate plate height (average over all characters):
    intTotalOfCharHeights = 0
    for matchingChar in listOfMatchingChars:
        intTotalOfCharHeights = intTotalOfCharHeights + matchingChar.intBoundingRectHeight
    fltAverageCharHeight = intTotalOfCharHeights / len(listOfMatchingChars)
    intPlateHeight = int(fltAverageCharHeight * PlateHeightPaddingFactor)

    # Calculate correction angle of plate region (simple geometry calculation):
    fltOpposite = listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterY - listOfMatchingChars[0].intCenterY
    fltHypotenuse = (listOfMatchingChars[0] - listOfMatchingChars[len(listOfMatchingChars) - 1])
    fltCorrectionAngleInRad = asin(fltOpposite / fltHypotenuse)
    fltCorrectionAngleInDeg = fltCorrectionAngleInRad * (180.0 / pi)

    # Rotate the entire image (affine warp), for compensating the angle of the plate region:
    rotationMatrix = getRotationMatrix2D(tuple(ptPlateCenter), fltCorrectionAngleInDeg, 1.0)
    height, width, _ = imgOriginal.shape
    imgRotated = warpAffine(imgOriginal, rotationMatrix, (width, height))

    # Crop the plate from the image:
    imgCropped = getRectSubPix(imgRotated, (intPlateWidth, intPlateHeight), tuple(ptPlateCenter))

    # Create and return possiblePlate object, which packs most the above information:
    possiblePlate = PossiblePlate()
    possiblePlate.rrLocationOfPlateInScene = (tuple(ptPlateCenter), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg)
    possiblePlate.imgPlate = imgCropped

    return possiblePlate
