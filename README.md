# The Promise and Perils of Managing the ML Supply Chain in the Era of Software 2.0: Lessons Learned from Hugging Face

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

### Data Used in Analysis

## Scripts