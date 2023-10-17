# github-graph
project for the course Data Intensive Computing ID2221

## Instructions - Graph Visualization

### Prerequisites
- Install conda by following the instructions on the official website.
- Create a new environment by running `conda create --name github-graph`.
- Activate the environment by running `conda activate github-graph`.

## Instructions - Scraper

### How to run the project
1. Navigate to the project directory.
2. Create a `.env` file in the root directory.
3. You can set your API key by running `echo "your_api_key_here" > .env`.
4. Install the requirements by running `conda install --file requirements.txt`.
5. Run the scraper by running `python src/scraper.py`.

## Instructions - Streaming

### Prerequisites

Install the necessary versions needed to run the application - this includes:
- `apache-spark 3.5.0` 
- `python 3.12.0`.

It is recommended to use the `pyenv` library to handle moving between different python versions.

### How to run

1. Navigate to the `src` directory
2. Run the `spark-submit streamer.py` command
3. Move commit files to the `src/input_files` directory

The streaming appliciation will store checkpoints in the `src/checkpoints` directory, and remember output files in the `src/output_files` directory. To re-run the application without checkpoints/old outputs, remove these directories and re-run the streaming application in step 2 above.