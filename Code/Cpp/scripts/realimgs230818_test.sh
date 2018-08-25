#!/bin/sh

base='/Users/shahargino/Documents/ImageProcessing'

default_args='--batch --imgEnhancementMode=2 --mode="no_police" --ROI="(10,250,1260,500)" --confidence_thr=0.1 --PerspectiveWarp0="(0,0)" --PerspectiveWarp1="(1260,100)" --PerspectiveWarp2="(1260,600)" --PerspectiveWarp3="(0,500)"'

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

#--------------- I M A G E ---------------------------------|-- Expected --|------- Arguments ------|------------------- Waivers -------------------
StartCase
LPR_test "$base/LPR/Database/Real_Images_230818/in/1.jpeg"      "5991131"              ""               "Angled view + Last digit is partly erased"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_230818/in/2.jpeg"      "3901173"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_230818/in/3.jpeg"      "2212432"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_230818/in/4.jpeg"      "2464679"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_230818/in/5.jpeg"      "2946974"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_230818/in/6.jpeg"      "4766266"
LPR_test "$base/LPR/Database/Real_Images_230818/out/9.jpeg"     "4766266"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_230818/in/7.jpeg"      "5714272"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_230818/in/9.jpeg"      "6807312"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_230818/in/10.jpeg"     "2081271"
LPR_test "$base/LPR/Database/Real_Images_230818/in/11.jpeg"     "2081271"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_230818/in/12.jpeg"     "7774250"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_230818/in/13.jpeg"     "1930639"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_230818/in/14.jpeg"     "8853153"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_230818/in/15.jpeg"     "9985378"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_230818/in/16.jpeg"     "4314528"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_230818/in/17.jpeg"     "9775039"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_230818/out/1.jpeg"     "1749362"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_230818/out/2.jpeg"     "3414437"
LPR_test "$base/LPR/Database/Real_Images_230818/out/5.jpeg"     "3414437"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_230818/out/3.jpeg"     "4457037"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_230818/out/4.jpeg"     "4883330"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_230818/out/6.jpeg"     "2333337"
LPR_test "$base/LPR/Database/Real_Images_230818/out/10.jpeg"    "2333337"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_230818/out/7.jpeg"     "8734113"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_230818/out/8.jpeg"     "6356554"
EndCase

secPerImg=`echo "scale=2; 100*$SECONDS/$imgs" | bc`
casespassRate=`echo "scale=2; 100*$casespass/$cases" | bc`
printf "Summary:  Cases PassRate=$casespassRate%% ($casespass/$cases)\n"
printf "Elapsed time: ${SECONDS}sec (${secPerImg}sec per image )\n\n"
