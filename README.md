# ITSC-4155-Team-12

This repo is for ITSC-4155 group 12 of the 2023 spring semester.

# Project Description

This site allows users to navigate through a vast array of films. These films are accomponied by relevant information, such as: actors, runtimes, critic scores, and what platforms one can find these films on. The site allows users to easily add films to a personal queue, and at the end of their session they can allow the site to
randomly choose a film from their list.

# Setup

## Prerequisites
    - NodeJS
    - Make
    - Python
    - Pip
    - Virtualenv

## Backend 

IT IS RECCOMENDED TO RUN VSCODE IN ADMINISTRATOR MODE IF YOU ARE ON WINDOWS

The current project setup requires the use of a unix system, I highly recommend using the Windows Subsytem for Linux (WSL2: https://learn.microsoft.com/en-us/windows/wsl/install) if you want to use this project on Windows! If you are using Windows then the current iteration of Makefile will not work correctly.

### Project Setup

This project requires the preinstallation of Make, Pip, and Virtualenv.

To setup, simply run the command: `make init` while in the backend directory.

To test the project, simply run the command: `make test` while in the backend directory.

If additional dependencies are needed, they can be added using the command: `poetry add [DEPENDENCY NAME]`

## Frontend 

Make sure that npm is installed before continuing.

To get started, React can be installed with the command: `npm install react`

After react is installed, navigate to the frontend directory and run the command: `npm start` to start the server.

For more information, check the readme in the frontend directory.

# TO RUN PROJECT

You must run flask app and react app seperately.

for flask, make sure you are in the backend directory and run `poetry run flask run`

for react, make sure you are in the frontend directory and run `npm start`

# API

Currently the only api endpoint is "/search-prod-info?query={query}"