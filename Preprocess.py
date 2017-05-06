# !/usr/bin/python
#  _     _                           ____  _       _         ____                            _ _   _
# | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
# | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
# | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
# |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
#                                                                                |___/
# (c) Shahar Gino, May-2017, sgino209@gmail.com

from cv2 import split, GaussianBlur, adaptiveThreshold, getStructuringElement, morphologyEx, add, subtract, cvtColor, \
    COLOR_BGR2HSV, ADAPTIVE_THRESH_GAUSSIAN_C, THRESH_BINARY_INV, MORPH_RECT, MORPH_TOPHAT, MORPH_BLACKHAT

# ---------------------------------------------------------------------------------------------------------------
def preprocess(imgOriginal, PreprocessGaussKernel, PreprocessThreshBlockSize, PreprocessThreshweight, PreprocessMorphKernel):

    # Color-Space-Conversion (CSC): switch from BGR to HSV and take "V" component:
    imgHSV = cvtColor(imgOriginal, COLOR_BGR2HSV)
    _, _, imgGrayscale = split(imgHSV)

    # Increase contrast (morphological):
    imgMaxContrastGrayscale = maximizeContrast(imgGrayscale, PreprocessMorphKernel)

    # Blurring:
    imgBlurred = GaussianBlur(imgMaxContrastGrayscale, PreprocessGaussKernel, 0)

    # Adaptive Threshold:
    imgThresh = adaptiveThreshold(imgBlurred, 255.0, ADAPTIVE_THRESH_GAUSSIAN_C, THRESH_BINARY_INV, PreprocessThreshBlockSize, PreprocessThreshweight)

    return imgGrayscale, imgThresh

# ---------------------------------------------------------------------------------------------------------------
def maximizeContrast(imgGrayscale, PreprocessMorphKernel):
    """ Morphological filtering for increasing contrast: OutputImage = InputImage + TopHat - BlackHat """

    structuringElement = getStructuringElement(MORPH_RECT, PreprocessMorphKernel)

    imgTopHat = morphologyEx(imgGrayscale, MORPH_TOPHAT, structuringElement)
    imgBlackHat = morphologyEx(imgGrayscale, MORPH_BLACKHAT, structuringElement)

    imgGrayscalePlusTopHat = add(imgGrayscale, imgTopHat)
    imgGrayscalePlusTopHatMinusBlackHat = subtract(imgGrayscalePlusTopHat, imgBlackHat)

    return imgGrayscalePlusTopHatMinusBlackHat
