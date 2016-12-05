#!/bin/bash
  echo
  echo "FCC Spider"

# global variables
  echo
  echo "User permissions required for execution:"
  echo "Ability to delete compiled python files in project."

# Clean Function
clrData () {
  mkdir common # make output directory
  mkdir export # make output directory
  rm -f ./common/*.json # removes all previous outputs for clean operation
  rm -rf ./export/* # removes previous export data
}

# action
  echo
  echo -e "Action:"
  if [ -n "${1}" ]; then
    echo -e "+ User: (${1})."
    set -x # echo commands
    set -x
    find . -name "*.pyc" -type f -delete # clear compiled / cache python files for clean operation
    if [ "${2}" == "full" ]; then
      clrData
      scrapy crawl map -a username=${1}
      scrapy crawl desc -a username=${1}
      scrapy crawl profile -a username=${1}
      scrapy crawl export -a username=${1}
    elif [ "${2}" == "scrape" ]; then
      clrData
      scrapy crawl map -a username=${1}
      scrapy crawl desc -a username=${1}
      scrapy crawl profile -a username=${1}
    elif [ "${2}" == "empty" ]; then
      clrData
      scrapy crawl map -a username=${1}
      scrapy crawl desc -a username=${1}
    elif [ "${2}" == "export" ]; then
      scrapy crawl export -a username=${1}
    fi
    find . -name "*.pyc" -type f -delete
    set +x # echo off
  else
    echo "+ Application Comments:"
    echo "+ Usage   : ./fccSpider.sh [username] [action]"
    echo "+ Example : ./fccSpider.sh htko89 full"
    echo "+ Actions : See below."
    echo "++ full : Downloads the FCC curriculum map, challenge descriptions, personal completion profile, export results"
    echo "++ scrape : Downloads the FCC curriculum map, challenge descriptions, personal completion profile"
    echo "++ empty  : Downloads the FCC curriculum map, challenge descriptions."
    echo "++ export : Exports existing results to export folder. Scrape must have run at least once before or errors will occur"
  fi
  echo
