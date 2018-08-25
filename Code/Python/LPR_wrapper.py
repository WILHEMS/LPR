#!/usr/bin/python
#  _     _                           ____  _       _         ____                            _ _   _
# | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
# | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
# | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
# |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
#                                                                                |___/
# (c) Shahar Gino, July-2017, sgino209@gmail.com

from numpy import loadtxt, float32
from DetectChars import detectCharsInPlates
from DetectPlates import detectPlatesInScene
from cv2 import ml, imshow, imwrite, waitKey
from Auxiliary import info, debug, error, Colors, imshow_scaled, drawRedRectangleAroundPlate, \
    writeLicensePlateCharsOnImage, isTemplateFound

# ---------------------------------------------------------------------------------------------------------------
class LPR_wrapper:
    """ LPR top class: generates KNN classifier, Loads input image, detects plates, detects chars and reports """

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
    def __init__(self, PreprocessGaussKernel, PreprocessThreshBlockSize, PreprocessThreshweight, PreprocessMorphKernel,
                 PlateWidthPaddingFactor, PlateHeightPaddingFactor, FindRectangledPlate,
                 MinPixelWidth, MaxPixelWidth, MinPixelHeight, MaxPixelHeight, MinAspectRatio, MaxAspectRatio, MinPixelArea, MaxPixelArea,
                 MinDiagSizeMultipleAway, MaxDiagSizeMultipleAway, MinChangeInArea, MaxChangeInArea,
                 MinChangeInWidth, MaxChangeInWidth, MinChangeInHeight, MaxChangeInHeight, MinHistNormThr,
                 MinAngleBetweenChars, MaxAngleBetweenChars, MinNumberOfMatchingChars, MaxNumberOfMatchingChars,
                 ResizedCharImageWidth, ResizedCharImageHeight, NoVerticalAlign, kClassfications, kFlattenedImages, kFactorKNN,
                 NoOcrTextualFixes, NoOcrKnnFixes, NoOcrDigitsOnly, batchMode, blueMaxThrH, blueMinThrS, OpMode, debugMode):
        """ Constructor """

        self.PreprocessGaussKernel = PreprocessGaussKernel
        self.PreprocessThreshBlockSize = PreprocessThreshBlockSize
        self.PreprocessThreshweight = PreprocessThreshweight
        self.PreprocessMorphKernel = PreprocessMorphKernel
        self.PlateWidthPaddingFactor = PlateWidthPaddingFactor
        self.PlateHeightPaddingFactor = PlateHeightPaddingFactor
        self.FindRectangledPlate = FindRectangledPlate
        self.MinPixelWidth = MinPixelWidth
        self.MaxPixelWidth = MaxPixelWidth
        self.MinPixelHeight = MinPixelHeight
        self.MaxPixelHeight = MaxPixelHeight
        self.MinAspectRatio = MinAspectRatio
        self.MaxAspectRatio = MaxAspectRatio
        self.MinPixelArea = MinPixelArea
        self.MaxPixelArea = MaxPixelArea
        self.MinDiagSizeMultipleAway = MinDiagSizeMultipleAway
        self.MaxDiagSizeMultipleAway = MaxDiagSizeMultipleAway
        self.MinChangeInArea = MinChangeInArea
        self.MaxChangeInArea = MaxChangeInArea
        self.MinChangeInWidth = MinChangeInWidth
        self.MaxChangeInWidth = MaxChangeInWidth
        self.MinChangeInHeight = MinChangeInHeight
        self.MaxChangeInHeight = MaxChangeInHeight
        self.MinHistNormThr = MinHistNormThr
        self.MinAngleBetweenChars = MinAngleBetweenChars
        self.MaxAngleBetweenChars = MaxAngleBetweenChars
        self.MinNumberOfMatchingChars = MinNumberOfMatchingChars
        self.MaxNumberOfMatchingChars = MaxNumberOfMatchingChars
        self.ResizedCharImageWidth = ResizedCharImageWidth
        self.ResizedCharImageHeight = ResizedCharImageHeight
        self.NoVerticalAlign = NoVerticalAlign
        self.kClassfications = kClassfications
        self.kFlattenedImages = kFlattenedImages
        self.kFactorKNN = kFactorKNN
        self.kNearest = None
        self.NoOcrTextualFixes = NoOcrTextualFixes
        self.NoOcrKnnFixes = NoOcrKnnFixes
        self.NoOcrDigitsOnly = NoOcrDigitsOnly
        self.batchMode = batchMode
        self.blueMaxThrH = blueMaxThrH
        self.blueMinThrS = blueMinThrS
        self.OpMode = OpMode
        self.debugMode = debugMode
        self.imgOriginalScene = None

        self.train_knn_classifier()

        debug("Input arguments: %s" % self.__dict__, debugMode)

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
    def train_knn_classifier(self):
        """ K-Nearest-Neighbours (KNN) classifier training for digits recognition: https://www.youtube.com/watch?v=ZD_tfNpKzHY 
            Training reference:  http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_ml/py_knn/py_knn_opencv/py_knn_opencv.html """

        # KNN construction, by machine-learning (ML) library of OpenCV2:
        self.kNearest = ml.KNearest_create()
        self.kNearest.setDefaultK(self.kFactorKNN)

        # Training (MNIST based, https://en.wikipedia.org/wiki/MNIST_database):
        try:
            npaClassifications = loadtxt(self.kClassfications, float32)  # Read in training classifications
        except IOError:
            error("Unable to open KNN training files, exiting program (%s)" % self.kClassfications)
            return

        try:
            npaFlattenedImages = loadtxt(self.kFlattenedImages, float32)  # Read in training images
        except IOError:
            error("Unable to open KNN training files, exiting program (%s)" % self.kFlattenedImages)
            return

        # Reshape numpy array to 1d, necessary to pass to call to train
        npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))

        # Train KNN object:
        self.kNearest.train(npaFlattenedImages, ml.ROW_SAMPLE, npaClassifications)

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
    def detect_plates_in_scene(self, imgOriginalScene):
        """ Detect plates in scene (geometrical analysis) """

        listOfPossiblePlates = detectPlatesInScene(imgOriginalScene,
                                                   self.PreprocessGaussKernel,
                                                   self.PreprocessThreshBlockSize,
                                                   self.PreprocessThreshweight,
                                                   self.PreprocessMorphKernel,
                                                   self.PlateWidthPaddingFactor,
                                                   self.PlateHeightPaddingFactor,
                                                   self.FindRectangledPlate,
                                                   self.MinPixelWidth, self.MaxPixelWidth,
                                                   self.MinPixelHeight, self.MaxPixelHeight,
                                                   self.MinAspectRatio, self.MaxAspectRatio,
                                                   self.MinPixelArea, self.MaxPixelArea,
                                                   self.MaxDiagSizeMultipleAway,
                                                   self.MinNumberOfMatchingChars, self.MaxNumberOfMatchingChars,
                                                   self.MinAngleBetweenChars, self.MaxAngleBetweenChars,
                                                   self.MinChangeInArea, self.MaxChangeInArea,
                                                   self.MinChangeInWidth, self.MaxChangeInWidth,
                                                   self.MinChangeInHeight, self.MaxChangeInHeight,
                                                   self.MinHistNormThr,
                                                   self.OpMode,
                                                   self.debugMode)
        return listOfPossiblePlates

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
    def detect_characters_in_plate(self, listOfPossiblePlates):
        """ Detect characters in the pre-detected plate (OCR analysis, over KNN engine) """

        listOfPossibleChars = detectCharsInPlates(listOfPossiblePlates,
                                                  self.PreprocessGaussKernel,
                                                  self.PreprocessThreshBlockSize,
                                                  self.PreprocessThreshweight,
                                                  self.PreprocessMorphKernel,
                                                  self.MinPixelWidth, self.MaxPixelWidth,
                                                  self.MinPixelHeight, self.MaxPixelHeight,
                                                  self.MinAspectRatio, self.MaxAspectRatio,
                                                  self.MinPixelArea, self.MaxPixelArea,
                                                  self.MinDiagSizeMultipleAway, self.MaxDiagSizeMultipleAway,
                                                  self.MinNumberOfMatchingChars, self.MaxNumberOfMatchingChars,
                                                  self.MinAngleBetweenChars, self.MaxAngleBetweenChars,
                                                  self.MinChangeInArea, self.MaxChangeInArea,
                                                  self.MinChangeInWidth, self.MaxChangeInWidth,
                                                  self.MinChangeInHeight, self.MaxChangeInHeight,
                                                  self.ResizedCharImageWidth, self.ResizedCharImageHeight,
                                                  self.kNearest,
                                                  self.kFactorKNN,
                                                  self.NoVerticalAlign,
                                                  self.NoOcrTextualFixes,
                                                  self.NoOcrKnnFixes,
                                                  self.NoOcrDigitsOnly,
                                                  self.blueMaxThrH,
                                                  self.blueMinThrS,
                                                  self.OpMode,
                                                  self.debugMode)
        return listOfPossibleChars

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
    def set_OpMode(self, imgOriginalScene, template, template_name, template_thr):

        (is_found, _) = isTemplateFound(imgOriginalScene, template, template_name, template_thr, self.debugMode)

        if is_found:
            info('OpMode auto-set to %s' % template_name)
            self.OpMode = template_name

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
    def report_result(self, imgOriginalScene, ROI, listOfPossibleChars, out_file="result.png", maxRes=(720, 1280), sweep_mode=True):
        """ Report the anlaysis result """

        result = "N/A"

        # Show the scene image (original):
        if not self.batchMode:
            imshow_scaled("imgOriginalScene", imgOriginalScene, maxRes)

        # Show output results (if any):
        if len(listOfPossibleChars) > 0:

            # Sort the list of possible plates in descending order, i.e. most number of chars to least number of chars:
            listOfPossibleChars.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)

            # Assume the plate with the most recognized characters is the actual plate:
            licPlate = listOfPossibleChars[0]

            # Fix license plate coordinates, accomodate ROI cropping:
            plateCenter = licPlate.rrLocationOfPlateInScene[0]
            licPlate.rrLocationOfPlateInSceneGbl = ((plateCenter[0] + ROI[0], plateCenter[1] + ROI[1]),
                                                    licPlate.rrLocationOfPlateInScene[1],
                                                    licPlate.rrLocationOfPlateInScene[2])

            # Show crop of plate and threshold of plate:
            if not self.batchMode:
                imshow("imgPlate", licPlate.imgPlate)
                imshow("imgThresh", licPlate.imgThresh)

            # Show LPR analysis result (if any):
            if len(licPlate.strChars) > 0:

                # Draw red rectangle around plate:
                drawRedRectangleAroundPlate(imgOriginalScene, licPlate, Colors.red)

                # Write license plate text on the image:
                writeLicensePlateCharsOnImage(imgOriginalScene, licPlate, Colors.yellow)

                # # Re-show scene image (optional downsize):
                if not self.batchMode:
                    imshow_scaled("imgOriginalScene", imgOriginalScene, maxRes)

                # Write image out to file:
                if not sweep_mode:
                    imwrite(out_file, imgOriginalScene)

                # Write license plate text to std out:
                info("license plate read from image = %s (w=%d,bs=%d)" % (licPlate.strChars, self.PreprocessThreshweight, self.PreprocessThreshBlockSize))
                result = licPlate.strChars 

            else:
                info("no characters were detected")

        else:
            info("no license plates were detected")

        # Hold windows open until user presses a key:
        if not self.batchMode:
            waitKey(0)

        return result
