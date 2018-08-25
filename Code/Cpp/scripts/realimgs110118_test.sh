#!/bin/sh

base='/Users/shahargino/Documents/ImageProcessing'

default_args='--batch --imgEnhancementMode --mode="no_police" --ROI="(10,300,1700,500)" --MinAspectRatio=0.2 --PreprocessMorphKernel="(1,1)"'

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
LPR_test "$base/LPR/Database/Real_Images_110118/0.jpg"     "1237233"
LPR_test "$base/LPR/Database/Real_Images_110118/1.jpg"     "1237233"
LPR_test "$base/LPR/Database/Real_Images_110118/2.jpg"     "1237233"
LPR_test "$base/LPR/Database/Real_Images_110118/3.jpg"     "1237233"
LPR_test "$base/LPR/Database/Real_Images_110118/4.jpg"     "1237233"
LPR_test "$base/LPR/Database/Real_Images_110118/5.jpg"     "1237233"
LPR_test "$base/LPR/Database/Real_Images_110118/6.jpg"     "1237233"
LPR_test "$base/LPR/Database/Real_Images_110118/7.jpg"     "1237233"
LPR_test "$base/LPR/Database/Real_Images_110118/8.jpg"     "1237233"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/9.jpg"     "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/10.jpg"    "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/11.jpg"    "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/12.jpg"    "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/13.jpg"    "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/14.jpg"    "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/15.jpg"    "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/16.jpg"    "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/17.jpg"    "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/18.jpg"    "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/19.jpg"    "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/20.jpg"    "5229537"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/21.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/22.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/23.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/24.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/25.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/26.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/27.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/28.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/29.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/30.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/31.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/32.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/33.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/34.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/35.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/36.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/37.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/38.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/39.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/40.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/41.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/42.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/43.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/44.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/45.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/46.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/47.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/48.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/49.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/50.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/51.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/52.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/53.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/54.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/55.jpg"    "9713352"
LPR_test "$base/LPR/Database/Real_Images_110118/56.jpg"    "9713352"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/57.jpg"    "4606355"
LPR_test "$base/LPR/Database/Real_Images_110118/58.jpg"    "4606355"
LPR_test "$base/LPR/Database/Real_Images_110118/59.jpg"    "4606355"
LPR_test "$base/LPR/Database/Real_Images_110118/60.jpg"    "4606355"
LPR_test "$base/LPR/Database/Real_Images_110118/61.jpg"    "4606355"
LPR_test "$base/LPR/Database/Real_Images_110118/62.jpg"    "4606355"
LPR_test "$base/LPR/Database/Real_Images_110118/63.jpg"    "4606355"
LPR_test "$base/LPR/Database/Real_Images_110118/64.jpg"    "4606355"
LPR_test "$base/LPR/Database/Real_Images_110118/65.jpg"    "4606355"
LPR_test "$base/LPR/Database/Real_Images_110118/66.jpg"    "4606355"
LPR_test "$base/LPR/Database/Real_Images_110118/67.jpg"    "4606355"
LPR_test "$base/LPR/Database/Real_Images_110118/68.jpg"    "4606355"
LPR_test "$base/LPR/Database/Real_Images_110118/69.jpg"    "4606355"
LPR_test "$base/LPR/Database/Real_Images_110118/70.jpg"    "4606355"
LPR_test "$base/LPR/Database/Real_Images_110118/71.jpg"    "4606355"
LPR_test "$base/LPR/Database/Real_Images_110118/72.jpg"    "4606355"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/73.jpg"    "1332967"
LPR_test "$base/LPR/Database/Real_Images_110118/74.jpg"    "1332967"
LPR_test "$base/LPR/Database/Real_Images_110118/75.jpg"    "1332967"
LPR_test "$base/LPR/Database/Real_Images_110118/76.jpg"    "1332967"
LPR_test "$base/LPR/Database/Real_Images_110118/77.jpg"    "1332967"
LPR_test "$base/LPR/Database/Real_Images_110118/78.jpg"    "1332967"
LPR_test "$base/LPR/Database/Real_Images_110118/79.jpg"    "1332967"
LPR_test "$base/LPR/Database/Real_Images_110118/80.jpg"    "1332967"
LPR_test "$base/LPR/Database/Real_Images_110118/81.jpg"    "1332967"
LPR_test "$base/LPR/Database/Real_Images_110118/82.jpg"    "1332967"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/83.jpg"    "4249559"             ""              "Poor Resolution + digits touches plate border"
LPR_test "$base/LPR/Database/Real_Images_110118/84.jpg"    "4249559"             ""              "Poor Resolution + digits touches plate border"
LPR_test "$base/LPR/Database/Real_Images_110118/85.jpg"    "4249559"             ""              "Poor Resolution + digits touches plate border"
LPR_test "$base/LPR/Database/Real_Images_110118/86.jpg"    "4249559"             ""              "Poor Resolution + digits touches plate border"
LPR_test "$base/LPR/Database/Real_Images_110118/87.jpg"    "4249559"             ""              "Poor Resolution + digits touches plate border"
LPR_test "$base/LPR/Database/Real_Images_110118/88.jpg"    "4249559"             ""              "Poor Resolution + digits touches plate border"
LPR_test "$base/LPR/Database/Real_Images_110118/89.jpg"    "4249559"             ""              "Poor Resolution + digits touches plate border"
LPR_test "$base/LPR/Database/Real_Images_110118/90.jpg"    "4249559"             ""              "Poor Resolution + digits touches plate border"
LPR_test "$base/LPR/Database/Real_Images_110118/91.jpg"    "4249559"             ""              "Poor Resolution + digits touches plate border"
LPR_test "$base/LPR/Database/Real_Images_110118/92.jpg"    "4249559"             ""              "Poor Resolution + digits touches plate border"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/93.jpg"    "7044112"
LPR_test "$base/LPR/Database/Real_Images_110118/94.jpg"    "7044112"
LPR_test "$base/LPR/Database/Real_Images_110118/95.jpg"    "7044112"
LPR_test "$base/LPR/Database/Real_Images_110118/96.jpg"    "7044112"
LPR_test "$base/LPR/Database/Real_Images_110118/97.jpg"    "7044112"
LPR_test "$base/LPR/Database/Real_Images_110118/98.jpg"    "7044112"
LPR_test "$base/LPR/Database/Real_Images_110118/99.jpg"    "7044112"
LPR_test "$base/LPR/Database/Real_Images_110118/100.jpg"   "7044112"
LPR_test "$base/LPR/Database/Real_Images_110118/101.jpg"   "7044112"
LPR_test "$base/LPR/Database/Real_Images_110118/102.jpg"   "7044112"
LPR_test "$base/LPR/Database/Real_Images_110118/103.jpg"   "7044112"
LPR_test "$base/LPR/Database/Real_Images_110118/104.jpg"   "7044112"
LPR_test "$base/LPR/Database/Real_Images_110118/105.jpg"   "7044112"
LPR_test "$base/LPR/Database/Real_Images_110118/106.jpg"   "7044112"
LPR_test "$base/LPR/Database/Real_Images_110118/107.jpg"   "7044112"
LPR_test "$base/LPR/Database/Real_Images_110118/108.jpg"   "7044112"
LPR_test "$base/LPR/Database/Real_Images_110118/109.jpg"   "7044112"
LPR_test "$base/LPR/Database/Real_Images_110118/110.jpg"   "7044112"
LPR_test "$base/LPR/Database/Real_Images_110118/111.jpg"   "7044112"
LPR_test "$base/LPR/Database/Real_Images_110118/112.jpg"   "7044112"
LPR_test "$base/LPR/Database/Real_Images_110118/113.jpg"   "7044112"
LPR_test "$base/LPR/Database/Real_Images_110118/114.jpg"   "7044112"
LPR_test "$base/LPR/Database/Real_Images_110118/115.jpg"   "7044112"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/116.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/117.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/118.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/119.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/120.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/121.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/122.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/123.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/124.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/125.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/126.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/127.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/128.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/129.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/130.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/131.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/132.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/133.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/134.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/135.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/136.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/137.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/138.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/139.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/140.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/141.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/142.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/143.jpg"   "5229537"
LPR_test "$base/LPR/Database/Real_Images_110118/144.jpg"   "5229537"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/145.jpg"   "2885233"
LPR_test "$base/LPR/Database/Real_Images_110118/146.jpg"   "2885233"
LPR_test "$base/LPR/Database/Real_Images_110118/147.jpg"   "2885233"
LPR_test "$base/LPR/Database/Real_Images_110118/148.jpg"   "2885233"
LPR_test "$base/LPR/Database/Real_Images_110118/149.jpg"   "2885233"
LPR_test "$base/LPR/Database/Real_Images_110118/150.jpg"   "2885233"
LPR_test "$base/LPR/Database/Real_Images_110118/151.jpg"   "2885233"
LPR_test "$base/LPR/Database/Real_Images_110118/152.jpg"   "2885233"
LPR_test "$base/LPR/Database/Real_Images_110118/153.jpg"   "2885233"
LPR_test "$base/LPR/Database/Real_Images_110118/154.jpg"   "2885233"
LPR_test "$base/LPR/Database/Real_Images_110118/155.jpg"   "2885233"
LPR_test "$base/LPR/Database/Real_Images_110118/156.jpg"   "2885233"
LPR_test "$base/LPR/Database/Real_Images_110118/157.jpg"   "2885233"
LPR_test "$base/LPR/Database/Real_Images_110118/158.jpg"   "2885233"
LPR_test "$base/LPR/Database/Real_Images_110118/159.jpg"   "2885233"
LPR_test "$base/LPR/Database/Real_Images_110118/160.jpg"   "2885233"
LPR_test "$base/LPR/Database/Real_Images_110118/161.jpg"   "2885233"
LPR_test "$base/LPR/Database/Real_Images_110118/162.jpg"   "2885233"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/163.jpg"   "2922761"
LPR_test "$base/LPR/Database/Real_Images_110118/164.jpg"   "2922761"
LPR_test "$base/LPR/Database/Real_Images_110118/165.jpg"   "2922761"
LPR_test "$base/LPR/Database/Real_Images_110118/166.jpg"   "2922761"
LPR_test "$base/LPR/Database/Real_Images_110118/167.jpg"   "2922761"
LPR_test "$base/LPR/Database/Real_Images_110118/168.jpg"   "2922761"
LPR_test "$base/LPR/Database/Real_Images_110118/169.jpg"   "2922761"
LPR_test "$base/LPR/Database/Real_Images_110118/170.jpg"   "2922761"
LPR_test "$base/LPR/Database/Real_Images_110118/171.jpg"   "2922761"
LPR_test "$base/LPR/Database/Real_Images_110118/172.jpg"   "2922761"
LPR_test "$base/LPR/Database/Real_Images_110118/173.jpg"   "2922761"
LPR_test "$base/LPR/Database/Real_Images_110118/174.jpg"   "2922761"
LPR_test "$base/LPR/Database/Real_Images_110118/175.jpg"   "2922761"
LPR_test "$base/LPR/Database/Real_Images_110118/176.jpg"   "2922761"
LPR_test "$base/LPR/Database/Real_Images_110118/177.jpg"   "2922761"
LPR_test "$base/LPR/Database/Real_Images_110118/178.jpg"   "2922761"
LPR_test "$base/LPR/Database/Real_Images_110118/179.jpg"   "2922761"
LPR_test "$base/LPR/Database/Real_Images_110118/180.jpg"   "2922761"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/181.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/182.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/183.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/184.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/185.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/186.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/187.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/188.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/189.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/190.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/191.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/192.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/193.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/194.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/195.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/196.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/197.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/198.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/199.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/200.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/201.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/202.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/203.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/204.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/205.jpg"   "7882084"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/206.jpg"   "6016669"
LPR_test "$base/LPR/Database/Real_Images_110118/207.jpg"   "6016669"
LPR_test "$base/LPR/Database/Real_Images_110118/208.jpg"   "6016669"
LPR_test "$base/LPR/Database/Real_Images_110118/209.jpg"   "6016669"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/210.jpg"   "5711711"
LPR_test "$base/LPR/Database/Real_Images_110118/211.jpg"   "5711711"
LPR_test "$base/LPR/Database/Real_Images_110118/212.jpg"   "5711711"
LPR_test "$base/LPR/Database/Real_Images_110118/213.jpg"   "5711711"
LPR_test "$base/LPR/Database/Real_Images_110118/214.jpg"   "5711711"
LPR_test "$base/LPR/Database/Real_Images_110118/215.jpg"   "5711711"
LPR_test "$base/LPR/Database/Real_Images_110118/216.jpg"   "5711711"
LPR_test "$base/LPR/Database/Real_Images_110118/217.jpg"   "5711711"
LPR_test "$base/LPR/Database/Real_Images_110118/218.jpg"   "5711711"
LPR_test "$base/LPR/Database/Real_Images_110118/219.jpg"   "5711711"
LPR_test "$base/LPR/Database/Real_Images_110118/220.jpg"   "5711711"
LPR_test "$base/LPR/Database/Real_Images_110118/221.jpg"   "5711711"
LPR_test "$base/LPR/Database/Real_Images_110118/222.jpg"   "5711711"
LPR_test "$base/LPR/Database/Real_Images_110118/223.jpg"   "5711711"
LPR_test "$base/LPR/Database/Real_Images_110118/224.jpg"   "5711711"
LPR_test "$base/LPR/Database/Real_Images_110118/225.jpg"   "5711711"
LPR_test "$base/LPR/Database/Real_Images_110118/226.jpg"   "5711711"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/227.jpg"   "7437161"
LPR_test "$base/LPR/Database/Real_Images_110118/228.jpg"   "7437161"
LPR_test "$base/LPR/Database/Real_Images_110118/229.jpg"   "7437161"
LPR_test "$base/LPR/Database/Real_Images_110118/230.jpg"   "7437161"
LPR_test "$base/LPR/Database/Real_Images_110118/231.jpg"   "7437161"
LPR_test "$base/LPR/Database/Real_Images_110118/232.jpg"   "7437161"
LPR_test "$base/LPR/Database/Real_Images_110118/233.jpg"   "7437161"
LPR_test "$base/LPR/Database/Real_Images_110118/234.jpg"   "7437161"
LPR_test "$base/LPR/Database/Real_Images_110118/235.jpg"   "7437161"
LPR_test "$base/LPR/Database/Real_Images_110118/236.jpg"   "7437161"
LPR_test "$base/LPR/Database/Real_Images_110118/237.jpg"   "7437161"
LPR_test "$base/LPR/Database/Real_Images_110118/238.jpg"   "7437161"
LPR_test "$base/LPR/Database/Real_Images_110118/239.jpg"   "7437161"
LPR_test "$base/LPR/Database/Real_Images_110118/240.jpg"   "7437161"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/241.jpg"   "9084612"             ""              "Digits touches bottom flag"
LPR_test "$base/LPR/Database/Real_Images_110118/242.jpg"   "9084612"             ""              "Digits touches bottom flag"
LPR_test "$base/LPR/Database/Real_Images_110118/243.jpg"   "9084612"             ""              "Digits touches bottom flag"
LPR_test "$base/LPR/Database/Real_Images_110118/244.jpg"   "9084612"             ""              "Digits touches bottom flag"
LPR_test "$base/LPR/Database/Real_Images_110118/245.jpg"   "9084612"             ""              "Digits touches bottom flag"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/246.jpg"   "7346211"
LPR_test "$base/LPR/Database/Real_Images_110118/247.jpg"   "7346211"
LPR_test "$base/LPR/Database/Real_Images_110118/248.jpg"   "7346211"
LPR_test "$base/LPR/Database/Real_Images_110118/249.jpg"   "7346211"
LPR_test "$base/LPR/Database/Real_Images_110118/250.jpg"   "7346211"
LPR_test "$base/LPR/Database/Real_Images_110118/251.jpg"   "7346211"
LPR_test "$base/LPR/Database/Real_Images_110118/252.jpg"   "7346211"
LPR_test "$base/LPR/Database/Real_Images_110118/253.jpg"   "7346211"
LPR_test "$base/LPR/Database/Real_Images_110118/254.jpg"   "7346211"
LPR_test "$base/LPR/Database/Real_Images_110118/255.jpg"   "7346211"
LPR_test "$base/LPR/Database/Real_Images_110118/256.jpg"   "7346211"
LPR_test "$base/LPR/Database/Real_Images_110118/257.jpg"   "7346211"
LPR_test "$base/LPR/Database/Real_Images_110118/258.jpg"   "7346211"
LPR_test "$base/LPR/Database/Real_Images_110118/259.jpg"   "7346211"
LPR_test "$base/LPR/Database/Real_Images_110118/260.jpg"   "7346211"
LPR_test "$base/LPR/Database/Real_Images_110118/261.jpg"   "7346211"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/262.jpg"   "2599223"             ""              "Poor Resolution + digits touches plate border"
LPR_test "$base/LPR/Database/Real_Images_110118/263.jpg"   "2599223"             ""              "Poor Resolution + digits touches plate border"
LPR_test "$base/LPR/Database/Real_Images_110118/264.jpg"   "2599223"             ""              "Poor Resolution + digits touches plate border"
LPR_test "$base/LPR/Database/Real_Images_110118/265.jpg"   "2599223"             ""              "Poor Resolution + digits touches plate border"
LPR_test "$base/LPR/Database/Real_Images_110118/266.jpg"   "2599223"             ""              "Poor Resolution + digits touches plate border"
LPR_test "$base/LPR/Database/Real_Images_110118/267.jpg"   "2599223"             ""              "Poor Resolution + digits touches plate border"
LPR_test "$base/LPR/Database/Real_Images_110118/268.jpg"   "2599223"             ""              "Poor Resolution + digits touches plate border"
LPR_test "$base/LPR/Database/Real_Images_110118/269.jpg"   "2599223"             ""              "Poor Resolution + digits touches plate border"
LPR_test "$base/LPR/Database/Real_Images_110118/270.jpg"   "2599223"             ""              "Poor Resolution + digits touches plate border"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/271.jpg"   "8635057"
LPR_test "$base/LPR/Database/Real_Images_110118/272.jpg"   "8635057"
LPR_test "$base/LPR/Database/Real_Images_110118/273.jpg"   "8635057"
LPR_test "$base/LPR/Database/Real_Images_110118/274.jpg"   "8635057"
LPR_test "$base/LPR/Database/Real_Images_110118/275.jpg"   "8635057"
LPR_test "$base/LPR/Database/Real_Images_110118/276.jpg"   "8635057"
LPR_test "$base/LPR/Database/Real_Images_110118/277.jpg"   "8635057"
LPR_test "$base/LPR/Database/Real_Images_110118/278.jpg"   "8635057"
LPR_test "$base/LPR/Database/Real_Images_110118/279.jpg"   "8635057"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/280.jpg"   "1950530"
LPR_test "$base/LPR/Database/Real_Images_110118/281.jpg"   "1950530"
LPR_test "$base/LPR/Database/Real_Images_110118/282.jpg"   "1950530"
LPR_test "$base/LPR/Database/Real_Images_110118/283.jpg"   "1950530"
LPR_test "$base/LPR/Database/Real_Images_110118/284.jpg"   "1950530"
LPR_test "$base/LPR/Database/Real_Images_110118/285.jpg"   "1950530"
LPR_test "$base/LPR/Database/Real_Images_110118/286.jpg"   "1950530"
LPR_test "$base/LPR/Database/Real_Images_110118/287.jpg"   "1950530"
LPR_test "$base/LPR/Database/Real_Images_110118/288.jpg"   "1950530"
LPR_test "$base/LPR/Database/Real_Images_110118/289.jpg"   "1950530"
LPR_test "$base/LPR/Database/Real_Images_110118/290.jpg"   "1950530"
LPR_test "$base/LPR/Database/Real_Images_110118/291.jpg"   "1950530"
LPR_test "$base/LPR/Database/Real_Images_110118/292.jpg"   "1950530"
LPR_test "$base/LPR/Database/Real_Images_110118/293.jpg"   "1950530"
LPR_test "$base/LPR/Database/Real_Images_110118/294.jpg"   "1950530"
LPR_test "$base/LPR/Database/Real_Images_110118/295.jpg"   "1950530"
LPR_test "$base/LPR/Database/Real_Images_110118/296.jpg"   "1950530"
LPR_test "$base/LPR/Database/Real_Images_110118/297.jpg"   "1950530"
LPR_test "$base/LPR/Database/Real_Images_110118/298.jpg"   "1950530"
LPR_test "$base/LPR/Database/Real_Images_110118/299.jpg"   "1950530"
LPR_test "$base/LPR/Database/Real_Images_110118/300.jpg"   "1950530"
LPR_test "$base/LPR/Database/Real_Images_110118/301.jpg"   "1950530"
LPR_test "$base/LPR/Database/Real_Images_110118/302.jpg"   "1950530"
LPR_test "$base/LPR/Database/Real_Images_110118/303.jpg"   "1950530"
LPR_test "$base/LPR/Database/Real_Images_110118/304.jpg"   "1950530"
LPR_test "$base/LPR/Database/Real_Images_110118/305.jpg"   "1950530"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/306.jpg"   "4488867"
LPR_test "$base/LPR/Database/Real_Images_110118/307.jpg"   "4488867"
LPR_test "$base/LPR/Database/Real_Images_110118/308.jpg"   "4488867"
LPR_test "$base/LPR/Database/Real_Images_110118/309.jpg"   "4488867"
LPR_test "$base/LPR/Database/Real_Images_110118/310.jpg"   "4488867"
LPR_test "$base/LPR/Database/Real_Images_110118/311.jpg"   "4488867"
LPR_test "$base/LPR/Database/Real_Images_110118/312.jpg"   "4488867"
LPR_test "$base/LPR/Database/Real_Images_110118/313.jpg"   "4488867"
LPR_test "$base/LPR/Database/Real_Images_110118/314.jpg"   "4488867"
LPR_test "$base/LPR/Database/Real_Images_110118/315.jpg"   "4488867"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/316.jpg"   "1950530"             ""              "Hard angle"
LPR_test "$base/LPR/Database/Real_Images_110118/317.jpg"   "1950530"             ""              "Hard angle"
LPR_test "$base/LPR/Database/Real_Images_110118/318.jpg"   "1950530"             ""              "Hard angle"
LPR_test "$base/LPR/Database/Real_Images_110118/319.jpg"   "1950530"             ""              "Hard angle"
LPR_test "$base/LPR/Database/Real_Images_110118/320.jpg"   "1950530"             ""              "Hard angle"
LPR_test "$base/LPR/Database/Real_Images_110118/321.jpg"   "1950530"             ""              "Hard angle"
LPR_test "$base/LPR/Database/Real_Images_110118/322.jpg"   "1950530"             ""              "Hard angle"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/323.jpg"   "1332967"
LPR_test "$base/LPR/Database/Real_Images_110118/324.jpg"   "1332967"
LPR_test "$base/LPR/Database/Real_Images_110118/325.jpg"   "1332967"
LPR_test "$base/LPR/Database/Real_Images_110118/326.jpg"   "1332967"
LPR_test "$base/LPR/Database/Real_Images_110118/327.jpg"   "1332967"
LPR_test "$base/LPR/Database/Real_Images_110118/328.jpg"   "1332967"
LPR_test "$base/LPR/Database/Real_Images_110118/329.jpg"   "1332967"
LPR_test "$base/LPR/Database/Real_Images_110118/330.jpg"   "1332967"
LPR_test "$base/LPR/Database/Real_Images_110118/331.jpg"   "1332967"
LPR_test "$base/LPR/Database/Real_Images_110118/332.jpg"   "1332967"
LPR_test "$base/LPR/Database/Real_Images_110118/333.jpg"   "1332967"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/334.jpg"   "3022862"
LPR_test "$base/LPR/Database/Real_Images_110118/335.jpg"   "3022862"
LPR_test "$base/LPR/Database/Real_Images_110118/336.jpg"   "3022862"
LPR_test "$base/LPR/Database/Real_Images_110118/337.jpg"   "3022862"
LPR_test "$base/LPR/Database/Real_Images_110118/338.jpg"   "3022862"
LPR_test "$base/LPR/Database/Real_Images_110118/339.jpg"   "3022862"
LPR_test "$base/LPR/Database/Real_Images_110118/340.jpg"   "3022862"
LPR_test "$base/LPR/Database/Real_Images_110118/341.jpg"   "3022862"
LPR_test "$base/LPR/Database/Real_Images_110118/342.jpg"   "3022862"
LPR_test "$base/LPR/Database/Real_Images_110118/343.jpg"   "3022862"
LPR_test "$base/LPR/Database/Real_Images_110118/344.jpg"   "3022862"
LPR_test "$base/LPR/Database/Real_Images_110118/345.jpg"   "3022862"
LPR_test "$base/LPR/Database/Real_Images_110118/346.jpg"   "3022862"
LPR_test "$base/LPR/Database/Real_Images_110118/347.jpg"   "3022862"
LPR_test "$base/LPR/Database/Real_Images_110118/348.jpg"   "3022862"
LPR_test "$base/LPR/Database/Real_Images_110118/349.jpg"   "3022862"
LPR_test "$base/LPR/Database/Real_Images_110118/350.jpg"   "3022862"
LPR_test "$base/LPR/Database/Real_Images_110118/351.jpg"   "3022862"
LPR_test "$base/LPR/Database/Real_Images_110118/352.jpg"   "3022862"
LPR_test "$base/LPR/Database/Real_Images_110118/353.jpg"   "3022862"
LPR_test "$base/LPR/Database/Real_Images_110118/354.jpg"   "3022862"
LPR_test "$base/LPR/Database/Real_Images_110118/355.jpg"   "3022862"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/356.jpg"   "6666567"             ""              "Poor resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/357.jpg"   "6666567"             ""              "Poor resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/358.jpg"   "6666567"             ""              "Poor resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/359.jpg"   "6666567"             ""              "Poor resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/360.jpg"   "6666567"             ""              "Poor resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/361.jpg"   "6666567"             ""              "Poor resolution"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/362.jpg"   "9084412"
LPR_test "$base/LPR/Database/Real_Images_110118/363.jpg"   "9084412"
LPR_test "$base/LPR/Database/Real_Images_110118/364.jpg"   "9084412"
LPR_test "$base/LPR/Database/Real_Images_110118/365.jpg"   "9084412"
LPR_test "$base/LPR/Database/Real_Images_110118/366.jpg"   "9084412"
LPR_test "$base/LPR/Database/Real_Images_110118/367.jpg"   "9084412"
LPR_test "$base/LPR/Database/Real_Images_110118/368.jpg"   "9084412"
LPR_test "$base/LPR/Database/Real_Images_110118/369.jpg"   "9084412"
LPR_test "$base/LPR/Database/Real_Images_110118/370.jpg"   "9084412"
LPR_test "$base/LPR/Database/Real_Images_110118/371.jpg"   "9084412"
LPR_test "$base/LPR/Database/Real_Images_110118/372.jpg"   "9084412"
LPR_test "$base/LPR/Database/Real_Images_110118/373.jpg"   "9084412"
LPR_test "$base/LPR/Database/Real_Images_110118/374.jpg"   "9084412"
LPR_test "$base/LPR/Database/Real_Images_110118/375.jpg"   "9084412"
LPR_test "$base/LPR/Database/Real_Images_110118/376.jpg"   "9084412"
LPR_test "$base/LPR/Database/Real_Images_110118/377.jpg"   "9084412"
LPR_test "$base/LPR/Database/Real_Images_110118/378.jpg"   "9084412"
LPR_test "$base/LPR/Database/Real_Images_110118/379.jpg"   "9084412"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/380.jpg"   "8010839"
LPR_test "$base/LPR/Database/Real_Images_110118/381.jpg"   "8010839"
LPR_test "$base/LPR/Database/Real_Images_110118/382.jpg"   "8010839"
LPR_test "$base/LPR/Database/Real_Images_110118/383.jpg"   "8010839"
LPR_test "$base/LPR/Database/Real_Images_110118/384.jpg"   "8010839"
LPR_test "$base/LPR/Database/Real_Images_110118/385.jpg"   "8010839"
LPR_test "$base/LPR/Database/Real_Images_110118/386.jpg"   "8010839"
LPR_test "$base/LPR/Database/Real_Images_110118/387.jpg"   "8010839"
LPR_test "$base/LPR/Database/Real_Images_110118/388.jpg"   "8010839"
LPR_test "$base/LPR/Database/Real_Images_110118/389.jpg"   "8010839"
LPR_test "$base/LPR/Database/Real_Images_110118/390.jpg"   "8010839"
LPR_test "$base/LPR/Database/Real_Images_110118/391.jpg"   "8010839"
LPR_test "$base/LPR/Database/Real_Images_110118/392.jpg"   "8010839"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/393.jpg"   "6984176"
LPR_test "$base/LPR/Database/Real_Images_110118/394.jpg"   "6984176"
LPR_test "$base/LPR/Database/Real_Images_110118/395.jpg"   "6984176"
LPR_test "$base/LPR/Database/Real_Images_110118/396.jpg"   "6984176"
LPR_test "$base/LPR/Database/Real_Images_110118/397.jpg"   "6984176"
LPR_test "$base/LPR/Database/Real_Images_110118/398.jpg"   "6984176"
LPR_test "$base/LPR/Database/Real_Images_110118/399.jpg"   "6984176"
LPR_test "$base/LPR/Database/Real_Images_110118/400.jpg"   "6984176"
LPR_test "$base/LPR/Database/Real_Images_110118/401.jpg"   "6984176"
LPR_test "$base/LPR/Database/Real_Images_110118/402.jpg"   "6984176"
LPR_test "$base/LPR/Database/Real_Images_110118/403.jpg"   "6984176"
LPR_test "$base/LPR/Database/Real_Images_110118/404.jpg"   "6984176"
LPR_test "$base/LPR/Database/Real_Images_110118/405.jpg"   "6984176"
LPR_test "$base/LPR/Database/Real_Images_110118/406.jpg"   "6984176"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/407.jpg"   "1775539"
LPR_test "$base/LPR/Database/Real_Images_110118/408.jpg"   "1775539"
LPR_test "$base/LPR/Database/Real_Images_110118/409.jpg"   "1775539"
LPR_test "$base/LPR/Database/Real_Images_110118/410.jpg"   "1775539"
LPR_test "$base/LPR/Database/Real_Images_110118/411.jpg"   "1775539"
LPR_test "$base/LPR/Database/Real_Images_110118/412.jpg"   "1775539"
LPR_test "$base/LPR/Database/Real_Images_110118/413.jpg"   "1775539"
LPR_test "$base/LPR/Database/Real_Images_110118/414.jpg"   "1775539"
LPR_test "$base/LPR/Database/Real_Images_110118/415.jpg"   "1775539"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/416.jpg"   "8336158"
LPR_test "$base/LPR/Database/Real_Images_110118/417.jpg"   "8336158"
LPR_test "$base/LPR/Database/Real_Images_110118/418.jpg"   "8336158"
LPR_test "$base/LPR/Database/Real_Images_110118/419.jpg"   "8336158"
LPR_test "$base/LPR/Database/Real_Images_110118/420.jpg"   "8336158"
LPR_test "$base/LPR/Database/Real_Images_110118/421.jpg"   "8336158"
LPR_test "$base/LPR/Database/Real_Images_110118/422.jpg"   "8336158"
LPR_test "$base/LPR/Database/Real_Images_110118/423.jpg"   "8336158"
LPR_test "$base/LPR/Database/Real_Images_110118/424.jpg"   "8336158"
LPR_test "$base/LPR/Database/Real_Images_110118/425.jpg"   "8336158"
LPR_test "$base/LPR/Database/Real_Images_110118/426.jpg"   "8336158"
LPR_test "$base/LPR/Database/Real_Images_110118/427.jpg"   "8336158"
LPR_test "$base/LPR/Database/Real_Images_110118/428.jpg"   "8336158"
LPR_test "$base/LPR/Database/Real_Images_110118/429.jpg"   "8336158"
LPR_test "$base/LPR/Database/Real_Images_110118/430.jpg"   "8336158"
LPR_test "$base/LPR/Database/Real_Images_110118/431.jpg"   "8336158"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/432.jpg"   "3408334"
LPR_test "$base/LPR/Database/Real_Images_110118/433.jpg"   "3408334"
LPR_test "$base/LPR/Database/Real_Images_110118/434.jpg"   "3408334"
LPR_test "$base/LPR/Database/Real_Images_110118/435.jpg"   "3408334"
LPR_test "$base/LPR/Database/Real_Images_110118/436.jpg"   "3408334"
LPR_test "$base/LPR/Database/Real_Images_110118/437.jpg"   "3408334"
LPR_test "$base/LPR/Database/Real_Images_110118/438.jpg"   "3408334"
LPR_test "$base/LPR/Database/Real_Images_110118/439.jpg"   "3408334"
LPR_test "$base/LPR/Database/Real_Images_110118/440.jpg"   "3408334"
LPR_test "$base/LPR/Database/Real_Images_110118/441.jpg"   "3408334"
LPR_test "$base/LPR/Database/Real_Images_110118/442.jpg"   "3408334"
LPR_test "$base/LPR/Database/Real_Images_110118/443.jpg"   "3408334"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/444.jpg"   "9084412"
LPR_test "$base/LPR/Database/Real_Images_110118/445.jpg"   "9084412"
LPR_test "$base/LPR/Database/Real_Images_110118/446.jpg"   "9084412"
LPR_test "$base/LPR/Database/Real_Images_110118/447.jpg"   "9084412"
LPR_test "$base/LPR/Database/Real_Images_110118/448.jpg"   "9084412"
LPR_test "$base/LPR/Database/Real_Images_110118/449.jpg"   "9084412"
LPR_test "$base/LPR/Database/Real_Images_110118/450.jpg"   "9084412"
LPR_test "$base/LPR/Database/Real_Images_110118/451.jpg"   "9084412"
LPR_test "$base/LPR/Database/Real_Images_110118/452.jpg"   "9084412"
LPR_test "$base/LPR/Database/Real_Images_110118/453.jpg"   "9084412"
LPR_test "$base/LPR/Database/Real_Images_110118/454.jpg"   "9084412"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/455.jpg"   "6494111"
LPR_test "$base/LPR/Database/Real_Images_110118/456.jpg"   "6494111"
LPR_test "$base/LPR/Database/Real_Images_110118/457.jpg"   "6494111"
LPR_test "$base/LPR/Database/Real_Images_110118/458.jpg"   "6494111"
LPR_test "$base/LPR/Database/Real_Images_110118/459.jpg"   "6494111"
LPR_test "$base/LPR/Database/Real_Images_110118/460.jpg"   "6494111"
LPR_test "$base/LPR/Database/Real_Images_110118/461.jpg"   "6494111"
LPR_test "$base/LPR/Database/Real_Images_110118/462.jpg"   "6494111"
LPR_test "$base/LPR/Database/Real_Images_110118/463.jpg"   "6494111"
LPR_test "$base/LPR/Database/Real_Images_110118/464.jpg"   "6494111"
LPR_test "$base/LPR/Database/Real_Images_110118/465.jpg"   "6494111"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/466.jpg"   "8010839"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(3,3)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/467.jpg"   "8010839"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(3,3)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/468.jpg"   "8010839"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(3,3)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/469.jpg"   "8010839"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(3,3)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/470.jpg"   "8010839"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(3,3)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/471.jpg"   "8010839"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(3,3)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/472.jpg"   "8010839"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(3,3)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/473.jpg"   "8010839"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(3,3)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/474.jpg"   "8010839"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(3,3)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/475.jpg"   "8010839"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(3,3)\""  "Tweaked"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/477.jpg"   "2922761"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/478.jpg"   "2922761"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/479.jpg"   "2922761"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/480.jpg"   "2922761"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/481.jpg"   "2922761"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/482.jpg"   "2922761"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/483.jpg"   "2922761"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/484.jpg"   "2922761"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/485.jpg"   "2922761"             ""              "Poor Resolution"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/486.jpg"   "3903637"
LPR_test "$base/LPR/Database/Real_Images_110118/487.jpg"   "3903637"
LPR_test "$base/LPR/Database/Real_Images_110118/488.jpg"   "3903637"
LPR_test "$base/LPR/Database/Real_Images_110118/489.jpg"   "3903637"
LPR_test "$base/LPR/Database/Real_Images_110118/490.jpg"   "3903637"
LPR_test "$base/LPR/Database/Real_Images_110118/491.jpg"   "3903637"
LPR_test "$base/LPR/Database/Real_Images_110118/492.jpg"   "3903637"
LPR_test "$base/LPR/Database/Real_Images_110118/493.jpg"   "3903637"
LPR_test "$base/LPR/Database/Real_Images_110118/494.jpg"   "3903637"
LPR_test "$base/LPR/Database/Real_Images_110118/495.jpg"   "3903637"
LPR_test "$base/LPR/Database/Real_Images_110118/496.jpg"   "3903637"
LPR_test "$base/LPR/Database/Real_Images_110118/497.jpg"   "3903637"
LPR_test "$base/LPR/Database/Real_Images_110118/498.jpg"   "3903637"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/499.jpg"   "2629085"  "--PreprocessZoomIn=1.4 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/500.jpg"   "2629085"  "--PreprocessZoomIn=1.4 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/501.jpg"   "2629085"  "--PreprocessZoomIn=1.4 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/502.jpg"   "2629085"  "--PreprocessZoomIn=1.4 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/503.jpg"   "2629085"  "--PreprocessZoomIn=1.4 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/504.jpg"   "2629085"  "--PreprocessZoomIn=1.4 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/505.jpg"   "2629085"  "--PreprocessZoomIn=1.4 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/506.jpg"   "2629085"  "--PreprocessZoomIn=1.4 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/507.jpg"   "2629085"  "--PreprocessZoomIn=1.4 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/508.jpg"   "2629085"  "--PreprocessZoomIn=1.4 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/509.jpg"   "2629085"  "--PreprocessZoomIn=1.4 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/510.jpg"   "2629085"  "--PreprocessZoomIn=1.4 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/511.jpg"   "2629085"  "--PreprocessZoomIn=1.4 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/512.jpg"   "2629085"  "--PreprocessZoomIn=1.4 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/513.jpg"   "2629085"  "--PreprocessZoomIn=1.4 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/514.jpg"   "5901567"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/515.jpg"   "5901567"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/516.jpg"   "5901567"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/517.jpg"   "5901567"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/518.jpg"   "5901567"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/519.jpg"   "5901567"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/520.jpg"   "5901567"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/521.jpg"   "5901567"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/522.jpg"   "5901567"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/523.jpg"   "5901567"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/524.jpg"   "29645501"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/525.jpg"   "29645501"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/526.jpg"   "29645501"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/527.jpg"   "29645501"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/528.jpg"   "29645501"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/529.jpg"   "29645501"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/530.jpg"   "29645501"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/531.jpg"   "29645501"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/532.jpg"   "29645501"             ""              "Poor Resolution"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/533.jpg"   "2135468"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/534.jpg"   "2135468"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/535.jpg"   "2135468"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/536.jpg"   "2135468"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/537.jpg"   "2135468"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/538.jpg"   "2135468"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/539.jpg"   "2135468"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/540.jpg"   "2135468"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/541.jpg"   "2135468"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/542.jpg"   "2135468"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/543.jpg"   "2135468"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/544.jpg"   "2135468"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/545.jpg"   "2135468"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/546.jpg"   "2135468"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/547.jpg"   "2135468"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/548.jpg"   "2135468"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/549.jpg"   "2135468"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/550.jpg"   "2135468"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/551.jpg"   "2135468"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/552.jpg"   "6666567"
LPR_test "$base/LPR/Database/Real_Images_110118/553.jpg"   "6666567"
LPR_test "$base/LPR/Database/Real_Images_110118/554.jpg"   "6666567"
LPR_test "$base/LPR/Database/Real_Images_110118/555.jpg"   "6666567"
LPR_test "$base/LPR/Database/Real_Images_110118/556.jpg"   "6666567"
LPR_test "$base/LPR/Database/Real_Images_110118/557.jpg"   "6666567"
LPR_test "$base/LPR/Database/Real_Images_110118/558.jpg"   "6666567"
LPR_test "$base/LPR/Database/Real_Images_110118/559.jpg"   "6666567"
LPR_test "$base/LPR/Database/Real_Images_110118/560.jpg"   "6666567"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/561.jpg"   "1203332"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/562.jpg"   "1203332"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/563.jpg"   "1203332"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/564.jpg"   "1203332"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/565.jpg"   "1203332"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/566.jpg"   "1203332"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/567.jpg"   "1203332"             ""              "Poor Resolution"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/568.jpg"   "7444009"
LPR_test "$base/LPR/Database/Real_Images_110118/569.jpg"   "7444009"
LPR_test "$base/LPR/Database/Real_Images_110118/570.jpg"   "7444009"
LPR_test "$base/LPR/Database/Real_Images_110118/571.jpg"   "7444009"
LPR_test "$base/LPR/Database/Real_Images_110118/572.jpg"   "7444009"
LPR_test "$base/LPR/Database/Real_Images_110118/573.jpg"   "7444009"
LPR_test "$base/LPR/Database/Real_Images_110118/574.jpg"   "7444009"
LPR_test "$base/LPR/Database/Real_Images_110118/575.jpg"   "7444009"
LPR_test "$base/LPR/Database/Real_Images_110118/576.jpg"   "7444009"
LPR_test "$base/LPR/Database/Real_Images_110118/577.jpg"   "7444009"
LPR_test "$base/LPR/Database/Real_Images_110118/578.jpg"   "7444009"
LPR_test "$base/LPR/Database/Real_Images_110118/579.jpg"   "7444009"
LPR_test "$base/LPR/Database/Real_Images_110118/580.jpg"   "7444009"
LPR_test "$base/LPR/Database/Real_Images_110118/581.jpg"   "7444009"
LPR_test "$base/LPR/Database/Real_Images_110118/582.jpg"   "7444009"
LPR_test "$base/LPR/Database/Real_Images_110118/583.jpg"   "7444009"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/584.jpg"   "7632732"
LPR_test "$base/LPR/Database/Real_Images_110118/585.jpg"   "7632732"
LPR_test "$base/LPR/Database/Real_Images_110118/586.jpg"   "7632732"
LPR_test "$base/LPR/Database/Real_Images_110118/587.jpg"   "7632732"
LPR_test "$base/LPR/Database/Real_Images_110118/588.jpg"   "7632732"
LPR_test "$base/LPR/Database/Real_Images_110118/589.jpg"   "7632732"
LPR_test "$base/LPR/Database/Real_Images_110118/590.jpg"   "7632732"
LPR_test "$base/LPR/Database/Real_Images_110118/591.jpg"   "7632732"
LPR_test "$base/LPR/Database/Real_Images_110118/592.jpg"   "7632732"
LPR_test "$base/LPR/Database/Real_Images_110118/593.jpg"   "7632732"
LPR_test "$base/LPR/Database/Real_Images_110118/594.jpg"   "7632732"
LPR_test "$base/LPR/Database/Real_Images_110118/595.jpg"   "7632732"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/596.jpg"   "8609538"
LPR_test "$base/LPR/Database/Real_Images_110118/597.jpg"   "8609538"
LPR_test "$base/LPR/Database/Real_Images_110118/598.jpg"   "8609538"
LPR_test "$base/LPR/Database/Real_Images_110118/599.jpg"   "8609538"
LPR_test "$base/LPR/Database/Real_Images_110118/600.jpg"   "8609538"
LPR_test "$base/LPR/Database/Real_Images_110118/601.jpg"   "8609538"
LPR_test "$base/LPR/Database/Real_Images_110118/602.jpg"   "8609538"
LPR_test "$base/LPR/Database/Real_Images_110118/603.jpg"   "8609538"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/604.jpg"   "3903637"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/605.jpg"   "3903637"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/606.jpg"   "3903637"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/607.jpg"   "3903637"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/608.jpg"   "3903637"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/609.jpg"   "3903637"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/610.jpg"   "3903637"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/611.jpg"   "3903637"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/612.jpg"   "3903637"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/613.jpg"   "3903637"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/614.jpg"   "3903637"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/615.jpg"   "3903637"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/616.jpg"   "3903637"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/617.jpg"   "3903637"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/618.jpg"   "3903637"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/619.jpg"   "3903637"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/620.jpg"   "3903637"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/621.jpg"   "3903637"  "--PreprocessZoomIn=1.7 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/622.jpg"   "3903637"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/623.jpg"   "3903637"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/624.jpg"   "3903637"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/625.jpg"   "3903637"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/626.jpg"   "3903637"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/627.jpg"   "3903637"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/628.jpg"   "3903637"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/629.jpg"   "8931985"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/630.jpg"   "8931985"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/631.jpg"   "8931985"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/632.jpg"   "8931985"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/633.jpg"   "8931985"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/634.jpg"   "8931985"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/635.jpg"   "8931985"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/636.jpg"   "8931985"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/637.jpg"   "8931985"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/638.jpg"   "8931985"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/639.jpg"   "8931985"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/640.jpg"   "8931985"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/641.jpg"   "8931985"             ""              "Poor Resolution"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/642.jpg"   "8515481"
LPR_test "$base/LPR/Database/Real_Images_110118/643.jpg"   "8515481"
LPR_test "$base/LPR/Database/Real_Images_110118/644.jpg"   "8515481"
LPR_test "$base/LPR/Database/Real_Images_110118/645.jpg"   "8515481"
LPR_test "$base/LPR/Database/Real_Images_110118/646.jpg"   "8515481"
LPR_test "$base/LPR/Database/Real_Images_110118/647.jpg"   "8515481"
LPR_test "$base/LPR/Database/Real_Images_110118/648.jpg"   "8515481"
LPR_test "$base/LPR/Database/Real_Images_110118/649.jpg"   "8515481"
LPR_test "$base/LPR/Database/Real_Images_110118/650.jpg"   "8515481"
LPR_test "$base/LPR/Database/Real_Images_110118/651.jpg"   "8515481"
LPR_test "$base/LPR/Database/Real_Images_110118/652.jpg"   "8515481"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/653.jpg"   "29645301"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/654.jpg"   "29645301"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/655.jpg"   "29645301"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/656.jpg"   "29645301"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/657.jpg"   "29645301"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/658.jpg"   "29645301"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/659.jpg"   "29645301"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/660.jpg"   "29645301"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/661.jpg"   "29645301"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/662.jpg"   "29645301"             ""              "Poor Resolution"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/663.jpg"   "7632732"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/664.jpg"   "7632732"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/665.jpg"   "7632732"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/666.jpg"   "7632732"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/667.jpg"   "7632732"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/668.jpg"   "7632732"             ""              "Poor Resolution"
LPR_test "$base/LPR/Database/Real_Images_110118/669.jpg"   "7632732"             ""              "Poor Resolution"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/670.jpg"   "8373973"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/671.jpg"   "8373973"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/672.jpg"   "8373973"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/673.jpg"   "8373973"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/674.jpg"   "8373973"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/675.jpg"   "8373973"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/676.jpg"   "8373973"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/677.jpg"   "8373973"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/678.jpg"   "8373973"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/679.jpg"   "8373973"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/680.jpg"   "8373973"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/681.jpg"   "8373973"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(5,5)\""  "Tweaked"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/682.jpg"   "1531768"             ""              "Hard angle"
LPR_test "$base/LPR/Database/Real_Images_110118/683.jpg"   "1531768"             ""              "Hard angle"
LPR_test "$base/LPR/Database/Real_Images_110118/684.jpg"   "1531768"             ""              "Hard angle"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/685.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/686.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/687.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/688.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/689.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/690.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/691.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/692.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/693.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/694.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/695.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/696.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/697.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/698.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/699.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/700.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/701.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/702.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/703.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/704.jpg"   "7882084"
LPR_test "$base/LPR/Database/Real_Images_110118/705.jpg"   "7882084"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/706.jpg"   "5518676"
LPR_test "$base/LPR/Database/Real_Images_110118/707.jpg"   "5518676"
LPR_test "$base/LPR/Database/Real_Images_110118/708.jpg"   "5518676"
LPR_test "$base/LPR/Database/Real_Images_110118/709.jpg"   "5518676"
LPR_test "$base/LPR/Database/Real_Images_110118/710.jpg"   "5518676"
LPR_test "$base/LPR/Database/Real_Images_110118/711.jpg"   "5518676"
LPR_test "$base/LPR/Database/Real_Images_110118/712.jpg"   "5518676"
LPR_test "$base/LPR/Database/Real_Images_110118/713.jpg"   "5518676"
LPR_test "$base/LPR/Database/Real_Images_110118/714.jpg"   "5518676"
LPR_test "$base/LPR/Database/Real_Images_110118/715.jpg"   "5518676"
LPR_test "$base/LPR/Database/Real_Images_110118/716.jpg"   "5518676"
LPR_test "$base/LPR/Database/Real_Images_110118/717.jpg"   "5518676"
LPR_test "$base/LPR/Database/Real_Images_110118/718.jpg"   "5518676"
LPR_test "$base/LPR/Database/Real_Images_110118/719.jpg"   "5518676"
LPR_test "$base/LPR/Database/Real_Images_110118/720.jpg"   "5518676"
LPR_test "$base/LPR/Database/Real_Images_110118/721.jpg"   "5518676"
LPR_test "$base/LPR/Database/Real_Images_110118/722.jpg"   "5518676"
LPR_test "$base/LPR/Database/Real_Images_110118/723.jpg"   "5518676"
EndCase

StartCase
LPR_test "$base/LPR/Database/Real_Images_110118/724.jpg"   "3107369"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/725.jpg"   "3107369"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/726.jpg"   "3107369"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/727.jpg"   "3107369"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/728.jpg"   "3107369"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/729.jpg"   "3107369"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/730.jpg"   "3107369"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/731.jpg"   "3107369"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/732.jpg"   "3107369"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/733.jpg"   "3107369"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/734.jpg"   "3107369"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
LPR_test "$base/LPR/Database/Real_Images_110118/735.jpg"   "3107369"  "--PreprocessZoomIn=1.6 --PreprocessGaussKernel=\"(9,9)\""  "Tweaked"
EndCase


secPerImg=`echo "scale=2; 100*$SECONDS/$imgs" | bc`
casespassRate=`echo "scale=2; 100*$casespass/$cases" | bc`
printf "Summary:  Cases PassRate=$casespassRate%% ($casespass/$cases)\n"
printf "Elapsed time: ${SECONDS}sec (${secPerImg}sec per image )\n\n"
