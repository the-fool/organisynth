#!/bin/bash
set -e

cmd=$1
shift
args="$@"

elm () {
    elm-live $1/Main.elm --output=$1/elm.js
}

cms () {
    elm color_mono_seq
}

cmr () {
    elm color_mono_rhythmer
}

case $cmd in
    cmr) cmr;;
    cms) cms;;
esac
