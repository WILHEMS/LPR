#!/bin/sh

base='/Users/shahargino/Documents/ImageProcessing'

default_args='--batch --imgEnhancementMode=2 --mode="no_police" --ROI="(10,250,1700,500)" --confidence_thr=0.1 --PreprocessZoomIn=1.3 --PlateWidthPaddingFactor=1.2 --PreprocessMorphKernel="(1,1)"'

LPR_test() {
  res=`build/lpr -i $1 $default_args $3 | grep "LPR Result: "`
  pass=`echo $res | grep -w $2`
  act=`echo $res | cut -d" " -f4`
  info=`echo $res | cut -d" " -f5-`
  ((cnt++))
  ((imgs++))
  if [[ -n "$pass" ]]; then
    ((pcnt++))
    echo "$1 PASSED!\t(pass=$pcnt/$cnt)\t$info\t$3"
  else
    printf "$1 FAILED!\t(pass=$pcnt/$cnt)\t$info\t(ACT=$act EXP=$2)\t$4\n"
  fi

  lpr=`echo $res | cut -d" " -f4`
  vals=("${vals[@]}" "$lpr")
}

StartCase() {
  cnt=0; 
  pcnt=0;
  vals=()
}

EndCase() {
  ((cases++))
  passRate=`echo "scale=2; 100*$pcnt/$cnt" | bc`
  uniqVals=$(echo "${vals[@]}" | tr ' ' '\n' | sort -u)
  uniqVals=(${uniqVals//\n/ })
  printf "Case #$cases: PassRate=$passRate%% ($pcnt/$cnt), Hist: "
  casepass=1
  for k in "${uniqVals[@]}"; do
    hist=0
    for v in "${vals[@]}"; do
      if [ "$k" == "$v" ]; then ((hist++)); fi
    done
    printf "$k=$hist,"
    if ([ "$hist" -gt "$pcnt" ] && [ "$k" != "N/A" ]) || [ "$pcnt" -eq 0 ]; then casepass=0; fi
  done
  if [ "$casepass" == 1 ]; then
    printf " --> PASSED!"
    ((casespass++))
  else
    printf " --> FAILED!"
  fi
  printf "\n\n"
  unset vals
}

SECONDS=0
cases=0
casespass=0
imgs=0

#--------------- I M A G E ----------------------------------------|-- Expected --|------- Arguments ------|---- Waivers ----
StartCase
LPR_test "$base/LPR/Database/Real_Images_150818/capture3747.jpeg"     "6785631"
LPR_test "$base/LPR/Database/Real_Images_150818/capture3748.jpeg"     "6785631"
LPR_test "$base/LPR/Database/Real_Images_150818/capture3749.jpeg"     "6785631"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_150818/capture3762.jpeg"     "5248771"
LPR_test "$base/LPR/Database/Real_Images_150818/capture3763.jpeg"     "5248771"
LPR_test "$base/LPR/Database/Real_Images_150818/capture3764.jpeg"     "5248771"    "--PreprocessMorphKernel='(3,3)'"
EndCase

StartCase 
LPR_test "$base/LPR/Database/Real_Images_150818/capture3779.jpeg"     "6265633"    "--NoOcrKnnFixes"                 "KNN OCR Fix disabled"
LPR_test "$base/LPR/Database/Real_Images_150818/capture3781.jpeg"     "6265633"    ""                                "Angled image"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_150818/capture3793.jpeg"     "7304132"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_150818/capture3825.jpeg"     "3402439"    "--NoOcrKnnFixes --PreprocessMorphKernel='(3,3)'"  "Low quality"
LPR_test "$base/LPR/Database/Real_Images_150818/capture3826.jpeg"     "3402439"    "--NoOcrKnnFixes"                 "KNN OCR Fix disabled"
LPR_test "$base/LPR/Database/Real_Images_150818/capture3827.jpeg"     "3402439"    ""                                "Angled image, low quality"
LPR_test "$base/LPR/Database/Real_Images_150818/capture3828.jpeg"     "3402439"    ""                                "Angled image"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_150818/capture3877.jpeg"     "8732737"
LPR_test "$base/LPR/Database/Real_Images_150818/capture3878.jpeg"     "8732737"
LPR_test "$base/LPR/Database/Real_Images_150818/capture3879.jpeg"     "8732737"    ""                                "Angled image"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_150818/capture3898.jpeg"     "18992401"   ""                                "Low quality"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_150818/capture3919.jpeg"     "2464679"    ""                                "Angled image, low quality"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_150818/capture3930.jpeg"     "4629411"
LPR_test "$base/LPR/Database/Real_Images_150818/capture3931.jpeg"     "4629411"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_150818/capture3940.jpeg"     "4136230"
LPR_test "$base/LPR/Database/Real_Images_150818/capture3941.jpeg"     "4136230"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_150818/capture3970.jpeg"     "7144379"
LPR_test "$base/LPR/Database/Real_Images_150818/capture3971.jpeg"     "7144379"
LPR_test "$base/LPR/Database/Real_Images_150818/capture3974.jpeg"     "7144379"    "--PreprocessZoomIn=1.4"          "ZoomIn x4"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_150818/capture3992.jpeg"     "14628501"   "--PreprocessZoomIn=1.4"          "ZoomIn x4"
LPR_test "$base/LPR/Database/Real_Images_150818/capture3993.jpeg"     "14628501"   "--PreprocessZoomIn=1.4"          "ZoomIn x4"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_150818/capture4029.jpeg"     "6320874"    "--PreprocessZoomIn=1.4 --PlateWidthPaddingFactor=1.2 --NoOcrKnnFixes --PreprocessGaussKernel='(1,1)'"   "Angled image" 
LPR_test "$base/LPR/Database/Real_Images_150818/capture4030.jpeg"     "6320874"    ""                                "Angled image, low quality"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_150818/capture4120.jpeg"     "28214201"   "--PreprocessZoomIn=1.4 --NoOcrKnnFixes"  "Angled image"
LPR_test "$base/LPR/Database/Real_Images_150818/capture4121.jpeg"     "28214201"   "--NoOcrKnnFixes --PreprocessMorphKernel='(3,3)'"   "KNN OCR Fix disabled"
LPR_test "$base/LPR/Database/Real_Images_150818/capture4122.jpeg"     "28214201"   ""                                "Angled image"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_150818/capture4355.jpeg"     "4883330"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_150818/capture4380.jpeg"     "7774250"    "--NoOcrKnnFixes --PreprocessMorphKernel='(3,3)'"  "KNN OCR Fix disabled"
LPR_test "$base/LPR/Database/Real_Images_150818/capture4381.jpeg"     "7774250"    ""                                "Blurred image"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_150818/capture4513.jpeg"     "2777885"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_150818/capture4586.jpeg"     "6356554"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_150818/capture4683.jpeg"     "6807312"
EndCase

secPerImg=`echo "scale=2; 100*$SECONDS/$imgs" | bc`
casespassRate=`echo "scale=2; 100*$casespass/$cases" | bc`
printf "Summary:  Cases PassRate=$casespassRate%% ($casespass/$cases)\n"
printf "Elapsed time: ${SECONDS}sec (${secPerImg}sec per image )\n\n"
