#!/bin/bash

# Skript erwartet als Argument einen Ordner mit allen Scans darin
# 1_0001.jpg
# 1_0002.jpg
# ...
# 1_00024.jpg
# 2_0001.jpg
# ...
# 2_00028.jpg
# ...

if [ $# -gt 0 ]
then    
    cd $1
fi

# Bash allows filename patterns which match no files to expand to a null string, rather than themselves
shopt -s nullglob

for i in *.jpg
do
    FILENAME=$i
    VID=$(echo $FILENAME | cut -d'_' -f 1)
    mkdir -p $VID
done


for i in *.tif
do
    FILENAME=$i
    VID=$(echo $FILENAME | cut -d'_' -f 1)
    mkdir -p $VID
done

for i in *.jpg
do
    FILENAME=$i
    VID=$(echo $FILENAME | cut -d'_' -f 1)
    TO=$VID"/"$i
    mv $i $TO
done

for i in *.tif
do
    FILENAME=$i
    VID=$(echo $FILENAME | cut -d'_' -f 1)
    TO=$VID"/"$i
    mv $i $TO
done

