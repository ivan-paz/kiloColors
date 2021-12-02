# Some useful commands to extract images and debug

Extract .jpg images form a video

ffmpeg -i NAME.MP4 -r 0.25 -qscale:v 1 -qmin 1 -qmax 1 image_%04d.jpg

Select a band of collor

magick negro-RGB4.JPG -color-threshold 'sRGB(20,0,0)-sRGB(255,20,15)' redNegro.gif

**this setting has been effective to catch the white**

 > magick Images/_DSC7315.JPG -color-threshold 'sRGB(80,80,100)-sRGB(255,255,255)' white.gif


