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

## Architecture 
## Cosine Similarity 
How does it work? 
Cosine similarity is a technique used to determine how similar two documents or vectors are, regardless of their size. It works by measuring the cosine of the angle between the two vectors when they are represented in a multi-dimensional space.

Think of it like this: you have a movie recommendation system that recommends movies based on the similarity of their plot summaries. Each movie is represented by a vector that contains information about the words and phrases used in the plot summary. For example, the plot summary for the movie "The Godfather" might be represented by a vector that includes words like "mafia", "family", and "crime".

When a user searches for a movie to watch, their search query is represented by a vector. The system then compares the user's query vector to the vectors of all the movies in the database using cosine similarity.

If the cosine similarity between the user's query and a particular movie vector is high, that means the plot summary of the movie is very similar to the user's search query. This suggests that the movie may be a good recommendation for the user.

On the other hand, if the cosine similarity between the user's query and a particular movie vector is low, that means the plot summary of the movie is not very similar to the user's search query. This suggests that the movie may not be a good recommendation for the user.

In this way, cosine similarity helps the recommendation system to find movies that are most similar to the user's search query, regardless of the length or complexity of the plot summaries.



