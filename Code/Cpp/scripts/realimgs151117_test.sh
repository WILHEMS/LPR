#!/bin/sh

codec='png'
base='/Users/shahargino/Documents/ImageProcessing'

default_args='--batch --imgEnhancementMode=1 --mode=="no_police" --ROI="(480,432,768,378)"'

LPR_test() {
  res=`build/lpr -i $1 $default_args $3 | grep "LPR Result: "`
  pass=`echo $res | grep -w $2`
  if [ "$pass" ]; then
    echo "$1 PASSED! \t$3"
  else
    act=`echo $res | cut -d" " -f4`
    printf "$1 FAILED! (ACT=$act EXP=$2) $4\n"
  fi
} 

#--------------- I M A G E ----------------------------|-- Expected --|------- Arguments ------|---- Waivers ----
LPR_test "$base/LPR/Database/Real_ROImage_151117/0.$codec"    "6369286"
printf "\n"

LPR_test "$base/LPR/Database/Real_ROImage_151117/1.$codec"    "2311750"
LPR_test "$base/LPR/Database/Real_ROImage_151117/2.$codec"    "2311750"
LPR_test "$base/LPR/Database/Real_ROImage_151117/3.$codec"    "2311750"
LPR_test "$base/LPR/Database/Real_ROImage_151117/4.$codec"    "2311750"
LPR_test "$base/LPR/Database/Real_ROImage_151117/5.$codec"    "2311750"
printf "\n"

LPR_test "$base/LPR/Database/Real_ROImage_151117/6.$codec"    "7988809"
printf "\n"

LPR_test "$base/LPR/Database/Real_ROImage_151117/7.$codec"    "8113673"
LPR_test "$base/LPR/Database/Real_ROImage_151117/8.$codec"    "8113673"
LPR_test "$base/LPR/Database/Real_ROImage_151117/9.$codec"    "8113673"
LPR_test "$base/LPR/Database/Real_ROImage_151117/10.$codec"   "8113673"
LPR_test "$base/LPR/Database/Real_ROImage_151117/11.$codec"   "8113673"
printf "\n"

LPR_test "$base/LPR/Database/Real_ROImage_151117/12.$codec"   "1326230"
LPR_test "$base/LPR/Database/Real_ROImage_151117/13.$codec"   "1326230"
LPR_test "$base/LPR/Database/Real_ROImage_151117/14.$codec"   "1326230"
LPR_test "$base/LPR/Database/Real_ROImage_151117/15.$codec"   "1326230"
LPR_test "$base/LPR/Database/Real_ROImage_151117/16.$codec"   "1326230"
LPR_test "$base/LPR/Database/Real_ROImage_151117/17.$codec"   "1326230"
LPR_test "$base/LPR/Database/Real_ROImage_151117/18.$codec"   "1326230"
LPR_test "$base/LPR/Database/Real_ROImage_151117/19.$codec"   "1326230"
LPR_test "$base/LPR/Database/Real_ROImage_151117/20.$codec"   "1326230"
LPR_test "$base/LPR/Database/Real_ROImage_151117/21.$codec"   "1326230"
LPR_test "$base/LPR/Database/Real_ROImage_151117/22.$codec"   "1326230"
LPR_test "$base/LPR/Database/Real_ROImage_151117/23.$codec"   "1326230"
LPR_test "$base/LPR/Database/Real_ROImage_151117/24.$codec"   "1326230"
LPR_test "$base/LPR/Database/Real_ROImage_151117/25.$codec"   "1326230"
LPR_test "$base/LPR/Database/Real_ROImage_151117/26.$codec"   "1326230"
LPR_test "$base/LPR/Database/Real_ROImage_151117/27.$codec"   "1326230"
LPR_test "$base/LPR/Database/Real_ROImage_151117/28.$codec"   "1326230"
printf "\n"

LPR_test "$base/LPR/Database/Real_ROImage_151117/29.$codec"   "18855901"
LPR_test "$base/LPR/Database/Real_ROImage_151117/30.$codec"   "18855901"
printf "\n"

LPR_test "$base/LPR/Database/Real_ROImage_151117/31.$codec"   "6633653"
LPR_test "$base/LPR/Database/Real_ROImage_151117/32.$codec"   "6633653"
LPR_test "$base/LPR/Database/Real_ROImage_151117/33.$codec"   "6633653"
printf "\n"

LPR_test "$base/LPR/Database/Real_ROImage_151117/34.$codec"   "9228931"
LPR_test "$base/LPR/Database/Real_ROImage_151117/35.$codec"   "9228931"
LPR_test "$base/LPR/Database/Real_ROImage_151117/36.$codec"   "9228931"
printf "\n"

LPR_test "$base/LPR/Database/Real_ROImage_151117/37.$codec"   "2765338"
LPR_test "$base/LPR/Database/Real_ROImage_151117/38.$codec"   "2765338"
printf "\n"

LPR_test "$base/LPR/Database/Real_ROImage_151117/39.$codec"   "2425085"
printf "\n"

LPR_test "$base/LPR/Database/Real_ROImage_151117/40.$codec"   "3599456"
LPR_test "$base/LPR/Database/Real_ROImage_151117/41.$codec"   "3599456"
LPR_test "$base/LPR/Database/Real_ROImage_151117/42.$codec"   "3599456"
LPR_test "$base/LPR/Database/Real_ROImage_151117/43.$codec"   "3599456"
LPR_test "$base/LPR/Database/Real_ROImage_151117/44.$codec"   "3599456"
LPR_test "$base/LPR/Database/Real_ROImage_151117/45.$codec"   "3599456"
LPR_test "$base/LPR/Database/Real_ROImage_151117/46.$codec"   "3599456"
LPR_test "$base/LPR/Database/Real_ROImage_151117/47.$codec"   "3599456"
LPR_test "$base/LPR/Database/Real_ROImage_151117/48.$codec"   "3599456"
LPR_test "$base/LPR/Database/Real_ROImage_151117/49.$codec"   "3599456"
LPR_test "$base/LPR/Database/Real_ROImage_151117/50.$codec"   "3599456"
LPR_test "$base/LPR/Database/Real_ROImage_151117/51.$codec"   "3599456"
printf "\n"

LPR_test "$base/LPR/Database/Real_ROImage_151117/52.$codec"   "7421613"
LPR_test "$base/LPR/Database/Real_ROImage_151117/53.$codec"   "7421613"
LPR_test "$base/LPR/Database/Real_ROImage_151117/54.$codec"   "7421613"
LPR_test "$base/LPR/Database/Real_ROImage_151117/55.$codec"   "7421613"
printf "\n"

LPR_test "$base/LPR/Database/Real_ROImage_151117/56.$codec"   "3080934"
LPR_test "$base/LPR/Database/Real_ROImage_151117/57.$codec"   "3080934"
LPR_test "$base/LPR/Database/Real_ROImage_151117/58.$codec"   "3080934"
LPR_test "$base/LPR/Database/Real_ROImage_151117/59.$codec"   "3080934"
LPR_test "$base/LPR/Database/Real_ROImage_151117/60.$codec"   "3080934"
LPR_test "$base/LPR/Database/Real_ROImage_151117/61.$codec"   "3080934"
LPR_test "$base/LPR/Database/Real_ROImage_151117/62.$codec"   "3080934"
printf "\n"

LPR_test "$base/LPR/Database/Real_ROImage_151117/63.$codec"   "4469737"
LPR_test "$base/LPR/Database/Real_ROImage_151117/64.$codec"   "4469737"
printf "\n"

LPR_test "$base/LPR/Database/Real_ROImage_151117/65.$codec"   "9566773"
LPR_test "$base/LPR/Database/Real_ROImage_151117/66.$codec"   "9566773"
LPR_test "$base/LPR/Database/Real_ROImage_151117/67.$codec"   "9566773"
LPR_test "$base/LPR/Database/Real_ROImage_151117/68.$codec"   "9566773"
LPR_test "$base/LPR/Database/Real_ROImage_151117/69.$codec"   "9566773"
LPR_test "$base/LPR/Database/Real_ROImage_151117/70.$codec"   "9566773"
printf "\n"

LPR_test "$base/LPR/Database/Real_ROImage_151117/71.$codec"   "5419232"
LPR_test "$base/LPR/Database/Real_ROImage_151117/72.$codec"   "5419232"
LPR_test "$base/LPR/Database/Real_ROImage_151117/73.$codec"   "5419232"
LPR_test "$base/LPR/Database/Real_ROImage_151117/74.$codec"   "5419232"
printf "\n"

LPR_test "$base/LPR/Database/Real_ROImage_151117/75.$codec"   "18855801"
printf "\n"

LPR_test "$base/LPR/Database/Real_ROImage_151117/76.$codec"   "6546080"
LPR_test "$base/LPR/Database/Real_ROImage_151117/77.$codec"   "6546080"
LPR_test "$base/LPR/Database/Real_ROImage_151117/78.$codec"   "6546080"
printf "\n"

LPR_test "$base/LPR/Database/Real_ROImage_151117/79.$codec"   "3973154"
printf "\n"

LPR_test "$base/LPR/Database/Real_ROImage_151117/80.$codec"   "6175858"
LPR_test "$base/LPR/Database/Real_ROImage_151117/81.$codec"   "6175858"
LPR_test "$base/LPR/Database/Real_ROImage_151117/82.$codec"   "6175858"
LPR_test "$base/LPR/Database/Real_ROImage_151117/83.$codec"   "6175858"
LPR_test "$base/LPR/Database/Real_ROImage_151117/84.$codec"   "6175858"
printf "\n"

LPR_test "$base/LPR/Database/Real_ROImage_151117/85.$codec"   "1824931"
printf "\n"

LPR_test "$base/LPR/Database/Real_ROImage_151117/86.$codec"   "8899152"
LPR_test "$base/LPR/Database/Real_ROImage_151117/87.$codec"   "8899152"
LPR_test "$base/LPR/Database/Real_ROImage_151117/88.$codec"   "8899152"
LPR_test "$base/LPR/Database/Real_ROImage_151117/89.$codec"   "8899152"
LPR_test "$base/LPR/Database/Real_ROImage_151117/90.$codec"   "8899152"
LPR_test "$base/LPR/Database/Real_ROImage_151117/91.$codec"   "8899152"
LPR_test "$base/LPR/Database/Real_ROImage_151117/92.$codec"   "8899152"
LPR_test "$base/LPR/Database/Real_ROImage_151117/93.$codec"   "8899152"
printf "\n"
