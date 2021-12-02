#!/bin/bash

for filename in Images/*.JPG;
do

  echo "image = $filename"
  for color in "red" "white" "blue";
  do
    if  [ "$color" = "red" ]; then
      t="sRGB(20,0,0)-sRGB(255,20,20)"
    elif [ "$color" = "white" ]; then
      t="sRGB(80,80,100)-sRGB(255,255,255)"
    else
      t="sRGB(0,0,20)-sRGB(20,20,255)"
    fi
    echo "color=$color threshold=$t $color.jpg"

    #echo -n "$filename, $color, " >> verbose.csv
    #magick $filename -fuzz 50% -color-threshold $t \
    #  -define connected-components:verbose=true             \
    #  -define connected-components:area-threshold=10      \
    #  -define medianFilterImage:radius=8 \
    #  -connected-components 10 $color.jpg | (echo -n "$filename, $color, "; grep -c "rgb(255,255,255)") >> results.csv 

    echo -n "$filename, $color, " >> verbose.csv
    magick $filename -fuzz 50% -color-threshold $t \
      -define connected-components:verbose=true             \
      -define connected-components:area-threshold=50      \
      -define medianFilterImage:radius=8 \
      -connected-components 10 $color.jpg | tee >((echo -n "$filename, $color, "; grep -c "rgb(255,255,255)") >> results.csv) >> verbose.csv 

  done
done
