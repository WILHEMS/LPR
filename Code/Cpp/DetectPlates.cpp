// DetectPlates.cpp
//  _     _                           ____  _       _         ____                            _ _   _
// | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
// | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
// | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
// |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
//                                                                                |___/
// (c) Shahar Gino, July-2017, sgino209@gmail.com

#include "DetectPlates.hpp"

// ------------------------------------------------------------------------------------------------------------------------------
std::vector<PossiblePlate> detectPlatesInScene(cv::Mat &imgOriginalScene, plate_params_t plate_params) {
    
    cv::RNG rng;
    cv::Mat imgThreshScene;
    cv::Mat imgGrayscaleScene;
    std::vector<PossiblePlate> vectorOfPossiblePlates;
    char buffer[100];

    // Pre-processing (CSC --> contrast --> blur --> threshold):
    preprocess(imgOriginalScene,
               imgGrayscaleScene,
               imgThreshScene,
               plate_params.PreprocessGaussKernel,
               plate_params.PreprocessThreshBlockSize,
               plate_params.PreprocessThreshweight,
               plate_params.PreprocessMorphKernel,
               plate_params.OpMode, "platesDet");

    // Find all possible characters in the scene (finds all contours that could be characters, w/o OCR yet):
    std::vector<PossibleChar> vectorOfPossibleCharsInScene = findPossibleCharsInImage(imgThreshScene,
                                                                                      plate_params.MinPixelWidth,  plate_params.MaxPixelWidth,
                                                                                      plate_params.MinPixelHeight, plate_params.MaxPixelHeight,
                                                                                      plate_params.MinAspectRatio, plate_params.MaxAspectRatio,
                                                                                      plate_params.MinPixelArea,   plate_params.MaxPixelArea,
                                                                                      plate_params.debugMode);
    
    // Given a list of all possible chars, find groups of matching characters (later on, each group will attempt to be recognized as a plate):
    std::vector<std::vector<PossibleChar> > vectorOfVectorsOfMatchingCharsInScene = findVectorOfVectorsOfMatchingChars(vectorOfPossibleCharsInScene,
                                                                                                                       plate_params.MinNumberOfMatchingChars,
                                                                                                                       plate_params.MaxNumberOfMatchingChars,
                                                                                                                       plate_params.MinAngleBetweenChars,
                                                                                                                       plate_params.MaxAngleBetweenChars,
                                                                                                                       plate_params.MinChangeInArea,
                                                                                                                       plate_params.MaxChangeInArea,
                                                                                                                       plate_params.MinChangeInWidth,
                                                                                                                       plate_params.MaxChangeInWidth,
                                                                                                                       plate_params.MinChangeInHeight,
                                                                                                                       plate_params.MaxChangeInHeight,
                                                                                                                       plate_params.MaxDiagSizeMultipleAway);
    
    // For each group of matching chars, attempt to extract plate:
    for (auto &vectorOfMatchingChars : vectorOfVectorsOfMatchingCharsInScene) {
        
        PossiblePlate possiblePlate = extractPlate(imgOriginalScene,
                                                   vectorOfMatchingChars,
                                                   plate_params.PlateWidthPaddingFactor,
                                                   plate_params.PlateHeightPaddingFactor);
        
        // Add plate to list of possible plates (if found):
        if (!possiblePlate.imgPlate.empty()) {

            // Verify that the plate has enough saturation:
            cv::Mat imgHSV, imgS;
            std::vector<cv::Mat> vectorOfBGRImages, vectorOfHSVImages;
            cv::cvtColor(possiblePlate.imgPlate, imgHSV, CV_BGR2HSV);
            cv::split(imgHSV, vectorOfHSVImages);
            imgS = vectorOfHSVImages[1];
            int N = imgS.total();
            int histSize = 256;
            float range[] = { 0, 256 };
            const float* histRange = { range };
            cv::MatND s_hist;
            cv::calcHist( &imgS, 1, 0, cv::Mat(), s_hist, 1, &histSize, &histRange, true, false );
            float hist_norm = 0;
            for( int h = 0; h < histSize; h++ ) { 
                hist_norm += h * s_hist.at<float>(h)/N; 
            }

            if (hist_norm > plate_params.MinHistNormThr) {
                vectorOfPossiblePlates.push_back(possiblePlate);
            } 
            else if (plate_params.debugMode) {

                char buffer[100];
                sprintf(buffer, "Plates rejected: HistNorm=%.2f", hist_norm);
                debug(buffer);
            }
        }
    }
    
    // Add rectangle plate candidate:
    if (plate_params.FindRectangledPlate) {
    
        PossiblePlate possiblePlate = findRectangledPlate(imgOriginalScene,
                                                          imgThreshScene,
                                                          0.45,   // circularity_min
                                                          0.65,   // circularity_max
                                                          3.5,    // aspect_ratio_min
                                                          4.4,    // aspect_ratio_max
                                                          0.005,  // area_norm_min
                                                          0.03,   // area_norm_max
                                                          plate_params.debugMode);
    
        if (!possiblePlate.imgPlate.empty()) {
            possiblePlate.rectFind = true;
            vectorOfPossiblePlates.push_back(possiblePlate);
        }
    }

    if (plate_params.debugMode) {
      sprintf(buffer, "%lu possible plates found", vectorOfPossiblePlates.size());
      debug(buffer);
    }

    // -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
    if (plate_params.debugMode) {
    
        // Original image:
        cv::imwrite("img_original.jpg", imgOriginalScene);
        
        // Pre-processing images:
        cv::imwrite("img_gray.jpg",      imgGrayscaleScene);
        cv::imwrite("img_threshold.jpg", imgThreshScene);
        
        // Possible characters in image:
        cv::Mat imgContours(imgOriginalScene.size(), CV_8UC3, SCALAR_BLACK);
        std::vector<std::vector<cv::Point> > contours;
        
        for (auto &possibleChar : vectorOfPossibleCharsInScene) {
            contours.push_back(possibleChar.contour);
        }
        cv::drawContours(imgContours, contours, -1, SCALAR_WHITE);
        cv::imwrite("img_contours_possible_chars.jpg", imgContours);
        
        // Matching characters:
        sprintf(buffer, "#listOfListsOfMatchingCharsInScene = %lu", vectorOfVectorsOfMatchingCharsInScene.size());
        debug(buffer);
        
        imgContours = cv::Mat(imgOriginalScene.size(), CV_8UC3, SCALAR_BLACK);
        
        for (auto &vectorOfMatchingChars : vectorOfVectorsOfMatchingCharsInScene) {
            int intRandomBlue = rng.uniform(0, 256);
            int intRandomGreen = rng.uniform(0, 256);
            int intRandomRed = rng.uniform(0, 256);
            
            std::vector<std::vector<cv::Point> > contours;
            
            sprintf(buffer, "#listOfMatchingChars = %lu", vectorOfMatchingChars.size());
            debug(buffer);
            for (auto &matchingChar : vectorOfMatchingChars) {
                contours.push_back(matchingChar.contour);
            }
            cv::drawContours(imgContours, contours, -1, cv::Scalar((double)intRandomBlue, (double)intRandomGreen, (double)intRandomRed));
        }
        cv::imwrite("img_contours_matching_chars.jpg", imgContours);
        
        // Possible license-plates:
        for (unsigned int i = 0; i < vectorOfPossiblePlates.size(); i++) {
            cv::Point2f p2fRectPoints[4];
            
            vectorOfPossiblePlates[i].rrLocationOfPlateInScene.points(p2fRectPoints);
            
            for (int j = 0; j < 4; j++) {
                const cv::Scalar color = vectorOfPossiblePlates[i].rectFind ? SCALAR_GREEN : SCALAR_RED;
                cv::line(imgContours, p2fRectPoints[j], p2fRectPoints[(j + 1) % 4], color, 2);
            }
            char buffer [50];
            sprintf (buffer, "img_contours_possible_plates_%d.jpg", i);
            cv::imwrite(buffer, imgContours);
            sprintf (buffer, "img_plate_%d.jpg", i);
            cv::imwrite(buffer, vectorOfPossiblePlates[i].imgPlate);
        }
        
        debug("Plate detection complete");
    }

    return vectorOfPossiblePlates;
}

// ------------------------------------------------------------------------------------------------------------------------------
PossiblePlate extractPlate(cv::Mat &imgOriginal, std::vector<PossibleChar> &vectorOfMatchingChars, double PlateWidthPaddingFactor, double PlateHeightPaddingFactor) {
    
    PossiblePlate possiblePlate;

    // Sort characters from left to right based on x position:
    std::sort(vectorOfMatchingChars.begin(), vectorOfMatchingChars.end(), PossibleChar::sortCharsLeftToRight);

    // Calculate the plate centroid (average of leftmost and righhtmost characters):
    double dblPlateCenterX = (double)(vectorOfMatchingChars[0].intCenterX + vectorOfMatchingChars[vectorOfMatchingChars.size() - 1].intCenterX) / 2.0;
    double dblPlateCenterY = (double)(vectorOfMatchingChars[0].intCenterY + vectorOfMatchingChars[vectorOfMatchingChars.size() - 1].intCenterY) / 2.0;
    cv::Point2d p2dPlateCenter(dblPlateCenterX, dblPlateCenterY);

    // Calculate plate width (rightmost - leftmost characters):
    int intPlateWidth = (int)(PlateWidthPaddingFactor * (vectorOfMatchingChars[vectorOfMatchingChars.size() - 1].boundingRect.x +
                                                         vectorOfMatchingChars[vectorOfMatchingChars.size() - 1].boundingRect.width -
                                                         vectorOfMatchingChars[0].boundingRect.x));

    // Calculate plate height (average over all characters):
    double intTotalOfCharHeights = 0;
    for (auto &matchingChar : vectorOfMatchingChars) {
        intTotalOfCharHeights = intTotalOfCharHeights + matchingChar.boundingRect.height;
    }
    double dblAverageCharHeight = (double)intTotalOfCharHeights / vectorOfMatchingChars.size();
    int intPlateHeight = (int)(dblAverageCharHeight * PlateHeightPaddingFactor);

    // Calculate correction angle of plate region (simple geometry calculation):
    double dblOpposite = vectorOfMatchingChars[vectorOfMatchingChars.size() - 1].intCenterY - vectorOfMatchingChars[0].intCenterY;
    double dblHypotenuse = distanceBetweenChars(vectorOfMatchingChars[0], vectorOfMatchingChars[vectorOfMatchingChars.size() - 1]);
    double dblCorrectionAngleInRad = asin(dblOpposite / dblHypotenuse);
    double dblCorrectionAngleInDeg = dblCorrectionAngleInRad * (180.0 / CV_PI);

    // Rotate the entire image (affine warp), for compensating the angle of the plate region:
    cv::Mat imgRotated;
    cv::Mat rotationMatrix;
    rotationMatrix = cv::getRotationMatrix2D(p2dPlateCenter, dblCorrectionAngleInDeg, 1.0);
    cv::warpAffine(imgOriginal, imgRotated, rotationMatrix, imgOriginal.size());

    // Crop the plate from the image:
    cv::Mat imgCropped;
    possiblePlate.rrLocationOfPlateInScene = cv::RotatedRect(p2dPlateCenter, cv::Size2f((float)intPlateWidth, (float)intPlateHeight), (float)dblCorrectionAngleInDeg);
    cv::getRectSubPix(imgRotated, possiblePlate.rrLocationOfPlateInScene.size, possiblePlate.rrLocationOfPlateInScene.center, imgCropped);

    // Create and return possiblePlate object, which packs most the above information:
    possiblePlate.imgPlate = imgCropped;

    return(possiblePlate);
}

// ------------------------------------------------------------------------------------------------------------------------------
PossiblePlate findRectangledPlate(cv::Mat &imgOriginalScene, cv::Mat &imgThresh, double circularity_min, double circularity_max,
                                  double aspect_ratio_min, double aspect_ratio_max, double area_norm_min, double area_norm_max, bool debugMode) {
    
    // Initialization:
    cv::Rect res_box;
    int rect_cntr = 0;
    int max_rect_area = 0;
    double res_area_norm = 0;
    double res_circularity = 0;
    double res_aspect_ratio = 0;
    PossiblePlate possiblePlate;
    cv::Point2d p2dPlateCenter(0,0);
    
    // Find contours:
    std::vector<std::vector<cv::Point> > contours;
    cv::findContours(imgThresh.clone(), contours, CV_RETR_LIST, CV_CHAIN_APPROX_NONE);

    // For each contour:
    for (std::vector<cv::Point>& contour : contours) {
        
        // Compute convex hull:
        std::vector<cv::Point> hull;
        convexHull(contour, hull);
        
        // Compute circularity, used for shape classification:
        double area = contourArea(hull);
        double area_norm = contourArea(hull) / imgThresh.size().area();
        double perimeter = arcLength(hull, true);
        double circularity = (4 * CV_PI * area) / (perimeter * perimeter);
        
        // Shape classification (rectangle):
        if ((circularity > circularity_min) && (circularity < circularity_max) && (area > max_rect_area)) {
        
            cv::Rect box = boundingRect(contour);
            double aspect_ratio = (double)box.width / box.height;
            
            if ((aspect_ratio > aspect_ratio_min) && (aspect_ratio < aspect_ratio_max) &&
                (area_norm > area_norm_min) && (area_norm < area_norm_max)) {
                
                // Registration:
                res_box = box;
                max_rect_area = area;
                res_area_norm = area_norm;
                res_aspect_ratio = aspect_ratio;
                res_circularity = circularity;

                for ( size_t i=0; i<contour.size(); i++ )
                {
                    p2dPlateCenter.x += contour[i].x;
                    p2dPlateCenter.y += contour[i].y;
                }
                p2dPlateCenter.x /= contour.size();
                p2dPlateCenter.y /= contour.size();
                
                rect_cntr++;
            }
        }
    }
    
    if (rect_cntr > 0) {

        // Crop the plate from the image:
        cv::Mat imgCropped;
        possiblePlate.rrLocationOfPlateInScene = cv::RotatedRect(p2dPlateCenter, cv::Size2f((float)res_box.width, (float)res_box.height), 0);
        cv::getRectSubPix(imgOriginalScene, possiblePlate.rrLocationOfPlateInScene.size, possiblePlate.rrLocationOfPlateInScene.center, imgCropped);
        possiblePlate.imgPlate = imgCropped;
        
        // -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
        if (debugMode) {
            
            char buffer[200];
            sprintf(buffer, "rect #%d: box.w=%d, box.h=%d, AR=%.4f, area=%.4f, circ=%.4f",
                    rect_cntr-1, res_box.width, res_box.height, res_aspect_ratio, res_area_norm, res_circularity);
            debug(buffer);
        }
    }
    
    return possiblePlate;
}
