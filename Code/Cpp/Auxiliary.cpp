// Auxiliary.cpp
//  _     _                           ____  _       _         ____                            _ _   _
// | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
// | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
// | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
// |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
//                                                                                |___/
// (c) Shahar Gino, July-2017, sgino209@gmail.com

#include "Auxiliary.hpp"

// ------------------------------------------------------------------------------------------------------------------------------
void generic_message(std::string message, std::string severity) {
    
    char buffer[100];
    sprintf(buffer, "%s: %s", severity.c_str(), message.c_str());
    
    std::cout << buffer << std::endl;
}

void info(std::string message)  { generic_message(message, "INFO");  }
void debug(std::string message) { generic_message(message, "DEBUG"); }
void error(std::string message) { generic_message(message, "ERROR"); }

// ------------------------------------------------------------------------------------------------------------------------------
void drawRedRectangleAroundPlate(cv::Mat &imgOriginalScene, PossiblePlate &licPlate) {
    
    cv::Point2f p2fRectPoints[4];
    
    // Get 4 vertices of rotated rectangle:
    licPlate.rrLocationOfPlateInScene.points(p2fRectPoints);
    
    // Draw 4 red lines:
    for (int i = 0; i < 4; i++) {
        cv::line(imgOriginalScene, p2fRectPoints[i], p2fRectPoints[(i + 1) % 4], SCALAR_RED, 2);
    }
}

// ------------------------------------------------------------------------------------------------------------------------------
void writeLicensePlateCharsOnImage(cv::Mat &imgOriginalScene, PossiblePlate &licPlate) {
    
    // Retrieve basic geometric metrics:
    cv::Point ptCenterOfTextArea;         // the center of the area the text will be written to
    cv::Point ptLowerLeftTextOrigin;      // the bottom left of the area that the text will be written to
    
    // Font styling (type, scale, thickness):
    int intFontFace = CV_FONT_HERSHEY_SIMPLEX;
    double dblFontScale = (double)licPlate.imgPlate.rows / 30.0;
    int intFontThickness = (int)round(dblFontScale * 1.5);
    int intBaseline = 0;
    cv::Size textSize = cv::getTextSize(licPlate.strChars, intFontFace, dblFontScale, intFontThickness, &intBaseline);
    
    // The horizontal location of the text area is the same as the plate:
    ptCenterOfTextArea.x = (int)licPlate.rrLocationOfPlateInScene.center.x;
    
    // The vertical location of the test area depends on the license-plate location in the scene image::
    if (licPlate.rrLocationOfPlateInScene.center.y < (imgOriginalScene.rows * 0.75)) {
        ptCenterOfTextArea.y = (int)round(licPlate.rrLocationOfPlateInScene.center.y) + (int)round((double)licPlate.imgPlate.rows * 1.6);  // chars below the plate
    }
    else {
        ptCenterOfTextArea.y = (int)round(licPlate.rrLocationOfPlateInScene.center.y) - (int)round((double)licPlate.imgPlate.rows * 1.6);  // chars above the plate
    }
    
    // Calculate the lower left origin of the text area based on the text area center, width, and height:
    ptLowerLeftTextOrigin.x = (int)(ptCenterOfTextArea.x - (textSize.width / 2));
    ptLowerLeftTextOrigin.y = (int)(ptCenterOfTextArea.y + (textSize.height / 2));
    
    // Write the text on the image:
    cv::putText(imgOriginalScene, licPlate.strChars, ptLowerLeftTextOrigin, intFontFace, dblFontScale, SCALAR_YELLOW, intFontThickness);
}

// ------------------------------------------------------------------------------------------------------------------------------
bool ROI_adjust(uint_x4_t ROI, cv::Mat &imgOriginalScene, int* W, int* H, uint_x4_t *adjROI) {
    
    cv::Size s = imgOriginalScene.size();
    int imgH = s.height;
    int imgW = s.width;
    bool autoRoiMode = false;
    
    if ((ROI.get_len() == 2) && (ROI.get_x1() == -1) && (ROI.get_x2() == -1)) {
        
        (*adjROI).set(int(imgW * W[0]/100.0), 1);
        (*adjROI).set(int(imgH * H[0]/100.0), 2);
        (*adjROI).set(int(imgW * W[1]/100.0), 3);
        (*adjROI).set(int(imgH * H[1]/100.0), 4);
        
        autoRoiMode = true;
        
        if (((W[0]+W[1]+W[2]) != 100) || ((H[0]+H[1]+H[2]) != 100)) {
            error("Invalid autoROI settings, doesnt converge to 100 percent");
        }
    }
    
    else if ((ROI.get_len() == 2) && (ROI.get_x1() == 0) && (ROI.get_x2() == 0)) {
        
        (*adjROI).set(0, 1);
        (*adjROI).set(0, 2);
        (*adjROI).set(imgW, 3);
        (*adjROI).set(imgH, 4);
    }
    
    else {
        *adjROI = ROI;
    }
    
    return autoRoiMode;
}

// ------------------------------------------------------------------------------------------------------------------------------
cv::Mat crop_roi_from_image(cv::Mat &imgOriginalScene, uint_x4_t ROI, bool autoRoiMode) {
    
    int imgW;
    int imgH;
    unsigned int roiW;
    unsigned int roiH;
    char buffer[100];
    
    if (ROI.get_x3() == -1 || ROI.get_x4() == -1) {
        
        cv::Size s = imgOriginalScene.size();
        imgH = s.height;
        imgW = s.width;
        roiW = imgW;
        roiH = imgH;
    }
    else {
        
        roiW = ROI.get_x3();
        roiH = ROI.get_x4();
    }
    
    double roiCx = ROI.get_x1() + roiW / 2.0;
    double roiCy = ROI.get_x2() + roiH / 2.0;
    
    cv::Mat imgCropped;
    cv::getRectSubPix(imgOriginalScene, cv::Size2f((float)roiW, (float)roiH), cv::Point2f((float)roiCx, (float)roiCy), imgCropped);
    
    sprintf(buffer, "ROI size: (Cx,Cy)=(%.2f,%.2f), WxH=%dx%d, autoROI=%d", roiCx, roiCy, roiW, roiH, int(autoRoiMode));
    info(buffer);
    
    return imgCropped;
}

// ------------------------------------------------------------------------------------------------------------------------------
cv::Mat load_input_scene_image(std::string imageFile, std::string ImType,
                               std::string onvif_ip, unsigned int onvif_port, std::string onvif_user, std::string onvif_passwd) {
    
    cv::Mat imgOriginalScene;
    char buffer[100];
    
    if (imageFile == "onvif") {
        onvif_camera mycam = onvif_camera(onvif_ip, onvif_port, onvif_user, onvif_passwd);
        imgOriginalScene = mycam.snaphot_capture();
    } else {
        imgOriginalScene = cv::imread(imageFile);
    }
    
    if (imgOriginalScene.empty()) {
        sprintf(buffer, "%s not read from file", ImType.c_str());
        error(buffer);
        #if defined(WIN32) || defined(_WIN32) || defined(__WIN32) && !defined(__CYGWIN__)
        _getch();
        #else
        wgetch(stdscr);
        #endif
    }
    
    cv::Size s = imgOriginalScene.size();
    int imgH = s.height;
    int imgW = s.width;
    sprintf(buffer, "%s size: WxH=%dx%d", ImType.c_str(), imgW, imgH);
    info(buffer);
    
    return imgOriginalScene;
}

// ------------------------------------------------------------------------------------------------------------------------------
bool isTemplateFound(cv::Mat &imgOriginal, cv::Mat &imgTemplate, std::string template_name, double_xy_t template_thr, double_xy_t *templateLoc, bool debugMode) {

    cv::RNG rng;
    bool is_found = false;
    char buffer[100];
    double minVal, maxVal;
    int result_cols, result_rows, tH=0, tW=0, startX, startY, endX, endY;
    cv::Point minLoc, maxLoc;
    cv::Mat gray, edged_gray, template_gray, result, edged_template;
    
    // Convert original image to gray, and move to edge representation (boot + more accurate TM):
    cv::cvtColor(imgOriginal, gray, CV_BGR2GRAY);
    Canny(gray, edged_gray, 50, 200);
    cv::Mat clone;
    cv::cvtColor(edged_gray, clone, CV_GRAY2RGB);

    // Convert template to gray:
    cv::cvtColor(imgTemplate, template_gray, CV_BGR2GRAY);

    // Loop over the scales of the template:
    double found[5] = {0, 0, 0, 0, 0};
    std::vector<double> scales = linspace(0.15, 1.0, 20);
    std::vector<double>::reverse_iterator scale = scales.rbegin();
    for (; scale!= scales.rend(); ++scale) {

        // Resize the template according to the scale, and keep track of the ratio of the resizing:
        
        cv::Mat template_gray_cloned = template_gray.clone();
        cv::Mat resized;
        cv::resize(template_gray_cloned, resized, cv::Size(), *scale, *scale);
        tH = resized.rows;
        tW = resized.cols;
        
        // Detect edges in the resized template, and apply template matching to find it in the edged image:
        Canny(resized, edged_template, 50, 200);
        result_cols =  edged_gray.cols - edged_template.cols + 1;
        result_rows = edged_gray.rows - edged_template.rows + 1;
        result.create( result_rows, result_cols, CV_32FC1 );
        cv::matchTemplate(edged_gray, edged_template, result, cv::TM_CCORR_NORMED);
        minMaxLoc( result, &minVal, &maxVal, &minLoc, &maxLoc, cv::Mat() );

        // Check to see if the iteration should be visualized:
        if (debugMode) {

            // Draw a bounding box around the detected region
            int intRandomBlue = rng.uniform(0, 256);
            int intRandomGreen = rng.uniform(0, 256);
            int intRandomRed = rng.uniform(0, 256);
            cv::Scalar randColor = cv::Scalar((double)intRandomBlue, (double)intRandomGreen, (double)intRandomRed);
            sprintf(buffer, "maxVal=%.2f", maxVal);
            cv::putText(clone, buffer, cv::Point(maxLoc.x, maxLoc.y-20), cv::FONT_HERSHEY_SIMPLEX, 1, randColor, 2);
            cv::rectangle(clone, cv::Rect(maxLoc.x, maxLoc.y, tW, tH), randColor, 2);
            sprintf(buffer, "maxVal=%.3f, tH=%d, tW=%d", maxVal, tH, tW);
            debug(buffer);
        }

        // If we have found a new maximum correlation value, then update the book-keeping variable:
        if (maxVal > found[0]) {
            found[0] = maxVal;
            found[1] = maxLoc.x;
            found[2] = maxLoc.y;
            found[3] = tH;
            found[4] = tW;
        }
    }
    
    if (debugMode) {
        sprintf(buffer, "TemplateMatching_%s.jpg", template_name.c_str());
        cv::imwrite(buffer, clone);
    }
    
    if (templateLoc && (found[0] == 0)) {

        *templateLoc = double_xy_t(0, 0);
    }
    
    else {

        // Unpack the book-keeping varaible and compute the (x, y) coordinates of the bounding box based on the resized ratio:
        maxVal = found[0];
        maxLoc = cv::Point(found[1],found[2]);
        tH = int(found[3]);
        tW = int(found[4]);
        startX = int(maxLoc.x);
        startY = int(maxLoc.y);
        endX = int((maxLoc.x + tW));
        endY = int((maxLoc.y + tH));
        
        cv::Mat imgCropped;
        cv::getRectSubPix(imgOriginal, cv::Size2f((float)tW, (float)tH), cv::Point2f((float)(maxLoc.x+tW/2), (float)(maxLoc.y+tH/2)), imgCropped);
        cv::Scalar tempVal = mean(imgCropped);
        double avg_color = (tempVal.val[0] + tempVal.val[1] + tempVal.val[2]) / 3;

        // draw a bounding box around the detected result and display the image
        is_found = (maxVal >= template_thr.get_x()) && (avg_color > template_thr.get_y());

        if (is_found) {

            sprintf(buffer, "%s vehicle detected! (val1=%.2f, val2=%.2f)", template_name.c_str(), found[0], avg_color);
            info(buffer);

            if (debugMode) {

                cv::Mat imgOriginalCopy = imgOriginal.clone();
                cv::rectangle(imgOriginalCopy, cv::Rect(startX, startY, endX-startX, endY-startY), SCALAR_GREEN, 2);
                sprintf(buffer, "maxVal=%.2f, avgRed=%.2f", maxVal, avg_color);
                cv::putText(imgOriginalCopy, buffer, cv::Point(10,30), cv::FONT_HERSHEY_SIMPLEX, 1, SCALAR_GREEN, 2);
                sprintf(buffer, "img_%s_symbol.jpg", template_name.c_str());
                cv::imwrite(buffer, imgOriginalCopy);
            }
        }
    }

    if (templateLoc) {
        *templateLoc = double_xy_t(maxLoc.x+tW/2, maxLoc.y+tH/2);
    }
    
    return is_found;
}

// ------------------------------------------------------------------------------------------------------------------------------
std::vector<double> linspace(double min, double max, int n)
{
    std::vector<double> result;
    // vector iterator
    int iterator = 0;
    
    for (int i = 0; i <= n-2; i++)
    {
        double temp = min + i*(max-min)/(floor((double)n) - 1);
        result.insert(result.begin() + iterator, temp);
        iterator += 1;
    }
    
    result.insert(result.begin() + iterator, max);
    return result;
}

// ------------------------------------------------------------------------------------------------------------------------------
bool is_digits(const std::string &str)
{
    return str.find_first_not_of("0123456789") == std::string::npos;
}

// ------------------------------------------------------------------------------------------------------------------------------
double sample_image(cv::Mat &imgGray, uint_x4_t sampleRect, unsigned int maxVal) {
    
    unsigned int y0 = sampleRect.get_x1();
    unsigned int x0 = sampleRect.get_x2();
    unsigned int w  = sampleRect.get_x3();
    unsigned int h  = sampleRect.get_x4();
    
    unsigned int sampleSum = 0;
    for (unsigned int y=0; y<h; y++) {
        for (unsigned int x=0; x<w; x++) {
            sampleSum += imgGray.at<unsigned char>(y0+y, x0+x);
        }
    }
    
    double sample = double(sampleSum) / (w * h * maxVal);
    
    return sample;
}
