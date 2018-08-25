// DetectPlates.hpp
//  _     _                           ____  _       _         ____                            _ _   _
// | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
// | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
// | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
// |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
//                                                                                |___/
// (c) Shahar Gino, July-2017, sgino209@gmail.com

#ifndef DETECT_PLATES_H
#define DETECT_PLATES_H

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include "Main.hpp"
#include "PossiblePlate.hpp"
#include "PossibleChar.hpp"
#include "Preprocess.hpp"
#include "DetectChars.hpp"
#include "Auxiliary.hpp"

// ----------------------------------- Types, globals and definitions -----------------------------------------------------------

typedef struct plate_params {
    
    cv::Mat imgOriginalScene;
    uint_xy_t PreprocessGaussKernel;
    unsigned int PreprocessThreshBlockSize;
    unsigned int PreprocessThreshweight;
    uint_xy_t PreprocessMorphKernel;
    double PlateWidthPaddingFactor;
    double PlateHeightPaddingFactor;
    bool FindRectangledPlate;
    unsigned int MinPixelWidth;
    unsigned int MaxPixelWidth;
    unsigned int MinPixelHeight;
    unsigned int MaxPixelHeight;
    double MinAspectRatio;
    double MaxAspectRatio;
    unsigned int MinPixelArea;
    unsigned int MaxPixelArea;
    double MaxDiagSizeMultipleAway;
    unsigned int MinNumberOfMatchingChars;
    unsigned int MaxNumberOfMatchingChars;
    double MinAngleBetweenChars;
    double MaxAngleBetweenChars;
    double MinChangeInArea;
    double MaxChangeInArea;
    double MinChangeInWidth;
    double MaxChangeInWidth;
    double MinChangeInHeight;
    double MaxChangeInHeight;
    double MinHistNormThr;
    std::string OpMode;
    bool debugMode;
    
    plate_params(cv::Mat _imgOriginalScene, uint_xy_t _PreprocessGaussKernel, unsigned int _PreprocessThreshBlockSize, unsigned int _PreprocessThreshweight,
                 uint_xy_t _PreprocessMorphKernel, double _PlateWidthPaddingFactor, double _PlateHeightPaddingFactor, bool _FindRectangledPlate,
                 unsigned int _MinPixelWidth, unsigned int _MaxPixelWidth, unsigned int _MinPixelHeight, unsigned int _MaxPixelHeight, double _MinAspectRatio,
                 double _MaxAspectRatio, unsigned int _MinPixelArea, unsigned int _MaxPixelArea, double _MaxDiagSizeMultipleAway,
                 unsigned int _MinNumberOfMatchingChars, unsigned int _MaxNumberOfMatchingChars, double _MinAngleBetweenChars, double _MaxAngleBetweenChars,
                 double _MinChangeInArea, double _MaxChangeInArea, double _MinChangeInWidth, double _MaxChangeInWidth, double _MinChangeInHeight,
                 double _MaxChangeInHeight, double _MinHistNormThr, std::string _OpMode, bool _debugMode):
    
    imgOriginalScene(_imgOriginalScene),
    PreprocessGaussKernel(_PreprocessGaussKernel),
    PreprocessThreshBlockSize(_PreprocessThreshBlockSize),
    PreprocessThreshweight(_PreprocessThreshweight),
    PreprocessMorphKernel(_PreprocessMorphKernel),
    PlateWidthPaddingFactor(_PlateWidthPaddingFactor),
    PlateHeightPaddingFactor(_PlateHeightPaddingFactor),
    FindRectangledPlate(_FindRectangledPlate),
    MinPixelWidth(_MinPixelWidth),
    MaxPixelWidth(_MaxPixelWidth),
    MinPixelHeight(_MinPixelHeight),
    MaxPixelHeight(_MaxPixelHeight),
    MinAspectRatio(_MinAspectRatio),
    MaxAspectRatio(_MaxAspectRatio),
    MinPixelArea(_MinPixelArea),
    MaxPixelArea(_MaxPixelArea),
    MaxDiagSizeMultipleAway(_MaxDiagSizeMultipleAway),
    MinNumberOfMatchingChars(_MinNumberOfMatchingChars),
    MaxNumberOfMatchingChars(_MaxNumberOfMatchingChars),
    MinAngleBetweenChars(_MinAngleBetweenChars),
    MaxAngleBetweenChars(_MaxAngleBetweenChars),
    MinChangeInArea(_MinChangeInArea),
    MaxChangeInArea(_MaxChangeInArea),
    MinChangeInWidth(_MinChangeInWidth),
    MaxChangeInWidth(_MaxChangeInWidth),
    MinChangeInHeight(_MinChangeInHeight),
    MaxChangeInHeight(_MaxChangeInHeight),
    MinHistNormThr(_MinHistNormThr),
    OpMode(_OpMode),
    debugMode(_debugMode) {}
    
} plate_params_t;

// -------------------------------------------- Functions declaration -----------------------------------------------------------

// License Plate Detection in a given input image scene, using geometrical analysis techniques
std::vector<PossiblePlate> detectPlatesInScene(cv::Mat &imgOriginalScene, plate_params_t plate_params);

// Extract license-plate in the provided image, based on given contours group that corresponds for matching characters
PossiblePlate extractPlate(cv::Mat &imgOriginal, std::vector<PossibleChar> &vectorOfMatchingChars, double PlateWidthPaddingFactor, double PlateHeightPaddingFactor);

// Find rectangles
PossiblePlate findRectangledPlate(cv::Mat &imgOriginalScene, cv::Mat &imgThresh, double circularity_min, double circularity_max,
                                  double aspect_ratio_min, double aspect_ratio_max, double area_norm_min, double area_norm_max, bool debugMode);

# endif	// DETECT_PLATES_H
