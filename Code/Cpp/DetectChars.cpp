// DetectChars.cpp
//  _     _                           ____  _       _         ____                            _ _   _
// | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
// | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
// | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
// |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
//                                                                                |___/
// (c) Shahar Gino, July-2017, sgino209@gmail.com

#include "DetectChars.hpp"

// ------------------------------------------------------------------------------------------------------------------------------
std::vector<PossiblePlate> detectCharsInPlates(std::vector<PossiblePlate> &vectorOfPossiblePlates, char_params_t char_params) {

    cv::RNG rng;
    cv::Mat imgContours;
    char buffer[100];
    unsigned int intPlateCounter;
    std::vector<PossibleChar> longestVectorOfMatchingCharsInPlate;
    
    // Early break condition (empty input):
    if (vectorOfPossiblePlates.empty()) {
        return(vectorOfPossiblePlates);
    }

    // For each possible plate --> preprocess, find all characters, try to group them, remove overlaps and perform OCR:
    intPlateCounter = 0;
    for (auto &possiblePlate : vectorOfPossiblePlates) {
        
        // Pre-processing (CSC --> contrast --> blur --> threshold):
        preprocess(possiblePlate.imgPlate, possiblePlate.imgGrayscale, possiblePlate.imgThresh,
                   char_params.PreprocessGaussKernel, char_params.PreprocessThreshBlockSize,
                   char_params.PreprocessThreshweight, char_params.PreprocessMorphKernel, char_params.OpMode, "charsDet");
        
        // Increase size of plate image for easier viewing and char detection:
        cv::resize(possiblePlate.imgThresh, possiblePlate.imgThresh, cv::Size(), 1.6, 1.6);
        
        // Threshold again to eliminate any gray areas:
        cv::threshold(possiblePlate.imgThresh, possiblePlate.imgThresh, 0.0, 255.0, CV_THRESH_BINARY | CV_THRESH_OTSU);
        
        // Perform Opening again to eliminate characters that touch border:
        cv::Mat kernel = cv::Mat::ones(3, 3, CV_8U);
        morphologyEx(possiblePlate.imgThresh.clone(), possiblePlate.imgThresh, cv::MORPH_OPEN, kernel);
        
        // Find all possible chars in the plate (finds all contours that could be chars):
        std::vector<PossibleChar> vectorOfPossibleCharsInPlate = findPossibleCharsInImage(possiblePlate.imgThresh,
                                                                                          char_params.MinPixelWidth, char_params.MaxPixelWidth,
                                                                                          char_params.MinPixelHeight, char_params.MaxPixelHeight,
                                                                                          char_params.MinAspectRatio, char_params.MaxAspectRatio,
                                                                                          char_params.MinPixelArea, char_params.MaxPixelArea,
                                                                                          char_params.debugMode);
        
        // Remove possibleChars that are "too blue" (filters garbage from the Israeli symbol):
        if (!(char_params.OpMode=="police")) {
          RemoveTooBlueChars(vectorOfPossibleCharsInPlate, possiblePlate.imgPlate, char_params.blueMaxThrH, char_params.blueMinThrS, char_params.debugMode); 
        }

        // Given a list of all possible chars, find groups of matching chars within the plate:
        std::vector<std::vector<PossibleChar> > vectorOfVectorsOfMatchingCharsInPlate = findVectorOfVectorsOfMatchingChars(vectorOfPossibleCharsInPlate,
                                                                                                                           char_params.MinNumberOfMatchingChars,
                                                                                                                           char_params.MaxNumberOfMatchingChars,
                                                                                                                           char_params.MinAngleBetweenChars,
                                                                                                                           char_params.MaxAngleBetweenChars,
                                                                                                                           char_params.MinChangeInArea,
                                                                                                                           char_params.MaxChangeInArea,
                                                                                                                           char_params.MinChangeInWidth,
                                                                                                                           char_params.MaxChangeInWidth,
                                                                                                                           char_params.MinChangeInHeight,
                                                                                                                           char_params.MaxChangeInHeight,
                                                                                                                           char_params.MaxDiagSizeMultipleAway);
        
        // If groups of matching chars were found in the plate:
        if (vectorOfVectorsOfMatchingCharsInPlate.size() > 0) {
        
            // Within each list of matching chars, sort chars from left to right and remove inner overlapping chars:
            for (auto &vectorOfMatchingChars : vectorOfVectorsOfMatchingCharsInPlate) {
            
                std::sort(vectorOfMatchingChars.begin(), vectorOfMatchingChars.end(), PossibleChar::sortCharsLeftToRight);
                vectorOfMatchingChars = removeInnerOverlappingChars(vectorOfMatchingChars, char_params.MinDiagSizeMultipleAway);
            }

            // Within each possible plate, loop through all the vectors of matching chars, get the index of the one with the most chars:
            unsigned long intLenOfLongestVectorOfChars = 0;
            unsigned int intIndexOfLongestVectorOfChars = 0;
            for (unsigned int i = 0; i < vectorOfVectorsOfMatchingCharsInPlate.size(); i++) {
                if (vectorOfVectorsOfMatchingCharsInPlate[i].size() > intLenOfLongestVectorOfChars) {
                    intLenOfLongestVectorOfChars = vectorOfVectorsOfMatchingCharsInPlate[i].size();
                    intIndexOfLongestVectorOfChars = i;
                }
            }
            
            // Suppose that the longest list of matching chars within the plate is the actual list of chars:
            longestVectorOfMatchingCharsInPlate = vectorOfVectorsOfMatchingCharsInPlate[intIndexOfLongestVectorOfChars];
            
            // Characters Vertical alignment:
            bool vertical_align_check_pass = true;
            if (char_params.NoVerticalAlign) {
                vertical_align_check_pass = charactersVerticalAlignCheck(longestVectorOfMatchingCharsInPlate,
                                                                         3.5, 
                                                                         char_params.MaxChangeInHeight,
                                                                         char_params.debugMode);
            }
            else {
                charactersVerticalAlign(longestVectorOfMatchingCharsInPlate, 0.05, 0.1, char_params.debugMode);
            }
           
            // Characters recognition (OCR):
            if (vertical_align_check_pass) {

                possiblePlate.strChars = recognizeCharsInPlate(possiblePlate.imgThresh,
                                                               longestVectorOfMatchingCharsInPlate,
                                                               char_params.ResizedCharImageWidth,
                                                               char_params.ResizedCharImageHeight,
                                                               char_params.kNearest,
                                                               char_params.kFactorKNN,
                                                               char_params.NoOcrKnnFixes,
                                                               intPlateCounter,
                                                               char_params.debugMode);
                
                if (!char_params.NoOcrTextualFixes) {
                    possiblePlate.strChars = OcrTextualCorrections(possiblePlate.strChars,
                                                                   char_params.OpMode,
                                                                   char_params.NoOcrDigitsOnly,
                                                                   char_params.debugMode);
                }
                
                if (!char_params.NoOcrDigitsOnly && !is_digits(possiblePlate.strChars) && !(char_params.OpMode=="police")) {
                    if (char_params.debugMode) {      
                      sprintf(buffer, "Deleting invalid OCR result (%s), since it not digits only", possiblePlate.strChars.c_str());
                      debug(buffer);
                    }
                    possiblePlate.strChars = "";
                }
            }
        }
        
        // -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
        if (char_params.debugMode) {
            
            char buffer [100];
            cv::Mat imgContours1;
            cv::Mat imgContours2;
            cv::Mat imgContours3;
            cv::Mat imgContours4;
            std::vector<std::vector<cv::Point> > contours;
            
            auto matsize = possiblePlate.imgThresh.size();
            imgContours1 = cv::Mat(matsize, CV_8UC3, SCALAR_BLACK);
            imgContours2 = cv::Mat(matsize, CV_8UC3, SCALAR_BLACK);
            imgContours3 = cv::Mat(matsize, CV_8UC3, SCALAR_BLACK);
            imgContours4 = cv::Mat(matsize, CV_8UC3, SCALAR_BLACK);
            
            sprintf(buffer, "#listOfPossibleCharsInPlate = %lu", vectorOfPossibleCharsInPlate.size());
            debug(buffer);

            contours.clear();
            for (auto &possibleChar : vectorOfPossibleCharsInPlate) {
                contours.push_back(possibleChar.contour);
            }
            cv::drawContours(imgContours1, contours, -1, SCALAR_WHITE);
            
            sprintf(buffer, "#listOfListsOfMatchingCharsInPlate = %lu", vectorOfVectorsOfMatchingCharsInPlate.size());
            debug(buffer);

            if (vectorOfVectorsOfMatchingCharsInPlate.size() > 0) {

                contours.clear();
                for (auto &vectorOfMatchingChars : vectorOfVectorsOfMatchingCharsInPlate) {
                    int intRandomBlue = rng.uniform(0, 256);
                    int intRandomGreen = rng.uniform(0, 256);
                    int intRandomRed = rng.uniform(0, 256);
                    for (auto &matchingChar : vectorOfMatchingChars) {
                        contours.push_back(matchingChar.contour);
                    }
                    cv::drawContours(imgContours2, contours, -1, cv::Scalar((double)intRandomBlue, (double)intRandomGreen, (double)intRandomRed));
                }
                
                for (auto &vectorOfMatchingChars : vectorOfVectorsOfMatchingCharsInPlate) {
                    int intRandomBlue = rng.uniform(0, 256);
                    int intRandomGreen = rng.uniform(0, 256);
                    int intRandomRed = rng.uniform(0, 256);
                    contours.clear();
                    for (auto &matchingChar : vectorOfMatchingChars) {
                        contours.push_back(matchingChar.contour);
                    }
                    cv::drawContours(imgContours3, contours, -1, cv::Scalar((double)intRandomBlue, (double)intRandomGreen, (double)intRandomRed));
                }
                
                contours.clear();
                for (auto &matchingChar : longestVectorOfMatchingCharsInPlate) {
                    contours.push_back(matchingChar.contour);
                }
                cv::drawContours(imgContours4, contours, -1, SCALAR_WHITE);
            }
            
            sprintf (buffer, "img_possible_plate_%d.jpg", intPlateCounter);
            cv::imwrite(buffer, possiblePlate.imgPlate);
            
            sprintf (buffer, "img_possible_plate_gray_%d.jpg", intPlateCounter);
            cv::imwrite(buffer, possiblePlate.imgGrayscale);
            
            sprintf (buffer, "img_possible_plate_threshold_%d.jpg", intPlateCounter);
            cv::imwrite(buffer, possiblePlate.imgThresh);

            sprintf (buffer, "img_possible_plate_contours1_%d.jpg", intPlateCounter);
            cv::imwrite(buffer, imgContours1);
            
            if (vectorOfVectorsOfMatchingCharsInPlate.size() > 0) {
            
                sprintf (buffer, "img_possible_plate_contours2_%d.jpg", intPlateCounter);
                cv::imwrite(buffer, imgContours2);

                sprintf (buffer, "img_possible_plate_contours3_%d.jpg", intPlateCounter);
                cv::imwrite(buffer, imgContours3);
                
                sprintf (buffer, "img_possible_plate_contours4_%d.jpg", intPlateCounter);
                cv::imwrite(buffer, imgContours4);
            }
            
            if (vectorOfVectorsOfMatchingCharsInPlate.size() > 0) {
                sprintf(buffer, "Characters found in plate number #%d = %s", intPlateCounter, possiblePlate.strChars.c_str());
                debug(buffer);
                intPlateCounter++;
            }
            else {
                sprintf(buffer, "Characters found in plate number #%d = (none)", intPlateCounter);
                debug(buffer);
            }
        }
        
        // -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
        // If no groups of matching chars were found in the plate, continue for next plate candidate:
        if (vectorOfVectorsOfMatchingCharsInPlate.size() == 0) {
            
            possiblePlate.strChars = "";
            continue;
        }
    }
    
    if (char_params.debugMode) {
        debug("Characters detection complete");
    }

    return(vectorOfPossiblePlates);
}

// ------------------------------------------------------------------------------------------------------------------------------
std::vector<PossibleChar> findPossibleCharsInImage(cv::Mat &imgBinary, unsigned int MinPixelWidth, unsigned int MaxPixelWidth,
                                                   unsigned int MinPixelHeight, unsigned int MaxPixelHeight, double MinAspectRatio,
                                                   double MaxAspectRatio, unsigned int MinPixelArea, unsigned int MaxPixelArea, bool debugMode) {
    
    // Initialization:
    std::vector<PossibleChar> vectorOfPossibleChars;
    cv::Mat imgBinaryCopy = imgBinary.clone();
    
    // Find all contours in the image:
    std::vector<std::vector<cv::Point> > contours;
    cv::findContours(imgBinaryCopy, contours, CV_RETR_LIST, CV_CHAIN_APPROX_SIMPLE);

    // Foreach contour, check if it describes a possible character:
    cv::Mat clone;
    cv::cvtColor(imgBinaryCopy, clone, CV_GRAY2RGB);
    cv::Mat imgContours = cv::Mat::zeros(clone.size(), CV_8UC3);
    int intCountOfPossibleChars = 0;
    for (unsigned int i = 0; i < contours.size(); i++) {
        
        // Register the contour as a possible character (+calculate intrinsic metrics):
        PossibleChar possibleChar(contours[i],
                                  MinPixelWidth, MaxPixelWidth,
                                  MinPixelHeight, MaxPixelHeight,
                                  MinAspectRatio, MaxAspectRatio,
                                  MinPixelArea, MaxPixelArea);

        // If contour is a possible char, increment count of possible chars and add to list of possible chars:
        if (possibleChar.checkIfPossibleChar()) {
            intCountOfPossibleChars++;
            vectorOfPossibleChars.push_back(possibleChar);
        }
        
        if (debugMode) {
            cv::drawContours(imgContours, contours, i, SCALAR_WHITE);
        }
    }
    
    // -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
    if (debugMode) {
        
        char buffer[100];
        sprintf(buffer, "Amount of detected contours: %lu", contours.size());
        debug(buffer);
        sprintf(buffer, "Amount of possible characters: %d", intCountOfPossibleChars);
        debug(buffer);
        cv::imwrite("img_contours_all.jpg", imgContours);
    }

    return(vectorOfPossibleChars);
}

// ------------------------------------------------------------------------------------------------------------------------------
std::vector<std::vector<PossibleChar> > findVectorOfVectorsOfMatchingChars(const std::vector<PossibleChar> &vectorOfPossibleChars,
                                                                           unsigned int MinNumberOfMatchingChars, unsigned int MaxNumberOfMatchingChars,
                                                                           double MinAngleBetweenChars, double MaxAngleBetweenChars,
                                                                           double MinChangeInArea, double MaxChangeInArea,
                                                                           double MinChangeInWidth, double MaxChangeInWidth,
                                                                           double MinChangeInHeight, double MaxChangeInHeight,
                                                                           double MaxDiagSizeMultipleAway) {

    std::vector<std::vector<PossibleChar> > vectorOfVectorsOfMatchingChars;

    // For each possible character in the one big list of characters, do:
    for (auto &possibleChar : vectorOfPossibleChars) {

        // Find all characters in the big list that match the current character (+ add the current character):
        std::vector<PossibleChar> vectorOfMatchingChars = findVectorOfMatchingChars(possibleChar, vectorOfPossibleChars,
                                                                                    MaxDiagSizeMultipleAway,
                                                                                    MinAngleBetweenChars, MaxAngleBetweenChars,
                                                                                    MinChangeInArea, MaxChangeInArea,
                                                                                    MinChangeInWidth, MaxChangeInWidth,
                                                                                    MinChangeInHeight, MaxChangeInHeight);
        
        vectorOfMatchingChars.push_back(possibleChar);

        // If current list not too short and not too long, then it may be a valid plate candidate:
        if (vectorOfMatchingChars.size() >= MinNumberOfMatchingChars &&
            vectorOfMatchingChars.size() <= MaxNumberOfMatchingChars) {

            // Add the cluster of characters to the list of lists of matching characters:
            vectorOfVectorsOfMatchingChars.push_back(vectorOfMatchingChars);

            // Remove the current list of matching characters from the big list, for not using same characters twice:
            std::vector<PossibleChar> vectorOfPossibleCharsWithCurrentMatchesRemoved;
            for (auto &possChar : vectorOfPossibleChars) {
                if (std::find(vectorOfMatchingChars.begin(), vectorOfMatchingChars.end(), possChar) == vectorOfMatchingChars.end()) {
                    vectorOfPossibleCharsWithCurrentMatchesRemoved.push_back(possChar);
                }
            }

            // Recursive call (+ declare a new vector of vectors of chars to get result from recursive call):
            std::vector<std::vector<PossibleChar> > recursiveVectorOfVectorsOfMatchingChars;
            recursiveVectorOfVectorsOfMatchingChars = findVectorOfVectorsOfMatchingChars(vectorOfPossibleCharsWithCurrentMatchesRemoved,
                                                                                         MinNumberOfMatchingChars, MaxNumberOfMatchingChars,
                                                                                         MinAngleBetweenChars, MaxAngleBetweenChars,
                                                                                         MinChangeInArea, MaxChangeInArea,
                                                                                         MinChangeInWidth, MaxChangeInWidth,
                                                                                         MinChangeInHeight, MaxChangeInHeight,
                                                                                         MaxDiagSizeMultipleAway);

            // For each list of matching characters found by recursive call, add to the list of lists of matching chars:
            for (auto &recursiveVectorOfMatchingChars : recursiveVectorOfVectorsOfMatchingChars) {
                vectorOfVectorsOfMatchingChars.push_back(recursiveVectorOfMatchingChars);
            }

            break;
        }
    }

    return(vectorOfVectorsOfMatchingChars);
}

// ------------------------------------------------------------------------------------------------------------------------------
std::vector<PossibleChar> findVectorOfMatchingChars(const PossibleChar &possibleChar, const std::vector<PossibleChar> &vectorOfChars, double MaxDiagSizeMultipleAway,
                                                    double MinAngleBetweenChars, double MaxAngleBetweenChars, double MinChangeInArea, double MaxChangeInArea,
                                                    double MinChangeInWidth, double MaxChangeInWidth, double MinChangeInHeight, double MaxChangeInHeight) {
    
    std::vector<PossibleChar> vectorOfMatchingChars;

    // For each character in big list, do:
    for (auto &possibleMatchingChar : vectorOfChars) {

        // Bypass self matches, to avoid double insertions of current char:
        if (possibleMatchingChar == possibleChar) {
            
            continue;
        }
        
        // Compute intrinsic metrics for characters match-up:
        double dblDistanceBetweenChars = distanceBetweenChars(possibleChar, possibleMatchingChar);
        double dblAngleBetweenChars = angleBetweenChars(possibleChar, possibleMatchingChar);
        double dblChangeInArea = (double)abs(possibleMatchingChar.boundingRect.area() - possibleChar.boundingRect.area()) / (double)possibleChar.boundingRect.area();
        double dblChangeInWidth = (double)abs(possibleMatchingChar.boundingRect.width - possibleChar.boundingRect.width) / (double)possibleChar.boundingRect.width;
        double dblChangeInHeight = (double)abs(possibleMatchingChar.boundingRect.height - possibleChar.boundingRect.height) / (double)possibleChar.boundingRect.height;

        // Check if characters match, and add the current character to list of matching characters if so:
        if (dblDistanceBetweenChars < (possibleChar.dblDiagonalSize * MaxDiagSizeMultipleAway) &&
            dblAngleBetweenChars >= MinAngleBetweenChars &&
            dblAngleBetweenChars < MaxAngleBetweenChars &&
            dblChangeInArea >= MinChangeInArea &&
            dblChangeInArea < MaxChangeInArea &&
            dblChangeInWidth >= MinChangeInWidth &&
            dblChangeInWidth < MaxChangeInWidth &&
            dblChangeInHeight >= MinChangeInHeight &&
            dblChangeInHeight < MaxChangeInHeight) {
            
            vectorOfMatchingChars.push_back(possibleMatchingChar);
        }
    }

    return(vectorOfMatchingChars);
}

// ------------------------------------------------------------------------------------------------------------------------------
double distanceBetweenChars(const PossibleChar &firstChar, const PossibleChar &secondChar) {
    
    int intX = abs(firstChar.intCenterX - secondChar.intCenterX);
    int intY = abs(firstChar.intCenterY - secondChar.intCenterY);

    return(sqrt(pow(intX, 2) + pow(intY, 2)));
}

// ------------------------------------------------------------------------------------------------------------------------------
double angleBetweenChars(const PossibleChar &firstChar, const PossibleChar &secondChar) {
    
    double dblAdj = abs(firstChar.intCenterX - secondChar.intCenterX);
    double dblOpp = abs(firstChar.intCenterY - secondChar.intCenterY);

    double dblAngleInRad = atan(dblOpp / dblAdj);

    // Calculate angle in degrees:
    double dblAngleInDeg = dblAngleInRad * (180.0 / CV_PI);

    return(dblAngleInDeg);
}

// ------------------------------------------------------------------------------------------------------------------------------
std::vector<PossibleChar> removeInnerOverlappingChars(std::vector<PossibleChar> &vectorOfMatchingChars, double MinDiagSizeMultipleAway) {
    std::vector<PossibleChar> vectorOfMatchingCharsWithInnerCharRemoved(vectorOfMatchingChars);

    for (auto &currentChar : vectorOfMatchingChars) {
        for (auto &otherChar : vectorOfMatchingChars) {
            
            // If current char and other char are not the same character:
            if (currentChar != otherChar) {

                // If current character and other character have center points at almost the same location:
                if (distanceBetweenChars(currentChar, otherChar) < (currentChar.dblDiagonalSize * MinDiagSizeMultipleAway)) {

                    // Overlapping characters handling: identify which character is smaller and remove it (if not already removed on a previous pass)
                    if (currentChar.boundingRect.area() < otherChar.boundingRect.area()) {
                      
                        std::vector<PossibleChar>::iterator currentCharIterator = std::find(vectorOfMatchingCharsWithInnerCharRemoved.begin(), vectorOfMatchingCharsWithInnerCharRemoved.end(), currentChar);
                      
                        if (currentCharIterator != vectorOfMatchingCharsWithInnerCharRemoved.end()) {
                            vectorOfMatchingCharsWithInnerCharRemoved.erase(currentCharIterator);
                        }
                    }
                    else {

                        std::vector<PossibleChar>::iterator otherCharIterator = std::find(vectorOfMatchingCharsWithInnerCharRemoved.begin(), vectorOfMatchingCharsWithInnerCharRemoved.end(), otherChar);

                        if (otherCharIterator != vectorOfMatchingCharsWithInnerCharRemoved.end()) {
                            vectorOfMatchingCharsWithInnerCharRemoved.erase(otherCharIterator);
                        }
                    }
                }
            }
        }
    }

    return(vectorOfMatchingCharsWithInnerCharRemoved);
}

// ------------------------------------------------------------------------------------------------------------------------------
std::string recognizeCharsInPlate(cv::Mat &imgThresh, std::vector<PossibleChar> &vectorOfMatchingChars, unsigned int ResizedCharImageWidth,
                                  unsigned int ResizedCharImageHeight, cv::Ptr<cv::ml::KNearest> kNearest, unsigned int intkFactorKNN,
                                  bool NoOcrKnnFixes, unsigned int intPlateCounter, bool debugMode) {
    
    std::string strChars;
    cv::Mat imgThreshColor;

    // Sort characters from left to right:
    std::sort(vectorOfMatchingChars.begin(), vectorOfMatchingChars.end(), PossibleChar::sortCharsLeftToRight);

    // Make Color Version of Threshold image, for drawing contours in color on it:
    cv::cvtColor(imgThresh, imgThreshColor, CV_GRAY2BGR);

    // For each character in the plate
    for (auto &currentChar : vectorOfMatchingChars) {
        
        // Draw a green box around the character:
        cv::rectangle(imgThreshColor, currentChar.boundingRect, SCALAR_GREEN, 2);

        // Crop the characters out of threshold image:
        cv::Mat imgROItoBeCloned = imgThresh(currentChar.boundingRect);
        
        // Resize the image (necessary for later OCR):
        cv::Mat imgROI = imgROItoBeCloned.clone();
        cv::Mat imgROIResized;
        cv::resize(imgROI, imgROIResized, cv::Size(ResizedCharImageWidth, ResizedCharImageHeight));

        // Convert Mat to float, necessary for call to findNearest, and flatten Matrix into one row:
        cv::Mat matROIFloat;
        imgROIResized.convertTo(matROIFloat, CV_32FC1);
        cv::Mat matROIFlattenedFloat = matROIFloat.reshape(1, 1);

        // OCR, by calling findNearest (KNN):
        cv::Mat matCurrentChar(0, 0, CV_32F);
        kNearest->findNearest(matROIFlattenedFloat, intkFactorKNN, matCurrentChar);
        float fltCurrentChar = (float)matCurrentChar.at<float>(0, 0);
        char npaResultAscii = char(int(fltCurrentChar));
        
        // KNN fix, 6-->5:
        if (!NoOcrKnnFixes) {
            npaResultAscii = OcrKnnCorrections(npaResultAscii, imgROIResized, currentChar.dblAspectRatio, debugMode);
        }
        
        // Get character from results (+convert from Mat to double), and append it to the full string:
        std::string strCurrentChar(&npaResultAscii);
        strChars = strChars + strCurrentChar;
    }

    // -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
    if (debugMode) {
        
        char buffer [100];
        sprintf (buffer, "img_ocr_result_%d.jpg", intPlateCounter);
        cv::imwrite(buffer, imgThreshColor);
    }

    return(strChars);
}

// ------------------------------------------------------------------------------------------------------------------------------
std::string OcrTextualCorrections(std::string strChars, std::string mode, bool NoOcrDigitsOnly, bool debugMode) {
    
    char buffer[100];
    std::string strCharsFinal(strChars);
    std::size_t found = 0;

    if (mode == "police") {
        std::string strCharsPre(strCharsFinal);
        strCharsFinal.pop_back();
        strCharsFinal += "@";
        if (debugMode) {
          sprintf(buffer, "Textual OCR change (police): %s --> %s", strCharsPre.c_str(), strCharsFinal.c_str());
          debug(buffer);
        }
    }

    if (!NoOcrDigitsOnly) {
        found = strCharsFinal.find('A');
        if (found != std::string::npos) {
            std::string strCharsPre(strCharsFinal);
            std::replace(strCharsFinal.begin(), strCharsFinal.end(), 'A', '4');
            if (debugMode) {
                sprintf(buffer, "Textual OCR change: %s --> %s", strCharsPre.c_str(), strCharsFinal.c_str());
                debug(buffer);
            }
        }

        found = strCharsFinal.find('B');
        if (found != std::string::npos) {
            std::string strCharsPre(strCharsFinal);
            std::replace(strCharsFinal.begin(), strCharsFinal.end(), 'B', '8');
            if (debugMode) {
                sprintf(buffer, "Textual OCR change: %s --> %s", strCharsPre.c_str(), strCharsFinal.c_str());
                debug(buffer);
            }
        }

        found = strCharsFinal.find('Z');
        if (found != std::string::npos) {
            std::string strCharsPre(strCharsFinal);
            std::replace(strCharsFinal.begin(), strCharsFinal.end(), 'Z', '4');
            if (debugMode) {
                sprintf(buffer, "Textual OCR change: %s --> %s", strCharsPre.c_str(), strCharsFinal.c_str());
                debug(buffer);
            }
        }
        
        found = strCharsFinal.find('I');
        if (found != std::string::npos) {
            std::string strCharsPre(strCharsFinal);
            std::replace(strCharsFinal.begin(), strCharsFinal.end(), 'I', '1');
            if (debugMode) {
                sprintf(buffer, "Textual OCR change: %s --> %s", strCharsPre.c_str(), strCharsFinal.c_str());
                debug(buffer);
            }
        }
        
        found = strCharsFinal.find('L');
        if (found != std::string::npos) {
            std::string strCharsPre(strCharsFinal);
            std::replace(strCharsFinal.begin(), strCharsFinal.end(), 'L', '1');
            if (debugMode) {
                sprintf(buffer, "Textual OCR change: %s --> %s", strCharsPre.c_str(), strCharsFinal.c_str());
                debug(buffer);
            }
        }

        found = strCharsFinal.find('J');
        if (found != std::string::npos) {
            std::string strCharsPre(strCharsFinal);
            std::replace(strCharsFinal.begin(), strCharsFinal.end(), 'J', '3');
            if (debugMode) {
                sprintf(buffer, "Textual OCR change: %s --> %s", strCharsPre.c_str(), strCharsFinal.c_str());
                debug(buffer);
            }
        }
    }

    return strCharsFinal;
}

// ------------------------------------------------------------------------------------------------------------------------------
char OcrKnnCorrections(char npaResultAscii, cv::Mat npaROIResized, double charAspectRatio, bool debugMode) {

    char buffer[100];
    char npaResultAsciiFinal = npaResultAscii;
    unsigned int imgH = npaROIResized.rows;
    unsigned int imgW = npaROIResized.cols;
    
    //if (debugMode) {
    //    print_character(npaROIResized);
    //    sprintf(buffer, "npaResultAscii=%s\n",    npaResultAscii);   debug(buffer);
    //    sprintf(buffer, "charAspectRatio=%.2f\n", charAspectRatio);  debug(buffer);
    //}

    // -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    // '2' --> '7'/'1':
    if (npaResultAscii == '2') {
        
        double bottom_right_sum = sample_image(npaROIResized, uint_x4_t((unsigned int)(0.87 * imgH), imgW-4, 2, 4), 255);
       
        if ((charAspectRatio < 0.4) && (bottom_right_sum < 0.8)) {

            npaResultAsciiFinal = '1';
          
            if (debugMode) {
                sprintf(buffer, "KNN OCR fix (%.2f,%.2f): 2 --> 1", bottom_right_sum, charAspectRatio);
                debug(buffer);
            }
        }
        
        if (bottom_right_sum < 0.4) {
            
            npaResultAsciiFinal = '7';
            
            if (debugMode) {
                sprintf(buffer, "KNN OCR fix (%.2f,%.2f): 2 --> 7", bottom_right_sum, charAspectRatio);
                debug(buffer);
            }
        }
    }

    // -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    // '3' --> '6'/'1':
    if (npaResultAscii == '3') {
        
        double mid_left_sum = sample_image(npaROIResized, uint_x4_t((unsigned int)(0.47 * imgH), 0, 4, 2), 255);
        
        if (mid_left_sum > 0.5) {
            
            npaResultAsciiFinal = '6';
            
            if (debugMode) {
                sprintf(buffer, "KNN OCR fix (%.2f): 3 --> 6", mid_left_sum);
                debug(buffer);
            }
        }
        
        if (charAspectRatio < 0.4) {

            npaResultAsciiFinal = '1';
          
            if (debugMode) {
                sprintf(buffer, "KNN OCR fix (%.2f,%.2f): 3 --> 1", mid_left_sum, charAspectRatio);
                debug(buffer);
            }
        }
    }

    // -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    // '5'-->'6':
    else if (npaResultAscii == '5') {
        
        double top_left_sum = sample_image(npaROIResized, uint_x4_t(1, 0, 4, 2), 255);

        double mid_left_sum = sample_image(npaROIResized, uint_x4_t((unsigned int)(0.65 * imgH), 0, 4, 2), 255);
        
        if ((top_left_sum < 0.5) && (mid_left_sum > 0.1)) {
            
            npaResultAsciiFinal = '6';
        
            if (debugMode) {
                sprintf(buffer, "KNN OCR fix (%.2f,%.2f): 5 --> 6", top_left_sum, mid_left_sum);
                debug(buffer);
            }
        }
    }

    // -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    // '6'-->'8'/'5'/'4':
    else if (npaResultAscii == '6') {
        
        double top_right_sum = sample_image(npaROIResized, uint_x4_t((unsigned int)(0.35 * imgH), imgW-6, 4, 2), 255);
        
        double mid_left_sum = sample_image(npaROIResized, uint_x4_t((unsigned int)(0.65 * imgH), 0, 4, 2), 255);

        double bottom_left_sum = sample_image(npaROIResized, uint_x4_t(imgH-3, 5, 2, 4), 255);        
        
        if (top_right_sum > 0.5) {
            
            npaResultAsciiFinal = '8';
        
            if (debugMode) {
                sprintf(buffer, "KNN OCR fix (%.2f,%.2f,%.2f): 6 --> 8", top_right_sum, mid_left_sum, bottom_left_sum);
                debug(buffer);
            }
        }
        else if (mid_left_sum < 0.1) {
            
            npaResultAsciiFinal = '5';
        
            if (debugMode) {
                sprintf(buffer, "KNN OCR fix (%.2f,%.2f,%.2f): 6 --> 5", top_right_sum, mid_left_sum, bottom_left_sum);
                debug(buffer);
            }
        }
        else if (bottom_left_sum < 0.1) {
            
            npaResultAsciiFinal = '4';
        
            if (debugMode) {
                sprintf(buffer, "KNN OCR fix (%.2f,%.2f,%.2f): 6 --> 4", top_right_sum, mid_left_sum, bottom_left_sum);
                debug(buffer);
            }
        }
    }
    
    // -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    // '7' --> '1':
    else if (npaResultAscii == '7') {

        double bottom_left_sum = sample_image(npaROIResized, uint_x4_t((unsigned int)(0.85 * imgH), 0, 6, 2), 255);

        if ((bottom_left_sum < 0.25) && (charAspectRatio < 0.45)) {
            
            npaResultAsciiFinal = '1';
            
            if (debugMode) {
                sprintf(buffer, "KNN OCR fix (%.2f,%.2f): 7 --> 1", bottom_left_sum, charAspectRatio);
                debug(buffer);
            }
        }
    }
    
    // -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    // '8'-->'9'/'6'/'0':
    if (npaResultAscii == '8') {
        
        double bottom_left_sum = sample_image(npaROIResized, uint_x4_t((unsigned int)(0.6 * imgH), 0, 4, 2), 255);
        
        double top_right_sum = sample_image(npaROIResized, uint_x4_t((unsigned int)(0.35 * imgH), imgW-6, 4, 2), 255);
        
        double mid_sum = sample_image(npaROIResized, uint_x4_t((unsigned int)(0.45 * imgH), (unsigned int)(0.5 * imgW), 4, 2), 255);
       
        if (bottom_left_sum < 0.2) {
            
            npaResultAsciiFinal = '9';
            
            if (debugMode) {
                sprintf(buffer, "KNN OCR fix (%.2f): 8 --> 9", bottom_left_sum);
                debug(buffer);
            }
        }
        
        else if (top_right_sum < 0.2) {
            
            npaResultAsciiFinal = '6';
            
            if (debugMode) {
                sprintf(buffer, "KNN OCR fix (%.2f): 8 --> 6", top_right_sum);
                debug(buffer);
            }
        }
        
        else if (mid_sum < 0.2) {
            
            npaResultAsciiFinal = '0';
            
            if (debugMode) {
                sprintf(buffer, "KNN OCR fix (%.2f): 8 --> 0", mid_sum);
                debug(buffer);
            }
        }
    }
    
    // -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    // 'B'-->'0'/'5'/'6':
    else if (npaResultAscii == 'B') {
        
        double mid_sum = sample_image(npaROIResized, uint_x4_t((unsigned int)(0.5 * imgH), (unsigned int)(0.5 * imgW), 4, 2), 255);
        
        double bottom_left_sum = sample_image(npaROIResized, uint_x4_t((unsigned int)(0.6 * imgH), 0, 4, 2), 255);
        
        double top_right_sum = sample_image(npaROIResized, uint_x4_t((unsigned int)(0.35 * imgH), imgW-6, 4, 2), 255);
        
        if (top_right_sum < 0.2) {
            
            if (bottom_left_sum < 0.2) {

                npaResultAsciiFinal = '5';
                
                if (debugMode) {
                    sprintf(buffer, "KNN OCR fix (%.2f,%.2f): B --> 5", bottom_left_sum, top_right_sum);
                    debug(buffer);
                }
            }
            else {

                npaResultAsciiFinal = '6';
                
                if (debugMode) {
                    sprintf(buffer, "KNN OCR fix (%.2f,%.2f): B --> 6", bottom_left_sum, top_right_sum);
                    debug(buffer);
                }
            }
        }
        else if (mid_sum < 0.2) {
            
            npaResultAsciiFinal = '0';
            
            if (debugMode) {
                sprintf(buffer, "KNN OCR fix (%.2f): B --> 0", mid_sum);
                debug(buffer);
            }
        }
    }
   
    // -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    // 'J'-->'5':
    else if (npaResultAscii == 'J') {
       
        double top_left_sum = sample_image(npaROIResized, uint_x4_t((unsigned int)(0.2 * imgH), 1, 2, 4), 255);
        
        if (top_left_sum > 0.7) {
            
            npaResultAsciiFinal = '5';
            
            if (debugMode) {
                sprintf(buffer, "KNN OCR fix (%.2f): J --> 5", top_left_sum);
                debug(buffer);
            }
        }
    }

    // -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    // 'Z'-->'2':
    else if (npaResultAscii == 'Z') {
        
        double top_left_sum = sample_image(npaROIResized, uint_x4_t(1, 1, 2, 4), 255);
        
        if (top_left_sum > 0.4) {
            
            npaResultAsciiFinal = '2';
            
            if (debugMode) {
                sprintf(buffer, "KNN OCR fix (%.2f): Z --> 2", top_left_sum);
                debug(buffer);
            }
        }
    }

    return npaResultAsciiFinal;
}

// ------------------------------------------------------------------------------------------------------------------------------
bool charactersVerticalAlignCheck(std::vector<PossibleChar> vectorOfMatchingChars, double errY_thr, double errH_thr, bool debugMode) {

    bool res = true;
    char buffer[100];
    double medianY, medianH;
    double errY=0, errH=0;
    std::size_t size = vectorOfMatchingChars.size();
    std::vector<PossibleChar> vectorOfMatchingCharsCopy(vectorOfMatchingChars);
    
    std::sort(vectorOfMatchingCharsCopy.begin(), vectorOfMatchingCharsCopy.end(), PossibleChar::sortCharsTopToBottom);
    
    if (size % 2 == 0) {
        medianY = double((vectorOfMatchingCharsCopy[size/2-1].boundingRect.y + vectorOfMatchingCharsCopy[size/2].boundingRect.y)) / 2;
        medianH = double((vectorOfMatchingCharsCopy[size/2-1].boundingRect.height + vectorOfMatchingCharsCopy[size/2].boundingRect.height)) / 2;
    } else {
        medianY = double(vectorOfMatchingCharsCopy[size/2].boundingRect.y);
        medianH = double(vectorOfMatchingCharsCopy[size/2].boundingRect.height);
    }
    
    for (auto &matchingChar : vectorOfMatchingChars) {
        errY += (std::abs(matchingChar.boundingRect.y - medianY) / medianY);
        errH += (std::abs(matchingChar.boundingRect.height - medianH) / medianH);
    }
    if (errY > errY_thr and errH > errH_thr) {    
      res = false;
      info("charactersVerticalAlignCheck failed!");
    }
    if (debugMode) {
        sprintf(buffer, "(errY, errH) = (%.2f,%.2f)", errY, errH);
        debug(buffer);
    }
    return res;
}

// ------------------------------------------------------------------------------------------------------------------------------
void charactersVerticalAlign(std::vector<PossibleChar> &vectorOfMatchingChars, double errY_thr, double errH_thr, bool debugMode) {

    char buffer[100];
    double medianY, medianH;
    std::size_t size = vectorOfMatchingChars.size();
    std::vector<PossibleChar> vectorOfMatchingCharsCopy(vectorOfMatchingChars);
    
    std::sort(vectorOfMatchingCharsCopy.begin(), vectorOfMatchingCharsCopy.end(), PossibleChar::sortCharsTopToBottom);
    
    if (size % 2 == 0) {
        medianY = double((vectorOfMatchingCharsCopy[size/2-1].boundingRect.y + vectorOfMatchingCharsCopy[size/2].boundingRect.y)) / 2;
        medianH = double((vectorOfMatchingCharsCopy[size/2-1].boundingRect.height + vectorOfMatchingCharsCopy[size/2].boundingRect.height)) / 2;
    } else {
        medianY = double(vectorOfMatchingCharsCopy[size/2].boundingRect.y);
        medianH = double(vectorOfMatchingCharsCopy[size/2].boundingRect.height);
    }
    
    for (auto &matchingChar : vectorOfMatchingChars) {
        
        double errY = std::abs(matchingChar.boundingRect.y - medianY) / medianY;
        double errH = std::abs(matchingChar.boundingRect.height - medianH) / medianH;
        
        if (errY > errY_thr and errH > errH_thr) {
            
            if (debugMode) {
                sprintf(buffer, "Vertical fix --> (y,w): (%d,%d)-->(%d,%d)",
                        matchingChar.boundingRect.y, matchingChar.boundingRect.height, (int)medianY, (int)medianH);
                debug(buffer);
            }
            
            matchingChar.boundingRect = cv::Rect(matchingChar.boundingRect.x,
                                                 (int)medianY,
                                                 matchingChar.boundingRect.width,
                                                 (int)medianH);;
            
            matchingChar.intCenterY = (matchingChar.boundingRect.y + matchingChar.boundingRect.y + matchingChar.boundingRect.height) / 2;
            
            matchingChar.dblDiagonalSize = sqrt(pow(matchingChar.boundingRect.width, 2) + pow(matchingChar.boundingRect.height, 2));
            
            matchingChar.dblAspectRatio = (float)matchingChar.boundingRect.width / (float)matchingChar.boundingRect.height;
        }
    }
}

// ------------------------------------------------------------------------------------------------------------------------------
// Remove possibleChars that are "too blue" (probably part of the Israeli symbol):
void RemoveTooBlueChars(std::vector<PossibleChar> &vectorOfPossibleChars, const cv::Mat &imgPlate, double blueMaxThrH, double blueMinThrS, bool debugMode)
{
    cv::Mat imgHSV; 
    cv::cvtColor(imgPlate, imgHSV, CV_BGR2HSV);
    std::vector<cv::Mat> vectorOfHSVImages;       
    cv::resize(imgHSV, imgHSV, cv::Size(), 1.6, 1.6);
    cv::split(imgHSV, vectorOfHSVImages);
    std::vector<std::vector<cv::Point> > contours;
    std::vector<PossibleChar>::iterator toBeRemoved;
    bool isToBeRemoved = false;
    double toBeRemovedH = 0.0; 
    double toBeRemovedS = 0.0; 
    for (auto it = vectorOfPossibleChars.begin(); it != vectorOfPossibleChars.end(); it++) {
        auto possibleChar = (*it);
        cv::Mat mask = cv::Mat::zeros(vectorOfHSVImages[0].size(), CV_8UC1);
        contours.clear();
        contours.push_back(possibleChar.contour);
        cv::drawContours(mask, contours, -1, SCALAR_WHITE, CV_FILLED);
        cv::Scalar tempValH = cv::mean(vectorOfHSVImages[0], mask);
        cv::Scalar tempValS = cv::mean(vectorOfHSVImages[1], mask);
        double myMAtMeanH = tempValH.val[0];
        double myMAtMeanS = tempValS.val[0];
        if ((myMAtMeanH > blueMaxThrH) && (myMAtMeanS < blueMinThrS)) {
          toBeRemoved = it;
          toBeRemovedH = myMAtMeanH;
          toBeRemovedS = myMAtMeanS;
          isToBeRemoved = true;
        }
        //std::cout << "### " << myMAtMeanH << "," << myMAtMeanS << std::endl; 
        //cv::imshow("xxx",mask);
        //cv::waitKey(0);
    }
    if (isToBeRemoved) {
      if (debugMode) {
        char buffer[100];
        sprintf(buffer, "Possible char removed (too blue) --> (x,y,h,s)=(%d,%d,%.2f,%.2f)",  (*toBeRemoved).intCenterX,  (*toBeRemoved).intCenterY, toBeRemovedH, toBeRemovedS);
        debug(buffer);
      }
      vectorOfPossibleChars.erase(toBeRemoved);
    }
}

// ------------------------------------------------------------------------------------------------------------------------------
void print_character(cv::Mat &imgGray) {
    
    unsigned int imgH = imgGray.rows;
    unsigned int imgW = imgGray.cols;
    
    for (int k1=0; k1<imgH; k1++) {
        for (int k2=0; k2<imgW; k2++) {
            printf("%3d,",imgGray.at<unsigned char>(k1, k2));
        }
        printf("\n");
    }
    std::cout << "--------------------------------------------------------------------------" << std::endl;
}

