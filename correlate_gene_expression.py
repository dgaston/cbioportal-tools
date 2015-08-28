__author__ = 'dgaston'

import argparse
import csv
import itertools

from scipy import spearmanr

import cbioportal

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cases', help="Input file with study, case, and profile ids [Required]")
    parser.add_argument('-g', '--genes', help="Text file with list of genes to evaluate for correlations")
    parser.add_argument('-o', '--output', help='Output file name')

    args = parser.parse_args()

    with open(args.genes, 'rU') as genefile:
        genes = genefile.read().splitlines()

    gene_list = "+".join(genes)

    with open(args.output, 'w') as outfile:
        outfile.write("Study\tCase List\tProfile\tGenes\tNumbers\tSpearman's Rho\tP-Value\n")
        with open(args.cases, 'rU') as casefile:
            reader = csv.reader(casefile, dialect='excel-tab')
            for row in reader:
                profile_data = cbioportal.get_multi_gene(row[1], row[2], gene_list)
                header = profile_data.pop(0)
                for pair in itertools.combinations(profile_data, 2):
                    gene1 = pair[0].pop(0)
                    gene2 = pair[1].pop(0)
                    expression1 = list()
                    expression2 = list()

                    for values in itertools.izip(expression1, expression2):
                        if values[0] != 'NaN' and values[1] != 'NaN':
                            expression1.append(float(values[0]))
                            expression2.append(float(values[1]))

                    rho, pvalue = spearmanr(expression1, expression2)
                    outfile.write("%s\t%s\t%s\t%s - %s\t%s, %s\t%s\t%s\n" %
                                  (row[0], row[1], row[2], gene1, gene2, len(expression1), len(expression2),
                                   rho, pvalue))
