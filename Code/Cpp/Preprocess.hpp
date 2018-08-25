// Preprocess.hpp
//  _     _                           ____  _       _         ____                            _ _   _
// | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
// | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
// | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
// |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
//                                                                                |___/
// (c) Shahar Gino, July-2017, sgino209@gmail.com

#ifndef PREPROCESS_H
#define PREPROCESS_H

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
#include "Auxiliary.hpp"

// ----------------------------------- Types, globals and definitions -----------------------------------------------------------

const cv::Size GAUSSIAN_SMOOTH_FILTER_SIZE = cv::Size(5, 5);
const int ADAPTIVE_THRESH_BLOCK_SIZE = 19;
const int ADAPTIVE_THRESH_WEIGHT = 9;

// -------------------------------------------- Functions declaration -----------------------------------------------------------

// Pre-processing (CSC --> contrast --> blur --> threshold):
void preprocess(cv::Mat &imgOriginal, cv::Mat &imgGrayscale, cv::Mat &imgThresh, uint_xy_t PreprocessGaussKernel, unsigned int PreprocessThreshBlockSize,
                unsigned int PreprocessThreshweight, uint_xy_t PreprocessMorphKernel, std::string OpMode, std::string phase);

// Morphological filtering for increasing contrast: OutputImage = InputImage + TopHat - BlackHat
cv::Mat maximizeContrast(cv::Mat &imgGrayscale, uint_xy_t PreprocessMorphKernel);

// Image enhancement, applies Warming effect (+CLAHE) and Saturation effect (+Gamma)
cv::Mat imageEnhancement(cv::Mat &imgOriginal, double clahe_clipLimit, uint_xy_t clahe_tileGridSize, double gamma, imgEnhancement_mode_t mode, bool debugMode);

cv::Mat imageEnhancement_mode0(cv::Mat &imgOriginal, double clahe_clipLimit, uint_xy_t clahe_tileGridSize, double gamma);

cv::Mat imageEnhancement_mode1(cv::Mat &imgOriginal);

// Perspective Transform (+warping):
cv::Mat perspectiveWarp(cv::Mat &imgOriginal, uint_xy_t pnt0, uint_xy_t pnt1, uint_xy_t pnt2, uint_xy_t pnt3);

#endif	// PREPROCESS_H

