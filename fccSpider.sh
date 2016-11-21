#!/bin/bash
  echo
  echo "FCC Spider"

# global variables
  echo
  echo "User permissions required for execution:"
  echo "Ability to delete compiled python files in project."

# action
  echo
  echo -e "Action:"
  if [ "$1" == "fccProfile" ]; then
    echo -e "+ Spider: ($1) with username: ($2)"
    set -x # echo commands
    set -x
    mkdir output
    find . -name "*.pyc" -type f -delete
    if [ -n "$2" ]; then
      # cd fccSpider
      scrapy crawl $1 -o ./output/$1.json -t json -a username=$2
      find . -name "*.pyc" -type f -delete
    else
      echo -e "Please supply a username"
    fi
    set +x # echo off
  else
    echo "+ Application Comments:"
    echo "+ Usage   : ./fccSpider.sh [spiderName] [username]"
    echo "+ Example : ./fccSpider.sh fccProfile myfccusername"
    echo "+ Available spiders are:"
    echo "+ "$(ls ./scrapy/spiders/*_spider.py)
  fi
  echo
