#!/bin/bash
  echo
  echo -e "FCC Spider"

# global variables
  echo
  echo -e "Authentication:"
  sudo echo "Sudo Permission"

# action
  echo
  echo -e "Action:"
  if [ -f "./spiders/$1_spider.py" ]; then
    echo -e "+ Spider: ($1) with username: ($2)"
    set -x # echo commands
    set -x
    find . -name "*.pyc" -type f -delete
    if [ -n "$2" ]; then
      scrapy crawl $1 -o $1.json -t json -a username=$2
    else
      echo -e "Please supply a username"
    fi
    set +x # echo off
  else
    echo "+ Application Usage:"
    echo "+ ./fccSpider.sh [spider] [username]"
    echo "+ Available spiders are:"
    echo $(ls ./spiders/*_spider.py)
    echo "Ex: + ./fccSpider.sh fccMap myfccusername"
  fi
  echo
