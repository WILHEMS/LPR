// Main.hpp
//  _     _                           ____  _       _         ____                            _ _   _
// | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
// | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
// | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
// |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
//                                                                                |___/
// (c) Shahar Gino, July-2017, sgino209@gmail.com

#ifndef MAIN_HPP
#define MAIN_HPP

#include <iostream>
#include <iomanip>
#include <getopt.h>
#include <dirent.h>
#include <unistd.h>
#include "LPR_wrapper.hpp"

// -------------------------------- getopt interface, for retreiving user-arguments ---------------------------------------------

#define no_argument 0
#define required_argument 1
#define optional_argument 2

enum lpr_arg_t {
    LPR_PREPROCESSGAUSSKERNEL = 0,
    LPR_PREPROCESSTHRESHBLOCKSIZE,
    LPR_PREPROCESSTHRESHWEIGHT,
    LPR_PREPROCESSMORPHKERNEL,
    LPR_PREPROCESSZOOMIN,
    LPR_PLATEWIDTHPADDINGFACTOR,
    LPR_PLATEHEIGHTPADDINGFACTOR,
    LPR_FINDRECTPLATE,
    LPR_ROI,
    LPR_MINPIXELWIDTH,
    LPR_MAXPIXELWIDTH,
    LPR_MINPIXELHEIGHT,
    LPR_MAXPIXELHEIGHT,
    LPR_MINASPECTRATIO,
    LPR_MAXASPECTRATIO,
    LPR_MINPIXELAREA,
    LPR_MAXPIXELAREA,
    LPR_MINDIAGSIZEMULTIPLEAWAY,
    LPR_MAXDIAGSIZEMULTIPLEAWAY,
    LPR_MINCHANGEINAREA,
    LPR_MAXCHANGEINAREA,
    LPR_MINCHANGEINWIDTH,
    LPR_MAXCHANGEINWIDTH,
    LPR_MINCHANGEINHEIGHT,
    LPR_MAXCHANGEINHEIGHT,
    LPR_MINHISTNORMTHR,
    LPR_MINANGLEBETWEENCHARS,
    LPR_MAXANGLEBETWEENCHARS,
    LPR_MINNUMBEROFMATCHINGCHARS,
    LPR_MAXNUMBEROFMATCHINGCHARS,
    LPR_RESIZEDCHARIMAGEWIDTH,
    LPR_RESIZEDCHARIMAGEHEIGHT,
    LPR_NOVERTICALALIGN,
    LPR_KCLASSFICATIONS,
    LPR_KFLATTENEDIMAGES,
    LPR_KFACTORKNN,
    LPR_NOOCRTEXTUALFIXES,
    LPR_NOOCRKNNFIXES,
    LPR_NOOCRDIGITSONLY,
    LPR_POLICETEMPLATE,
    LPR_POLICETEMPLATETHR,
    LPR_ONVIFIP,
    LPR_ONVIFPORT,
    LPR_ONVIFUSER,
    LPR_ONVIFPASSWD,
    LPR_ONVIFTEST,
    LPR_CONFIDENCETHR,
    LPR_IMGENHANCEMENTMODE,
    LPR_PREPROCESSPWARPPNT0, 
    LPR_PREPROCESSPWARPPNT1, 
    LPR_PREPROCESSPWARPPNT2, 
    LPR_PREPROCESSPWARPPNT3, 
    LPR_BLUEMAXTHRH,
    LPR_BLUEMINTHRS,
    LPR_BATCH,
    LPR_OPMODE,
    LPR_DEBUG,
    LPR_ARGS_NUM
};
typedef enum lpr_arg_t lpr_arg_t;

const struct option longopts[] =
{
    {"version",                    no_argument,       0, 'v' },
    {"help",                       no_argument,       0, 'h' },
    {"image",                      required_argument, 0, 'i' },
    {"PreprocessGaussKernel",      required_argument, 0, LPR_PREPROCESSGAUSSKERNEL },
    {"PreprocessThreshBlockSize",  required_argument, 0, LPR_PREPROCESSTHRESHBLOCKSIZE },
    {"PreprocessThreshweight",     required_argument, 0, LPR_PREPROCESSTHRESHWEIGHT },
    {"PreprocessMorphKernel",      required_argument, 0, LPR_PREPROCESSMORPHKERNEL },
    {"PreprocessZoomIn",           required_argument, 0, LPR_PREPROCESSZOOMIN },
    {"PlateWidthPaddingFactor",    required_argument, 0, LPR_PLATEWIDTHPADDINGFACTOR },
    {"PlateHeightPaddingFactor",   required_argument, 0, LPR_PLATEHEIGHTPADDINGFACTOR },
    {"FindRectangledPlate",        no_argument,       0, LPR_FINDRECTPLATE },
    {"ROI",                        required_argument, 0, LPR_ROI },
    {"MinPixelWidth",              required_argument, 0, LPR_MINPIXELWIDTH },
    {"MaxPixelWidth",              required_argument, 0, LPR_MAXPIXELWIDTH },
    {"MinPixelHeight",             required_argument, 0, LPR_MINPIXELHEIGHT },
    {"MaxPixelHeight",             required_argument, 0, LPR_MAXPIXELHEIGHT },
    {"MinAspectRatio",             required_argument, 0, LPR_MINASPECTRATIO },
    {"MaxAspectRatio",             required_argument, 0, LPR_MAXASPECTRATIO },
    {"MinPixelArea",               required_argument, 0, LPR_MINPIXELAREA },
    {"MaxPixelArea",               required_argument, 0, LPR_MAXPIXELAREA },
    {"MinDiagSizeMultipleAway",    required_argument, 0, LPR_MINDIAGSIZEMULTIPLEAWAY },
    {"MaxDiagSizeMultipleAway",    required_argument, 0, LPR_MAXDIAGSIZEMULTIPLEAWAY },
    {"MinChangeInArea",            required_argument, 0, LPR_MINCHANGEINAREA },
    {"MaxChangeInArea",            required_argument, 0, LPR_MAXCHANGEINAREA },
    {"MinChangeInWidth",           required_argument, 0, LPR_MINCHANGEINWIDTH },
    {"MaxChangeInWidth",           required_argument, 0, LPR_MAXCHANGEINWIDTH },
    {"MinChangeInHeight",          required_argument, 0, LPR_MINCHANGEINHEIGHT },
    {"MaxChangeInHeight",          required_argument, 0, LPR_MAXCHANGEINHEIGHT },
    {"MinHistNormThr",             required_argument, 0, LPR_MINHISTNORMTHR },
    {"MinAngleBetweenChars",       required_argument, 0, LPR_MINANGLEBETWEENCHARS },
    {"MaxAngleBetweenChars",       required_argument, 0, LPR_MAXANGLEBETWEENCHARS },
    {"MinNumberOfMatchingChars",   required_argument, 0, LPR_MINNUMBEROFMATCHINGCHARS },
    {"MaxNumberOfMatchingChars",   required_argument, 0, LPR_MAXNUMBEROFMATCHINGCHARS },
    {"ResizedCharImageWidth",      required_argument, 0, LPR_RESIZEDCHARIMAGEWIDTH },
    {"ResizedCharImageHeight",     required_argument, 0, LPR_RESIZEDCHARIMAGEHEIGHT },
    {"NoVerticalAlign",            no_argument,       0, LPR_NOVERTICALALIGN },
    {"kClassfications",            required_argument, 0, LPR_KCLASSFICATIONS },
    {"kFlattenedImages",           required_argument, 0, LPR_KFLATTENEDIMAGES },
    {"kFactorKNN",                 required_argument, 0, LPR_KFACTORKNN },
    {"NoOcrTextualFixes",          no_argument,       0, LPR_NOOCRTEXTUALFIXES },
    {"NoOcrKnnFixes",              no_argument,       0, LPR_NOOCRKNNFIXES },
    {"NoOcrDigitsOnly",            no_argument,       0, LPR_NOOCRDIGITSONLY },
    {"PoliceTemplate",             required_argument, 0, LPR_POLICETEMPLATE },
    {"PoliceTemplateThr",          required_argument, 0, LPR_POLICETEMPLATETHR },
    {"onvif_ip",                   required_argument, 0, LPR_ONVIFIP },
    {"onvif_port",                 required_argument, 0, LPR_ONVIFPORT },
    {"onvif_user",                 required_argument, 0, LPR_ONVIFUSER },
    {"onvif_admin",                required_argument, 0, LPR_ONVIFPASSWD },
    {"onvif_test",                 no_argument,       0, LPR_ONVIFTEST },
    {"confidence_thr",             required_argument, 0, LPR_CONFIDENCETHR },
    {"imgEnhancementMode",         required_argument, 0, LPR_IMGENHANCEMENTMODE },
    {"PerspectiveWarp0",           required_argument, 0, LPR_PREPROCESSPWARPPNT0 },
    {"PerspectiveWarp1",           required_argument, 0, LPR_PREPROCESSPWARPPNT1 },
    {"PerspectiveWarp2",           required_argument, 0, LPR_PREPROCESSPWARPPNT2 },
    {"PerspectiveWarp3",           required_argument, 0, LPR_PREPROCESSPWARPPNT3 },
    {"blueMaxThrH",                required_argument, 0, LPR_BLUEMAXTHRH },
    {"blueMinThrS",                required_argument, 0, LPR_BLUEMINTHRS },
    {"batch",                      no_argument,       0, LPR_BATCH },
    {"mode",                       required_argument, 0, LPR_OPMODE },
    {"debug",                      no_argument,       0, LPR_DEBUG }
};

// -------------------------------------------- Functions declaration -----------------------------------------------------------
// Main Algo stages:
// stage1:  Scene Image --> preprocess --> find possible chars --> find matching chars --> extract plate --> List of possible plates (img+meta)
// stage2:  Possible Plates --> preprocess --> THR --> find possible chars --> find matching chars --> remove overlapping chars --> Take longest chars phrase
// stage3:  Chars Phrase --> sort chars (left to right) --> crop chars, one by one (from THR image) + resize char --> OCR (KNN)
//
// KNN training:
// - Classification file:  contains 180 lines, which lists all ascii symbols for digits (48-57) and characters (65-90) - 5 lines per symbol
// - FlattenedImages file: contains 180 lines, corresponds with the Classification file, each contains 5 flattened images (20x30, column-stack)
int main(int argc, char** argv);

// Auxiliary function - returns folder name for results to be stored at (lpr_results_%d%m%y_%H%M%S_imgFile)
std::string get_envpath(std::string ImageFile);

// Auxiliary function - prints usage information
void usage(char *);

#endif	// MAIN_HPP

