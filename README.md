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

### nc data arrays
x = [40, 41, 42, 40, 41, 42, 40, 41, 42] # long

y= [1, 1, 1, 0, 0, 0, -1, -1, -1] # lat

z = [0, 2, 0, 2, 4, 2, 1, 2, 1] # pressure

image grid:

			<- x - longitude
	 _ _40 41 42 _
	1 |  0  2  0
	0 |  2  4  2
   -1 |  1  2  1
    🠕			 z - pressure, temperature, windy etc. data 
	y - latitude