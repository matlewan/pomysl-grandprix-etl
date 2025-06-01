# Chessmanager analysis

Application for downloading and analysing data of chess tournaments "Pomysł GrandPrix" in Posnan. Source data is available on chessmanager.com. Example websites on chessmanager:
- [tournaments list](https://www.chessmanager.com/en/tournaments?name=Pomysl+GrandPrix)
- [tournament info](https://www.chessmanager.com/en/tournaments/6247242935042048)
- [tournament players](https://www.chessmanager.com/en/tournaments/6247242935042048/players)
- [tournament rounds](https://www.chessmanager.com/en/tournaments/6247242935042048/rounds)
- [tournament results](https://www.chessmanager.com/en/tournaments/6247242935042048/results)

## Goals
- download data from chessmanager and expose it in JSON format
- compute final results of GrandPrix editions, where GrandPrix edition consists of 5 consecutive tournaments
- calculate statistics of all players, eg. head-to-head results, overall/tournament performance
- publish raw data to allow browse it without leaving this website

## How to run
Visit website https://matlewan.github.io/pomysl-grandprix/

## Requirements / tools
- python and pip
- vue.js
- npm and npx 

## How to develop

1. Install python libraries
    ```sh
    cd backend-python
    pip install -r requirements.txt
    ```

1. Download data from chessmanager.com to JSON file

    ```sh
    cd backend
    python -m src.download
    python -m src.process
    ```
