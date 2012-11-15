#!/bin/bash

x=$(cat .directory_counter.txt)
mkdir "test${x}"
ln -s `pwd`/coTrace.py `pwd`"/test${x}"/coTrace.py

x=$(( $x + 1 ))
rm .directory_counter.txt
echo $x > .directory_counter.txt

