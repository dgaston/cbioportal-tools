__author__ = 'dgaston'

import argparse
import csv
import itertools
import scipy.stats

import cbioportal

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cases', help="Input file with study, case, and profile ids [Required]")
    parser.add_argument('-g', '--genes', help="Text file with list of genes to evaluate for correlations. The first "
                                              "listed gene will control the binning")
    parser.add_argument('-o', '--output', help='Output file name')

    args = parser.parse_args()

    # Gene1 will be the genes whose expression controls binning
    with open(args.genes, 'rU') as genefile:
        genes = genefile.read().splitlines()

    prime_gene = genes.pop(0)

    with open(args.output, 'w') as outfile:
        outfile.write("Study\tCase List\tProfile\tGenes\tNumbers\tSpearman's Rho\tP-Value\n")
        with open(args.cases, 'rU') as casefile:
            reader = csv.reader(casefile, dialect='excel-tab')
            reader.next()
            for row in reader:
                profile_data = cbioportal.get_multi_gene(row[1], row[2], genes)
                header = profile_data.pop(0)

                # Because gene expression data is returned in alphabetical order we have to find the line
                # containing our control gene data line, remove it from the data_lines, and isolated it for comparisons
                primary_data = list()
                i = 0
                for line in profile_data:
                    data = line.split()
                    # Remove Gene ID
                    data.pop(0)
                    gene = data.pop(0)
                    if gene == prime_gene:
                        primary_data = data
                        profile_data.pop(i)
                        break
                    i += 1

                # Analyse the expression distribution of the control gene and assign samples to expression bins

                for data_line in profile_data:
                    data = data_line.split()

                    # Remove Gene ID and gene gene name
                    data.pop(0)
                    gene1 = data.pop(0)

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
