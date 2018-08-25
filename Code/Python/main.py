#!/usr/bin/python
#  _     _                           ____  _       _         ____                            _ _   _
# | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
# | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
# | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
# |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
#                                                                                |___/
# (c) Shahar Gino, July-2017, sgino209@gmail.com

from time import time
from sys import exit, argv
from ast import literal_eval
from datetime import datetime
from LPR_wrapper import LPR_wrapper
from getopt import getopt, GetoptError
from Preprocess import imageEnhancement
from os import path, makedirs, chdir, getcwd
from onvif_capture import onvif_snapshot_test
from Auxiliary import Struct, info, debug, error, load_input_scene_image, crop_roi_from_image, ROI_adjust

__version__ = "1.61"

# ---------------------------------------------------------------------------------------------------------------
def usage():
    script_name = path.basename(__file__)
    print ''
    print '%s -i [image_file]' % script_name
    print ''
    print 'Optional preprocssing flags:                  --imgEnhancementEn --PreprocessGaussKernel --PreprocessThreshBlockSize'
    print 'Optional preprocssing flags (cont.):          --PreprocessThreshweight --PreprocessMorphKernel --blueMaxThrH --blueMinThrS'
    print 'Optional plate-detection flags:               --PlateWidthPaddingFactor --PlateHeightPaddingFactor --FindRectangledPlate'
    print 'Optional plate-detection flags (cont.):       --MinPixelWidth --MaxPixelWidth --MinPixelHeight --MaxPixelHeight'
    print 'Optional plate-detection flags (cont.):       --MinAspectRatio --MaxAspectRatio --MinPixelArea --MaxPixelArea'
    print 'Optional characters-detection flags:          --MinDiagSizeMultipleAway --MaxDiagSizeMultipleAway --MinChangeInArea --MaxChangeInArea'
    print 'Optional characters-detection flags (cont.):  --MinChangeInWidth --MaxChangeInWidth --MinChangeInHeight --MaxChangeInHeight --MinHistNormThr'
    print 'Optional characters-detection flags (cont.):  --MinAngleBetweenChars --MaxAngleBetweenChars --MinNumberOfMatchingChars --MaxNumberOfMatchingChars'
    print 'Optional characters-detection flags (cont.):  --ResizedCharImageWidth --ResizedCharImageHeight --kFactorKNN'
    print 'Optional characters-detection flags (cont.):  --NoVerticalAlign --NoOcrTextualFixes --NoOcrKnnFixes --NoOcrDigitsOnly'
    print 'Optional ONVIF parameters:                    --onvif_ip --onvif_port --onvif_user --onvif_passwd --onvif_test'
    print 'Optional misc. flags:                         --PoliceTemplate --PoliceTemplateThr --ROI --batch --mode --debug --version'
    print ''
    print 'Note about ROI settings:'
    print '   ROI = (startX, startY, width, height)'
    print '   setting ROI to (0,0) will set ROI to be equals to the whole input image'
    print '   setting ROI to (-1,-1) will set the system into autoROI mode, i.e. ROI euals to 20%-(60%)-20% x 40%-(50%)-10%'
    print ''

# ---------------------------------------------------------------------------------------------------------------
def main(_argv):
    """ Main function """

    # Default parameters:
    args = Struct(
        ImageFile=getcwd()+"/../../Database/Israel/1.jpg",
        PreprocessGaussKernel=(5, 5),
        PreprocessThreshBlockSize=19,
        PreprocessThreshweight=9,
        PreprocessMorphKernel=(3, 3),
        PlateWidthPaddingFactor=1.3,
        PlateHeightPaddingFactor=1.5,
        FindRectangledPlate=False,
        ROI=(-1, -1),
        MinPixelWidth=2,
        MaxPixelWidth=float("inf"),
        MinPixelHeight=8,
        MaxPixelHeight=float("inf"),
        MinAspectRatio=0.25,
        MaxAspectRatio=1.0,
        MinPixelArea=80,
        MaxPixelArea=float("inf"),
        MinDiagSizeMultipleAway=0.3,
        MaxDiagSizeMultipleAway=4,
        MinChangeInArea=0,
        MaxChangeInArea=0.5,
        MinChangeInWidth=0,
        MaxChangeInWidth=0.8,
        MinChangeInHeight=0,
        MaxChangeInHeight=0.2,
        MinHistNormThr=65,
        MinAngleBetweenChars=0,
        MaxAngleBetweenChars=12.0,
        MinNumberOfMatchingChars=6,
        MaxNumberOfMatchingChars=8,
        ResizedCharImageWidth=20,
        ResizedCharImageHeight=30,
        NoVerticalAlign=True,
        kClassfications=getcwd()+"/KNN_training/classifications.txt",
        kFlattenedImages=getcwd()+"/KNN_training/flattened_images.txt",
        kFactorKNN=2,
        NoOcrTextualFixes=False,
        NoOcrKnnFixes=False,
        NoOcrDigitsOnly=False,
        PoliceTemplate=getcwd()+"/Templates/p_template.png",
        PoliceTemplateThr=(0.495, 60),
        onvif_ip='192.168.226.201',
        onvif_port=80,
        onvif_user='admin',
        onvif_passwd='123456',
        onvif_test=False,
        imgEnhancementEn=False,
        blueMaxThrH=40,
        blueMinThrS=60,
        batchMode=False,
        OpMode="auto",
        debugMode=False
        )

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
    # User-Arguments parameters (overrides Defaults):
    try:
        opts, user_args = getopt(_argv, "hvi:", ["PreprocessGaussKernel=", "PreprocessThreshBlockSize=",
                                                 "PreprocessThreshweight=", "PreprocessMorphKernel=",
                                                 "PlateWidthPaddingFactor=", "PlateHeightPaddingFactor=",
                                                 "FindRectangledPlate", "ROI=",
                                                 "MinPixelWidth=", "MaxPixelWidth=",
                                                 "MinPixelHeight=", "MaxPixelHeight=",
                                                 "MinAspectRatio=", "MaxAspectRatio=",
                                                 "MinPixelArea=", "MaxPixelArea=",
                                                 "MinDiagSizeMultipleAway=", "MaxDiagSizeMultipleAway=",
                                                 "MinChangeInArea=", "MaxChangeInArea=",
                                                 "MinChangeInWidth=", "MaxChangeInWidth=",
                                                 "MinChangeInHeight=", "MaxChangeInHeight=",
                                                 "MinHistNormThr=",
                                                 "MinAngleBetweenChars=", "MaxAngleBetweenChars=",
                                                 "MinNumberOfMatchingChars=", "MaxNumberOfMatchingChars=",
                                                 "ResizedCharImageWidth=", "ResizedCharImageHeight=",
                                                 "NoVerticalAlign", "kClassfications=", "kFlattenedImages=",
                                                 "kFactorKNN=", "NoOcrTextualFixes", "NoOcrKnnFixes",
                                                 "NoOcrDigitsOnly", "PoliceTemplate=", "PoliceTemplateThr",
                                                 "onvif_ip=", "onvif_port=", "onvif_user=", "onvif_passwd=",
                                                 "onvif_test", "imgEnhancementEn", "blueMaxThrH=", "blueMinThrS=",
                                                 "batch", "mode=", "debug", "version"])

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
            elif opt in "--FindRectangledPlate":
                args.FindRectangledPlate = True
            elif opt in "--ROI":
                args.ROI = literal_eval(user_arg)
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
            elif opt in "--MinHistNormThr":
                args.MinHistNormThr = float(user_arg)
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
            elif opt in "--NoVerticalAlign":
                args.NoVerticalAlign = True
            elif opt in "--kClassfications":
                args.kClassfications = user_arg
            elif opt in "--kFlattenedImages":
                args.kFlattenedImages = user_arg
            elif opt in "--kFactorKNN":
                args.kFactorKNN = int(user_arg)
            elif opt in "--NoOcrTextualFixes":
                args.NoOcrTextualFixes = True
            elif opt in "--NoOcrKnnFixes":
                args.NoOcrKnnFixes = True
            elif opt in "--NoOcrDigitsOnly":
                args.NoOcrDigitsOnly = True
            elif opt in "--PoliceTemplate":
                args.PoliceTemplate = user_arg
            elif opt in "--PoliceTemplateThr":
                args.PoliceTemplateThr = literal_eval(user_arg)
            elif opt in "--onvif_ip":
                args.onvif_ip = user_arg
            elif opt in "--onvif_port":
                args.onvif_port = int(user_arg)
            elif opt in "--onvif_user":
                args.onvif_user = user_arg
            elif opt in "--onvif_passwd":
                args.onvif_passwd = user_arg
            elif opt in "--onvif_test":
                args.onvif_test = True
            elif opt in "--imgEnhancementEn":
                args.imgEnhancementEn = True
            elif opt in "--blueMaxThrH":
                args.blueMaxThrH = float(user_arg)
            elif opt in "--blueMinThrS":
                args.blueMinThrS = float(user_arg)
            elif opt in "--batch":
                args.batchMode = True
            elif opt in "--mode":
                args.OpMode = user_arg
            elif opt in "--debug":
                args.debugMode = True
            elif opt in "--version" or opt == '-v':
                info("LPR version: %s" % __version__)
                exit()

    except GetoptError, e:
        error(str(e))
        usage()
        exit(2)

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
    if args.onvif_test:
        onvif_snapshot_test()
        return 0

    # Create a working environment:
    envpath = datetime.now().strftime("lpr_results_%d%m%y_%H%M%S_") + args.ImageFile.split('/')[-1].replace('.','_')
    if not path.exists(envpath):
        makedirs(envpath)
    cwd = getcwd()
    chdir(envpath)

    # Generate an LPR object:
    lpr = LPR_wrapper(args.PreprocessGaussKernel,      # Preprocessing: gaussian kernel, for smoothing
                      args.PreprocessThreshBlockSize,  # Preprocessing: adaptive threshold, block size
                      args.PreprocessThreshweight,     # Preprocessing: adaptive threshold, weight
                      args.PreprocessMorphKernel,      # Preprocessing: morphological structuring kernel
                      args.PlateWidthPaddingFactor,    # Plate width padding factor, used for plate extraction
                      args.PlateHeightPaddingFactor,   # Plate height padding factor, used for plate extraction
                      args.FindRectangledPlate,        # Add another plate candidate, in addition to longest matching characters approach
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
                      args.MinHistNormThr,             # Minimal saturation threshold that a Plate must reach, lower boundary
                      args.MinAngleBetweenChars,       # Angle difference (degrees) for matching characters decision, lower boundary
                      args.MaxAngleBetweenChars,       # Angle difference (degrees) for matching characters decision, upper boundary
                      args.MinNumberOfMatchingChars,   # Minimal amount of characters in the plate ("matching characters")
                      args.MaxNumberOfMatchingChars,   # Maximal amount of characters in the plate ("matching characters")
                      args.ResizedCharImageWidth,      # Character Resizing width attribute (in pixels), necessary for the OCR stage
                      args.ResizedCharImageHeight,     # Character Resizing height attribute (in pixels), necessary for the OCR stage
                      args.NoVerticalAlign,            # Characters Vertical alignment, i.e. fix outlier characters along y-axis
                      args.kClassfications,            # KNN training data: classification results (see openCV docs)
                      args.kFlattenedImages,           # KNN training data: flattened images (see openCV docs)
                      args.kFactorKNN,                 # KNN factor, for digits classification
                      args.NoOcrTextualFixes,          # Do not perform manual OCR texutal corrections, e.g. 'I'-->'1'
                      args.NoOcrKnnFixes,              # Do not perform manual OCR KNN corrections, e.g. '6'-->'5'
                      args.NoOcrDigitsOnly,            # Do not drop OCR results with english alphabet characters (digits only)
                      args.batchMode,                  # Run in batch mode, minimal debug info and w/o figures
                      args.blueMaxThrH,                # Maximal Hue for a charater to be classified as "blue" (higher H will get waived)
                      args.blueMinThrS,                # Minimal Saturation for a charater to be classified as "blue" (lower S will get waived)
                      args.OpMode,                     # Run in a specific operational mode, e.g. "police"
                      args.debugMode)                  # Enable debug printouts and intermediate figures

    # Load input scene image:
    imgOriginalScene = load_input_scene_image(args.ImageFile, 'Image',
                                              args.onvif_ip, args.onvif_port, args.onvif_user, args.onvif_passwd)

    if imgOriginalScene is None:
        return 1

    # Image enhancement:
    if (args.imgEnhancementEn):
        imgEnhanced = imageEnhancement(imgOriginalScene, 2, (8,8), 3)
    else:
        imgEnhanced = imgOriginalScene

    # Crop the ROI from the image:
    ROI, autoRoiMode = ROI_adjust(args.ROI, imgEnhanced, (20,60,20), (40,50,10))  # autoROI
    imgCropped = crop_roi_from_image(imgEnhanced, ROI, autoRoiMode)

    # OpMode auto-mode (check for a police vehicle):
    if lpr.OpMode == "auto":
        PoliceTemplate = load_input_scene_image(args.PoliceTemplate, 'PoliceTemplate')
        lpr.set_OpMode(imgCropped, PoliceTemplate, 'police', args.PoliceTemplateThr)

    # Seek for plates, then for characters, from Max to Min number of digits (greedy):
    A = lpr.MinNumberOfMatchingChars
    B = lpr.MaxNumberOfMatchingChars
        
    scoreboard_max = 0
    scoreboard_winners = {}

    result = "N/A" 

    for thr_weight in range(3,13,2):

        for thr_blk_size in range(9,23,2):

            lpr.PreprocessThreshweight = thr_weight
            lpr.PreprocessThreshBlockSize = thr_blk_size

            for numOfMatchingChar in range(B, A-1, -1):

                debug("------ W=%d, BS=%d, #Chars=%d" % (thr_weight, thr_blk_size, numOfMatchingChar), args.debugMode)

                lpr.MinNumberOfMatchingChars = numOfMatchingChar
                lpr.MaxNumberOfMatchingChars = numOfMatchingChar

                # Plates detection (within the given image):
                listOfPossiblePlates = lpr.detect_plates_in_scene(imgCropped)

                # Characters detection (within the pre-detected plate):
                listOfPossibleChars = lpr.detect_characters_in_plate(listOfPossiblePlates)

                if len(listOfPossibleChars) > 0 and len(listOfPossibleChars[0].strChars) > 0:

                    # Report the analysis result:
                    if args.ImageFile == "onvif":
                        out_file = 'onvif_out.png'
                    else:
                        out_file = path.basename(args.ImageFile).replace(".", "_out.")

                    result = lpr.report_result(imgEnhanced, ROI, listOfPossibleChars, out_file)

                    if result != "N/A":

                        pts = 1
                        if len(result) > A and len(result) <= B:  # main course gets higher weight
                            pts = 4

                        if result in scoreboard_winners:
                            scoreboard_winners[result] += pts
                        else:
                            scoreboard_winners[result] = pts

                        if scoreboard_winners[result] > scoreboard_max:
                          imgOut = listOfPossibleChars[0].imgPlate.copy()
                          scoreboard_max = scoreboard_winners[result]

                        break

    maxVal = 0;
    for key, value in scoreboard_winners.iteritems():
        print "%s --> %d" % (key,value)
        if value > maxVal:
          maxVal = value;
          result = key;

    # Restore path:
    chdir(cwd)

    info("LPR Result: %s" % result)
    
    return result

# ---------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    t0 = time()
    print 'Start'

    main(argv[1:])

    t1 = time()
    t_elapsed_sec = t1 - t0
    print('Done! (%.2f sec)' % t_elapsed_sec)

