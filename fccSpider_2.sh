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
  if [ -n "$1" ]; then
    echo -e "+ User: ($1)."
    set -x # echo commands
    set -x
    mkdir output # make output directory
    # rm -f ./output/*.json # removes all previous outputs for clean operation
    find . -name "*.pyc" -type f -delete # clear compiled / cache python files for clean operation
    scrapy crawl challenge -a username=$1
    find . -name "*.pyc" -type f -delete
    set +x # echo off
  else
    echo "+ Application Comments:"
    echo "+ Usage   : ./fccSpider.sh [username]"
    echo "+ Example : ./fccSpider.sh myfccusername"
  fi
  echo
