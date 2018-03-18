#!/usr/bin/env bash

pushd ~/TLP

git stash
git pull
git stash pop
pipenv shell
#sudo PYTHONPATH=. python TLP &

popd