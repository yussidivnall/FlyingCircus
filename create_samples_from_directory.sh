#!/bin/bash
[[ -e $1 ]] && [[ -e $2 ]] || exit 
positive_in_path=$1
negative_in_path=$2
output_vec=$3

positives="positives.dat"
negatives="negatives.dat"
rm $positives
rm $negatives
echo "Creating positive images index"
find $positive_in_path -name '*.png' -exec identify -format '%i 1 0 0 %w %h' \{\} \; > $positives
#find $negative_in_path -name '*.png' -exec identify -format '%i 1 0 0 %w %h' \{\} \; > $negatives
echo "Creating negative images index"
find  $negative_in_path -name '*.png' > $negatives
num_pos=`wc -l $positives`
#echo "opencv_createsamples -info $positives -vec $output_vec -w 20 -h 20 -num $(($num_pos-100))"
opencv_createsamples -info $positives -vec $output_vec -w 20 -h 20 -num `wc -l $positives`

#For some reason this fails, might be that -npos needs to be less than opencv_createsamples...-num
#No explanation, and not sure how much less
#See comments in http://achuwilson.wordpress.com/2011/07/01/create-your-own-haar-classifier-for-detecting-objects-in-opencv/
#opencv_haartraining -data out_training -vec out.vec -bg negatives.txt -w 20 -h 20 -nneg 3000 -npos 2829 -mode all

