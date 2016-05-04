#!/usr/bin/env python

import argparse
import csv
import sys
import itertools
import numpy as np
import cbioportal

from collections import defaultdict


def collect_data(infile, genes):

    sample_data = defaultdict(dict)

    with open(infile, 'rU') as casefile:
        reader = csv.reader(casefile, dialect='excel-tab')
        reader.next()
        for row in reader:
            if row[0].startswith("#"):
                sys.stderr.write("WARNING: Skipping commented input line\n")
                continue

            print row
            profile_data = cbioportal.get_multi_gene(row[1], row[2], genes)
            clin_data = cbioportal.get_clin_data(row[1])

            profile_header = profile_data.pop(0)
            clin_header = clin_data.pop(0)

            profile_header_data = profile_header.split()
            profile_header_data.pop(0)
            profile_header_data.pop(0)

            if len(profile_data) <= 0:
                sys.stderr.write("ERROR: No profile data retrieved for query, "
                                 "with response header: {}\n".format(profile_header))
                continue

            if len(clin_data) <= 0:
                sys.stderr.write("ERROR: No clinical data retrieved for query, "
                                 "with response header: {}\n".format(clin_header))
                continue

            for line in profile_data:
                data = line.split()
                data.pop(0)
                gene_id = data.pop(0)

                # print gene_id

                i = 0
                for value in data:
                    # sys.stdout.write("{}: {}\n".format(profile_header_data[i], value))
                    sample_data[profile_header_data[i]][gene_id] = value
                    i += 1

            for line in clin_data:
                if not line.strip():
                    continue
                data = line.split()
                sample_data[data[0]]['AGE'] = data[1]

    return sample_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cases', help="Input file with study, case, and profile ids [Required]")
    parser.add_argument('-g', '--genes', help="Text file with list of genes to evaluate for correlations. The first "
                                              "listed gene will control the binning")
    parser.add_argument('-o', '--output', help='Output file name. Will overwrite existing.')

    args = parser.parse_args()

    with open(args.genes, 'rU') as genefile:
        genes = genefile.read().splitlines()

    with open(args.output, 'w') as outfile:
        outfile.write("Sample\tAge")
        for gene in genes:
            outfile.write("\t{}".format(gene))
        outfile.write("\n")

        sample_data_dict = collect_data(args.cases, genes)

        for sample in sample_data_dict:
            outfile.write("{}\t{}".format(sample, sample_data_dict[sample]['AGE']))

            for gene in genes:
                outfile.write("\t{}".format(sample_data_dict[sample].get(gene) or "NaN"))
            outfile.write("\n")

