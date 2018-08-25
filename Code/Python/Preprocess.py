#!/usr/bin/python
#  _     _                           ____  _       _         ____                            _ _   _
# | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
# | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
# | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
# |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
#                                                                                |___/
# (c) Shahar Gino, July-2017, sgino209@gmail.com

from cv2 import split, merge, GaussianBlur, adaptiveThreshold, getStructuringElement, morphologyEx, add, subtract,\
    cvtColor, createCLAHE, LUT, COLOR_BGR2HSV, COLOR_HSV2BGR, ADAPTIVE_THRESH_GAUSSIAN_C, THRESH_BINARY_INV, \
    MORPH_RECT, MORPH_TOPHAT, MORPH_BLACKHAT
from scipy.interpolate import UnivariateSpline
from numpy import uint8, array, arange


# ---------------------------------------------------------------------------------------------------------------
def preprocess(imgOriginal, PreprocessGaussKernel, PreprocessThreshBlockSize, PreprocessThreshweight, PreprocessMorphKernel, OpMode, phase):
    """ Preprocessing for both Plates and Characters detection """

    # Color-Space-Conversion (CSC): switch from BGR to HSV and take "V" component:
    imgHSV = cvtColor(imgOriginal, COLOR_BGR2HSV)

    if OpMode == "police":
        _, imgGrayscale, _ = split(imgHSV)

    else:
        _, _, imgGrayscale = split(imgHSV)

    # Increase contrast (morphological):
    imgMaxContrastGrayscale = maximizeContrast(imgGrayscale, PreprocessMorphKernel)

    # Blurring:
    if phase == "platesDet":
        gaussKernel = (PreprocessGaussKernel[0]+2,PreprocessGaussKernel[1]+2)
    else:
        gaussKernel = PreprocessGaussKernel

    imgBlurred = GaussianBlur(imgMaxContrastGrayscale, gaussKernel, 0)

    # Adaptive Threshold:
    imgThresh = adaptiveThreshold(imgBlurred, 255.0, ADAPTIVE_THRESH_GAUSSIAN_C, THRESH_BINARY_INV, PreprocessThreshBlockSize, PreprocessThreshweight)

    return imgGrayscale, imgThresh

# ---------------------------------------------------------------------------------------------------------------
def maximizeContrast(imgGrayscale, PreprocessMorphKernel):
    """ Morphological filtering for increasing contrast: OutputImage = InputImage + TopHat - BlackHat """

    structuringElement = getStructuringElement(MORPH_RECT, PreprocessMorphKernel)

    imgTopHat = morphologyEx(imgGrayscale, MORPH_TOPHAT, structuringElement)      # = Image - Opening[Image] = Image - dilate[erode[Image]] --> "lowFreq"
    imgBlackHat = morphologyEx(imgGrayscale, MORPH_BLACKHAT, structuringElement)  # = Closing[Image] - Image = erode[dilate[Image]] - Image --> "highFreq"

    imgGrayscalePlusTopHat = add(imgGrayscale, imgTopHat)
    imgGrayscalePlusTopHatMinusBlackHat = subtract(imgGrayscalePlusTopHat, imgBlackHat)

    return imgGrayscalePlusTopHatMinusBlackHat

# ---------------------------------------------------------------------------------------------------------------
def imageEnhancement(imgOriginal, clahe_clipLimit, clahe_tileGridSize, gamma, debugMode=False):
    """ Image enhancement, applies Warming effect (+CLAHE) and Saturation effect (+Gamma) """

    # Refs: (1) http://www.askaswiss.com/2016/02/how-to-manipulate-color-temperature-opencv-python.html
    #       (2) http://www.pyimagesearch.com/2015/10/05/opencv-gamma-correction
    #       (3) http://docs.opencv.org/trunk/d3/dc1/tutorial_basic_linear_transform.html
    #       (4) http://docs.opencv.org/2.4/doc/tutorials/core/basic_linear_transform/basic_linear_transform.html

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
    def adjust_gamma(image, gamma=1.0):
        """ Build and apply a lookup table mapping the pixel values [0, 255] to their adjusted gamma values """

        invGamma = 1.0 / gamma
        table = array([((i / 255.0) ** invGamma) * 255 for i in arange(0, 256)]).astype("uint8")

        return LUT(image, table)

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
    def create_LUT_8UC1(x, y):
        """" Basic LUT generation, returns a 256-element list of the interpolated f(x) values for every value of x. """

        spl = UnivariateSpline(x, y)
        return spl(xrange(256))

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..

    incr_ch_lut = create_LUT_8UC1([0, 64, 128, 192, 256],
                                  [0, 70, 140, 210, 256])
    decr_ch_lut = create_LUT_8UC1([0, 64, 128, 192, 256],
                                  [0, 30, 80, 120, 192])

    # Warming effect (R,G incr.) + CLAHE:
    b, g, r = split(imgOriginal)
    c_r = LUT(r, incr_ch_lut).astype(uint8)
    c_b = LUT(b, decr_ch_lut).astype(uint8)
    clahe = createCLAHE(clipLimit=clahe_clipLimit, tileGridSize=clahe_tileGridSize)
    B = clahe.apply(c_b)
    G = clahe.apply(g)
    R = clahe.apply(c_r)
    imgWarm = merge((B, G, R))

    # Saturation effect (S incr.) + Gamma:
    h, s, v = split(cvtColor(imgWarm, COLOR_BGR2HSV))
    c_s = LUT(s, incr_ch_lut).astype(uint8)
    imgSat = cvtColor(merge((h, c_s, v)), COLOR_HSV2BGR)
    imgOut = adjust_gamma(imgSat, gamma=gamma)

    # Debug:
    if (debugMode):
        from matplotlib import pyplot as plt
        from cv2 import COLOR_BGR2RGB
        imgIn = cvtColor(imgOriginal, COLOR_BGR2RGB)
        imgOut = cvtColor(imgOut, COLOR_BGR2RGB)
        plt.subplot(211), plt.imshow(imgIn, 'gray'), plt.title('Original')
        plt.subplot(212), plt.imshow(imgOut, 'gray'), plt.title('Enhanced')
        plt.show()
        exit(0)

    return imgOut

