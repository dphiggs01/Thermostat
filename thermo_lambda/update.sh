#!/usr/bin/env bash
WORKING_DIR=`pwd`
FUNCTION_NM=$1
FUNCTION_DIR=${WORKING_DIR}/${FUNCTION_NM}
ZIP_FILE='fileb://'${WORKING_DIR}'/index.zip'

echo $FUNCTION_DIR
if [ ! -d "$FUNCTION_DIR" ]; then
    echo no directory with function name passed! usage update.sh set_away
    exit
else
    cd $1
    zip -r ../index.zip *
    aws --output 'json' lambda 'update-function-code' \
        --function-name ${FUNCTION_NM} \
        --zip-file $ZIP_FILE
fi
