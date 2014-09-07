#!/bin/sh
hg log | grep summary | sed s/summary\:\ \ \ \ /-/ > ews-aenderungen.log
