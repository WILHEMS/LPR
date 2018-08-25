#!/bin/sh

base='/Users/shahargino/Documents/ImageProcessing'

default_args='--batch --ROI="(0,0,960,324)" --imgEnhancementMode=1 --mode=="no_police"'

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

#--------------- I M A G E ----------------------------|-- Expected --|------- Arguments ------|---- Waivers ----
StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/0.jpg"    "6190555" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/1.jpg"    "6190555"
LPR_test "$base/LPR/Database/Real_ROImage_270917/2.jpg"    "6190555"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/3.jpg"    "4067953"
LPR_test "$base/LPR/Database/Real_ROImage_270917/4.jpg"    "4067953"
LPR_test "$base/LPR/Database/Real_ROImage_270917/5.jpg"    "4067953"
LPR_test "$base/LPR/Database/Real_ROImage_270917/6.jpg"    "4067953"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/7.jpg"    "6045538" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/8.jpg"    "6045538" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/9.jpg"    "6045538" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/10.jpg"   "6045538" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/11.jpg"   "6045538" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/12.jpg"   "6045538" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/13.jpg"   "6045538" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/14.jpg"   "6045538" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/15.jpg"   "6045538" 
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/16.jpg"   "4852034" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/17.jpg"   "4852034" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/18.jpg"   "4852034" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/19.jpg"   "4852034" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/20.jpg"   "4852034" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/21.jpg"   "4852034" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/22.jpg"   "4852034" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/23.jpg"   "4852034" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/24.jpg"   "4852034" 
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/25.jpg"   "6604785" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/26.jpg"   "6604785" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/27.jpg"   "6604785" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/28.jpg"   "6604785" 
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/29.jpg"   "3840678" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/30.jpg"   "3840678" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/31.jpg"   "3840678" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/32.jpg"   "3840678" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/33.jpg"   "3840678" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/34.jpg"   "3840678" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/35.jpg"   "3840678" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/36.jpg"   "3840678" 
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/37.jpg"   "2179132" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/38.jpg"   "2179132" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/39.jpg"   "2179132" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/40.jpg"   "2179132" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/41.jpg"   "2179132" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/42.jpg"   "2179132" 
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/43.jpg"   "4300238"
LPR_test "$base/LPR/Database/Real_ROImage_270917/44.jpg"   "4300238"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/45.jpg"   "5532469"
LPR_test "$base/LPR/Database/Real_ROImage_270917/46.jpg"   "5532469"
LPR_test "$base/LPR/Database/Real_ROImage_270917/47.jpg"   "5532469"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/48.jpg"   "2084162" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/49.jpg"   "2084162" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/50.jpg"   "2084162" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/51.jpg"   "2084162" 
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/52.jpg"   "8145211"
LPR_test "$base/LPR/Database/Real_ROImage_270917/53.jpg"   "8145211"
LPR_test "$base/LPR/Database/Real_ROImage_270917/54.jpg"   "8145211"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/55.jpg"   "2126363"
LPR_test "$base/LPR/Database/Real_ROImage_270917/56.jpg"   "2126363"
LPR_test "$base/LPR/Database/Real_ROImage_270917/57.jpg"   "2126363"
LPR_test "$base/LPR/Database/Real_ROImage_270917/58.jpg"   "2126363"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/59.jpg"   "8531813"
LPR_test "$base/LPR/Database/Real_ROImage_270917/60.jpg"   "8531813"
LPR_test "$base/LPR/Database/Real_ROImage_270917/61.jpg"   "8531813"
LPR_test "$base/LPR/Database/Real_ROImage_270917/62.jpg"   "8531813"
LPR_test "$base/LPR/Database/Real_ROImage_270917/63.jpg"   "8531813"
LPR_test "$base/LPR/Database/Real_ROImage_270917/64.jpg"   "8531813"
LPR_test "$base/LPR/Database/Real_ROImage_270917/65.jpg"   "8531813"
LPR_test "$base/LPR/Database/Real_ROImage_270917/66.jpg"   "8531813"
LPR_test "$base/LPR/Database/Real_ROImage_270917/67.jpg"   "8531813"
LPR_test "$base/LPR/Database/Real_ROImage_270917/68.jpg"   "8531813"
LPR_test "$base/LPR/Database/Real_ROImage_270917/69.jpg"   "8531813"
LPR_test "$base/LPR/Database/Real_ROImage_270917/70.jpg"   "8531813"
LPR_test "$base/LPR/Database/Real_ROImage_270917/71.jpg"   "8531813"
LPR_test "$base/LPR/Database/Real_ROImage_270917/72.jpg"   "8531813"
LPR_test "$base/LPR/Database/Real_ROImage_270917/73.jpg"   "8531813"
LPR_test "$base/LPR/Database/Real_ROImage_270917/74.jpg"   "8531813"
LPR_test "$base/LPR/Database/Real_ROImage_270917/75.jpg"   "8531813"
LPR_test "$base/LPR/Database/Real_ROImage_270917/76.jpg"   "8531813"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/79.jpg"   "3914476"
LPR_test "$base/LPR/Database/Real_ROImage_270917/80.jpg"   "3914476"
LPR_test "$base/LPR/Database/Real_ROImage_270917/81.jpg"   "3015434"
LPR_test "$base/LPR/Database/Real_ROImage_270917/82.jpg"   "3015434"
LPR_test "$base/LPR/Database/Real_ROImage_270917/83.jpg"   "3015434"
LPR_test "$base/LPR/Database/Real_ROImage_270917/84.jpg"   "3015434"
LPR_test "$base/LPR/Database/Real_ROImage_270917/85.jpg"   "3015434"
LPR_test "$base/LPR/Database/Real_ROImage_270917/86.jpg"   "3015434"
LPR_test "$base/LPR/Database/Real_ROImage_270917/87.jpg"   "3015434"
LPR_test "$base/LPR/Database/Real_ROImage_270917/88.jpg"   "3015434"
LPR_test "$base/LPR/Database/Real_ROImage_270917/89.jpg"   "3015434"
LPR_test "$base/LPR/Database/Real_ROImage_270917/90.jpg"   "3015434"
LPR_test "$base/LPR/Database/Real_ROImage_270917/91.jpg"   "3015434"
LPR_test "$base/LPR/Database/Real_ROImage_270917/92.jpg"   "3015434"
LPR_test "$base/LPR/Database/Real_ROImage_270917/93.jpg"   "3015434"
LPR_test "$base/LPR/Database/Real_ROImage_270917/94.jpg"   "3015434"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/96.jpg"   "5063175"
LPR_test "$base/LPR/Database/Real_ROImage_270917/97.jpg"   "5063175"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/98.jpg"   "6653550"
LPR_test "$base/LPR/Database/Real_ROImage_270917/99.jpg"   "6653550"
LPR_test "$base/LPR/Database/Real_ROImage_270917/100.jpg"  "6653550"
LPR_test "$base/LPR/Database/Real_ROImage_270917/101.jpg"  "6653550"
LPR_test "$base/LPR/Database/Real_ROImage_270917/102.jpg"  "6653550"
LPR_test "$base/LPR/Database/Real_ROImage_270917/103.jpg"  "6653550"
LPR_test "$base/LPR/Database/Real_ROImage_270917/104.jpg"  "6653550"
LPR_test "$base/LPR/Database/Real_ROImage_270917/105.jpg"  "6653550"
LPR_test "$base/LPR/Database/Real_ROImage_270917/106.jpg"  "6653550"
LPR_test "$base/LPR/Database/Real_ROImage_270917/107.jpg"  "6653550"
LPR_test "$base/LPR/Database/Real_ROImage_270917/108.jpg"  "6653550"
LPR_test "$base/LPR/Database/Real_ROImage_270917/109.jpg"  "6653550"
LPR_test "$base/LPR/Database/Real_ROImage_270917/110.jpg"  "6653550"
LPR_test "$base/LPR/Database/Real_ROImage_270917/111.jpg"  "6653550"
LPR_test "$base/LPR/Database/Real_ROImage_270917/112.jpg"  "6653550"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/114.jpg"  "5906770"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/115.jpg"  "1950174"
LPR_test "$base/LPR/Database/Real_ROImage_270917/116.jpg"  "1950174"
LPR_test "$base/LPR/Database/Real_ROImage_270917/117.jpg"  "1950174"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/118.jpg"  "5661780"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/119.jpg"  "8213437"
LPR_test "$base/LPR/Database/Real_ROImage_270917/120.jpg"  "8213437"
LPR_test "$base/LPR/Database/Real_ROImage_270917/121.jpg"  "8213437"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/122.jpg"  "8718072"
LPR_test "$base/LPR/Database/Real_ROImage_270917/123.jpg"  "8718072"
LPR_test "$base/LPR/Database/Real_ROImage_270917/124.jpg"  "8718072"
LPR_test "$base/LPR/Database/Real_ROImage_270917/125.jpg"  "8718072"
LPR_test "$base/LPR/Database/Real_ROImage_270917/126.jpg"  "8718072"
LPR_test "$base/LPR/Database/Real_ROImage_270917/127.jpg"  "8718072"
LPR_test "$base/LPR/Database/Real_ROImage_270917/128.jpg"  "8718072"
LPR_test "$base/LPR/Database/Real_ROImage_270917/129.jpg"  "8718072"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/130.jpg"  "2776134"
LPR_test "$base/LPR/Database/Real_ROImage_270917/131.jpg"  "2776134"
LPR_test "$base/LPR/Database/Real_ROImage_270917/132.jpg"  "2776134"
LPR_test "$base/LPR/Database/Real_ROImage_270917/133.jpg"  "2776134"
LPR_test "$base/LPR/Database/Real_ROImage_270917/134.jpg"  "2776134"
LPR_test "$base/LPR/Database/Real_ROImage_270917/135.jpg"  "2776134"
LPR_test "$base/LPR/Database/Real_ROImage_270917/136.jpg"  "2776134"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/137.jpg"  "7063976"
LPR_test "$base/LPR/Database/Real_ROImage_270917/138.jpg"  "7063976"
LPR_test "$base/LPR/Database/Real_ROImage_270917/139.jpg"  "7063976"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/140.jpg"  "7294637"
LPR_test "$base/LPR/Database/Real_ROImage_270917/141.jpg"  "7294637"
LPR_test "$base/LPR/Database/Real_ROImage_270917/142.jpg"  "7294637"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/143.jpg"  "1741734"
LPR_test "$base/LPR/Database/Real_ROImage_270917/144.jpg"  "1741734"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/145.jpg"  "5374581"
LPR_test "$base/LPR/Database/Real_ROImage_270917/146.jpg"  "5374581"
LPR_test "$base/LPR/Database/Real_ROImage_270917/147.jpg"  "5374581"
LPR_test "$base/LPR/Database/Real_ROImage_270917/148.jpg"  "5374581"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/149.jpg"  "5661680"
LPR_test "$base/LPR/Database/Real_ROImage_270917/150.jpg"  "5661680"
LPR_test "$base/LPR/Database/Real_ROImage_270917/151.jpg"  "5661680"
LPR_test "$base/LPR/Database/Real_ROImage_270917/152.jpg"  "5661680"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/154.jpg"  "4480039"
LPR_test "$base/LPR/Database/Real_ROImage_270917/155.jpg"  "4480039"
LPR_test "$base/LPR/Database/Real_ROImage_270917/156.jpg"  "4480039"
LPR_test "$base/LPR/Database/Real_ROImage_270917/157.jpg"  "4480039"
LPR_test "$base/LPR/Database/Real_ROImage_270917/158.jpg"  "4480039"
LPR_test "$base/LPR/Database/Real_ROImage_270917/159.jpg"  "4480039"
LPR_test "$base/LPR/Database/Real_ROImage_270917/160.jpg"  "4480039"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/161.jpg"  "2589064"
LPR_test "$base/LPR/Database/Real_ROImage_270917/162.jpg"  "2589064"
LPR_test "$base/LPR/Database/Real_ROImage_270917/163.jpg"  "2589064"
LPR_test "$base/LPR/Database/Real_ROImage_270917/164.jpg"  "2589064"
LPR_test "$base/LPR/Database/Real_ROImage_270917/165.jpg"  "2589064"
LPR_test "$base/LPR/Database/Real_ROImage_270917/166.jpg"  "2589064"
LPR_test "$base/LPR/Database/Real_ROImage_270917/167.jpg"  "2589064"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/168.jpg"  "4469737"
LPR_test "$base/LPR/Database/Real_ROImage_270917/169.jpg"  "4469737"
LPR_test "$base/LPR/Database/Real_ROImage_270917/170.jpg"  "4469737"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/171.jpg"  "7821584"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/172.jpg"  "8504530"
LPR_test "$base/LPR/Database/Real_ROImage_270917/173.jpg"  "8504530"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/174.jpg"  "9431431"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/175.jpg"  "5620064"
LPR_test "$base/LPR/Database/Real_ROImage_270917/176.jpg"  "5620064"
LPR_test "$base/LPR/Database/Real_ROImage_270917/177.jpg"  "5620064"
LPR_test "$base/LPR/Database/Real_ROImage_270917/178.jpg"  "5620064"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/179.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/180.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/181.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/182.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/183.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/184.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/185.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/186.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/187.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/188.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/189.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/190.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/191.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/192.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/193.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/194.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/195.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/196.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/197.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/198.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/199.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/200.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/201.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/202.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/203.jpg"  "8301930"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/204.jpg"  "25949801"
LPR_test "$base/LPR/Database/Real_ROImage_270917/205.jpg"  "25949801"
LPR_test "$base/LPR/Database/Real_ROImage_270917/206.jpg"  "25949801"
LPR_test "$base/LPR/Database/Real_ROImage_270917/207.jpg"  "25949801"
LPR_test "$base/LPR/Database/Real_ROImage_270917/208.jpg"  "25949801"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/209.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/210.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/211.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/212.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/213.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/214.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/215.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/216.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/217.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/218.jpg"  "8301930"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/219.jpg"  "2958839"
LPR_test "$base/LPR/Database/Real_ROImage_270917/220.jpg"  "2958839"
LPR_test "$base/LPR/Database/Real_ROImage_270917/221.jpg"  "2958839"
LPR_test "$base/LPR/Database/Real_ROImage_270917/222.jpg"  "2958839"
LPR_test "$base/LPR/Database/Real_ROImage_270917/223.jpg"  "2958839"
LPR_test "$base/LPR/Database/Real_ROImage_270917/224.jpg"  "2958839"
LPR_test "$base/LPR/Database/Real_ROImage_270917/225.jpg"  "2958839"
LPR_test "$base/LPR/Database/Real_ROImage_270917/226.jpg"  "2958839"
LPR_test "$base/LPR/Database/Real_ROImage_270917/227.jpg"  "2958839"
LPR_test "$base/LPR/Database/Real_ROImage_270917/228.jpg"  "2958839"
LPR_test "$base/LPR/Database/Real_ROImage_270917/229.jpg"  "2958839"
LPR_test "$base/LPR/Database/Real_ROImage_270917/230.jpg"  "2958839"
LPR_test "$base/LPR/Database/Real_ROImage_270917/231.jpg"  "2958839"
LPR_test "$base/LPR/Database/Real_ROImage_270917/232.jpg"  "2958839"
LPR_test "$base/LPR/Database/Real_ROImage_270917/233.jpg"  "2958839"
LPR_test "$base/LPR/Database/Real_ROImage_270917/234.jpg"  "2958839"
LPR_test "$base/LPR/Database/Real_ROImage_270917/235.jpg"  "2958839"
LPR_test "$base/LPR/Database/Real_ROImage_270917/236.jpg"  "2958839"
LPR_test "$base/LPR/Database/Real_ROImage_270917/237.jpg"  "2958839"
LPR_test "$base/LPR/Database/Real_ROImage_270917/238.jpg"  "2958839"
LPR_test "$base/LPR/Database/Real_ROImage_270917/239.jpg"  "2958839"
LPR_test "$base/LPR/Database/Real_ROImage_270917/240.jpg"  "2958839"
LPR_test "$base/LPR/Database/Real_ROImage_270917/241.jpg"  "2958839"
LPR_test "$base/LPR/Database/Real_ROImage_270917/242.jpg"  "2958839"
LPR_test "$base/LPR/Database/Real_ROImage_270917/243.jpg"  "2958839"
LPR_test "$base/LPR/Database/Real_ROImage_270917/244.jpg"  "2958839"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/245.jpg"  "6552654"
LPR_test "$base/LPR/Database/Real_ROImage_270917/246.jpg"  "6552654"
LPR_test "$base/LPR/Database/Real_ROImage_270917/247.jpg"  "6552654"
LPR_test "$base/LPR/Database/Real_ROImage_270917/248.jpg"  "6552654"
LPR_test "$base/LPR/Database/Real_ROImage_270917/249.jpg"  "6552654"
LPR_test "$base/LPR/Database/Real_ROImage_270917/250.jpg"  "6552654"
LPR_test "$base/LPR/Database/Real_ROImage_270917/251.jpg"  "6552654"
LPR_test "$base/LPR/Database/Real_ROImage_270917/252.jpg"  "6552654"
LPR_test "$base/LPR/Database/Real_ROImage_270917/253.jpg"  "6552654"
LPR_test "$base/LPR/Database/Real_ROImage_270917/254.jpg"  "6552654"
LPR_test "$base/LPR/Database/Real_ROImage_270917/255.jpg"  "6552654"
LPR_test "$base/LPR/Database/Real_ROImage_270917/256.jpg"  "6552654"
LPR_test "$base/LPR/Database/Real_ROImage_270917/257.jpg"  "6552654"
LPR_test "$base/LPR/Database/Real_ROImage_270917/258.jpg"  "6552654"
LPR_test "$base/LPR/Database/Real_ROImage_270917/259.jpg"  "6552654"
LPR_test "$base/LPR/Database/Real_ROImage_270917/260.jpg"  "6552654"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/261.jpg"  "4567779" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/262.jpg"  "4567779" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/263.jpg"  "4567779" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/264.jpg"  "4567779" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/265.jpg"  "4567779" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/266.jpg"  "4567779" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/267.jpg"  "4567779" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/268.jpg"  "4567779" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/269.jpg"  "4567779" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/270.jpg"  "4567779" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/271.jpg"  "4567779" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/272.jpg"  "4567779" 
LPR_test "$base/LPR/Database/Real_ROImage_270917/273.jpg"  "4567779" 
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/274.jpg"  "6297339"
LPR_test "$base/LPR/Database/Real_ROImage_270917/275.jpg"  "6297339"
LPR_test "$base/LPR/Database/Real_ROImage_270917/276.jpg"  "6297339"
LPR_test "$base/LPR/Database/Real_ROImage_270917/277.jpg"  "6297339"
LPR_test "$base/LPR/Database/Real_ROImage_270917/278.jpg"  "6297339"
LPR_test "$base/LPR/Database/Real_ROImage_270917/279.jpg"  "6297339"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/280.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/281.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/282.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/283.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/284.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/285.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/286.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/287.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/288.jpg"  "8301930"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/289.jpg"  "7511613"
LPR_test "$base/LPR/Database/Real_ROImage_270917/290.jpg"  "7511613"
LPR_test "$base/LPR/Database/Real_ROImage_270917/291.jpg"  "7511613"
LPR_test "$base/LPR/Database/Real_ROImage_270917/292.jpg"  "7511613"
LPR_test "$base/LPR/Database/Real_ROImage_270917/293.jpg"  "7511613"
LPR_test "$base/LPR/Database/Real_ROImage_270917/294.jpg"  "7511613"
LPR_test "$base/LPR/Database/Real_ROImage_270917/295.jpg"  "7511613"
LPR_test "$base/LPR/Database/Real_ROImage_270917/296.jpg"  "7511613"
LPR_test "$base/LPR/Database/Real_ROImage_270917/297.jpg"  "7511613"
LPR_test "$base/LPR/Database/Real_ROImage_270917/298.jpg"  "7511613"
LPR_test "$base/LPR/Database/Real_ROImage_270917/299.jpg"  "7511613"
LPR_test "$base/LPR/Database/Real_ROImage_270917/300.jpg"  "7511613"
LPR_test "$base/LPR/Database/Real_ROImage_270917/301.jpg"  "7511613"
LPR_test "$base/LPR/Database/Real_ROImage_270917/302.jpg"  "7511613"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/303.jpg"  "8702530"
LPR_test "$base/LPR/Database/Real_ROImage_270917/304.jpg"  "8702530"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/305.jpg"  "3047434"
LPR_test "$base/LPR/Database/Real_ROImage_270917/306.jpg"  "3047434"
LPR_test "$base/LPR/Database/Real_ROImage_270917/307.jpg"  "3047434"
LPR_test "$base/LPR/Database/Real_ROImage_270917/308.jpg"  "3047434"
LPR_test "$base/LPR/Database/Real_ROImage_270917/309.jpg"  "3047434"
LPR_test "$base/LPR/Database/Real_ROImage_270917/310.jpg"  "3047434"
LPR_test "$base/LPR/Database/Real_ROImage_270917/311.jpg"  "3047434"
LPR_test "$base/LPR/Database/Real_ROImage_270917/312.jpg"  "3047434"
LPR_test "$base/LPR/Database/Real_ROImage_270917/313.jpg"  "3047434"
LPR_test "$base/LPR/Database/Real_ROImage_270917/314.jpg"  "3047434"
LPR_test "$base/LPR/Database/Real_ROImage_270917/315.jpg"  "3047434"
LPR_test "$base/LPR/Database/Real_ROImage_270917/316.jpg"  "3047434"
LPR_test "$base/LPR/Database/Real_ROImage_270917/317.jpg"  "3047434"
LPR_test "$base/LPR/Database/Real_ROImage_270917/318.jpg"  "3047434"
LPR_test "$base/LPR/Database/Real_ROImage_270917/319.jpg"  "3047434"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/320.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/321.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/322.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/323.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/324.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/325.jpg"  "8301930"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/326.jpg"  "6952352"
LPR_test "$base/LPR/Database/Real_ROImage_270917/327.jpg"  "6952352"
LPR_test "$base/LPR/Database/Real_ROImage_270917/328.jpg"  "6952352"
LPR_test "$base/LPR/Database/Real_ROImage_270917/329.jpg"  "6952352"
LPR_test "$base/LPR/Database/Real_ROImage_270917/330.jpg"  "6952352"
LPR_test "$base/LPR/Database/Real_ROImage_270917/331.jpg"  "6952352"
LPR_test "$base/LPR/Database/Real_ROImage_270917/332.jpg"  "6952352"
LPR_test "$base/LPR/Database/Real_ROImage_270917/333.jpg"  "6952352"
LPR_test "$base/LPR/Database/Real_ROImage_270917/334.jpg"  "6952352"
LPR_test "$base/LPR/Database/Real_ROImage_270917/335.jpg"  "6952352"
LPR_test "$base/LPR/Database/Real_ROImage_270917/336.jpg"  "6952352"
LPR_test "$base/LPR/Database/Real_ROImage_270917/337.jpg"  "6952352"
LPR_test "$base/LPR/Database/Real_ROImage_270917/338.jpg"  "6952352"
LPR_test "$base/LPR/Database/Real_ROImage_270917/339.jpg"  "6952352"
LPR_test "$base/LPR/Database/Real_ROImage_270917/340.jpg"  "6952352"
LPR_test "$base/LPR/Database/Real_ROImage_270917/341.jpg"  "6952352"
LPR_test "$base/LPR/Database/Real_ROImage_270917/342.jpg"  "6952352"
LPR_test "$base/LPR/Database/Real_ROImage_270917/343.jpg"  "6952352"
LPR_test "$base/LPR/Database/Real_ROImage_270917/344.jpg"  "6952352"
LPR_test "$base/LPR/Database/Real_ROImage_270917/345.jpg"  "6952352"
LPR_test "$base/LPR/Database/Real_ROImage_270917/346.jpg"  "6952352"
LPR_test "$base/LPR/Database/Real_ROImage_270917/347.jpg"  "6952352"
LPR_test "$base/LPR/Database/Real_ROImage_270917/348.jpg"  "6952352"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/349.jpg"  "4080653"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/350.jpg"  "9312537"
LPR_test "$base/LPR/Database/Real_ROImage_270917/351.jpg"  "9312537"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/352.jpg"  "5798553"
LPR_test "$base/LPR/Database/Real_ROImage_270917/353.jpg"  "5798553"
LPR_test "$base/LPR/Database/Real_ROImage_270917/354.jpg"  "5798553"
LPR_test "$base/LPR/Database/Real_ROImage_270917/355.jpg"  "5798553"
LPR_test "$base/LPR/Database/Real_ROImage_270917/356.jpg"  "5798553"
LPR_test "$base/LPR/Database/Real_ROImage_270917/357.jpg"  "5798553"
LPR_test "$base/LPR/Database/Real_ROImage_270917/358.jpg"  "5798553"
LPR_test "$base/LPR/Database/Real_ROImage_270917/359.jpg"  "5798553"
LPR_test "$base/LPR/Database/Real_ROImage_270917/360.jpg"  "5798553"
LPR_test "$base/LPR/Database/Real_ROImage_270917/361.jpg"  "5798553"
LPR_test "$base/LPR/Database/Real_ROImage_270917/362.jpg"  "5798553"
LPR_test "$base/LPR/Database/Real_ROImage_270917/363.jpg"  "5798553"
LPR_test "$base/LPR/Database/Real_ROImage_270917/364.jpg"  "5798553"
LPR_test "$base/LPR/Database/Real_ROImage_270917/365.jpg"  "5798553"
LPR_test "$base/LPR/Database/Real_ROImage_270917/366.jpg"  "5798553"
LPR_test "$base/LPR/Database/Real_ROImage_270917/367.jpg"  "5798553"
LPR_test "$base/LPR/Database/Real_ROImage_270917/368.jpg"  "5798553"
LPR_test "$base/LPR/Database/Real_ROImage_270917/369.jpg"  "5798553"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/370.jpg"  "7445733"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/371.jpg"  "9312437"
LPR_test "$base/LPR/Database/Real_ROImage_270917/372.jpg"  "9312437"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/373.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/374.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/375.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/377.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/378.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/379.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/380.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/381.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/382.jpg"  "8301930"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/383.jpg"  "8504530"
LPR_test "$base/LPR/Database/Real_ROImage_270917/384.jpg"  "8504530"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/385.jpg"  "7572038"
LPR_test "$base/LPR/Database/Real_ROImage_270917/386.jpg"  "7572038"
LPR_test "$base/LPR/Database/Real_ROImage_270917/387.jpg"  "7572038"
LPR_test "$base/LPR/Database/Real_ROImage_270917/388.jpg"  "7572038"
LPR_test "$base/LPR/Database/Real_ROImage_270917/389.jpg"  "7572038"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/390.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/391.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/392.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/393.jpg"  "8301930"
LPR_test "$base/LPR/Database/Real_ROImage_270917/394.jpg"  "8301930"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/395.jpg"  "1072584"
LPR_test "$base/LPR/Database/Real_ROImage_270917/396.jpg"  "1072584"
LPR_test "$base/LPR/Database/Real_ROImage_270917/397.jpg"  "1072584"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/398.jpg"  "4489634"
LPR_test "$base/LPR/Database/Real_ROImage_270917/399.jpg"  "4489634"
LPR_test "$base/LPR/Database/Real_ROImage_270917/400.jpg"  "4489634"
LPR_test "$base/LPR/Database/Real_ROImage_270917/401.jpg"  "4489634"
LPR_test "$base/LPR/Database/Real_ROImage_270917/402.jpg"  "4489634"
LPR_test "$base/LPR/Database/Real_ROImage_270917/403.jpg"  "4489634"
LPR_test "$base/LPR/Database/Real_ROImage_270917/404.jpg"  "4489634"
LPR_test "$base/LPR/Database/Real_ROImage_270917/405.jpg"  "4489634"
LPR_test "$base/LPR/Database/Real_ROImage_270917/406.jpg"  "4489634"
LPR_test "$base/LPR/Database/Real_ROImage_270917/407.jpg"  "4489634"
LPR_test "$base/LPR/Database/Real_ROImage_270917/408.jpg"  "4489634"
LPR_test "$base/LPR/Database/Real_ROImage_270917/409.jpg"  "4489634"
LPR_test "$base/LPR/Database/Real_ROImage_270917/410.jpg"  "4489634"
LPR_test "$base/LPR/Database/Real_ROImage_270917/411.jpg"  "4489634"
LPR_test "$base/LPR/Database/Real_ROImage_270917/412.jpg"  "4489634"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/413.jpg"  "8410634"
LPR_test "$base/LPR/Database/Real_ROImage_270917/414.jpg"  "8410634"
LPR_test "$base/LPR/Database/Real_ROImage_270917/415.jpg"  "8410634"
LPR_test "$base/LPR/Database/Real_ROImage_270917/416.jpg"  "8410634"
LPR_test "$base/LPR/Database/Real_ROImage_270917/417.jpg"  "8410634"
LPR_test "$base/LPR/Database/Real_ROImage_270917/418.jpg"  "8410634"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/419.jpg"  "8423312"
LPR_test "$base/LPR/Database/Real_ROImage_270917/420.jpg"  "8423312"
LPR_test "$base/LPR/Database/Real_ROImage_270917/421.jpg"  "8423312"
LPR_test "$base/LPR/Database/Real_ROImage_270917/422.jpg"  "8423312"
LPR_test "$base/LPR/Database/Real_ROImage_270917/423.jpg"  "8423312"
LPR_test "$base/LPR/Database/Real_ROImage_270917/424.jpg"  "8423312"
LPR_test "$base/LPR/Database/Real_ROImage_270917/425.jpg"  "8423312"
LPR_test "$base/LPR/Database/Real_ROImage_270917/426.jpg"  "8423312"
LPR_test "$base/LPR/Database/Real_ROImage_270917/427.jpg"  "8423312"
LPR_test "$base/LPR/Database/Real_ROImage_270917/428.jpg"  "8423312"
LPR_test "$base/LPR/Database/Real_ROImage_270917/429.jpg"  "8423312"
LPR_test "$base/LPR/Database/Real_ROImage_270917/430.jpg"  "8423312"
LPR_test "$base/LPR/Database/Real_ROImage_270917/431.jpg"  "8423312"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_ROImage_270917/432.jpg"  "5910680"
EndCase

secPerImg=`echo "scale=2; 100*$SECONDS/$imgs" | bc`
casespassRate=`echo "scale=2; 100*$casespass/$cases" | bc`
printf "Summary:  Cases PassRate=$casespassRate%% ($casespass/$cases)\n"
printf "Elapsed time: ${SECONDS}sec (${secPerImg}sec per image )\n\n"
