#!/usr/bin/env bash

rm -rf ~/catkin_ws/src/amr31001/
cd ~/catkin_ws/src/
git clone --branch main --single-branch --depth=1 https://github.com/tom-howard/amr31001.git
catkin build amr31001

