# github-graph
project for the course Data Intensive Computing ID2221

## Instructions - Environment

Install the necessary versions needed to run the application - this includes:
- `python 3.12.0`

It is recommended to use the `pyenv` library to handle moving between different python versions.

You can then run the following command to install the needed packages from the `requirements.txt` file (make sure the terminal is in the root project directory):
- `pip install -r requirements.txt` 

## Instructions - Scraper

### How to run the project
1. Navigate to the project directory.
2. Create a `.env` file in the root directory.
3. You can set your API key by running `echo "your_api_key_here" > .env`.
4. Install the requirements by running `conda install --file requirements.txt`.
5. Run the scraper by running `python src/scraper.py`.

## Instructions - Streaming commits, Visualizing Relations

### How to run

1. Navigate to the `src` directory
2. Run the `python visualizer.py` command to start the visualization UI.
3. Run the `python importer.py` command to move files from the data folder (scraper) to the streaming application
4. Run the `python streamer.py` to start reading files from the input files directory
    - The moving of the files can also be done dynamically, i.e. in the case of a real streaming environment. The spark app reacts to changes in the directory and updates data as it runs.
5. Run the `python exporter.py` command to export files to the visualizer.
6. Browse the graph on your configured localhost address. On macOS, it should be `127.0.0.1` (see command line output for actual address when starting the visualizer)

The streaming appliciation will store checkpoints in the `src/checkpoints` directory, and remember output files in the `src/output_files` directory. To re-run the application without checkpoints/old outputs, remove these directories and re-run the streaming application in step 4 above.

Similarily, if you're moving files individually to the input\_files directory, you will need to run the exporter periodically to update the visualizer.