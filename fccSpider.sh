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
  if [ -n "${1}" ]; then
    echo -e "+ User: (${1})."
    set -x # echo commands
    set -x
    find . -name "*.pyc" -type f -delete # clear compiled / cache python files for clean operation
    if [ "${2}" == "scrape" ]; then
      mkdir common # make output directory
      mkdir export # make output directory
      rm -f ./common/*.json # removes all previous outputs for clean operation
      rm -f ./export/* # removes previous export data
      scrapy crawl map -a username=${1}
      scrapy crawl desc -a username=${1}
      scrapy crawl profile -a username=${1}
    elif [ "${2}" == "export" ]; then
      scrapy crawl export -a username=${1}
    fi
    find . -name "*.pyc" -type f -delete
    set +x # echo off
  else
    echo "+ Application Comments:"
    echo "+ Usage   : ./fccSpider.sh [username] [action]"
    echo "+ Example : ./fccSpider.sh htko89 scrape"
    echo "+ Actions : scrape, export"
  fi
  echo
