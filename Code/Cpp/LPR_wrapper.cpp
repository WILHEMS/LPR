// LPR_wrapper.cpp
//  _     _                           ____  _       _         ____                            _ _   _
// | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
// | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
// | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
// |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
//                                                                                |___/
// (c) Shahar Gino, July-2017, sgino209@gmail.com

#include "LPR_wrapper.hpp"

// ------------------------------------------------------------------------------------------------------------------------------
// Plates detection (within the given image):
std::vector<PossiblePlate> LPR_wrapper :: detect_plates_in_scene(cv::Mat imgOriginalScene) {

    plate_params_t plate_params(imgOriginalScene,
                                params.PreprocessGaussKernel,
                                params.PreprocessThreshBlockSize,
                                params.PreprocessThreshweight,
                                params.PreprocessMorphKernel,
                                params.PlateWidthPaddingFactor,
                                params.PlateHeightPaddingFactor,
                                params.FindRectangledPlate,
                                params.MinPixelWidth, params.MaxPixelWidth,
                                params.MinPixelHeight, params.MaxPixelHeight,
                                params.MinAspectRatio, params.MaxAspectRatio,
                                params.MinPixelArea, params.MaxPixelArea,
                                params.MaxDiagSizeMultipleAway,
                                params.MinNumberOfMatchingChars, params.MaxNumberOfMatchingChars,
                                params.MinAngleBetweenChars, params.MaxAngleBetweenChars,
                                params.MinChangeInArea, params.MaxChangeInArea,
                                params.MinChangeInWidth, params.MaxChangeInWidth,
                                params.MinChangeInHeight, params.MaxChangeInHeight,
                                params.MinHistNormThr, params.OpMode, params.debugMode);

    std::vector<PossiblePlate> listOfPossiblePlates = detectPlatesInScene(imgOriginalScene, plate_params);

    return listOfPossiblePlates;
}

// ------------------------------------------------------------------------------------------------------------------------------
// Characters detection (within the pre-detected plate, updated in-place the corresponding PossiblePlate objects):
std::vector<PossiblePlate> LPR_wrapper :: detect_characters_in_plate(std::vector<PossiblePlate> listOfPossiblePlates) {

    char_params_t char_params(listOfPossiblePlates,
                              params.PreprocessGaussKernel,
                              params.PreprocessThreshBlockSize,
                              params.PreprocessThreshweight,
                              params.PreprocessMorphKernel,
                              params.MinPixelWidth, params.MaxPixelWidth,
                              params.MinPixelHeight, params.MaxPixelHeight,
                              params.MinAspectRatio, params.MaxAspectRatio,
                              params.MinPixelArea, params.MaxPixelArea,
                              params.MinDiagSizeMultipleAway, params.MaxDiagSizeMultipleAway,
                              params.MinNumberOfMatchingChars, params.MaxNumberOfMatchingChars,
                              params.MinAngleBetweenChars, params.MaxAngleBetweenChars,
                              params.MinChangeInArea, params.MaxChangeInArea,
                              params.MinChangeInWidth, params.MaxChangeInWidth,
                              params.MinChangeInHeight, params.MaxChangeInHeight,
                              params.ResizedCharImageWidth, params.ResizedCharImageHeight,
                              params.kNearest,
                              params.kFactorKNN,
                              params.NoVerticalAlign,
                              params.NoOcrTextualFixes,
                              params.NoOcrKnnFixes,
                              params.NoOcrDigitsOnly,
                              params.blueMaxThrH,
                              params.blueMinThrS,
                              params.OpMode,
                              params.debugMode);

    std::vector<PossiblePlate> listOfPossibleChars = detectCharsInPlates(listOfPossiblePlates, char_params);

    return listOfPossibleChars;
}

// ------------------------------------------------------------------------------------------------------------------------------
void LPR_wrapper :: set_OpMode(cv::Mat &imgOriginalScene, cv::Mat &imgTemplate, std::string template_name, double_xy_t template_thr) {

    char buffer[100];
    double_xy_t *templateLoc = NULL;
    bool is_found = isTemplateFound(imgOriginalScene, imgTemplate, template_name, template_thr, templateLoc, params.debugMode);

    if (is_found) {
        sprintf(buffer, "OpMode auto-set to %s", template_name.c_str());
        debug(buffer);
        params.OpMode = template_name;
    }
}

// ------------------------------------------------------------------------------------------------------------------------------
// Report the analysis result:
std::string LPR_wrapper :: report_result(cv::Mat imgOriginalScene, uint_x4_t ROI, std::vector<PossiblePlate> listOfPossibleChars, std::string out_file, bool sweep_mode) {

    std::string result = "N/A";

    // Show the scene image (original):
    if (!params.batchMode) {
        cv::imshow("imgOriginalScene", imgOriginalScene);
    }

    // Show output results (if any):
    if (!listOfPossibleChars.empty()) {

        // Sort the list of possible plates in descending order, i.e. most number of chars to least number of chars:
        std::sort(listOfPossibleChars.begin(), listOfPossibleChars.end(), PossiblePlate::sortDescendingByNumberOfChars);

        // Assume the plate with the most recognized characters is the actual plate:
        PossiblePlate licPlate = listOfPossibleChars.front();

        // Fix license plate coordinates, accomodate ROI cropping:
        licPlate.rrLocationOfPlateInScene.center.x += ROI.get_x1();
        licPlate.rrLocationOfPlateInScene.center.y += ROI.get_x2();

        // Show crop of plate and threshold of plate:
        if (!params.batchMode) {
            cv::imshow("imgPlate", licPlate.imgPlate);
            cv::imshow("imgThresh", licPlate.imgThresh);
        }

        // Show LPR analysis result (if any):
        if (licPlate.strChars.length() > 0) {

            // Draw red rectangle around plate:
            drawRedRectangleAroundPlate(imgOriginalScene, licPlate);

            // Write license plate text on the image:
            writeLicensePlateCharsOnImage(imgOriginalScene, licPlate);

            // Re-show scene image:
            if (!params.batchMode) {
                cv::imshow("imgOriginalScene", imgOriginalScene);
            }

            // Write image out to file:
            if (!sweep_mode) {
              cv::imwrite(out_file, imgOriginalScene);
            }

            // Write license plate text to std out:
            char buffer[100];
            sprintf(buffer, "license plate read from image = %s (w=%lu,bs=%lu)", licPlate.strChars.c_str(), params.PreprocessThreshweight, params.PreprocessThreshBlockSize);
            info(buffer);
            result = licPlate.strChars;
        }
        else {
            info("no characters were detected");
        }
    }
    else {
        info("no license plates were detected");
    }

    // Hold windows open until user presses a key:
    if (!params.batchMode) {
        cv::waitKey(0);
    }

    return result;
}

// ------------------------------------------------------------------------------------------------------------------------------
void LPR_wrapper :: print_params(args_t params) {

    std::cout << "ImageFile = " << params.ImageFile << std::endl;
    std::cout << "PreprocessGaussKernel = " << params.PreprocessGaussKernel.to_string() << std::endl;
    std::cout << "PreprocessThreshBlockSize = " << params.PreprocessThreshBlockSize << std::endl;
    std::cout << "PreprocessThreshweight = " << params.PreprocessThreshweight << std::endl;
    std::cout << "PreprocessMorphKernel = " << params.PreprocessMorphKernel.to_string() << std::endl;
    std::cout << "PlateWidthPaddingFactor = " << params.PlateWidthPaddingFactor << std::endl;
    std::cout << "PlateHeightPaddingFactor = " << params.PlateHeightPaddingFactor << std::endl;
    std::cout << "FindRectangledPlate = " << params.FindRectangledPlate << std::endl;
    std::cout << "ROI = " << params.ROI.to_string() << std::endl;
    std::cout << "MinPixelWidth = " << params.MinPixelWidth << std::endl;
    std::cout << "MaxPixelWidth = " << params.MaxPixelWidth << std::endl;
    std::cout << "MinPixelHeight = " << params.MinPixelHeight << std::endl;
    std::cout << "MaxPixelHeight = " << params.MaxPixelHeight << std::endl;
    std::cout << "MinAspectRatio = " << params.MinAspectRatio << std::endl;
    std::cout << "MaxAspectRatio = " << params.MaxAspectRatio << std::endl;
    std::cout << "MinPixelArea = " << params.MinPixelArea << std::endl;
    std::cout << "MaxPixelArea = " << params.MaxPixelArea << std::endl;
    std::cout << "MinDiagSizeMultipleAway = " << params.MinDiagSizeMultipleAway << std::endl;
    std::cout << "MaxDiagSizeMultipleAway = " << params.MaxDiagSizeMultipleAway << std::endl;
    std::cout << "MinChangeInArea = " << params.MinChangeInArea << std::endl;
    std::cout << "MaxChangeInArea = " << params.MaxChangeInArea << std::endl;
    std::cout << "MinChangeInWidth = " << params.MinChangeInWidth << std::endl;
    std::cout << "MaxChangeInWidth = " << params.MaxChangeInWidth << std::endl;
    std::cout << "MinChangeInHeight = " << params.MinChangeInHeight << std::endl;
    std::cout << "MaxChangeInHeight = " << params.MaxChangeInHeight << std::endl;
    std::cout << "MinAngleBetweenChars = " << params.MinAngleBetweenChars << std::endl;
    std::cout << "MaxAngleBetweenChars = " << params.MaxAngleBetweenChars << std::endl;
    std::cout << "MinNumberOfMatchingChars = " << params.MinNumberOfMatchingChars << std::endl;
    std::cout << "MaxNumberOfMatchingChars = " << params.MaxNumberOfMatchingChars << std::endl;
    std::cout << "ResizedCharImageWidth = " << params.ResizedCharImageWidth << std::endl;
    std::cout << "ResizedCharImageHeight = " << params.ResizedCharImageHeight << std::endl;
    std::cout << "NoVerticalAlign = " << params.NoVerticalAlign << std::endl;
    std::cout << "kClassfications = " << params.kClassfications << std::endl;
    std::cout << "kFlattenedImages = " << params.kFlattenedImages << std::endl;
    std::cout << "kFactorKNN = " << params.kFactorKNN << std::endl;
    std::cout << "NoOcrTextualFixes = " << params.NoOcrTextualFixes << std::endl;
    std::cout << "NoOcrKnnFixes = " << params.NoOcrKnnFixes << std::endl;
    std::cout << "NoOcrDigitsOnly = " << params.NoOcrDigitsOnly << std::endl;
    std::cout << "imgEnhancementMode = " << params.imgEnhancementMode << std::endl;
    std::cout << "PerspectiveWarp0 = " << params.pWarpPnt0.to_string() << std::endl;
    std::cout << "PerspectiveWarp1 = " << params.pWarpPnt1.to_string() << std::endl;
    std::cout << "PerspectiveWarp2 = " << params.pWarpPnt2.to_string() << std::endl;
    std::cout << "PerspectiveWarp3 = " << params.pWarpPnt3.to_string() << std::endl;
    std::cout << "blueMaxThrH = " << params.blueMaxThrH << std::endl;
    std::cout << "blueMinThrS = " << params.blueMinThrS << std::endl;
    std::cout << "PoliceTemplate = " << params.PoliceTemplate << std::endl;
    std::cout << "PoliceTemplateThr = " << params.PoliceTemplateThr.to_string() << std::endl;
    std::cout << "batchMode = " << params.batchMode << std::endl;
    std::cout << "OpMode = " << params.OpMode << std::endl;
    std::cout << "debugMode = " << params.debugMode << std::endl;
}

// ==============================================================================================================================

int train_knn_classifier(args_t &args) {

    // Training (MNIST based, https://en.wikipedia.org/wiki/MNIST_database):
    // - Classification file:  contains 180 lines, which lists all ascii symbols for digits (48-57) and characters (65-90) - 5 lines per symbol
    // - FlattenedImages file: contains 180 lines, corresponds with the Classification file, each contains 5 flattened images (20x30, column-stack)

    // KNN construction, by machine-learning (ML) library of OpenCV2:
    args.kNearest = cv::ml::KNearest::create();
    args.kNearest->setDefaultK(args.kFactorKNN);

    // Read training classifications:
    cv::Mat matClassificationInts;
    cv::FileStorage fsClassifications(args.kClassfications, cv::FileStorage::READ);
    if (fsClassifications.isOpened() == false) {
        error("unable to open training classifications file, exiting program");
        return 1;
    }
    fsClassifications["classifications"] >> matClassificationInts;
    fsClassifications.release();

    // Read training images:
    cv::Mat matTrainingImagesAsFlattenedFloats;
    cv::FileStorage fsTrainingImages(args.kFlattenedImages, cv::FileStorage::READ);
    if (fsTrainingImages.isOpened() == false) {
        error("unable to open training images file, exiting program");
        return 1;
    }
    fsTrainingImages["images"] >> matTrainingImagesAsFlattenedFloats;
    fsTrainingImages.release();

    // Train KNN object:
    args.kNearest->train(matTrainingImagesAsFlattenedFloats, cv::ml::ROW_SAMPLE, matClassificationInts);

    return 0;
}

// ------------------------------------------------------------------------------------------------------------------------------

std::string frame_decoder(cv::Mat &imgOriginalScene, args_t args, std::vector<sweep_t> *_sweep, frame_dec_t &res_opt) {

    char buffer[100];
    std::vector<sweep_t> sweep;
    std::string result = "N/A";
    std::map<std::string,unsigned int> scoreboard_winners;
    std::vector<PossiblePlate> listOfPossiblePlates, listOfPossibleChars;
            
    // Generate an LPR detection object:
    LPR_wrapper *lpr = new LPR_wrapper(args);

    // Perform LPR detection algo:
    if (!imgOriginalScene.empty()) {

        // Crop the ROI from the image:
        uint_x4_t* ROI = new uint_x4_t(-1, -1);
        int W[3] = { 20, 60, 20 };
        int H[3] = { 40, 50, 10 };
        bool autoRoiMode = ROI_adjust(lpr->get_ROI(), imgOriginalScene, W, H, ROI);  // autoROI
        cv::Mat imgCropped = crop_roi_from_image(imgOriginalScene, *ROI, autoRoiMode);
        
        // Image enhancement:
        cv::Mat imgEnhanced = imgCropped.clone();
        if (args.imgEnhancementMode != IMG_ENHANCEMENT_MODE_DISABLED) {
          imgEnhanced = imageEnhancement(imgCropped, 2, uint_xy_t(8,8), 3, args.imgEnhancementMode, args.debugMode); 
        }

        // Zoom-In:
        if (args.PreprocessZoomIn != 1) {
          sprintf(buffer, "Digital zoom-in (ROI): x%.2f",args.PreprocessZoomIn);
          debug(buffer);
          cv::resize(imgEnhanced, imgEnhanced, cv::Size(), args.PreprocessZoomIn, args.PreprocessZoomIn, cv::INTER_CUBIC);
        }

        // Perspective Transform:
        if (!((args.pWarpPnt0.get_x() == args.pWarpPnt1.get_x()) && (args.pWarpPnt0.get_y() == args.pWarpPnt1.get_y()))) {
          imgEnhanced = perspectiveWarp(imgEnhanced, args.pWarpPnt0, args.pWarpPnt1, args.pWarpPnt2, args.pWarpPnt3);
        }

        // Tesseract override:
        if (args.confidence_thr >= 1) {
            res_opt.engine_type = true;
            return fallback_decode(imgOriginalScene, args.debugMode);
        }

        // OpMode auto-mode (check for a police vehicle):
        if (lpr->get_OpMode() == "auto") {
            cv::Mat PoliceTemplate = load_input_scene_image(lpr->get_PoliceTemplate(), "PoliceTemplate", "", 0, "", "");
            lpr->set_OpMode(imgEnhanced, PoliceTemplate, "police", lpr->get_PoliceTemplateThr());
        }

        // Sweep:
        if (_sweep) {
          sweep = *_sweep;
        } 
        else {
          sweep.push_back(sweep_st(args.PreprocessThreshweight, args.PreprocessThreshweight, 1));
          sweep.push_back(sweep_st(args.PreprocessThreshBlockSize, args.PreprocessThreshBlockSize, 1));
        } 

        // Seek for plates, then for characters, from Max to Min number of digits (greedy):
        unsigned int A = lpr->get_MinNumberOfMatchingChars();
        unsigned int B = lpr->get_MaxNumberOfMatchingChars();

        unsigned int sweep_space = 0;
        unsigned int scoreboard_max = 0;
        
        for (unsigned int thr_weight=sweep[SWEEP_THR_WEIGHT].from; thr_weight<=sweep[SWEEP_THR_WEIGHT].to; thr_weight+=sweep[SWEEP_THR_WEIGHT].step) {

            for (unsigned int thr_blk_size=sweep[SWEEP_THR_BLK_SIZE].from; thr_blk_size<=sweep[SWEEP_THR_BLK_SIZE].to; thr_blk_size+=sweep[SWEEP_THR_BLK_SIZE].step) {

                lpr->set_thr_weight(thr_weight);
                lpr->set_thr_blk_size(thr_blk_size);

                for (unsigned int numOfMatchingChar=B; numOfMatchingChar>=A; numOfMatchingChar--) {

                    if (args.debugMode) {
                        sprintf(buffer, "------ W=%lu, BS=%lu, #Chars=%lu", thr_weight, thr_blk_size, numOfMatchingChar);
                        debug(buffer);
                    }

                    lpr->set_MinNumberOfMatchingChars(numOfMatchingChar);
                    lpr->set_MaxNumberOfMatchingChars(numOfMatchingChar);

                    // Plates detection (within the given image):
                    listOfPossiblePlates = lpr->detect_plates_in_scene(imgEnhanced);

                    // Characters detection (within the pre-detected plate):
                    listOfPossibleChars = lpr->detect_characters_in_plate(listOfPossiblePlates);

                    if ((listOfPossiblePlates.size() > 0) && ((listOfPossibleChars.front().strChars.length() > 0))) {

                      // Report the analysis result:
                      std::string out_file = "imgNA";
                      if (args.ImageFile == "onvif") {
                          out_file = "onvif_out.png";
                      } else {
                          #if defined(WIN32) || defined(_WIN32) || defined(__WIN32) && !defined(__CYGWIN__)
                          std::size_t found1 = args.ImageFile.rfind("\");
                          #else
                          std::size_t found1 = args.ImageFile.rfind("/");
                          #endif
                          if (found1 != std::string::npos) {
                              out_file = args.ImageFile.substr(found1+1);
                              std::size_t found2 = out_file.rfind(".");
                              if (found2 != std::string::npos) {
                                  out_file.replace(found2,1,"_out.");
                              }
                          }
                      }

                      bool sweep_mode = !(_sweep == NULL);
                      result = lpr->report_result(imgOriginalScene.clone(), *ROI, listOfPossibleChars, out_file, sweep_mode);

                      if ((result != "N/A") && (result.length() >= A)) {
                          unsigned int pts = ((result.length() > A) && (result.length() <= B)) ? 10 : 1;   // main course gets higher weight
                          if (scoreboard_winners.find(result) == scoreboard_winners.end()) {
                            scoreboard_winners[result] = pts;
                          }
                          else {
                            scoreboard_winners[result] += pts;
                          }
                          if (scoreboard_winners[result] > scoreboard_max) {
                            res_opt.imgOut = listOfPossiblePlates.front().imgPlate.clone();
                            scoreboard_max = scoreboard_winners[result]; 
                          }
                          sweep_space += pts;
                          break;
                      }
                    }
                }

                sweep_space++;
            }
        }
   
        unsigned int maxVal = 0;
        unsigned int maxVal2 = 0;
        for (auto it = scoreboard_winners.begin(); it != scoreboard_winners.end(); ++it) {
            std::cout << it->first << " --> " << it->second << std::endl;
            if (it->second > maxVal) {
              maxVal2 = maxVal;
              maxVal = it->second;
              result = it->first;
            }
        }

        double confidence = (maxVal - maxVal2) / double(sweep_space);
        res_opt.confidence = confidence;
        
        // Tesseact engine (fallback):
        if (confidence < args.confidence_thr) {
            std::string fallback_res = fallback_decode(imgOriginalScene, args.debugMode);
            result = fallback_res;
            res_opt.engine_type = true;
        }
    }

    return result;
}

// ------------------------------------------------------------------------------------------------------------------------------

std::string fallback_decode(cv::Mat &img, bool debugMode=false) {

    // Tesseract is hereby used as a fallback, in case of a low confidence.
    // Ref:  https://opensource.google.com/projects/tesseract
    // Installation:
    //    Linux:  
    //      % sudo apt install tesseract-ocr
    //      % sudo apt install libtesseract-dev
    //    OSX:
    //      % brew install tesseract

    std::string result("N/A");
    
    // Tesseact engine (fallback):
    tesseract::TessBaseAPI tess;
    tess.Init(NULL, "eng");
    tess.SetPageSegMode(tesseract::PSM_SPARSE_TEXT);
    tess.SetImage((uchar*)img.data, img.size().width, img.size().height, img.channels(), img.step1());
    tess.Recognize(0);
    const char *out = tess.GetUTF8Text();
    std::string result_raw(out);

    // Post-processing:
    result_raw.erase(std::remove(result_raw.begin(), result_raw.end(), '\n'), result_raw.end());
    const std::string s(result_raw);
    std::regex rgx1(".*P\\s*late.*:(.*)");
    std::regex rgx2(".*P\\s*late.*o(.*)");
    std::smatch match1, match2;
    if (std::regex_search(s.begin(), s.end(), match1, rgx1)) {
      result = match1[1];
    } 
    else if (std::regex_search(s.begin(), s.end(), match2, rgx2)) {
      result = match2[1];
    }

    // Manual fixes:
    result = std::regex_replace( result, std::regex("‘1"), "4");
    std::replace( result.begin(), result.end(), '?', '7');
    std::replace( result.begin(), result.end(), 'B', '8');
    std::replace( result.begin(), result.end(), 'S', '5');
    std::replace( result.begin(), result.end(), 'I', '1');
    std::replace( result.begin(), result.end(), 'O', '0');
    std::replace( result.begin(), result.end(), 'Z', '2');
    std::replace( result.begin(), result.end(), 'Q', '4');

    // Epilog:
    tess.End();
    delete [] out;

    if (debugMode) {
        char buffer[100];
        sprintf(buffer, "Fallback (raw): %s", result_raw.c_str());
        debug(buffer);
    }
    
    return result;
}

