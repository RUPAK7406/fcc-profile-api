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
  if [ -f "./fccSpider/spiders/$2_spider.py" ]; then
    echo -e "+ User: ($1). Spider: ($2)."
    set -x # echo commands
    set -x
    mkdir output # make output directory
    rm -r ./output/* # removing all previous outputs
    find . -name "*.pyc" -type f -delete
    scrapy crawl $2 -o ./output/$2.json -t json -a username=$1
    find . -name "*.pyc" -type f -delete
    set +x # echo off
  else
    echo "+ Application Comments:"
    echo "+ Usage   : ./fccSpider.sh [username] [spiderName]"
    echo "+ Example : ./fccSpider.sh myfccusername fccProfile"
    echo "+ Available spiders are:"
    echo "+ "$(ls ./fccSpider/spiders/*_spider.py)
  fi
  echo
