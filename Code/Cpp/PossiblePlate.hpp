// PossiblePlate.hpp
//  _     _                           ____  _       _         ____                            _ _   _
// | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
// | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
// | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
// |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
//                                                                                |___/
// (c) Shahar Gino, July-2017, sgino209@gmail.com

#ifndef POSSIBLE_PLATE_H
#define POSSIBLE_PLATE_H

#include <string>
#include<opencv2/core/core.hpp>
#include<opencv2/highgui/highgui.hpp>
#include<opencv2/imgproc/imgproc.hpp>

// ------------------------------------------------------------------------------------------------------------------------------
class PossiblePlate {
public:
    // Member variables
    cv::Mat imgPlate;
    cv::Mat imgGrayscale;
    cv::Mat imgThresh;
    cv::RotatedRect rrLocationOfPlateInScene;
    cv::RotatedRect rrLocationOfPlateInSceneGbl;
    std::string strChars;
    bool rectFind = false;

    // -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. --
    static bool sortDescendingByNumberOfChars(const PossiblePlate &ppLeft, const PossiblePlate &ppRight) {
        return(ppLeft.strChars.length() > ppRight.strChars.length());
    }
    
    bool operator==(const PossiblePlate& plate) {
        return (plate.strChars == strChars);
    }
};

#endif  // POSSIBLE_PLATE_H
