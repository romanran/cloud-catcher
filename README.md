cloud-catcher

# Installation
Download and install Conda
https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html
    clone the project and run
    conda create --name cc
    conda activate cc

## Usage
In \batches copy and rename _batches_sample.py to batches.py and edit it
Then run this command
    python main.py batch_key
where batch_key is your key of a batch in batches.py

Wait for the success info and exit of the process.

Config for RGB recipes https://blaylockbk.github.io/goes2go/_build/html/reference_guide/index.html#rgb-recipes

### Developing
To add a dependency: conda install -c conda-forge your_lib