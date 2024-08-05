# The Promise and Perils of Managing the ML Supply Chain in the Era of Software 2.0: Lessons Learned from Hugging Face

**Note:** Due to the sheer volume of data to be shared, we have compressed many of the directories herein.  Some of the scripts require that these zip folders be extracted before running properly.

## Repository Structure
Our replication package is broken into two main parts: our data and the scripts used to mined, process, and analyze that data.  We more fully describe each of these pieces below.

## Data
Do to the large quantity of files, we have opted to provide most data in a zip file format.  The data can be broken into three main categories: raw data (what was directly mined from Hugging Face), cleaned data (a more concise, normalized, and usable version of the raw data), and data for analysis (produced graphs, spreadsheets, and the like).  We provide more information on each categories files and structure below.

### Raw Data
Here we describe the different files representing the raw data we extracted from Hugging Face.

#### model_lists 
Contains the results returned by using the Hugging Face API: `huggingface.co/api/models`.  We used a python script to programmatically step through all the pages returned and stored each page as it's own JSON file. Each file contains references to 1,000 models as well as some basic information describing them (ID, name, likes, downloads, etc). 

Each file as the date of mining appended to its name.

#### model_data
Contains the results returned by using the Hugging Face API: `huggingface.co/api/models/{owner_name}/{model_name}`.  We conducted a search for all the models with our previously collected model list and where possible, saved the resulting JSON to a file. Each file as the date of mining appended to its name.

The files have been organized and stored within zip folders to more easily facilitate sharing. The name of each zip folder represents the first character of the files contained within it.  For example, the model `ahmetyaylalioglu\llama2_prompt_recover_07-11-2024.json` would be found in `a.zip`. We also note that we replaced the `\` character in the model names with a character sequence very unlikely to occur in any model names: `_!##++##!_`.  We did this to prevent file system issues since the slash character is used in paths on Windows.

#### dataset_lists
Contains the results returned by using the Hugging Face API: `huggingface.co/api/datasets`.  We used a python script to programmatically step through all the pages returned and stored each page as it's own JSON file. Each file contains references to 1,000 models as well as some basic information describing them (ID, name, likes, downloads, etc). All information that we considered relevant for our purposes was available in this list, so we did not mine the full metadata for each individual dataset.

Each file as the date of mining appended to its name.

#### model_pages
Contains the raw HTML for the model pages where we weren't able to extract the model's metadata through the Hugging Face API.  These pages were grabbed and saved to file using a python script relying on the requests library.  We did not grab the associated CSS files since we were only concerned with the content and not the formatting of the pages.

Each file as the date of mining appended to its name.

#### html_to_json.json
A JSON file containing the relevant model information scraped from the HTML files found in the `model_pages` directory.

### Cleaned Data

#### model_data
Contains the cleaned and standardized model metadata stored across 77 JSON files.

#### datasets.json
A single JSON file containing all the dataset metadata relevant to our study.

#### indices
A collection of different indices that were created and used for mapping names during data normalization.

#### chains.json
A file containing all the linear chains (i.e. paths from some root base model to a sink node) that can be used to quickly and easily analyze the state of licensing in the ecosystem.

#### license_changes.json
A file containing the different license changes between base models and their derivatives along with associated counts.  For example, a base model licensed under `apache-2.0` and a derivative licened under `mit`.

#### license_type_mapping.csv
A CSV file that maps all licenses observed in our dataset to one of six pre-defined types: OSS, CC, ML, Data, Other, and Unknown.

### Graphs
The `graphs` folder contains three sub-folders (within the `lineages` directory), which have all been zipped for storage reasons, that contain the individual supply chains for models that have no dependents (i.e. they are sink nodes in the full Hugging Face model relation graph).  There are also two files (in different formats), that contain the full Hugging Face model relation graph: `model_relationship_graphml` and `model_relationship_graph.json`.

These are the sub-folders of the `lineages` directory:
- `graphml`: contains supply chain relationships for individual models in the graphml format.
- `json`: contains supply chain relationships for individual models in the json format.
- `text`: contains supply chain (and licensing) information for models in a human-readable, text format

Each of the three sub-folders above is further divided into index folders, each containing files starting with the character that names the folder.

### Data Used in Analysis
The `analysis.zip` file contains some additional files that were generated and used during the analysis process.

## Scripts

Three scripts can be found at the top-level of this repository:
- `main.py`: interface for interacting with the various sub-components and scripts.
- `quick_stats.py`: allows the researcher to get some quick statisitcs on the mined and processed data. 
- `analysis.py`: file containing functions that were used to collect information from the dataset during our analysis.

The remaining scripts created and used in this research can be found in the `scripts` folder. This folder contains six sub-directories:
- `analysis`: scripts that were used to analyze the mined and normalized data.
- `cleanup`: scripts that normalize and clean the mined data.
- `graphing`: script used to produce graphs from the cleaned data.
- `mining`: scripts used to mine data from Hugging Face, including those that use the API and requests + BeautifulSoup.
- `utilities`: contains scripts that are useful for interfacing with the data and are used by various portions of the repository.

Additionally, there are also two files at the top-level of the `scripts` directory:
- `config.py`: contains configuration information for the repository, notably the MODEL_SEPARATOR variable.
- `utils.py`: script that contain functions commonly used throughout the repository.