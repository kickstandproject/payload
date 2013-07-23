#!/bin/sh
TEMPDIR=`mktemp -d`
CFGFILE=stripe.conf.sample
tools/config/generate_sample.sh -b ./ -p stripe -o $TEMPDIR
if ! diff $TEMPDIR/$CFGFILE etc/stripe/$CFGFILE
then
    echo "E: stripe.conf.sample is not up to date, please run tools/config/generate_sample.sh"
    exit 42
fi
