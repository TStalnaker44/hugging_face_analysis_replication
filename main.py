
import os
import scripts.cleanup.find_and_update
import scripts.mining.get_model_list as gml
import scripts.mining.model_data_miner as mdm
import scripts.mining.get_dataset_list as gdl
import scripts.mining.data_scraper as ds
import scripts.cleanup.clean_datasets as cd
import scripts.cleanup.make_indices as mi
import scripts.cleanup.format_model_data as cmd
import scripts.cleanup.read_from_html as rf
import scripts.graphing.make_graph as mg
import scripts.graphing.create_lineages as cl
import scripts.graphing.make_chains as mkchains
import scripts.analysis.find_interesting_compliance_examples as fie
import scripts.analysis.get_license_changes as glc
import scripts.analysis.get_naming_issues as gni
import scripts.analysis.get_license_analysis as gla
import scripts.analysis.find_cycles as fc
import scripts.analysis.examine_chain_structure as ecs
import scripts.analysis.examine_owners as eo
import scripts.analysis.examine_declared_datasets as edd
import scripts.analysis.get_top_n_base_models as gtnbm
import scripts.analysis.get_top_n_datasets as gtnd
import scripts.analysis.get_top_n_models as gtnm

# INSTRUCTIONS: Set to True the tasks / analyses you wish to run

# Mining / cleaning / graphing tasks:

MINE_MODEL_LIST = False
MINE_DATASET_LIST = False
MINE_MODEL_DATA = False
MINE_UNAUTHORIZED_PAGES = False

MAKE_INDICES = False

FORMAT_MODEL_DATA = False
UPDATE_AMBIGUOUS_DATA = False
UPDATE_RENAMED_DATA = False
FIND_MISSING_DATA = False
REPLACE_DOIS = False

CONVERT_HTML_TO_JSON = False

CREATE_GRAPH = False
CREATE_LINEAGES = False
MAKE_CHAINS = False

# Analyses:

FIND_INTERESTING_EXAMPLES = False
GET_LICENSE_CHANGES = False
GET_NAME_ISSUES = False
GET_LICENSE_ANALYSIS = False
GET_CYCLES = False

EXAMINE_CHAIN_STRUCTURE = False
EXAMINE_OWNERS = False
EXAMINE_DECLARED_DATASETS = False

GET_TOP_N_BASE_MODELS = False
GET_TOP_N_DATASETS = False
GET_TOP_N_MODELS = False

# Mining utilities
if MINE_MODEL_LIST:
    gml.getModels(5000)
if MINE_DATASET_LIST:
    gdl.getDatasets(500)
if MINE_MODEL_DATA:
    mdm.mineData(1_000_000, 5)
if MINE_UNAUTHORIZED_PAGES:
    ds.mineWebPages(os.path.join("data", "raw_data", "log_files", "unauthorized.txt"))

# Data cleaning and preparation utilities
if MAKE_INDICES:
    mi.makeIndices()
if FORMAT_MODEL_DATA:
    cmd.main(thread_count=10)
if UPDATE_AMBIGUOUS_DATA:
    scripts.cleanup.find_and_update.find_and_update_ambiguous_models()
    scripts.cleanup.find_and_update.find_and_update_ambiguous_datasets()
if UPDATE_RENAMED_DATA:
    scripts.cleanup.find_and_update.find_and_update_renamed_models()
    scripts.cleanup.find_and_update.find_and_update_renamed_datasets()
if FIND_MISSING_DATA:
    scripts.cleanup.find_and_update.find_404_models()
if REPLACE_DOIS:
    scripts.cleanup.find_and_update.replaceDOIs()

if CONVERT_HTML_TO_JSON:
    rf.main()

if CREATE_GRAPH:
    mg.main()
if CREATE_LINEAGES:
    cl.main()
if MAKE_CHAINS:
    mkchains.main()

# Data analysis

if FIND_INTERESTING_EXAMPLES:
    fie.findExamples()
if GET_LICENSE_CHANGES:
    glc.main()
if GET_NAME_ISSUES:
    gni.main()
if GET_LICENSE_ANALYSIS:
    gla.main()
if GET_CYCLES:
    fc.main()

if EXAMINE_CHAIN_STRUCTURE:
    ecs.main()
if EXAMINE_OWNERS:
    eo.main()
if EXAMINE_DECLARED_DATASETS:
    edd.main()
if GET_TOP_N_BASE_MODELS:
    gtnbm.main()
if GET_TOP_N_DATASETS:
    gtnd.main()
if GET_TOP_N_MODELS:
    gtnm.main()

    

# cd.main()

