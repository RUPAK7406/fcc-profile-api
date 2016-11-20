#!/bin/bash
  echo
  echo -e "FCC Spider"

# global variables
  echo
  echo -e "Authentication:"
  sudo echo "Sudo permission to delete compiled python files in project"

# action
  echo
  echo -e "Action:"
  if [ -f "./scrapy/spiders/$1_spider.py" ]; then
    echo -e "+ Spider: ($1) with username: ($2)"
    set -x # echo commands
    set -x
    sudo find ./scrapy -name "*.pyc" -type f -delete
    if [ -n "$2" ]; then
      cd scrapy
      scrapy crawl $1 -o $1.json -t json -a username=$2
    else
      echo -e "Please supply a username"
    fi
    set +x # echo off
  else
    echo "+ Application Comments:"
    echo "+ Usage   : ./fccSpider.sh [spiderName] [username]"
    echo "+ Example : ./fccSpider.sh fccMap myfccusername"
    echo "+ Available spiders are:"
    echo "+ "$(ls ./scrapy/spiders/*_spider.py)
  fi
  echo
