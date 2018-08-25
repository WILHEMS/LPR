#!/usr/bin/python
#  _     _                           ____  _       _         ____                            _ _   _
# | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
# | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
# | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
# |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
#                                                                                |___/
# (c) Shahar Gino, July-2017, sgino209@gmail.com

from math import asin, pi
from random import randint
from Preprocess import preprocess
from PossiblePlate import PossiblePlate
from Auxiliary import info, debug, Colors
from numpy import zeros, uint8
from DetectChars import findListOfListsOfMatchingChars, findPossibleCharsInImage
from cv2 import line, boxPoints, warpAffine, drawContours, findContours, getRectSubPix, convexHull, arcLength, split, \
    getRotationMatrix2D, imwrite, RETR_LIST, CHAIN_APPROX_NONE, contourArea, boundingRect, cvtColor, calcHist, COLOR_BGR2HSV

# ---------------------------------------------------------------------------------------------------------------
def detectPlatesInScene(imgOriginalScene,
                        PreprocessGaussKernel, PreprocessThreshBlockSize, PreprocessThreshweight, PreprocessMorphKernel,
                        PlateWidthPaddingFactor, PlateHeightPaddingFactor, FindRectangledPlate,
                        MinPixelWidth, MaxPixelWidth, MinPixelHeight, MaxPixelHeight, MinAspectRatio, MaxAspectRatio, MinPixelArea, MaxPixelArea,
                        MaxDiagSizeMultipleAway, MinNumberOfMatchingChars, MaxNumberOfMatchingChars, MinAngleBetweenChars, MaxAngleBetweenChars,
                        MinChangeInArea, MaxChangeInArea, MinChangeInWidth, MaxChangeInWidth, MinChangeInHeight, MaxChangeInHeight, MinHistNormThr, OpMode, debugMode):
    """ License Plate Detection in a given input image scene, using geometrical analysis techniques """

    # Pre-processing (CSC --> contrast --> blur --> threshold):
    imgGrayscaleScene, imgThreshScene = preprocess(imgOriginalScene,
                                                   PreprocessGaussKernel,
                                                   PreprocessThreshBlockSize,
                                                   PreprocessThreshweight,
                                                   PreprocessMorphKernel,
                                                   OpMode, "platesDet")

    # Find all possible characters in the scene (finds all contours that could be characters, w/o OCR yet):
    listOfPossibleCharsInScene = findPossibleCharsInImage(imgThreshScene,
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

        possiblePlate = extractPlate(imgOriginalScene,
                                     listOfMatchingChars,
                                     PlateWidthPaddingFactor,
                                     PlateHeightPaddingFactor)

        # Add plate to list of possible plates (if found):
        if possiblePlate.imgPlate is not None:
            
            imgHSV = cvtColor(possiblePlate.imgPlate, COLOR_BGR2HSV)
            _, imgS, _ = split(imgHSV)
            N = imgS.size
            histSize = 256
            s_hist = calcHist([imgS], [0], None, [histSize], [0,256])
            hist_norm = 0
            for h in range(histSize):
              hist_norm += h * s_hist[h][0]/N

            # Verify that the plate has enough saturation:
            if hist_norm > MinHistNormThr:
                listOfPossiblePlates.append(possiblePlate)
            else:
                debug("Plates rejected: HistNorm=%.2f" % hist_norm, debugMode)

    # Add rectangle plate candidate:
    if (FindRectangledPlate):

        possiblePlate = findRectangledPlate(imgOriginalScene,
                                            imgThreshScene,
                                            0.45,   # circularity_min
                                            0.65,   # circularity_max
                                            3.5,    # aspect_ratio_min
                                            4.4,    # aspect_ratio_max
                                            0.005,  # area_norm_min
                                            0.03,   # area_norm_max
                                            debugMode)

        if (possiblePlate.imgPlate is not None):
            possiblePlate.rectFind = True
            listOfPossiblePlates.append(possiblePlate)

    debug("%d possible plates found" % len(listOfPossiblePlates), debugMode)

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
        debug("#listOfListsOfMatchingCharsInScene = %d" % len(listOfListsOfMatchingCharsInScene), True)
        imgContours = zeros((height, width, 3), uint8)
        for listOfMatchingChars in listOfListsOfMatchingCharsInScene:
            intRandomBlue = randint(0, 255)
            intRandomGreen = randint(0, 255)
            intRandomRed = randint(0, 255)
            contours = []
            debug("#listOfMatchingChars = %d" % len(listOfMatchingChars), True)
            for matchingChar in listOfMatchingChars:
                contours.append(matchingChar.contour)
            drawContours(imgContours, contours, -1, (intRandomBlue, intRandomGreen, intRandomRed))
            imwrite("img_contours_matching_chars.jpg", imgContours)

        # Possible license-plates:
        for i in range(0, len(listOfPossiblePlates)):
            p2fRectPoints = boxPoints(listOfPossiblePlates[i].rrLocationOfPlateInScene)
            color = Colors.red
            if listOfPossiblePlates[i].rectFind:
                color = Colors.green
            line(imgContours, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), color, 2)
            line(imgContours, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), color, 2)
            line(imgContours, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), color, 2)
            line(imgContours, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), color, 2)
            imwrite("img_contours_possible_plates_%d.jpg" % i, imgContours)
            imwrite("img_plate_%d.jpg" % i, listOfPossiblePlates[i].imgPlate)

        debug("Plate detection complete", True)

    return listOfPossiblePlates

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

# ---------------------------------------------------------------------------------------------------------------
def findRectangledPlate(imgOriginal, imgThresh, circularity_min, circularity_max, aspect_ratio_min,
                        aspect_ratio_max, area_norm_min, area_norm_max, debugMode):
    """ Find rectangles """

    # Initialization:
    rect_cntr = 0
    max_rect_area = 0
    res_area_norm = 0
    res_circularity = 0
    res_aspect_ratio = 0
    fltPlateCenterX = 0
    fltPlateCenterY = 0
    possiblePlate = PossiblePlate()

    # Find all contours in plate:
    imgThreshCopy = imgThresh.copy()
    _, contours, _ = findContours(imgThreshCopy, RETR_LIST, CHAIN_APPROX_NONE)

    # For each contour, check if it might be representing a rectangled plate:
    for contour in contours:

        # Compute convex hull:
        hull = convexHull(contour)

        # Compute circularity, used for shape classification:
        area = contourArea(hull)
        area_norm = contourArea(hull) / imgThresh.size
        perimeter = arcLength(hull, True)
        circularity = 0
        if perimeter > 0:
            circularity = (4 * pi * area) / (perimeter * perimeter)

        # Shape classification (rectangle):
        if ((circularity > circularity_min) and (circularity < circularity_max) and (area > max_rect_area)):

            box_x, box_y, box_width, box_height = boundingRect(contour)
            aspect_ratio = box_width / box_height

            if ((aspect_ratio > aspect_ratio_min) and (aspect_ratio < aspect_ratio_max) and
                (area_norm > area_norm_min) and (area_norm < area_norm_max)):

                # Registration:
                res_box = [box_x, box_y, box_width, box_height]
                max_rect_area = area
                res_area_norm = area_norm
                res_aspect_ratio = aspect_ratio
                res_circularity = circularity

                for i in range(0, len(contour)):

                    fltPlateCenterX += contour[i][0][0]
                    fltPlateCenterY += contour[i][0][1]

                fltPlateCenterX /= len(contour)
                fltPlateCenterY /= len(contour)

                rect_cntr += 1

    # Return result:
    if rect_cntr > 0:

        ptPlateCenter = fltPlateCenterX, fltPlateCenterY

        # Crop the plate from the image:
        possiblePlate.rrLocationOfPlateInScene = (tuple(ptPlateCenter), (res_box[2], res_box[3]), 0)
        imgCropped = getRectSubPix(imgOriginal, possiblePlate.rrLocationOfPlateInScene[1], possiblePlate.rrLocationOfPlateInScene[0])
        possiblePlate.imgPlate = imgCropped

        debug("rect #%d: box.w=%d, box.h=%d, AR=%.4f, area=%.4f, circ=%.4f" %
              (rect_cntr-1, res_box[2], res_box[3], res_aspect_ratio, res_area_norm, res_circularity), debugMode)

    return possiblePlate
