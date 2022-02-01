#!/usr/bin/env zsh

export PATH=$PATH:/usr/local/bin:
eval "$(pyenv init -)"
echo $PATH

pipenv run python exposurebot.py >> script.log 2>&1
