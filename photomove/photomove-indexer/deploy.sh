#!/usr/bin/env bash
PACKAGE_RELATIVE_PATH=./deployment_packages/code.zip 
PACKAGE_REAL_PATH=$(realpath $PACKAGE_RELATIVE_PATH)
cd ./function_code/
zip $PACKAGE_REAL_PATH lambda_function.py sqs_record_handler.py



aws lambda update-function-code \
--function-name $1 \
--zip-file fileb://$PACKAGE_REAL_PATH
