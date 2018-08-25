// LPR_wrapper.hpp
//  _     _                           ____  _       _         ____                            _ _   _
// | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
// | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
// | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
// |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
//                                                                                |___/
// (c) Shahar Gino, July-2017, sgino209@gmail.com

#ifndef LPR_WRAPPER
#define LPR_WRAPPER

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>
#include <iostream>
#include <regex>
#include "DetectPlates.hpp"
#include "PossiblePlate.hpp"
#include "DetectChars.hpp"
#include "Preprocess.hpp"
#include "Auxiliary.hpp"

#define LPRHOME std::string("/Users/shahargino/Documents/ImageProcessing/LPR")

// ----------------------------------- Types, globals and definitions -----------------------------------------------------------

typedef struct {

    std::string ImageFile = LPRHOME + std::string("/Database/Israel/1.jpg");

    uint_xy_t PreprocessGaussKernel = uint_xy_t(3, 3);     // Preprocessing: gaussian kernel, for smoothing
    unsigned int PreprocessThreshBlockSize = 19;           // Preprocessing: adaptive threshold, block size
    unsigned int PreprocessThreshweight = 9;               // Preprocessing: adaptive threshold, weight
    uint_xy_t PreprocessMorphKernel = uint_xy_t(3, 3);     // Preprocessing: morphological structuring kernel
    double PreprocessZoomIn = 1.0;                         // Preprocessing: digital zoom-in (bi-cubic) of the ROI
    double PlateWidthPaddingFactor = 1.3;                  // Plate width padding factor, used for plate extraction
    double PlateHeightPaddingFactor = 1.5;                 // Plate height padding factor, used for plate extraction
    bool FindRectangledPlate = false;                      // Add another plate candidate, in addition to longest matching characters approach
    uint_x4_t ROI = uint_x4_t(-1, -1);                     // Region-Of-Interest, ROI = (startX, startY, width, height), default(-1,-1)="auto"
    unsigned int MinPixelWidth = 2;                        // Minimal width (#pixels) for a character to be detected
    unsigned int MaxPixelWidth = UINT_MAX;                 // Maximal width (#pixels) for a character to be detected
    unsigned int MinPixelHeight = 8;                       // Minimal height (#pixels) for a character to be detected
    unsigned int MaxPixelHeight = UINT_MAX;                // Maximal height (#pixels) for a character to be detected
    double MinAspectRatio = 0.25;                          // Minimal aspect ratio (W/H) for a character to be detected
    double MaxAspectRatio = 1.0;                           // Maximal aspect ratio (W/H) for a character to be detected
    unsigned int MinPixelArea = 80;                        // Minimal area (#pixels) for a character to be detected
    unsigned int MaxPixelArea = UINT_MAX;                  // Maximal area (#pixels) for a character to be detected

    double MinDiagSizeMultipleAway = 0.3;                  // Sizing factor for overlapping characters decision (% of character size)
    double MaxDiagSizeMultipleAway = 4.0;                  // Sizing factor for matching characters decision (% of character size)
    double MinChangeInArea = 0.0;                          // Normalized Area difference for matching characters decision, lower boundary
    double MaxChangeInArea = 0.6;                          // Normalized Area difference for matching characters decision, upper boundary
    double MinChangeInWidth = 0.0;                         // Normalized Width difference for matching characters decision, lower boundary
    double MaxChangeInWidth = 0.8;                         // Normalized Width difference for matching characters decision, upper boundary
    double MinChangeInHeight = 0.0;                        // Normalized Height difference for matching characters decision, lower boundary
    double MaxChangeInHeight = 0.2;                        // Normalized Height difference for matching characters decision, upper boundary
    double MinHistNormThr = 65;                            // Minimal saturation threshold that a Plate must reach, lower boundary
    double MinAngleBetweenChars = 0.0;                     // Angle difference (degrees) for matching characters decision, lower boundary
    double MaxAngleBetweenChars = 12.0;                    // Angle difference (degrees) for matching characters decision, upper boundary
    unsigned int MinNumberOfMatchingChars = 6;             // Minimal amount of characters in the plate ("matching characters")
    unsigned int MaxNumberOfMatchingChars = 8;             // Maximal amount of characters in the plate ("matching characters")

    unsigned int ResizedCharImageWidth = 20;               // Character Resizing width attribute (in pixels), necessary for the OCR stage
    unsigned int ResizedCharImageHeight = 30;              // Character Resizing height attribute (in pixels), necessary for the OCR stage
    bool NoVerticalAlign = true;                           // Characters Vertical alignment, i.e. fix outlier characters along y-axis
    std::string kClassfications = LPRHOME + std::string("/Code/Cpp/KNN_training/classifications.xml");   // KNN training: classification
    std::string kFlattenedImages = LPRHOME + std::string("/Code/Cpp/KNN_training/images.xml"); // KNN training: flattened images
    unsigned int kFactorKNN = 2;                           // KNN factor, for digits classification
    cv::Ptr<cv::ml::KNearest> kNearest;                    // KNN object
    bool NoOcrTextualFixes = false;                        // Do not perform manual OCR texutal corrections, e.g. 'I'-->'1'
    bool NoOcrKnnFixes = false;                            // Do not perform manual OCR KNN corrections, e.g. '6'-->'5'
    bool NoOcrDigitsOnly = false;                          // Do not drop OCR results with english alphabet characters (digits only)
    std::string PoliceTemplate = LPRHOME + std::string("/Code/Cpp/Templates/p_template.png"); // Police template
    double_xy_t PoliceTemplateThr = double_xy_t(0.495, 60); // Thresholds for Police template-matching (match-factor thr, color thr)

    std::string onvif_ip = "192.168.226.201";              // ONVIF IP address
    unsigned int onvif_port = 80;                          // ONVIF PORT (HTTP)
    std::string onvif_user = "admin";                      // ONVIF UserName
    std::string onvif_passwd = "123456";                   // ONVIF Password
    bool onvif_test = false;                               // Run a sanity ONVIF check (take a snapshot and display on screen)

    double confidence_thr = 0.5;                           // Use Tesseract result in case native engine performs with confidence lower than confidence_thr.

    imgEnhancement_mode_t imgEnhancementMode = IMG_ENHANCEMENT_MODE_DISABLED; // Image enhancement, applies Warming effect (+CLAHE) and Saturation effect (+Gamma) 
    uint_xy_t pWarpPnt0 = uint_xy_t(0, 0);                 // Preprocessing: perspective transform (+warping), output quad points definition
    uint_xy_t pWarpPnt1 = uint_xy_t(0, 0);                 // Preprocessing: perspective transform (+warping), output quad points definition
    uint_xy_t pWarpPnt2 = uint_xy_t(0, 0);                 // Preprocessing: perspective transform (+warping), output quad points definition
    uint_xy_t pWarpPnt3 = uint_xy_t(0, 0);                 // Preprocessing: perspective transform (+warping), output quad points definition
    double blueMaxThrH = 40.0;                             // Maximal Hue for a charater to be classified as "blue" (higher H will get waived)
    double blueMinThrS = 60.0;                             // Minimal Saturation for a charater to be classified as "blue" (lower S will get waived)
    bool batchMode = false;                                // Run in batch mode, minimal debug info and w/o figures
    std::string OpMode = "auto";                           // Run in a specific operational mode, e.g. "police"
    bool debugMode = false;                                // Enable debug printouts and intermediate figures
} args_t;

typedef enum {
  SWEEP_THR_WEIGHT = 0,
  SWEEP_THR_BLK_SIZE,
  SWEEP_NUM
} sweep_vars_t; 

struct sweep_st {
  unsigned int from;
  unsigned int to;
  unsigned int step;
  sweep_st(unsigned int _from, unsigned int _to, unsigned int _step): 
    from(_from), to(_to), step(_step) {}
};
typedef struct sweep_st sweep_t;

struct frame_dec_st {
  cv::Mat imgOut;
  double confidence;
  bool engine_type;
  frame_dec_st(cv::Mat _imgOut, double _confidence, bool _engine_type): 
    imgOut(_imgOut), confidence(_confidence), engine_type(_engine_type) {}
};
typedef struct frame_dec_st frame_dec_t;

// -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. --
class LPR_wrapper {

    args_t params;

public:
    // Construnctor:
    LPR_wrapper(args_t args): params(args) {
        if (args.debugMode) {
            print_params(params);
        }
    }

    // Plates detection (within the given image)
    std::vector<PossiblePlate> detect_plates_in_scene(cv::Mat imgOriginalScene);

    // Characters detection (within the pre-detected plate)
    std::vector<PossiblePlate> detect_characters_in_plate(std::vector<PossiblePlate> listOfPossiblePlates);

    // Report the analysis result
    std::string report_result(cv::Mat imgOriginalScene, uint_x4_t ROI, std::vector<PossiblePlate> listOfPossibleChars, std::string out_file, bool sweep_mode=false);

    // Print parameters
    void print_params(args_t params);

    // Set API:
    void set_OpMode(cv::Mat &imgOriginalScene, cv::Mat &imgTemplate, std::string template_name, double_xy_t template_thr);
    void set_MinNumberOfMatchingChars(unsigned int MinNumberOfMatchingChars) { params.MinNumberOfMatchingChars = MinNumberOfMatchingChars; }
    void set_MaxNumberOfMatchingChars(unsigned int MaxNumberOfMatchingChars) { params.MaxNumberOfMatchingChars = MaxNumberOfMatchingChars; }
    void set_PlateWidthPaddingFactor(double PlateWidthPaddingFactor) { params.PlateWidthPaddingFactor = PlateWidthPaddingFactor; }
    void set_thr_weight(unsigned int thr_weight) { params.PreprocessThreshweight = thr_weight; }
    void set_thr_blk_size(unsigned int thr_blk_size) { params.PreprocessThreshBlockSize = thr_blk_size; }

    // Get API:
    uint_x4_t get_ROI() { return params.ROI; }
    std::string get_OpMode() { return params.OpMode; }
    std::string get_PoliceTemplate() { return params.PoliceTemplate; }
    double_xy_t get_PoliceTemplateThr() { return params.PoliceTemplateThr; }
    unsigned int get_MinNumberOfMatchingChars() { return params.MinNumberOfMatchingChars; }
    unsigned int get_MaxNumberOfMatchingChars() { return params.MaxNumberOfMatchingChars; }
    double get_PlateWidthPaddingFactor() { return params.PlateWidthPaddingFactor; }   
};

// -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. --

// K-Nearest-Neighbours (KNN) classifier training for digits recognition
int train_knn_classifier(args_t &args);

// Frame Decoder (main LPR API routine)
std::string frame_decoder(cv::Mat &imgOriginalScene, args_t args, std::vector<sweep_t> *_sweep, frame_dec_t &res_opt);
    
// Tesseract fallback (in case of a low confidence):
std::string fallback_decode(cv::Mat &img, bool debugMode);

# endif	// LPR_WRAPPER

