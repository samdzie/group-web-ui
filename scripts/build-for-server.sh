#!/bin/bash

# A script to build the Vue app and move the resulting dist directory
# to the server directory.

cd client
yarn install
yarn build
cd ..
cp -r client/dist server
