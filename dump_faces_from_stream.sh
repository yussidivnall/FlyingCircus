#!/bin/bash
#usage %progname <video> <outdir>
#[[ -e $1 ]] || echo "No such file"&& exit 1

#[[ $2 ]] || echo "No output directory given";exit 1
[[ -d $2 ]] || mkdir -p $2;

in_vid_name=`basename $1`
temp_dir="/tmp/face_dump/$in_vid_name/"
echo $in_vid_name
mkdir -p $temp_dir
ffmpeg -i $1 -r 1 "$temp_dir/$in_vid_name.frame%0d.png"
for fn in `ls $temp_dir`
do
    outpath="${2}${fn}"
    echo "dumping to $outpath "
#    echo python extract_faces.py -i $temp_dir$fn -o $outpath -c ./cascade_classifiers/haarcascade_frontalface_default.xml
    python extract_faces.py -i $temp_dir$fn -o $outpath -c ./cascade_classifiers/haarcascade_frontalface_default.xml
done
rm -r $temp_dir
