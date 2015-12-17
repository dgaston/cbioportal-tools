__author__ = 'dgaston'

import argparse
import csv
import itertools
import scipy.stats

import cbioportal

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cases', help="Input file with study, case, and profile ids [Required]")
    parser.add_argument('-g', '--genes', help="Text file with list of genes to evaluate for correlations")
    parser.add_argument('-o', '--output', help='Output file name')

    args = parser.parse_args()

    with open(args.genes, 'rU') as genefile:
        genes = genefile.read().splitlines()

    with open(args.output, 'w') as outfile:
        outfile.write("Study\tCase List\tProfile\tGenes\tNumbers\tSpearman's Rho\tP-Value\n")
        with open(args.cases, 'rU') as casefile:
            reader = csv.reader(casefile, dialect='excel-tab')
            reader.next()
            for row in reader:
                profile_data = cbioportal.get_multi_gene(row[1], row[2], genes)
                header = profile_data.pop(0)

                for pair in itertools.combinations(profile_data, 2):
                    data1 = pair[0].split()
                    data2 = pair[1].split()

                    # Remove Gene ID
                    data1.pop(0)
                    data2.pop(0)

                    gene1 = data1.pop(0)
                    gene2 = data2.pop(0)

                    expression1 = list()
                    expression2 = list()

                    for values in itertools.izip(data1, data2):
                        if values[0] != 'NaN' and values[1] != 'NaN':
                            expression1.append(float(values[0]))
                            expression2.append(float(values[1]))

                    if len(expression1) > 0 and len(expression2) > 0:
                        rho, pvalue = scipy.stats.spearmanr(expression1, expression2)
                        outfile.write("%s\t%s\t%s\t%s - %s\t%s, %s\t%s\t%s\n" %
                                      (row[0], row[1], row[2], gene1, gene2, len(expression1), len(expression2),
                                       rho, pvalue))
