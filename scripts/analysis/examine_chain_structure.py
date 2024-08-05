from ..utils import loadChainsData, print_stats

def main():
    chains = loadChainsData()
    print("Loaded chains for " + str(len(chains)) + " sinks")

    all_owners = get_model_owners(chains)
    print(str(len(all_owners)) + " total chains")
    num_owners = [len(k) for k in all_owners]
    print_stats(num_owners, 'Model owners in a chain')

    primary_counts = get_sink_owner_counts(chains)
    primary_counts_list = sorted(list(primary_counts.values()))
    print_stats(primary_counts_list, "Number of times a sink node's owner appears in its own chain")

    chain_licenses = get_licenses_in_chains(chains)
    chain_license_counts = sorted([len(k) for k in list(chain_licenses.values())])
    print_stats(chain_license_counts, "Licenses in a chain")

    chain_lengths = get_chain_lengths(chains)
    chain_lengths_list = sorted(chain_lengths.values())
    print_stats(chain_lengths_list, "Chain lengths")



#Get a list containing the sets of all unique model owners in each lineage chain
def get_model_owners(chains):
    all_owners = []
    for sink in list(chains.keys()):
        for chain in chains[sink]:
            owners = set()
            for model in chain:
                owner = model["model"].split("/")[0].lower()
                owners.add(owner)
            all_owners.append(owners)
    return all_owners

#Get a dictionary mapping each chain to the the number of times its sink node's owner appears in that model chain
def get_sink_owner_counts(chains):
    primary_counts = dict()
    for sink in list(chains.keys()):
        primary_owner = sink.split("_!##++##!_")[0].lower()
        i = 0
        for chain in chains[sink]:
            key = sink + "--" + str(i)
            primary_counts[key] = 0
            for model in chain:
                owner = model["model"].split("/")[0].lower()
                if owner == primary_owner:
                    primary_counts[key] += 1
            i += 1
    return primary_counts

#Get a dictionary mapping each chain to the licenses in that chain
def get_licenses_in_chains(chains):
    chain_licenses = dict()
    for sink in list(chains.keys()):
        i = 0
        for chain in chains[sink]:
            key = sink + "--" + str(i)
            licenses = set()
            for model in chain:
                for license in model["license"]:
                    licenses.add(license)
            chain_licenses[key] = licenses
            i += 1
    return chain_licenses

#Get a dictionary mapping each chain to the length of that chain
def get_chain_lengths(chains):
    chain_lengths = dict()
    for leaf in list(chains.keys()):
        i = 0
        for chain in chains[leaf]:
            key = leaf + "--" + str(i)
            chain_lengths[key] = len(chain)
            i += 1
    return chain_lengths


