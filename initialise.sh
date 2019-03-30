#!/bin/bash
if ! [ -e init ];
then
    sudo apt-get install python3-pip
    sudo pip3 install virtualenv
    sudo virtualenv topheadlines
    sudo virtualenv -p /usr/bin/python3 topheadlines
    source topheadlines/bin/activate
    sudo topheadlines/bin/pip3 install -r requirements.txt
    deactivate
    sudo touch init
    chmod u+x TopHeadlines.py
fi
echo "TopHeadlines.py ready to run !"
