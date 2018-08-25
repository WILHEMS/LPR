// onvif_capture.cpp
//  _     _                           ____  _       _         ____                            _ _   _
// | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
// | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
// | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
// |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
//                                                                                |___/
// (c) Shahar Gino, July-2017, sgino209@gmail.com

#include "onvif_capture.hpp"

// ------------------------------------------------------------------------------------------------------------------------------
std::string onvif_camera::get_host_name() {
    
    return "TBD";
}

// ------------------------------------------------------------------------------------------------------------------------------
std::string onvif_camera::get_time_str() {
    
    return "TBD";
}

// ------------------------------------------------------------------------------------------------------------------------------
cv::Mat onvif_camera::snaphot_capture() {
    
    std::string onvif_tmp_file("onvif_snapshot.jpg");
    std::system("onvif_snapshot/build/ipconvif -cIp '192.168.226.201' -cUsr 'admin' -cPwd '123456'");
    cv::Mat frame = cv::imread(onvif_tmp_file);
    std::remove(onvif_tmp_file.c_str());
    return frame;
}

// ------------------------------------------------------------------------------------------------------------------------------
void onvif_snapshot_test() {
    
    onvif_camera mycam = onvif_camera();
    
    cv::Mat frame = mycam.snaphot_capture();
    
    std::string frame_title = mycam.get_host_name() + "_" + mycam.get_time_str();
    
    cv::imshow(frame_title, frame);
    cv::waitKey(0);
}