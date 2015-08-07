#!/usr/bin/env bash
BRANCH=master
TARGET_REPO=textbook/textbook.github.io.git
PELICAN_OUTPUT_FOLDER=output

if [ "$TRAVIS_PULL_REQUEST" == "false" ]; then
    echo -e "Starting to deploy to Github Pages\n"
    if [ "$TRAVIS" == "true" ]; then
        git config --global user.email "travis@travis-ci.org"
        git config --global user.name "Travis"
    fi
    #go into directory and authenticate to remote
    cd $PELICAN_OUTPUT_FOLDER
    git checkout master
    git remote rm origin
    git remote add origin https://${GH_PAGES}@github.com/$TARGET_REPO
    #add, commit and push files
    git add -f -A .
    echo -e "Changes:\n"
    git status -s
    git commit -m "Travis build $TRAVIS_BUILD_NUMBER pushed to Github Pages"
    git push -fq origin $BRANCH > /dev/null
    echo -e "Deploy completed\n"
fi
