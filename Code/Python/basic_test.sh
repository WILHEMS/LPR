#!/bin/sh

base='/Users/shahargino/Documents/ImageProcessing'

LPR_test() {
  if [ "$# == 3" ]; then
    res=`python main.py -i $1 $3 --batch | grep -w $2`
  else
    res=`python main.py -i $1 --batch | grep -w $2`
  fi
  if [ "$res" ]; then
    echo "$1 PASSED!"
  else
    printf "$1 \033[1;31mFAILED\033[0m! $4\n"
  fi
} 

#---------------------------------------- I M A G E ----------------------------|-- Expected --|------- Arguments ------|---- Waivers ----
LPR_test "$base/LPR/Database/Israel/1.jpg"   "1777765"
LPR_test "$base/LPR/Database/Israel/2.jpg"   "6866866"
LPR_test "$base/LPR/Database/Israel/3.jpg"   "6666674"
LPR_test "$base/LPR/Database/Israel/4.jpg"   "9000004"
LPR_test "$base/LPR/Database/Israel/5.jpg"   "8226228"
LPR_test "$base/LPR/Database/Israel/6.jpg"   "7777779"
LPR_test "$base/LPR/Database/Israel/7.jpg"   "6930113"
LPR_test "$base/LPR/Database/Israel/8.jpg"   "2124212"
LPR_test "$base/LPR/Database/Israel/9.jpg"   "1173711"
LPR_test "$base/LPR/Database/Israel/10.jpg"  "5866666"
LPR_test "$base/LPR/Database/Israel/11.jpg"  "7777775"
LPR_test "$base/LPR/Database/Israel/12.jpg"  "4600000"
LPR_test "$base/LPR/Database/Israel/13.jpg"  "276363"
LPR_test "$base/LPR/Database/Israel/14.jpg"  "1366666"
LPR_test "$base/LPR/Database/Israel/15.jpg"  "9599974"
LPR_test "$base/LPR/Database/Israel/16.jpg"  "9426032"
LPR_test "$base/LPR/Database/Israel/17.jpg"  "69880074"
LPR_test "$base/LPR/Database/Israel/18.jpg"  "6377032"
LPR_test "$base/LPR/Database/Israel/19.jpg"  "6480812"
LPR_test "$base/LPR/Database/Israel/20.jpg"  "4000000"
LPR_test "$base/LPR/Database/Israel/21.jpg"  "1234567"
LPR_test "$base/LPR/Database/Israel/22.jpg"  "5188335"  ""                            "Numbers touch plate's boundaries"          
LPR_test "$base/LPR/Database/Israel/23.jpg"  "23383201" "--PreprocessThreshweight=7"  # dark scene
LPR_test "$base/LPR/Database/Israel/24.jpg"  "22436201"
LPR_test "$base/LPR/Database/Israel/25.jpg"  "18605001"
LPR_test "$base/LPR/Database/Israel/26.jpg"  "24767401"
LPR_test "$base/LPR/Database/Israel/27.jpg"  "5238117"
LPR_test "$base/LPR/Database/Israel/28.jpg"  "5503075"

LPR_test "$base/LPR/Database/Israel/p1.jpg"  "10529@"
LPR_test "$base/LPR/Database/Israel/p2.jpg"  "25129@"
LPR_test "$base/LPR/Database/Israel/p3.jpg"  "14883@"
LPR_test "$base/LPR/Database/Israel/p4.jpg"  "40015@"
LPR_test "$base/LPR/Database/Israel/p5.jpg"  "10256@"

