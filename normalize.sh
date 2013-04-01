#!/bin/bash

for p in `ls positives/*.png`;do
    echo $p
    filename=$(basename $p)
    convert $p -resize 256x256 normalised_positives/$filename
    done

