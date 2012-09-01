#!/bin/bash
#usage %progname <video> <outdir>
#[[ -e $1 ]] || echo "No such file"&& exit 1

#[[ $2 ]] || echo "No output directory given";exit 1
[[ -d $2 ]] || mkdir $2;


mkdir "/tmp/$1.temp/"
#mkdir  "$2/$fn/faces/"
#ffmpeg -i $1 -r 1/5 /tmp/$1.temp/frame%03d.png
ffmpeg -i $1 -r 1 /tmp/$1.temp/frame%03d.png
for fn in `ls /tmp/$1.temp/`
do
    outpath="${2}${fn}"
    echo "dumping to $outpath "
    echo python ./extract_faces.py -i /tmp/$1.temp/$fn -o $outpath -c ./cascade_classifiers/haarcascade_frontalface_default.xml
    python ./extract_faces.py -i /tmp/$1.temp/$fn -o $outpath -c ./cascade_classifiers/haarcascade_frontalface_default.xml
done
