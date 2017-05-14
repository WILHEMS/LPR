# !/usr/bin/python
#  _     _                           ____  _       _         ____                            _ _   _
# | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
# | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
# | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
# |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
#                                                                                |___/
# (c) Shahar Gino, May-2017, sgino209@gmail.com

from os import path
from time import time
from sys import exit, argv
from Auxiliary import Struct
from LPR_wrapper import LPR_wrapper
from getopt import getopt, GetoptError

__version__ = "1.0"

# ---------------------------------------------------------------------------------------------------------------
def usage():
    script_name = path.basename(__file__)
    print '%s -i [image_file]' % script_name
    print 'Optional preprocssing flags:                  --PreprocessGaussKernel --PreprocessThreshBlockSize --PreprocessThreshweight --PreprocessMorphKernel'
    print 'Optional plate-detection flags:               --PlateWidthPaddingFactor --PlateHeightPaddingFactor'
    print 'Optional plate-detection flags (cont.):       --MinPixelWidth --MaxPixelWidth --MinPixelHeight --MaxPixelHeight'
    print 'Optional plate-detection flags (cont.):       --MinAspectRatio --MaxAspectRatio --MinPixelArea --MaxPixelArea'
    print 'Optional characters-detection flags:          --MinDiagSizeMultipleAway --MaxDiagSizeMultipleAway --MinChangeInArea --MaxChangeInArea'
    print 'Optional characters-detection flags (cont.):  --MinChangeInWidth --MaxChangeInWidth --MinChangeInHeight --MaxChangeInHeight'
    print 'Optional characters-detection flags (cont.):  --MinAngleBetweenChars --MaxAngleBetweenChars --MinNumberOfMatchingChars --MaxNumberOfMatchingChars'
    print 'Optional characters-detection flags (cont.):  --ResizedCharImageWidth --ResizedCharImageHeight --kFactorKNN'
    print 'Optional misc. flags:                         --batch --debug'

# ---------------------------------------------------------------------------------------------------------------
def main(_argv):

    # Default parameters:
    args = Struct(
        ImageFile="/Users/shahargino/Documents/ImageProcessing/LPR/Database/1.jpg",
        PreprocessGaussKernel=(5, 5),
        PreprocessThreshBlockSize=19,
        PreprocessThreshweight=9,
        PreprocessMorphKernel=(3, 3),
        PlateWidthPaddingFactor=1.3,
        PlateHeightPaddingFactor=1.5,
        MinPixelWidth=2,
        MaxPixelWidth=float("inf"),
        MinPixelHeight=8,
        MaxPixelHeight=float("inf"),
        MinAspectRatio=0.25,
        MaxAspectRatio=1.0,
        MinPixelArea=80,
        MaxPixelArea=float("inf"),
        MinDiagSizeMultipleAway=0.3,
        MaxDiagSizeMultipleAway=5.0,
        MinChangeInArea=0,
        MaxChangeInArea=0.5,
        MinChangeInWidth=0,
        MaxChangeInWidth=0.8,
        MinChangeInHeight=0,
        MaxChangeInHeight=0.2,
        MinAngleBetweenChars=0,
        MaxAngleBetweenChars=12.0,
        MinNumberOfMatchingChars=3,
        MaxNumberOfMatchingChars=7,
        ResizedCharImageWidth=20,
        ResizedCharImageHeight=30,
        kClassfications="KNN_training/classifications.txt",
        kFlattenedImages="KNN_training/flattened_images.txt",
        kFactorKNN=1,
        batchMode=False,
        debugMode=False
        )

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
    # User-Arguments parameters (overrides Defaults):
    try:
        opts, user_args = getopt(_argv, "hi:", ["PreprocessGaussKernel=", "PreprocessThreshBlockSize=",
                                                "PreprocessThreshweight=", "PreprocessMorphKernel=",
                                                "PlateWidthPaddingFactor=", "PlateHeightPaddingFactor=",
                                                "MinPixelWidth=", "MaxPixelWidth=",
                                                "MinPixelHeight=", "MaxPixelHeight=",
                                                "MinAspectRatio=", "MaxAspectRatio=",
                                                "MinPixelArea=", "MaxPixelArea=",
                                                "MinDiagSizeMultipleAway=", "MaxDiagSizeMultipleAway=",
                                                "MinChangeInArea=", "MaxChangeInArea=",
                                                "MinChangeInWidth=", "MaxChangeInWidth=",
                                                "MinChangeInHeight=", "MaxChangeInHeight=",
                                                "MinAngleBetweenChars=", "MaxAngleBetweenChars=",
                                                "MinNumberOfMatchingChars=", "MaxNumberOfMatchingChars=",
                                                "ResizedCharImageWidth=", "ResizedCharImageHeight=",
                                                "kClassfications=", "kFlattenedImages=", "kFactorKNN=",
                                                "debug", "batch"])

        for opt, user_arg in opts:
            if opt == '-h':
                usage()
                exit()
            elif opt in "-i":
                args.ImageFile = user_arg
            elif opt in "--PreprocessGaussKernel":
                args.PreprocessGaussKernel = literal_eval(user_arg)
            elif opt in "--PreprocessThreshBlockSize":
                args.PreprocessThreshBlockSize = int(user_arg)
            elif opt in "--PreprocessThreshweight":
                args.PreprocessThreshweight = int(user_arg)
            elif opt in "--PreprocessMorphKernel":
                args.PreprocessMorphKernel = literal_eval(user_arg)
            elif opt in "--PlateWidthPaddingFactor":
                args.PlateWidthPaddingFactor = float(user_arg)
            elif opt in "--PlateHeightPaddingFactor":
                args.PlateHeightPaddingFactor = float(user_arg)
            elif opt in "--MinPixelWidth":
                args.MinPixelWidth = float(user_arg)
            elif opt in "--MaxPixelWidth":
                args.MaxPixelWidth = float(user_arg)
            elif opt in "--MinPixelHeight":
                args.MinPixelHeight = float(user_arg)
            elif opt in "--MaxPixelHeight":
                args.MaxPixelHeight = float(user_arg)
            elif opt in "--MinAspectRatio":
                args.MinAspectRatio = float(user_arg)
            elif opt in "--MaxAspectRatio":
                args.MaxAspectRatio = float(user_arg)
            elif opt in "--MinPixelArea":
                args.MinPixelArea = float(user_arg)
            elif opt in "--MaxPixelArea":
                args.MaxPixelArea = float(user_arg)
            elif opt in "--MinDiagSizeMultipleAway":
                args.MinDiagSizeMultipleAway = float(user_arg)
            elif opt in "--MaxDiagSizeMultipleAway":
                args.MaxDiagSizeMultipleAway = float(user_arg)
            elif opt in "--MinChangeInArea":
                args.MinChangeInArea = float(user_arg)
            elif opt in "--MaxChangeInArea":
                args.MaxChangeInArea = float(user_arg)
            elif opt in "--MinChangeInWidth":
                args.MinChangeInWidth = float(user_arg)
            elif opt in "--MaxChangeInWidth":
                args.MaxChangeInWidth = float(user_arg)
            elif opt in "--MinChangeInHeight":
                args.MinChangeInHeight = float(user_arg)
            elif opt in "--MaxChangeInHeight":
                args.MaxChangeInHeight = float(user_arg)
            elif opt in "--MinAngleBetweenChars":
                args.MinAngleBetweenChars = float(user_arg)
            elif opt in "--MaxAngleBetweenChars":
                args.MaxAngleBetweenChars = float(user_arg)
            elif opt in "--MinNumberOfMatchingChars":
                args.MinNumberOfMatchingChars = int(user_arg)
            elif opt in "--MaxNumberOfMatchingChars":
                args.MaxNumberOfMatchingChars = int(user_arg)
            elif opt in "--ResizedCharImageWidth":
                args.ResizedCharImageWidth = int(user_arg)
            elif opt in "--ResizedCharImageHeight":
                args.ResizedCharImageHeight = int(user_arg)
            elif opt in "--kClassfications":
                args.kClassfications = user_arg
            elif opt in "--kFlattenedImages":
                args.kFlattenedImages = user_arg
            elif opt in "--kFactorKNN":
                args.kFactorKNN = int(user_arg)
            elif opt in "--batch":
                args.batchMode = True
            elif opt in "--debug":
                args.debugMode = True

    except GetoptError:
        usage()
        exit(2)

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
    # Generate an LPR object:
    lpr = LPR_wrapper(args.PreprocessGaussKernel,      # Preprocessing: gaussian kernel, for smoothing
                      args.PreprocessThreshBlockSize,  # Preprocessing: adaptive threshold, block size
                      args.PreprocessThreshweight,     # Preprocessing: adaptive threshold, weight
                      args.PreprocessMorphKernel,      # Preprocessing: morphological structuring kernel
                      args.PlateWidthPaddingFactor,    # Plate width padding factor, used for plate extraction
                      args.PlateHeightPaddingFactor,   # Plate height padding factor, used for plate extraction
                      args.MinPixelWidth,              # Minimal width (#pixels) for a character to be detected
                      args.MaxPixelWidth,              # Maximal width (#pixels) for a character to be detected
                      args.MinPixelHeight,             # Minimal height (#pixels) for a character to be detected
                      args.MaxPixelHeight,             # Maximal height (#pixels) for a character to be detected
                      args.MinAspectRatio,             # Minimal aspect ratio (W/H) for a character to be detected
                      args.MaxAspectRatio,             # Maximal aspect ratio (W/H) for a character to be detected
                      args.MinPixelArea,               # Minimal area (#pixels) for a character to be detected
                      args.MaxPixelArea,               # Maximal area (#pixels) for a character to be detected
                      args.MinDiagSizeMultipleAway,    # Sizing factor for overlapping characters decision (% of character size)
                      args.MaxDiagSizeMultipleAway,    # Sizing factor for matching characters decision (% of character size)
                      args.MinChangeInArea,            # Normalized Area difference for matching characters decision, lower boundary
                      args.MaxChangeInArea,            # Normalized Area difference for matching characters decision, upper boundary
                      args.MinChangeInWidth,           # Normalized Width difference for matching characters decision, lower boundary
                      args.MaxChangeInWidth,           # Normalized Width difference for matching characters decision, upper boundary
                      args.MinChangeInHeight,          # Normalized Height difference for matching characters decision, lower boundary
                      args.MaxChangeInHeight,          # Normalized Height difference for matching characters decision, upper boundary
                      args.MinAngleBetweenChars,       # Angle difference (degrees) for matching characters decision, lower boundary
                      args.MaxAngleBetweenChars,       # Angle difference (degrees) for matching characters decision, upper boundary
                      args.MinNumberOfMatchingChars,   # Minimal amount of characters in the plate ("matching characters")
                      args.MaxNumberOfMatchingChars,   # Maximal amount of characters in the plate ("matching characters")
                      args.ResizedCharImageWidth,      # Character Resizing width attribute (in pixels), necessary for the OCR stage
                      args.ResizedCharImageHeight,     # Character Resizing height attribute (in pixels), necessary for the OCR stage
                      args.kClassfications,            # KNN training data: classification results (see openCV docs)
                      args.kFlattenedImages,           # KNN training data: flattened images (see openCV docs)
                      args.kFactorKNN,                 # KNN factor, for digits classification
                      args.batchMode,                  # Run in batch mode, minimal debug info and w/o figures
                      args.debugMode)                  # Enable debug printouts and intermediate figures

    # Load input scene image:
    imgOriginalScene = lpr.load_input_scene_image(args.ImageFile)

    # Plates detection (within the given image):
    listOfPossiblePlates = lpr.detect_plates_in_scene(imgOriginalScene)

    # Characters detection (within the pre-detected plate):
    listOfPossibleChars = lpr.detect_characters_in_plate(listOfPossiblePlates)

    # Report the analysis result:
    lpr.report_result(imgOriginalScene,
                      listOfPossibleChars,
                      path.basename(args.ImageFile).replace(".", "_out."))

# ---------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    t0 = time()
    print 'Start'

    main(argv[1:])

    t1 = time()
    t_elapsed_sec = t1 - t0
    print('Done! (%.2f sec)' % t_elapsed_sec)
