// onvif_capture.hpp
//  _     _                           ____  _       _         ____                            _ _   _
// | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
// | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
// | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
// |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
//                                                                                |___/
// (c) Shahar Gino, July-2017, sgino209@gmail.com

#ifndef ONVIF_CAPTURE_H
#define ONVIF_CAPTURE_H

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
#include <unistd.h>

// ----------------------------------- Types, globals and definitions -----------------------------------------------------------

class onvif_camera {
    
    std::string ip;
    unsigned int port;
    std::string user;
    std::string passwd;
    std::string wsdl;
    
public:
    
    // Constructors
    onvif_camera():\
        ip("192.168.226.201"), port(80), user("admin"), passwd("123456"), wsdl("/Library/Python/2.7/site-packages/python-onvif-master/wsdl") {}
    
    onvif_camera(std::string _ip, unsigned int _port, std::string _user, std::string _passwd, std::string _wsdl):\
        ip(_ip), port(_port), user(_user), passwd(_passwd), wsdl(_wsdl) {}
    
    onvif_camera(std::string _ip, unsigned int _port, std::string _user, std::string _passwd):\
        ip(_ip), port(_port), user(_user), passwd(_passwd), wsdl("/Library/Python/2.7/site-packages/python-onvif-master/wsdl") {}
    
    // Get Hostname
    std::string get_host_name();
    
    // Get system date and time as a formatted string
    std::string get_time_str();
    
    // Capture a frame snapshot
    cv::Mat snaphot_capture();
};

// -------------------------------------------- Functions declaration -----------------------------------------------------------

// Simple ONVIF test: capture a snapshot and figure it
void onvif_snapshot_test();

# endif	// ONVIF_CAPTURE_H
