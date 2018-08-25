// PossibleChar.cpp
//  _     _                           ____  _       _         ____                            _ _   _
// | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
// | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
// | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
// |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
//                                                                                |___/
// (c) Shahar Gino, July-2017, sgino209@gmail.com

#include "PossibleChar.hpp"

// ------------------------------------------------------------------------------------------------------------------------------
PossibleChar :: PossibleChar(std::vector<cv::Point> _contour, unsigned int _MinPixelWidth, unsigned int _MaxPixelWidth,
                           unsigned int _MinPixelHeight, unsigned int _MaxPixelHeight, double _MinAspectRatio, double _MaxAspectRatio,
                           unsigned int _MinPixelArea, unsigned int _MaxPixelArea) {
    contour = _contour;

    boundingRect = cv::boundingRect(contour);

    intCenterX = (boundingRect.x + boundingRect.x + boundingRect.width) / 2;
    intCenterY = (boundingRect.y + boundingRect.y + boundingRect.height) / 2;

    dblDiagonalSize = sqrt(pow(boundingRect.width, 2) + pow(boundingRect.height, 2));

    dblAspectRatio = (float)boundingRect.width / (float)boundingRect.height;
    
    MinPixelWidth = _MinPixelWidth;
    MaxPixelWidth = _MaxPixelWidth;
    MinPixelHeight = _MinPixelHeight;
    MaxPixelHeight = _MaxPixelHeight;
    MinAspectRatio = _MinAspectRatio;
    MaxAspectRatio = _MaxAspectRatio;
    MinPixelArea = _MinPixelArea;
    MaxPixelArea = _MaxPixelArea;
}

// ------------------------------------------------------------------------------------------------------------------------------
bool PossibleChar :: checkIfPossibleChar() {
    
    return (boundingRect.area() > MinPixelArea &&
            boundingRect.area() < MaxPixelArea &&
            boundingRect.width > MinPixelWidth &&
            boundingRect.width < MaxPixelWidth &&
            boundingRect.height > MinPixelHeight &&
            boundingRect.height < MaxPixelHeight &&
            dblAspectRatio > MinAspectRatio &&
            dblAspectRatio < MaxAspectRatio);
}
