__author__ = 'dgaston'

import cbioportal
import argparse
import csv


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cases', help="Input file with study, case, and profile ids [Required]")
    parser.add_argument('-g', '--genes', help="Text file with list of genes to evaluate for correlations")
    parser.add_argument('-o', '--output', help='Output file name')

    args = parser.parse_args()

    with open(args.genes, 'rU') as genefile:
        genes = genefile.read().splitlines()

    gene_list = ",".join(genes)

    with open (args.output, 'w') as outfile:
        with open (args.cases, 'rU') as casefile:
            reader = csv.reader(casefile, dialect='excel-tab')
            for row in reader:
                profile_data = cbioportal.get_multi_gene(row[1], row[2], gene_list)
