#!/bin/sh

base='/Users/shahargino/Documents/Projects/ImageProcessing/LPR/Database/LPRtests'

default_args='--batch --mode="no_police"'

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
LPR_test "$base/24_4_18_test/24_4_18/image1.jpeg"                               "8895839" 
LPR_test "$base/24_4_18_test/24_4_18/image2.jpeg"                               "5931865" 
LPR_test "$base/24_4_18_test/24_4_18/image3.jpeg"                               "6570533" 
LPR_test "$base/24_4_18_test/24_4_18/image4.jpeg"                               "4167368" 
LPR_test "$base/24_4_18_test/24_4_18/image5.jpeg"                               "4897851" 
LPR_test "$base/24_4_18_test/24_4_18/image6.jpeg"                               "6849936" 
LPR_test "$base/24_4_18_test/24_4_18/image7.jpeg"                               "15630901" 
LPR_test "$base/24_4_18_test/24_4_18/image8.jpeg"                               "2125430" 
LPR_test "$base/24_4_18_test/24_4_18/image9.jpeg"                               "8525070" 
LPR_test "$base/24_4_18_test/24_4_18/image10.jpeg"                              "29645401" 
LPR_test "$base/24_4_18_test/24_4_18/image11.jpeg"                              "4573308" 
LPR_test "$base/24_4_18_test/24_4_18/image12.jpeg"                              "2186737" 
LPR_test "$base/24_4_18_test/24_4_18/image13.jpeg"                              "9765137" 
LPR_test "$base/24_4_18_test/24_4_18/image14.jpeg"                              "7783938" 
LPR_test "$base/24_4_18_test/24_4_18/image15.jpeg"                              "8072128" 
LPR_test "$base/24_4_18_test/24_4_18/image16.jpeg"                              "8373973" 
LPR_test "$base/24_4_18_test/24_4_18/image17.jpeg"                              "5651238" 
LPR_test "$base/24_4_18_test/24_4_18/image18.jpeg"                              "8252671" 
LPR_test "$base/24_4_18_test/24_4_18/image19.jpeg"                              "4543172" 
LPR_test "$base/24_4_18_test/24_4_18/image20.jpeg"                              "7457939" 
LPR_test "$base/24_4_18_test/24_4_18/image21.jpeg"                              "4371674" 
LPR_test "$base/24_4_18_test/24_4_18/image22.jpeg"                              "5698133" 
LPR_test "$base/24_4_18_test/24_4_18/image23.jpeg"                              "4133754" 
LPR_test "$base/24_4_18_test/24_4_18/image24.jpeg"                              "7845611" 
LPR_test "$base/24_4_18_test/24_4_18/image25.jpeg"                              "4541455" 
LPR_test "$base/24_4_18_test/24_4_18/image26.jpeg"                              "27773401" 
LPR_test "$base/24_4_18_test/24_4_18/image27.jpeg"                              "37454301" 
LPR_test "$base/24_4_18_test/24_4_18/image28.jpeg"                              "1580664" 
LPR_test "$base/24_4_18_test/24_4_18/image29.jpeg"                              "3408334" 
LPR_test "$base/24_4_18_test/24_4_18/image30.jpeg"                              "4249159" 
LPR_test "$base/24_4_18_test/24_4_18/image31.jpeg"                              "6141731" 
LPR_test "$base/24_4_18_test/24_4_18/image32.jpeg"                              "7969538" 
LPR_test "$base/24_4_18_test/24_4_18/image33.jpeg"                              "5955478" 
LPR_test "$base/24_4_18_test/24_4_18/image34.jpeg"                              "3432811" 
LPR_test "$base/24_4_18_test/24_4_18/image35.jpeg"                              "2136111" 
LPR_test "$base/24_4_18_test/24_4_18/image36.jpeg"                              "7319854" 
LPR_test "$base/24_4_18_test/24_4_18/image37.jpeg"                              "2484330" 
LPR_test "$base/24_4_18_test/24_4_18/image38.jpeg"                              "5565464" 
LPR_test "$base/24_4_18_test/24_4_18/image39.jpeg"                              "31575801" 
LPR_test "$base/24_4_18_test/24_4_18/image41.jpeg"                              "6243376" 
LPR_test "$base/24_4_18_test/24_4_18/image42.jpeg"                              "1952775" 
LPR_test "$base/24_4_18_test/24_4_18/image43.jpeg"                              "29645301" 
LPR_test "$base/24_4_18_test/24_4_18/image44.jpeg"                              "1775539" 
LPR_test "$base/24_4_18_test/24_4_18/image45.jpeg"                              "6813757" 
LPR_test "$base/24_4_18_test/24_4_18/image46.jpeg"                              "2253339" 
LPR_test "$base/24_4_18_test/24_4_18/image47.jpeg"                              "4249159" 
LPR_test "$base/24_4_18_test/24_4_18/image48.jpeg"                              "3227572" 
LPR_test "$base/24_4_18_test/24_4_18/image49.jpeg"                              "4763954" 
LPR_test "$base/24_4_18_test/24_4_18/image50.jpeg"                              "6813757" 
LPR_test "$base/24_4_18_test/24_4_18/image51.jpeg"                              "1007037" 
LPR_test "$base/24_4_18_test/24_4_18/image52.jpeg"                              "3632278" 
LPR_test "$base/24_4_18_test/24_4_18/image53.jpeg"                              "9469937" 
LPR_test "$base/24_4_18_test/24_4_18/image54.jpeg"                              "4197734" 
LPR_test "$base/24_4_18_test/24_4_18/image55.jpeg"                              "5544778" 
LPR_test "$base/24_4_18_test/24_4_18/image56.jpeg"                              "5544778" 
LPR_test "$base/24_4_18_test/24_4_18/image57.jpeg"                              "3232532" 
LPR_test "$base/24_4_18_test/24_4_18/image58.jpeg"                              "2514434" 
LPR_test "$base/24_4_18_test/24_4_18/image59.jpeg"                              "1007037" 
LPR_test "$base/24_4_18_test/24_4_18/image60.jpeg"                              "4295039" 
LPR_test "$base/24_4_18_test/24_4_18/image61.jpeg"                              "1816337" 
LPR_test "$base/24_4_18_test/24_4_18/image62.jpeg"                              "3317832" 
LPR_test "$base/24_4_18_test/24_4_18/image63.jpeg"                              "9828754" 
LPR_test "$base/24_4_18_test/24_4_18/image64.jpeg"                              "3227572" 
LPR_test "$base/24_4_18_test/24_4_18/image65.jpeg"                              "5544778" 
LPR_test "$base/24_4_18_test/24_4_18/image66.jpeg"                              "2672337" 
LPR_test "$base/24_4_18_test/24_4_18/image67.jpeg"                              "3044470" 
LPR_test "$base/24_4_18_test/24_4_18/image68.jpeg"                              "7815038" 

LPR_test "$base/25_4_18_test/25_4_18/image1.jpeg"                               "9910510" 
LPR_test "$base/25_4_18_test/25_4_18/image2.jpeg"                               "7006238" 
LPR_test "$base/25_4_18_test/25_4_18/image3.jpeg"                               "16242701" 
LPR_test "$base/25_4_18_test/25_4_18/image4.jpeg"                               "3460454" 
LPR_test "$base/25_4_18_test/25_4_18/image5.jpeg"                               "8549514" 
LPR_test "$base/25_4_18_test/25_4_18/image6.jpeg"                               "7679714" 

LPR_test "$base/26_4_18_test/26_4_18/image1.jpeg"                               "7636555" 
LPR_test "$base/26_4_18_test/26_4_18/image2.jpeg"                               "7882084" 
LPR_test "$base/26_4_18_test/26_4_18/image3.jpeg"                               "2819080" 
LPR_test "$base/26_4_18_test/26_4_18/image4.jpeg"                               "7636555" 
LPR_test "$base/26_4_18_test/26_4_18/image7.jpeg"                               "23533201" 
LPR_test "$base/26_4_18_test/26_4_18/image9.jpeg"                               "6879211" 
LPR_test "$base/26_4_18_test/26_4_18/image11.jpeg"                              "4179454" 
LPR_test "$base/26_4_18_test/26_4_18/image13.jpeg"                              "8387880" 
LPR_test "$base/26_4_18_test/26_4_18/image15.jpeg"                              "3227572" 
LPR_test "$base/26_4_18_test/26_4_18/image17.jpeg"                              "3408334" 
LPR_test "$base/26_4_18_test/26_4_18/image19.jpeg"                              "5979455" 
LPR_test "$base/26_4_18_test/26_4_18/image21.jpeg"                              "8167284" 
LPR_test "$base/26_4_18_test/26_4_18/image23.jpeg"                              "5979455" 
LPR_test "$base/26_4_18_test/26_4_18/image27.jpeg"                              "2074550" 
LPR_test "$base/26_4_18_test/26_4_18/image29.jpeg"                              "8167284" 
LPR_test "$base/26_4_18_test/26_4_18/image30.jpeg"                              "2597263" 
LPR_test "$base/26_4_18_test/26_4_18/image37.jpeg"                              "3227572" 
LPR_test "$base/26_4_18_test/26_4_18/image39.jpeg"                              "9828754" 
LPR_test "$base/26_4_18_test/26_4_18/image41.jpeg"                              "6879211" 
LPR_test "$base/26_4_18_test/26_4_18/image43.jpeg"                              "19107101" 
LPR_test "$base/26_4_18_test/26_4_18/image45.jpeg"                              "4249459" 
LPR_test "$base/26_4_18_test/26_4_18/image47.jpeg"                              "1820513" 
LPR_test "$base/26_4_18_test/26_4_18/image49.jpeg"                              "3931175" 
LPR_test "$base/26_4_18_test/26_4_18/image51.jpeg"                              "4295039" 
LPR_test "$base/26_4_18_test/26_4_18/image53.jpeg"                              "2005633" 
LPR_test "$base/26_4_18_test/26_4_18/image55.jpeg"                              "1999478" 
LPR_test "$base/26_4_18_test/26_4_18/image57.jpeg"                              "7949454" 
LPR_test "$base/26_4_18_test/26_4_18/image59.jpeg"                              "2906274" 
LPR_test "$base/26_4_18_test/26_4_18/image61.jpeg"                              "9066612" 
LPR_test "$base/26_4_18_test/26_4_18/image63.jpeg"                              "2074550" 
LPR_test "$base/26_4_18_test/26_4_18/image65.jpeg"                              "7346211" 
LPR_test "$base/26_4_18_test/26_4_18/image67.jpeg"                              "4369230" 
LPR_test "$base/26_4_18_test/26_4_18/image69.jpeg"                              "1950530" 
LPR_test "$base/26_4_18_test/26_4_18/image71.jpeg"                              "3994581" 
LPR_test "$base/26_4_18_test/26_4_18/image73.jpeg"                              "1950530" 
LPR_test "$base/26_4_18_test/26_4_18/image75.jpeg"                              "8181480" 
LPR_test "$base/26_4_18_test/26_4_18/image77.jpeg"                              "2515454" 
LPR_test "$base/26_4_18_test/26_4_18/image81.jpeg"                              "9669069" 
LPR_test "$base/26_4_18_test/26_4_18/image83.jpeg"                              "2515454" 
LPR_test "$base/26_4_18_test/26_4_18/image85.jpeg"                              "9066612" 
LPR_test "$base/26_4_18_test/26_4_18/image87.jpeg"                              "5644230" 
LPR_test "$base/26_4_18_test/26_4_18/image89.jpeg"                              "2005633" 
LPR_test "$base/26_4_18_test/26_4_18/image91.jpeg"                              "3931175" 
LPR_test "$base/26_4_18_test/26_4_18/image93.jpeg"                              "5544878" 
LPR_test "$base/26_4_18_test/26_4_18/image95.jpeg"                              "4369230" 
LPR_test "$base/26_4_18_test/26_4_18/image97.jpeg"                              "4182455" 
LPR_test "$base/26_4_18_test/26_4_18/image99.jpeg"                              "8514552" 

LPR_test "$base/27_4_18_test/27_4_18/image1.jpeg"                               "2212676" 
LPR_test "$base/27_4_18_test/27_4_18/image3.jpeg"                               "4342875" 
LPR_test "$base/27_4_18_test/27_4_18/image5.jpeg"                               "3514266"
LPR_test "$base/27_4_18_test/27_4_18/image7.jpeg"                               "5783334" 
LPR_test "$base/27_4_18_test/27_4_18/image9.jpeg"                               "6255260" 
LPR_test "$base/27_4_18_test/27_4_18/image11.jpeg"                              "9788034" 
LPR_test "$base/27_4_18_test/27_4_18/image13.jpeg"                              "7887237" 
LPR_test "$base/27_4_18_test/27_4_18/image15.jpeg"                              "8981833" 
LPR_test "$base/27_4_18_test/27_4_18/image17.jpeg"                              "4221571" 
LPR_test "$base/27_4_18_test/27_4_18/image19.jpeg"                              "16242701" 
LPR_test "$base/27_4_18_test/27_4_18/image21.jpeg"                              "6384301" 
LPR_test "$base/27_4_18_test/27_4_18/image23.jpeg"                              "1259239"
LPR_test "$base/27_4_18_test/27_4_18/image25.jpeg"                              "3460454" 
LPR_test "$base/27_4_18_test/27_4_18/image27.jpeg"                              "4100073" 
LPR_test "$base/27_4_18_test/27_4_18/image29.jpeg"                              "8054839" 
LPR_test "$base/27_4_18_test/27_4_18/image31.jpeg"                              "8054839" 
LPR_test "$base/27_4_18_test/27_4_18/image33.jpeg"                              "6613550" 
LPR_test "$base/27_4_18_test/27_4_18/image35.jpeg"                              "5985616" 

LPR_test "$base/29_4_18_test/29_4_18/image1.jpeg"                               "1166467" 
LPR_test "$base/29_4_18_test/29_4_18/image3.jpeg"                               "7882084" 
LPR_test "$base/29_4_18_test/29_4_18/image5.jpeg"                               "8609538"
LPR_test "$base/29_4_18_test/29_4_18/image7.jpeg"                               "9910510" 
LPR_test "$base/29_4_18_test/29_4_18/image9.jpeg"                               "29679201" 
LPR_test "$base/29_4_18_test/29_4_18/image11.jpeg"                              "3149223" 
LPR_test "$base/29_4_18_test/29_4_18/image13.jpeg"                              "7679714" 
LPR_test "$base/29_4_18_test/29_4_18/image15.jpeg"                              "2608935" 
LPR_test "$base/29_4_18_test/29_4_18/image17.jpeg"                              "8549514" 
LPR_test "$base/29_4_18_test/29_4_18/image19.jpeg"                              "6450451" 
LPR_test "$base/29_4_18_test/29_4_18/image21.jpeg"                              "5491358" 
LPR_test "$base/29_4_18_test/29_4_18/image23.jpeg"                              "4221571"
LPR_test "$base/29_4_18_test/29_4_18/image25.jpeg"                              "5518676" 
LPR_test "$base/29_4_18_test/29_4_18/image27.jpeg"                              "7367911" 
LPR_test "$base/29_4_18_test/29_4_18/image29.jpeg"                              "2517930" 
LPR_test "$base/29_4_18_test/29_4_18/image31.jpeg"                              "7783938" 
LPR_test "$base/29_4_18_test/29_4_18/image33.jpeg"                              "4342875" 
LPR_test "$base/29_4_18_test/29_4_18/image35.jpeg"                              "1810511" 
LPR_test "$base/29_4_18_test/29_4_18/image37.jpeg"                              "9788034" 
LPR_test "$base/29_4_18_test/29_4_18/image39.jpeg"                              "4273755" 
LPR_test "$base/29_4_18_test/29_4_18/image41.jpeg"                              "1810511"
LPR_test "$base/29_4_18_test/29_4_18/image43.jpeg"                              "7088866" 
LPR_test "$base/29_4_18_test/29_4_18/image45.jpeg"                              "6543433" 
LPR_test "$base/29_4_18_test/29_4_18/image47.jpeg"                              "4393432" 
LPR_test "$base/29_4_18_test/29_4_18/image49.jpeg"                              "3872488" 
LPR_test "$base/29_4_18_test/29_4_18/image51.jpeg"                              "7755855" 
LPR_test "$base/29_4_18_test/29_4_18/image53.jpeg"                              "8256375" 
LPR_test "$base/29_4_18_test/29_4_18/image55.jpeg"                              "3872488" 
LPR_test "$base/29_4_18_test/29_4_18/image57.jpeg"                              "8496676" 
LPR_test "$base/29_4_18_test/29_4_18/image59.jpeg"                              "3460454"
LPR_test "$base/29_4_18_test/29_4_18/image61.jpeg"                              "7367911" 
LPR_test "$base/29_4_18_test/29_4_18/image63.jpeg"                              "3013473" 
LPR_test "$base/29_4_18_test/29_4_18/image65.jpeg"                              "8780239" 
LPR_test "$base/29_4_18_test/29_4_18/image67.jpeg"                              "4236363" 
LPR_test "$base/29_4_18_test/29_4_18/image69.jpeg"                              "3929030" 
LPR_test "$base/29_4_18_test/29_4_18/image71.jpeg"                              "7827909" 
LPR_test "$base/29_4_18_test/29_4_18/image73.jpeg"                              "4241930" 
LPR_test "$base/29_4_18_test/29_4_18/image75.jpeg"                              "9591738" 
LPR_test "$base/29_4_18_test/29_4_18/image77.jpeg"                              "3035331"
LPR_test "$base/29_4_18_test/29_4_18/image79.jpeg"                              "4612772" 
LPR_test "$base/29_4_18_test/29_4_18/image81.jpeg"                              "6187436" 
LPR_test "$base/29_4_18_test/29_4_18/image83.jpeg"                              "2212676" 
LPR_test "$base/29_4_18_test/29_4_18/image85.jpeg"                              "8163339" 
LPR_test "$base/29_4_18_test/29_4_18/image87.jpeg"                              "6464767" 
LPR_test "$base/29_4_18_test/29_4_18/image89.jpeg"                              "29645401" 
LPR_test "$base/29_4_18_test/29_4_18/image91.jpeg"                              "5955334" 
LPR_test "$base/29_4_18_test/29_4_18/image93.jpeg"                              "2669871" 
LPR_test "$base/29_4_18_test/29_4_18/image95.jpeg"                              "8183935"
LPR_test "$base/29_4_18_test/29_4_18/image97.jpeg"                              "13446801" 
LPR_test "$base/29_4_18_test/29_4_18/image99.jpeg"                              "16803001" 
LPR_test "$base/29_4_18_test/29_4_18/image101.jpeg"                             "5931865" 
LPR_test "$base/29_4_18_test/29_4_18/image103.jpeg"                             "8973461" 
LPR_test "$base/29_4_18_test/29_4_18/image105.jpeg"                             "9558537" 
LPR_test "$base/29_4_18_test/29_4_18/image107.jpeg"                             "2703985" 
LPR_test "$base/29_4_18_test/29_4_18/image109.jpeg"                             "1698778" 
LPR_test "$base/29_4_18_test/29_4_18/image111.jpeg"                             "7882084" 
LPR_test "$base/29_4_18_test/29_4_18/image113.jpeg"                             "3811930" 
EndCase

secPerImg=`echo "scale=2; 100*$SECONDS/$imgs" | bc`
casespassRate=`echo "scale=2; 100*$casespass/$cases" | bc`
printf "Summary:  Cases PassRate=$casespassRate%% ($casespass/$cases)\n"
printf "Elapsed time: ${SECONDS}sec (${secPerImg}sec per image )\n\n"
