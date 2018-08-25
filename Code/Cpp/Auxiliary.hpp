// Auxiliary.hpp
//  _     _                           ____  _       _         ____                            _ _   _
// | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
// | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
// | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
// |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
//                                                                                |___/
// (c) Shahar Gino, July-2017, sgino209@gmail.com

#ifndef AUXILIARY_H
#define AUXILIARY_H

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
#include <unistd.h>
#if defined(WIN32) || defined(_WIN32) || defined(__WIN32) && !defined(__CYGWIN__)
#include <conio.h>
#else
#include <curses.h>
#endif
#include "PossiblePlate.hpp"
#include "onvif_capture.hpp"

// ----------------------------------- Types, globals and definitions -----------------------------------------------------------

const cv::Scalar SCALAR_BLACK = cv::Scalar(0.0, 0.0, 0.0);
const cv::Scalar SCALAR_WHITE = cv::Scalar(255.0, 255.0, 255.0);
const cv::Scalar SCALAR_YELLOW = cv::Scalar(0.0, 255.0, 255.0);
const cv::Scalar SCALAR_GREEN = cv::Scalar(0.0, 255.0, 0.0);
const cv::Scalar SCALAR_RED = cv::Scalar(0.0, 0.0, 255.0);

typedef enum {
  IMG_ENHANCEMENT_MODE_DISABLED = 0,
  IMG_ENHANCEMENT_MODE_WARM_CLAHE_SAT_GAMMA,
  IMG_ENHANCEMENT_MODE_HIST_EQUALIZATION,
  IMG_ENHANCEMENT_MODE_MIXED0,
  IMG_ENHANCEMENT_MODE_MIXED1,
} imgEnhancement_mode_t; 


// -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. --

template <class _type>
class generic_xy_t {
    
    _type x;
    _type y;
    
public:
    generic_xy_t(_type x_, _type y_): x(x_), y(y_) {}
    
    std::string to_string()  { return "(" + std::to_string(x) + "," + std::to_string(y) + ")"; }
    
    void set_xy(char* s) {
        std::string str(s);
        std::size_t found1 = str.find("(");
        std::size_t found2 = str.find(",");
        std::size_t found3 = str.find(")");
        if ((found1 != std::string::npos) && (found2 != std::string::npos)) {
            std::string x_str = str.substr(found1+1, found2-found1-1);
            x = atoi(x_str.c_str());
        }
        if ((found2 != std::string::npos) && (found3 != std::string::npos)) {
            std::string y_str = str.substr(found2+1, found3-found2-1);
            y = atoi(y_str.c_str());
        }
    }
    
    _type get_x() { return x; }
    _type get_y() { return y; }
};

// --..--..--..--..--..--..--...--..--..--..--..--..--..--..--..--..--..--..--...--..--..--..--..--
class uint_xy_t : public generic_xy_t<unsigned int> {
    
public:
    uint_xy_t(unsigned int x_, unsigned int y_): generic_xy_t<unsigned int>(x_, y_) {}
};

// --..--..--..--..--..--..--...--..--..--..--..--..--..--..--..--..--..--..--...--..--..--..--..--
class double_xy_t : public generic_xy_t<double> {
    
public:
    double_xy_t(double x_, double y_): generic_xy_t<double>(x_, y_) {}
};

// --..--..--..--..--..--..--...--..--..--..--..--..--..--..--..--..--..--..--...--..--..--..--..--
class uint_x4_t {
    
    unsigned int x1;
    unsigned int x2;
    unsigned int x3;
    unsigned int x4;
    unsigned int len;
    
public:
    uint_x4_t(unsigned int x1_, unsigned int x2_): x1(x1_), x2(x2_), x3(0), x4(0), len(2) {}
    uint_x4_t(unsigned int x1_, unsigned int x2_, unsigned int x3_, unsigned int x4_): x1(x1_), x2(x2_), x3(x3_), x4(x4_), len(4) {}
    
    std::string to_string()  { return "(" + std::to_string(x1) + "," + std::to_string(x2) + "," + std::to_string(x3) + "," + std::to_string(x4) + ")"; }
    
    void set_x4(char* s) {
        std::string str(s);
        std::size_t found1 = str.find("(");
        std::size_t found2 = str.find(",");
        std::size_t found3 = 0;
        std::size_t found4 = 0;
        std::size_t found5 = str.find(")");
        std::string x_str;
        
        if (found2 != std::string::npos) {
            found3 = str.find(",", found2 + 1);
        }
        if (found3 != std::string::npos) {
            found4 = str.find(",", found3 + 1);
        }
        
        if ((found1 != std::string::npos) && (found2 != std::string::npos)) {
            std::string x_str = str.substr(found1+1, found2-found1-1);
            x1 = atoi(x_str.c_str());
        }
        if ((found2 != std::string::npos) && (found3 != std::string::npos)) {
            std::string x_str = str.substr(found2+1, found3-found2-1);
            x2 = atoi(x_str.c_str());
        }
        if ((found3 != std::string::npos) && (found4 != std::string::npos)) {
            std::string x_str = str.substr(found3+1, found4-found3-1);
            x3 = atoi(x_str.c_str());
        }
        if ((found4 != std::string::npos) && (found5 != std::string::npos)) {
            std::string x_str = str.substr(found4+1, found5-found4-1);
            x4 = atoi(x_str.c_str());
        }
    }
    
    void set(unsigned int x, unsigned int i) {
        
        if      (i==1) { x1 = x; }
        else if (i==2) { x2 = x; }
        else if (i==3) { x3 = x; }
        else if (i==4) { x4 = x; }
        else { std::cout << "ERROR: invalid i=" << i << std::endl; }
    }
    
    unsigned int get_x1() { return x1; }
    unsigned int get_x2() { return x2; }
    unsigned int get_x3() { return x3; }
    unsigned int get_x4() { return x4; }
    unsigned int get_len() { return len; }
};

// -------------------------------------------- Functions declaration -----------------------------------------------------------

// Auxiliary function for a info printout
void generic_message(std::string message, std::string severity);
void info(std::string message);
void debug(std::string message);
void error(std::string message);

// Mark a given license-plate (licPlate) with a colored rectangle
void drawRedRectangleAroundPlate(cv::Mat &imgOriginalScene, PossiblePlate &licPlate);

// Write the given license-plate characters (licPlate.strChars) the provided image (imgOriginalScene)
void writeLicensePlateCharsOnImage(cv::Mat &imgOriginalScene, PossiblePlate &licPlate);

// ROI adjustments
bool ROI_adjust(uint_x4_t ROI, cv::Mat &imgOriginalScene, int* W, int* H, uint_x4_t *adjROI);

// Crop a given ROI from a given Image; ROI=(startX,startY,W,H)
cv::Mat crop_roi_from_image(cv::Mat &imgOriginalScene, uint_x4_t ROI, bool autoRoiMode);

// Load input scene image (exit if fails)
cv::Mat load_input_scene_image(std::string imageFile, std::string ImType,
                               std::string onvif_ip, unsigned int onvif_port, std::string onvif_user, std::string onvif_passwd);

// Seeking for police symbol in a multi-Scale template-matching fashion
bool isTemplateFound(cv::Mat &imgOriginal, cv::Mat &imgTemplate, std::string template_name, double_xy_t template_thr, double_xy_t *templateLoc, bool debugMode);

// linspace implementation (C++)
std::vector<double> linspace(double min, double max, int n);

// Test a string for only numeric characters
bool is_digits(const std::string &str);

// Sample image in a given rectangle, represented as [x0,y0,w,h], where x0,y0 is the top-left coordinates of the sampling region
double sample_image(cv::Mat &imgGray, uint_x4_t sampleRect, unsigned int maxVal);

# endif	// AUXILIARY_H
