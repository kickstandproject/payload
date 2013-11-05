#!/bin/sh
TEMPDIR=`mktemp -d`
CFGFILE=payload.conf.sample
tools/config/generate_sample.sh -b ./ -p payload -o $TEMPDIR
if ! diff $TEMPDIR/$CFGFILE etc/payload/$CFGFILE
then
    echo "E: payload.conf.sample is not up to date, please run tools/config/generate_sample.sh"
    exit 42
fi
