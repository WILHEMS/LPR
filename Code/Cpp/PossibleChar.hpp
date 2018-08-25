// PossibleChar.hpp
//  _     _                           ____  _       _         ____                            _ _   _
// | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
// | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
// | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
// |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
//                                                                                |___/
// (c) Shahar Gino, July-2017, sgino209@gmail.com

#ifndef POSSIBLE_CHAR_H
#define POSSIBLE_CHAR_H

#include<opencv2/core/core.hpp>
#include<opencv2/highgui/highgui.hpp>
#include<opencv2/imgproc/imgproc.hpp>

// ------------------------------------------------------------------------------------------------------------------------------
class PossibleChar {
public:
    // Member variables
    std::vector<cv::Point> contour;
    cv::Rect boundingRect;
    int intCenterX;
    int intCenterY;
    double dblDiagonalSize;
    double dblAspectRatio;
    unsigned int MinPixelWidth;
    unsigned int MaxPixelWidth;
    unsigned int MinPixelHeight;
    unsigned int MaxPixelHeight;
    double MinAspectRatio;
    double MaxAspectRatio;
    unsigned int MinPixelArea;
    unsigned int MaxPixelArea;

    // -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. --
    // Constructor
    PossibleChar(std::vector<cv::Point> _contour, unsigned int MinPixelWidth, unsigned int MaxPixelWidth,
                 unsigned int MinPixelHeight, unsigned int MaxPixelHeight, double MinAspectRatio, double MaxAspectRatio,
                 unsigned int MinPixelArea, unsigned int MaxPixelArea);
    
    // -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. --
    // A 'first pass' over the contour, to see if it could be representing a character
    bool checkIfPossibleChar();
    
    // -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. --
    static bool sortCharsLeftToRight(const PossibleChar &pcLeft, const PossibleChar & pcRight) {
        return(pcLeft.intCenterX < pcRight.intCenterX);
    }

    // -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. --
    static bool sortCharsTopToBottom(const PossibleChar &pcTop, const PossibleChar & pcBottom) {
        return(pcTop.intCenterY < pcBottom.intCenterY);
    }
    
    // -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. --
    bool operator == (const PossibleChar& otherPossibleChar) const {
        if (this->contour == otherPossibleChar.contour) return true;
        else return false;
    }

    // -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. --
    bool operator != (const PossibleChar& otherPossibleChar) const {
        if (this->contour != otherPossibleChar.contour) return true;
        else return false;
    }
};

#endif  // POSSIBLE_CHAR_H
