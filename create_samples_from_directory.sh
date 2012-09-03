#!/bin/bash
[[ -e $1 ]] && [[ -e $2 ]] || exit 
positive_in_path=$1
negative_in_path=$2
output_vec=$3

positives="positives.dat"
negatives="negatives.dat"
rm $positives
rm $negatives
find $positive_in_path -name '*.png' -exec identify -format '%i 1 0 0 %w %h' \{\} \; > $positives
echo "Generating positive images index"
for fn in `find $positive_n_path -name "*.png"`
do
    width_height=`identify $fn |awk '{print $3}' | sed -e "s/x/ /g"`
    echo $fn 1 1 $width_height  >> $positives
done
echo "Generating negative images index"
for fn in `find $negative_n_path -name "*.png"`
do
    width_height=`identify $fn |awk '{print $3}' | sed -e "s/x/ /g"`
    echo $fn 1 1 $width_height  >> $negatives
done

opencv_createsamples -info $positives -vec $output_vec -w 20 -h 20 -num 10
