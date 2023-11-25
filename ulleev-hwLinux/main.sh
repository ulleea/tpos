#!/bin/bash
check() {
tmux ls | grep "0" && return 1
return 0
}

var=$(check)
echo $var
if [ $var==0 ]
then
tmux new-session -d
fi

if [ $#==3 ]
then
 python3 ./start.py $1 $2
else
 python3 ./start.py $1
fi
