#!/bin/bash

xelatex index.tex && mv index.pdf xelatex.pdf
lualatex index.tex && mv index.pdf lualatex.pdf
