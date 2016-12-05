#!/bin/bash
  echo
  echo "FCC Spider"

# global variables
  echo
  echo "User permissions required for execution:"
  echo "Ability to delete compiled python files in project."

# Clean Function
clrMap () {
  mkdir common # make output directory
  mkdir export # make output directory
  rm -f ./common/*.json # removes all previous outputs for clean operation
}

clrExport () {
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
      clrMap
      clrExport
      scrapy crawl map -a username=${1}
      scrapy crawl desc -a username=${1}
      scrapy crawl profile -a username=${1}
      scrapy crawl export -a username=${1}
    elif [ "${2}" == "map" ]; then
      clrMap
      scrapy crawl map -a username=${1}
      scrapy crawl desc -a username=${1}
    elif [ "${2}" == "profile" ]; then
      clrExport
      scrapy crawl profile -a username=${1}
      scrapy crawl export -a username=${1}
    elif [ "${2}" == "empty" ]; then
      clrExport
      scrapy crawl empty -a username=${1}
      scrapy crawl export -a username=${1}
    elif [ "${2}" == "clear" ]; then
      clrMap
      clrExport
    fi
    find . -name "*.pyc" -type f -delete
    set +x # echo off
  else
    echo "+ Application Comments:"
    echo "+ Usage   : ./fccSpider.sh [username] [action]"
    echo "+ Example : ./fccSpider.sh htko89 full"
    echo "+ Actions : See below."
    echo "++ full : Download FCC curriculum map & challenge descriptions, personal profile, export results"
    echo "++ map : Download FCC curriculum map & challenge descriptions."
    echo "++ profile : Download & export personal profile. Map must be downloaded or error will error."
    echo "++ empty  : Download & export empty profile. Map must be downloaded or error will error."
    echo "++ clear  : Deletes all maps and exports."
  fi
  echo
