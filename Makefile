################################################################################
# Makefile for RecipeMeal calculator : setup, commands
################################################################################

# Prefer bash shell
export SHELL=/bin/bash

## Define repositories dependencies paths

## Make sure of current python path
export PYTHONPATH=$(pwd)

self := $(abspath $(lastword $(MAKEFILE_LIST)))
parent := $(dir $(self))

ifneq (,$(VERBOSE))
    override VERBOSE:=
else
    override VERBOSE:=@
endif

.PHONY: test
test:
	$(VERBOSE) nosetests ./tests/test_recipe_api.py
.PHONY: smoke
smoke:
	$(VERBOSE) nosetests ./
.PHONY: install
install:
	$(VERBOSE) pip install -r requirements.txt
.PHONY: inspect
inspect:
	$(VERBOSE) pylint --ignore-patterns=venv,Makefile,README,requirements ./*

