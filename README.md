# Retro Game Recommendation Search Engine

## Team Members
* Rashaud Savage - rsavage3

## Motivation
1. This project was created for CS 410 

2. This search engine was created for users who are retro game enthusiasts as well as for those who may not necessarily be able to get the latest games right away. This search engine takes the title of a game and recommends retro games that may be similar in title, theme, and/or gameplay, etc.

### Tech Stack

* `python`
    * Python is a high-level, general-purpose programming language
* `Dash`
    * Dash is an open source framework for building data visualization interfaces
* `pybomb`
    * a python package for accessing the GiantBomb API
* `GiantBomb API`
    * APIs that provide full access to video game structured-wiki content data in XML and JSON formats
* `rank-bm25`
    * A collection of algorithms for querying a set of documents and returning the ones most relevant to the query

### Functions and Structure

* `app.py`
    * Contains the main code for the search engine and serving the website over Dash
* `all_games.csv`
    * Final dataset of all game csv files after being fused into one dataset
* `genesis_games.csv`
    * contains the data from Giantbomb for Sega Genesis games.
* `gb_games.csv`
    * contains the data from Giantbomb for Gameboy games.
* `gbc_games.csv`
    * contains the data from Giantbomb for Gameboy Color games.
* `gg_games.csv`
    * contains the data from Giantbomb for Game Gear games.
* `psx_games.csv`
    * contains the data from Giantbomb for Playstation 1 games.
* `snes_games.csv`
    * contains the data from Giantbomb for Super Nintendo Entertainment System games.
* `n64_games.csv`
    * contains the data from Giantbomb for Nintendo 64 games.
* `dataset_fuser.csv`
    * contains the code to fuse all game csv into one dataset.

### Initial Setup

These setup instructions are for MacOS Users and UNIX users, but can be adapted for other platforms too.

1. Get a [GiantBomb API Key](https://www.giantbomb.com/api/) from the Giantbomb site by signing up for a **FREE** account. Then add to the `app.py` file on the following line:

```bash
GIANTBOMB_API = " " # NEED TO INCLUDE API KEY! https://www.giantbomb.com/api/
```

2. Run the following command:

```bash
pip install -r requirements.txt
```

2b. Alternatively, if you prefer, there is a docker file included to help build an image on docker:
* `dockerfile`
    * A text document that contains all the commands a user could call on the command line to assemble an image of the project
    * Build the image
    * Go to docker and deploy the image

The initial setup in order to build this project is ready.

### Running the project

1. To build and run the project, run:

```bash
python app.py
```

This should open up the search interface on http://127.0.0.1:8050/  (Please double check the Local URL its running on from console output)


### Python Package Documentation

You can read more about the python packages and API's used for this project here:

* [Giantbomb API] (https://www.giantbomb.com/api/)
* [Rank-bm25] (https://pypi.org/project/rank-bm25/)
* [PyBomb] (https://pybomb.readthedocs.io/en/latest/)

