// DetectChars.hpp
//  _     _                           ____  _       _         ____                            _ _   _
// | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
// | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
// | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
// |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
//                                                                                |___/
// (c) Shahar Gino, July-2017, sgino209@gmail.com

#ifndef DETECT_CHARS_H
#define DETECT_CHARS_H

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/ml/ml.hpp>
#include "Main.hpp"
#include "PossibleChar.hpp"
#include "PossiblePlate.hpp"
#include "Preprocess.hpp"
#include "Auxiliary.hpp"

// ----------------------------------- Types, globals and definitions -----------------------------------------------------------

typedef struct char_params {
    
    std::vector<PossiblePlate> listOfPossiblePlates;
    uint_xy_t PreprocessGaussKernel;
    unsigned int PreprocessThreshBlockSize;
    unsigned int PreprocessThreshweight;
    uint_xy_t PreprocessMorphKernel;
    unsigned int MinPixelWidth;
    unsigned int MaxPixelWidth;
    unsigned int MinPixelHeight;
    unsigned int MaxPixelHeight;
    double MinAspectRatio;
    double MaxAspectRatio;
    unsigned int MinPixelArea;
    unsigned int MaxPixelArea;
    double MinDiagSizeMultipleAway;
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
    unsigned int ResizedCharImageWidth;
    unsigned int ResizedCharImageHeight;
    cv::Ptr<cv::ml::KNearest> kNearest;
    unsigned int kFactorKNN;
    bool NoVerticalAlign;
    bool NoOcrTextualFixes;
    bool NoOcrKnnFixes;
    bool NoOcrDigitsOnly;
    double blueMaxThrH;
    double blueMinThrS;
    std::string OpMode;
    bool debugMode;
    
    char_params(std::vector<PossiblePlate> _listOfPossiblePlates, uint_xy_t _PreprocessGaussKernel, unsigned int _PreprocessThreshBlockSize,
                unsigned int _PreprocessThreshweight, uint_xy_t _PreprocessMorphKernel, unsigned int _MinPixelWidth, unsigned int _MaxPixelWidth,
                unsigned int _MinPixelHeight, unsigned int _MaxPixelHeight, double _MinAspectRatio, double _MaxAspectRatio,
                unsigned int _MinPixelArea, unsigned int _MaxPixelArea, double _MinDiagSizeMultipleAway, double _MaxDiagSizeMultipleAway,
                unsigned int _MinNumberOfMatchingChars, unsigned int _MaxNumberOfMatchingChars, double _MinAngleBetweenChars, double _MaxAngleBetweenChars,
                double _MinChangeInArea, double _MaxChangeInArea, double _MinChangeInWidth, double _MaxChangeInWidth, double _MinChangeInHeight, double _MaxChangeInHeight,
                unsigned int _ResizedCharImageWidth, unsigned int _ResizedCharImageHeight, cv::Ptr<cv::ml::KNearest> _kNearest, unsigned int _kFactorKNN,
                bool _NoVerticalAlign, bool _NoOcrTextualFixes, bool _NoOcrKnnFixes, bool _NoOcrDigitsOnly, double _blueMaxThrH, double _blueMinThrS, 
                std::string _OpMode, bool _debugMode):
    
    listOfPossiblePlates(_listOfPossiblePlates),
    PreprocessGaussKernel(_PreprocessGaussKernel),
    PreprocessThreshBlockSize(_PreprocessThreshBlockSize),
    PreprocessThreshweight(_PreprocessThreshweight),
    PreprocessMorphKernel(_PreprocessMorphKernel),
    MinPixelWidth(_MinPixelWidth),
    MaxPixelWidth(_MaxPixelWidth),
    MinPixelHeight(_MinPixelHeight),
    MaxPixelHeight(_MaxPixelHeight),
    MinAspectRatio(_MinAspectRatio),
    MaxAspectRatio(_MaxAspectRatio),
    MinPixelArea(_MinPixelArea),
    MaxPixelArea(_MaxPixelArea),
    MinDiagSizeMultipleAway(_MinDiagSizeMultipleAway),
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
    ResizedCharImageWidth(_ResizedCharImageWidth),
    ResizedCharImageHeight(_ResizedCharImageHeight),
    kNearest(_kNearest),
    kFactorKNN(_kFactorKNN),
    NoVerticalAlign(_NoVerticalAlign),
    NoOcrTextualFixes(_NoOcrTextualFixes),
    NoOcrKnnFixes(_NoOcrKnnFixes),
    NoOcrDigitsOnly(_NoOcrDigitsOnly),
    blueMaxThrH(_blueMaxThrH),
    blueMinThrS(_blueMinThrS),
    OpMode(_OpMode),
    debugMode(_debugMode) {}
    
} char_params_t;

// -------------------------------------------- Functions declaration -----------------------------------------------------------

// Detect characters in the pre-detected plate (OCR analysis, over KNN engine)
std::vector<PossiblePlate> detectCharsInPlates(std::vector<PossiblePlate> &vectorOfPossiblePlates, char_params_t char_params);

// Find all possible chars in the plate (finds all contours that could be chars)
std::vector<PossibleChar> findPossibleCharsInImage(cv::Mat &imgBinary, unsigned int MinPixelWidth, unsigned int MaxPixelWidth,
                                                   unsigned int MinPixelHeight, unsigned int MaxPixelHeight, double MinAspectRatio,
                                                   double MaxAspectRatio, unsigned int MinPixelArea, unsigned int MaxPixelArea, bool debugMode);

// Re-arrange the one big list of characters (listOfPossibleChars) into a list of lists of matching characters (listOfListsOfMatchingChars)
// Note: characters that are not found to be in a group of matches do not need to be considered further
std::vector<std::vector<PossibleChar> > findVectorOfVectorsOfMatchingChars(const std::vector<PossibleChar> &vectorOfPossibleChars,
                                                                           unsigned int MinNumberOfMatchingChars, unsigned int MaxNumberOfMatchingChars,
                                                                           double MinAngleBetweenChars, double MaxAngleBetweenChars,
                                                                           double MinChangeInArea, double MaxChangeInArea,
                                                                           double MinChangeInWidth, double MaxChangeInWidth,
                                                                           double MinChangeInHeight, double MaxChangeInHeight,
                                                                           double MaxDiagSizeMultipleAway);

// Find all characters in the big list of possible characters, that match a single possible character and return those matching chars as a list
std::vector<PossibleChar> findVectorOfMatchingChars(const PossibleChar &possibleChar, const std::vector<PossibleChar> &vectorOfChars, double MaxDiagSizeMultipleAway,
                                                    double MinAngleBetweenChars, double MaxAngleBetweenChars, double MinChangeInArea, double MaxChangeInArea,
                                                    double MinChangeInWidth, double MaxChangeInWidth, double MinChangeInHeight, double MaxChangeInHeight);

// Use basic trigonometry (Pythagorean theorem) to calculate distancne between two given characters
double distanceBetweenChars(const PossibleChar &firstChar, const PossibleChar &secondChar);

// Use basic trigonometry (SOH, CAH, TOA) to calculate angle between two given characters
double angleBetweenChars(const PossibleChar &firstChar, const PossibleChar &secondChar);

// If we have two characters overlapping or to close to each other to possibly be separate chars, remove the inner (smaller) character.
// This is to prevent including the same character twice if two contours are found for the same character.
// For example, for the letter 'O', both the inner ring and the outer ring may be found as contours, but we should only include the character once
std::vector<PossibleChar> removeInnerOverlappingChars(std::vector<PossibleChar> &vectorOfMatchingChars, double MinDiagSizeMultipleAway);

// This is where we apply the actual char recognition
std::string recognizeCharsInPlate(cv::Mat &imgThresh, std::vector<PossibleChar> &vectorOfMatchingChars, unsigned int ResizedCharImageWidth,
                                  unsigned int ResizedCharImageHeight, cv::Ptr<cv::ml::KNearest> kNearest, unsigned int intkFactorKNN,
                                  bool NoOcrKnnFixes, unsigned int intPlateCounter, bool debugMode);

// OCR textual corrections:
std::string OcrTextualCorrections(std::string strChars, std::string mode, bool NoOcrDigitsOnly, bool debugMode);

// OCR KNN corrections:
char OcrKnnCorrections(char npaResultAscii, cv::Mat npaROIResized, double charAspectRatio, bool debugMode);

// Characters Vertical alignment check, i.e. check characters alignment along y-axis
bool charactersVerticalAlignCheck(std::vector<PossibleChar> vectorOfMatchingChars, double errY_thr, double errH_thr, bool debugMode);

// Characters Vertical alignment, i.e. fix outlier characters along y-axis
void charactersVerticalAlign(std::vector<PossibleChar> &vectorOfMatchingChars, double errY_thr, double errH_thr, bool debugMode);

// Remove possibleChars that are "too blue" (filters garbage from the Israeli symbol):
void RemoveTooBlueChars(std::vector<PossibleChar> &vectorOfPossibleChars, const cv::Mat &imgPlate, double blueMaxThrH, double blueMinThrS, bool debugMode); 

// Debug print image (useful for character OCR debug)
void print_character(cv::Mat &imgGray);

#endif	// DETECT_CHARS_H

