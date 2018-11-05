#!/usr/bin/env bash
WORKING_DIR=`pwd`
FUNCTION_NM=$1
FUNCTION_DIR=${WORKING_DIR}/${FUNCTION_NM}
ZIP_FILE='fileb://'${WORKING_DIR}'/index.zip'

#FUNCTION_NM=${FUNCTION_DIR:2}
echo $FUNCTION_DIR
if [ ! -d "$FUNCTION_DIR" ]; then
    echo no directory with function name passed! usage publish.sh set_away
    exit
else
    cd $1
    zip -r ../index.zip *
    aws --output 'json' lambda 'create-function' \
        --function-name $FUNCTION_NM \
        --handler 'lambda_function.lambda_handler' \
        --runtime 'python2.7' \
        --role  'arn:aws:iam::280056172273:role/alexa_lambda_role' \
        --timeout 3 \
        --memory-size 128 \
        --zip-file $ZIP_FILE
fi
