// Main.cpp
//  _     _                           ____  _       _         ____                            _ _   _
// | |   (_) ___ ___ _ __  ___  ___  |  _ \| | __ _| |_ ___  |  _ \ ___  ___ ___   __ _ _ __ (_) |_(_) ___  _ __
// | |   | |/ __/ _ \ '_ \/ __|/ _ \ | |_) | |/ _` | __/ _ \ | |_) / _ \/ __/ _ \ / _` | '_ \| | __| |/ _ \| '_ \
// | |___| | (__  __/ | | \__ \  __/ |  __/| | (_| | |_  __/ |  _ <  __/ (__ (_) | (_| | | | | | |_| | (_) | | | |
// |_____|_|\___\___|_| |_|___/\___| |_|   |_|\__,_|\__\___| |_| \_\___|\___\___/ \__, |_| |_|_|\__|_|\___/|_| |_|
//                                                                                |___/
// (c) Shahar Gino, July-2017, sgino209@gmail.com

#include "Main.hpp"

const char* lpr_version = "1.9";

// ------------------------------------------------------------------------------------------------------------------------------
int main(int argc, char** argv) {

    int index, iarg = 0;
    args_t args;
    std::clock_t t0,t1;
    double t_elapsed_sec;
    char buffer[100];

    // Prolog:
    t0 = std::clock();
    std::cout << "Start" << std::endl;

    // User arguments patch:
    while (iarg != -1)
    {
        iarg = getopt_long(argc, argv, "i:vh", longopts, &index);

        switch (iarg) {
            case 'h':                            usage(argv[0]);  exit(0);                                       break;
            case 'v':                    sprintf(buffer, "LPR version: %s", lpr_version); info(buffer); exit(0); break;
            case 'i':                            if (optarg) { args.ImageFile = optarg;                       }  break;
            case LPR_PREPROCESSGAUSSKERNEL:      if (optarg) { args.PreprocessGaussKernel.set_xy(optarg);     }  break;
            case LPR_PREPROCESSTHRESHBLOCKSIZE:  if (optarg) { args.PreprocessThreshBlockSize = atoi(optarg); }  break;
            case LPR_PREPROCESSTHRESHWEIGHT:     if (optarg) { args.PreprocessThreshweight = atoi(optarg);    }  break;
            case LPR_PREPROCESSMORPHKERNEL:      if (optarg) { args.PreprocessMorphKernel.set_xy(optarg);     }  break;
            case LPR_PREPROCESSZOOMIN:           if (optarg) { args.PreprocessZoomIn = atof(optarg);          }  break;
            case LPR_PLATEWIDTHPADDINGFACTOR:    if (optarg) { args.PlateWidthPaddingFactor = atof(optarg);   }  break;
            case LPR_PLATEHEIGHTPADDINGFACTOR:   if (optarg) { args.PlateHeightPaddingFactor = atof(optarg);  }  break;
            case LPR_FINDRECTPLATE:              args.FindRectangledPlate = true;                                break;
            case LPR_ROI:                        if (optarg) { args.ROI.set_x4(optarg);                       }  break;
            case LPR_MINPIXELWIDTH:              if (optarg) { args.MinPixelWidth = atoi(optarg);             }  break;
            case LPR_MAXPIXELWIDTH:              if (optarg) { args.MaxPixelWidth = atoi(optarg);             }  break;
            case LPR_MINPIXELHEIGHT:             if (optarg) { args.MinPixelHeight = atoi(optarg);            }  break;
            case LPR_MAXPIXELHEIGHT:             if (optarg) { args.MaxPixelHeight = atoi(optarg);            }  break;
            case LPR_MINASPECTRATIO:             if (optarg) { args.MinAspectRatio = atof(optarg);            }  break;
            case LPR_MAXASPECTRATIO:             if (optarg) { args.MaxAspectRatio = atof(optarg);            }  break;
            case LPR_MINPIXELAREA:               if (optarg) { args.MinPixelArea = atoi(optarg);              }  break;
            case LPR_MAXPIXELAREA:               if (optarg) { args.MaxPixelArea = atoi(optarg);              }  break;
            case LPR_MINDIAGSIZEMULTIPLEAWAY:    if (optarg) { args.MinDiagSizeMultipleAway = atof(optarg);   }  break;
            case LPR_MAXDIAGSIZEMULTIPLEAWAY:    if (optarg) { args.MaxDiagSizeMultipleAway = atof(optarg);   }  break;
            case LPR_MINCHANGEINAREA:            if (optarg) { args.MinChangeInArea = atof(optarg);           }  break;
            case LPR_MAXCHANGEINAREA:            if (optarg) { args.MaxChangeInArea = atof(optarg);           }  break;
            case LPR_MINCHANGEINWIDTH:           if (optarg) { args.MinChangeInWidth = atoi(optarg);          }  break;
            case LPR_MAXCHANGEINWIDTH:           if (optarg) { args.MaxChangeInWidth = atof(optarg);          }  break;
            case LPR_MINCHANGEINHEIGHT:          if (optarg) { args.MinChangeInHeight = atof(optarg);         }  break;
            case LPR_MAXCHANGEINHEIGHT:          if (optarg) { args.MaxChangeInHeight = atof(optarg);         }  break;
            case LPR_MINHISTNORMTHR:             if (optarg) { args.MinHistNormThr = atof(optarg);            }  break;
            case LPR_MINANGLEBETWEENCHARS:       if (optarg) { args.MinAngleBetweenChars = atof(optarg);      }  break;
            case LPR_MAXANGLEBETWEENCHARS:       if (optarg) { args.MaxAngleBetweenChars = atof(optarg);      }  break;
            case LPR_MINNUMBEROFMATCHINGCHARS:   if (optarg) { args.MinNumberOfMatchingChars = atoi(optarg);  }  break;
            case LPR_MAXNUMBEROFMATCHINGCHARS:   if (optarg) { args.MaxNumberOfMatchingChars = atoi(optarg);  }  break;
            case LPR_RESIZEDCHARIMAGEWIDTH:      if (optarg) { args.ResizedCharImageWidth = atoi(optarg);     }  break;
            case LPR_RESIZEDCHARIMAGEHEIGHT:     if (optarg) { args.ResizedCharImageHeight = atoi(optarg);    }  break;
            case LPR_NOVERTICALALIGN:            args.NoVerticalAlign = true;                                    break;
            case LPR_KCLASSFICATIONS:            if (optarg) { args.kClassfications = optarg;                 }  break;
            case LPR_KFLATTENEDIMAGES:           if (optarg) { args.kFlattenedImages = optarg;                }  break;
            case LPR_KFACTORKNN:                 if (optarg) { args.kFactorKNN = atoi(optarg);                }  break;
            case LPR_NOOCRTEXTUALFIXES:          args.NoOcrTextualFixes = true;                                  break;
            case LPR_NOOCRKNNFIXES:              args.NoOcrKnnFixes = true;                                      break;
            case LPR_NOOCRDIGITSONLY:            args.NoOcrDigitsOnly = true;                                    break;
            case LPR_POLICETEMPLATE:             if (optarg) { args.PoliceTemplate = optarg;                  }  break;
            case LPR_POLICETEMPLATETHR:          if (optarg) { args.PoliceTemplateThr.set_xy(optarg);         }  break;
            case LPR_ONVIFIP:                    if (optarg) { args.onvif_ip = optarg;                        }  break;
            case LPR_ONVIFPORT:                  if (optarg) { args.onvif_port = atoi(optarg);                }  break;
            case LPR_ONVIFUSER:                  if (optarg) { args.onvif_user = optarg;                      }  break;
            case LPR_ONVIFPASSWD:                if (optarg) { args.onvif_passwd = optarg;                    }  break;
            case LPR_ONVIFTEST:                  args.onvif_test = true;                                         break;
            case LPR_CONFIDENCETHR:              if (optarg) { args.confidence_thr = atof(optarg);            }  break;
            case LPR_IMGENHANCEMENTMODE:         if (optarg) { args.imgEnhancementMode = imgEnhancement_mode_t(atoi(optarg)); } break;
            case LPR_PREPROCESSPWARPPNT0:        if (optarg) { args.pWarpPnt0.set_xy(optarg);                 }  break;
            case LPR_PREPROCESSPWARPPNT1:        if (optarg) { args.pWarpPnt1.set_xy(optarg);                 }  break;
            case LPR_PREPROCESSPWARPPNT2:        if (optarg) { args.pWarpPnt2.set_xy(optarg);                 }  break;
            case LPR_PREPROCESSPWARPPNT3:        if (optarg) { args.pWarpPnt3.set_xy(optarg);                 }  break;
            case LPR_BLUEMAXTHRH:                args.blueMaxThrH = atof(optarg);;                               break;
            case LPR_BLUEMINTHRS:                args.blueMinThrS = atof(optarg);;                               break;
            case LPR_BATCH:                      args.batchMode = true;                                          break;
            case LPR_OPMODE:                     if (optarg) { args.OpMode = optarg;                          }  break;
            case LPR_DEBUG:                      args.debugMode = true;                                          break;
        }
    }

    if (args.onvif_test) {
        onvif_snapshot_test();
        return 0;
    }

    // Sweep definition:
    std::vector<sweep_t> sweep, *sweep_ptr=NULL;
    sweep.push_back(sweep_st(1, 13, 2));  //args.PreprocessThreshweight
    sweep.push_back(sweep_st(9, 23, 2));  //args.PreprocessThreshBlockSize
    if (!args.debugMode) {
        sweep_ptr = &sweep;
    }
    
    // Create a working environment (if not in sweep mode):
    if (!sweep_ptr) {
        std::string envpath = get_envpath(args.ImageFile);  // lpr_results_%d%m%y_%H%M%S_imgFile

        if (opendir(envpath.c_str()) == NULL) {
            std::string cmd = "mkdir " + envpath;
            system(cmd.c_str());
        }
        chdir(envpath.c_str());
    }
    
    // Load input scene image:
    cv::Mat imgOriginalScene = load_input_scene_image(args.ImageFile, "Image",
                                                      args.onvif_ip, args.onvif_port, args.onvif_user, args.onvif_passwd);
 
    // KNN Classifier generation (+training):
    train_knn_classifier(args);

    // LPR Decoding:
    cv::Mat LPimg;
    double confidence=0;
    bool engine_type=false;
    frame_dec_t res_opt = frame_dec_st(LPimg, confidence, engine_type);
    std::string lpr_result = frame_decoder(imgOriginalScene, args, sweep_ptr, res_opt);  //use sweep_ptr==NULL for utilizing a single default working-point (legacy)
    if (res_opt.engine_type) {
        sprintf(buffer, "LPR Result: %s (type=%d)", lpr_result.c_str(), res_opt.engine_type);
    } 
    else {
        sprintf(buffer, "LPR Result: %s (type=%d, conf=%.2f)", lpr_result.c_str(), res_opt.engine_type, res_opt.confidence);
    }
    info(buffer);

    // Epilog:
    t1 = std::clock();
    t_elapsed_sec = (t1 - t0) / (double)CLOCKS_PER_SEC;
    std::cout << "Done! (" << std::setprecision(2) << t_elapsed_sec << " sec)" << std::endl;

    return 0;
}

// ------------------------------------------------------------------------------------------------------------------------------
std::string get_envpath(std::string ImageFile) {

    time_t rawtime = std::time(nullptr);
    time(&rawtime);
    const auto timeinfo = localtime(&rawtime);
    char day_buf[50];  sprintf(day_buf,  "%02d", timeinfo->tm_mday);
    char mon_buf[50];  sprintf(mon_buf,  "%02d", timeinfo->tm_mon);
    char hour_buf[50]; sprintf(hour_buf, "%02d", timeinfo->tm_hour);
    char min_buf[50];  sprintf(min_buf,  "%02d", timeinfo->tm_min);
    char sec_buf[50];  sprintf(sec_buf,  "%02d", timeinfo->tm_sec);
    std::string timestr = std::string(day_buf) + std::string(mon_buf) + std::to_string(timeinfo->tm_year%100) + "_" +
                          std::string(hour_buf) + std::string(min_buf) + std::string(sec_buf);
    #if defined(WIN32) || defined(_WIN32) || defined(__WIN32) && !defined(__CYGWIN__)
    std::size_t found1 = ImageFile.rfind("\");
    #else
    std::size_t found1 = ImageFile.rfind("/");
    #endif
    std::string img_str = "imgNA";
    if (found1 != std::string::npos) {
        img_str = ImageFile.substr(found1+1);
        std::size_t found2 = img_str.rfind(".");
        if (found2 != std::string::npos) {
            img_str.replace(found2,1,"_");
        }
    }
    std::string envpath = "lpr_results_" + timestr + "_" + img_str;

    return envpath;
}

// ------------------------------------------------------------------------------------------------------------------------------
void usage(char *script_name) {

    std::cout << script_name << " -i [image_file]" << std::endl;
    std::cout << std::endl;
    std::cout << "Optional preprocssing flags:                  --imgEnhancementMode --PreprocessGaussKernel --PreprocessThreshBlockSize" << std::endl;
    std::cout << "Optional preprocssing flags (cont.):          --PreprocessThreshweight --PreprocessMorphKernel --PreprocessZoomIn --blueMaxThrH --blueMinThrS" << std::endl;
    std::cout << "Optional preprocssing flags (cont.):          --PerspectiveWarp0 --PerspectiveWarp1 --PerspectiveWarp2 --PerspectiveWarp3" << std::endl;
    std::cout << "Optional plate-detection flags:               --PlateWidthPaddingFactor --PlateHeightPaddingFactor --FindRectangledPlate" << std::endl;
    std::cout << "Optional plate-detection flags (cont.):       --MinPixelWidth --MaxPixelWidth --MinPixelHeight --MaxPixelHeight" << std::endl;
    std::cout << "Optional plate-detection flags (cont.):       --MinAspectRatio --MaxAspectRatio --MinPixelArea --MaxPixelArea" << std::endl;
    std::cout << "Optional characters-detection flags:          --MinDiagSizeMultipleAway --MaxDiagSizeMultipleAway --MinChangeInArea --MaxChangeInArea" << std::endl;
    std::cout << "Optional characters-detection flags (cont.):  --MinChangeInWidth --MaxChangeInWidth --MinChangeInHeight --MaxChangeInHeight --MinHistNormThr" << std::endl;
    std::cout << "Optional characters-detection flags (cont.):  --MinAngleBetweenChars --MaxAngleBetweenChars --MinNumberOfMatchingChars --MaxNumberOfMatchingChars" << std::endl;
    std::cout << "Optional characters-detection flags (cont.):  --ResizedCharImageWidth --ResizedCharImageHeight --kFactorKNN" << std::endl;
    std::cout << "Optional characters-detection flags (cont.):  --NoVerticalAlign --NoOcrTextualFixes --NoOcrKnnFixes --NoOcrDigitsOnly" << std::endl;
    std::cout << "Optional ONVIF parameters:                    --onvif_ip --onvif_port --onvif_user --onvif_passwd --onvif_test" << std::endl;
    std::cout << "Optional misc. flags:                         --confidence_thr --PoliceTemplate --PoliceTemplateThr --ROI" << std::endl;
    std::cout << "Optional misc. flags (cont.):                 --batch --mode --debug --version" << std::endl;
    std::cout << std::endl;
    std::cout << "Note about ROI settings:" << std::endl;
    std::cout << "   ROI = (startX, startY, width, height)" << std::endl;
    std::cout << "   setting ROI to (0,0) will set ROI to be equals to the whole input image" << std::endl;
    std::cout << "   setting ROI to (-1,-1) will set the system into autoROI mode, i.e. ROI euals to 20%-(60%)-20% x 40%-(50%)-10%" << std::endl;
    std::cout << std::endl;
}

