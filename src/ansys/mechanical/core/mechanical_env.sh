#!/bin/bash

# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Check if at least one argument was provided
if [ $# -lt 1 ]; then
    echo "Usage: ./.mechanical-env [-r REVISION] [COMMAND]"
    exit 1
fi

# Initialize variables
revision=""
path=""
command=""

# Process command line arguments
#while [ "$#" -gt 0 ]; do
#    case "$1" in
#        -r|--revision)
#            revision="$2"
#	    shift
#	    shift
#            ;;
#        -p|--path)
#	    path="$3"
#	    shift
#	    shift
#	    ;;
#        *)
#            command="$@"
#            break
#            ;;
#    esac
#done

# get command line options passed in by mechanical-env
# the colon after each letter means there's going to be
# a string after it
while getopts r:p:c: flag
do
    case "${flag}" in
        r|--revision) revision=${OPTARG};;
	p|--path) path=${OPTARG};;
	c|--command) command=${OPTARG};;
    esac
done

#echo $revision
#echo $path
#echo $command

# Check if a command was provided
if [ -z "$command" ]; then
    echo "Usage: mechanical-env [-r REVISION] [COMMAND]"
    exit 1
fi

# Determine the appropriate command to run find-mechanical
#if [ -n "$revision" ]; then
#    find_mechanical_command="find-mechanical -r $revision"
#else
#    find_mechanical_command="find-mechanical"
#fi

# Run the find-mechanical command and capture its output
# output="$path"  #$($find_mechanical_command)

# Check if there was an error
#if [ $? -ne 0 ]; then
#    echo "Error running the find-mechanical."
#    exit 1
#fi

# Extract and print the captured values
# read -r version DS_INSTALL_DIR <<< "$output"

# Envs
DS_INSTALL_DIR=$path
awp_root="AWP_ROOT${version}"
eval ${awp_root}=$DS_INSTALL_DIR/..

# Env vars used by workbench (mechanical) code
awp_locale="AWP_LOCALE${version}"
eval ${awp_locale}=en-us
cadoe_libdir="CADOE_LIBDIR${version}"
eval ${cadoe_libdir}=${!awp_root}/commonfiles/language/${!awp_locale}
ANSYSLIC_DIR=${!awp_root}/../shared_files/licensing
ANSYSCOMMON_DIR=${!awp_root}/commonfiles
ansyscl="ANSYSCL${version}_DIR"
eval ${ansyscl}=${!awp_root}/licensingclient

# MainWin vars
ANSISMAINWINLITEMODE=1
MWCONFIG_NAME=amd64_linux
MWDEBUG_LEVEL=0
MWHOME=${!awp_root}/commonfiles/MainWin/linx64/mw
MWOS=linux
MWREGISTRY=${DS_INSTALL_DIR}/WBMWRegistry/hklm_${MWCONFIG_NAME}.bin
MWRT_MODE=classic
MWRUNTIME=1
MWUSER_DIRECTORY="${HOME}/.mw"
MWDONT_XCLOSEDISPLAY=1

# dynamic library preload
LD_PRELOAD=libstdc++.so.6.0.28

# dynamic library load path
LD_LIBRARY_PATH=${!awp_root}/tp/stdc++\
:${!awp_root}/tp/openssl/1.1.1/linx64/lib\
:${MWHOME}/lib-amd64_linux\
:${MWHOME}/lib-amd64_linux_optimized\
:${LD_LIBRARY_PATH}\
:${!awp_root}/Tools/mono/Linux64/lib\
:${DS_INSTALL_DIR}/lib/linx64\
:${DS_INSTALL_DIR}/dll/linx64\
:${DS_INSTALL_DIR}/libshared/linx64\
:${!awp_root}/tp/IntelCompiler/2019.3.199/linx64/lib/intel64\
:${!awp_root}/tp/IntelMKL/2020.0.166/linx64/lib/intel64\
:${!awp_root}/tp/qt_fw/5.9.6/Linux64/lib\
:${!awp_root}/commonfiles/CAD/Acis/linx64\
:${!awp_root}/commonfiles/fluids/lib/linx64\
:${!awp_root}/Framework/bin/Linux64

# system path
PATH=${MWHOME}/bin-amd64_linux_optimized\
:${DS_INSTALL_DIR}/CommonFiles/linx64\
:${DS_INSTALL_DIR}/CADIntegration/linx64\
:${!awp_root}/Tools/mono/Linux64/bin\
:${PATH}

export $awp_root
export $awp_locale
export $cadoe_libdir
export ANSYSLIC_DIR
export ANSYSCOMMON_DIR
export $ansyscl

export ANSISMAINWINLITEMODE
export MWHOME
export MWCONFIG_NAME
export MWOS
export MWRUNTIME
export MWUSER_DIRECTORY
export MWRT_MODE
export MWDEBUG_LEVEL
export MWREGISTRY
export MWDONT_XCLOSEDISPLAY

export LD_PRELOAD
export LD_LIBRARY_PATH
export PATH

# run the command
eval $command
returnCode=$?
exit $returnCode
