#!/usr/bin/env python

import argparse
import csv
import sys
import itertools
import numpy as np
import scipy.stats

import cbioportal

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cases', help="Input file with study, case, and profile ids [Required]")
    parser.add_argument('-g', '--genes', help="Text file with list of genes to evaluate for correlations. The first "
                                              "listed gene will control the binning")
    parser.add_argument('-o', '--output', help='Output file name. Will overwrite existing.')
    parser.add_argument('-e', '--expression', help='File to write expression values per case for the binning control '
                                                   'gene. Opens in append-mode so delete if already exists')

    args = parser.parse_args()

    # Gene1 will be the genes whose expression controls binning
    with open(args.genes, 'rU') as genefile:
        genes = genefile.read().splitlines()

    prime_gene = genes[0]

    with open(args.output, 'w') as outfile:
        outfile.write("Study\tCase List\tProfile\tGenes\tMin Exp\t25th Pctl\tMedian\t75th Pctl\tMax\t"
                      "Bin1 (Low) #\tBin1 R\tBin1 p\t"
                      "Bin2 #\tBin2 R\tBin2 p\t"
                      "Bin3 #\tBin3 R\tBin3 p\t"
                      "Bin4 (High) #\tBin4 R\tBin4 p\n")
        with open(args.cases, 'rU') as casefile:
            reader = csv.reader(casefile, dialect='excel-tab')
            reader.next()
            for row in reader:
                if row[0].startswith("#"):
                    sys.stderr.write("WARNING: Skipping commented input line\n")
                    continue

                profile_data = cbioportal.get_multi_gene(row[1], row[2], genes)
                header = profile_data.pop(0)

                if len(profile_data) <= 0:
                    sys.stderr.write("ERROR: No data retrieved for query, with response header: {}\n".format(header))
                    continue

                # Because gene expression data is returned in alphabetical order we have to find the line
                # containing our control gene data line, remove it from the data_lines, and isolated it for comparisons
                primary_data = list()
                i = 0
                for line in profile_data:
                    # print line
                    data = line.split()
                    # Remove Gene ID
                    data.pop(0)
                    gene = data.pop(0)
                    if gene == prime_gene:
                        for e in data:
                            if e != 'NaN':
                                primary_data.append(float(e))
                        profile_data.pop(i)
                        break
                    i += 1

                if len(primary_data) <= 0:
                    sys.stderr.write("WARNING: No Expression values for data set. Skipping\n")
                    continue

                with open(args.expression, 'a') as expressionfile:
                    expressionfile.write("{}\t{}\t{}".format(row[0], row[1], row[2]))
                    for e in data:
                        if e != 'NaN':
                            expressionfile.write("\t{}".format(e))
                    expressionfile.write("\n")

                # Analyse the expression distribution of the control gene and assign samples to expression bins
                sorted_primary = np.asarray(sorted(primary_data))
                minimum = sorted_primary[0]
                maximum = sorted_primary[-1]
                lower = np.percentile(sorted_primary, 25)
                mid = np.percentile(sorted_primary, 50)
                upper = np.percentile(sorted_primary, 75)

                sys.stdout.write("For gene {gene} the 25th percentile is {low}, the median is {med}, and the 75th"
                                 "percentile is {up}\n".format(gene=prime_gene, low=lower, med=mid, up=upper))

                for data_line in profile_data:
                    data = data_line.split()

                    # Remove Gene ID and gene name
                    data.pop(0)
                    comp_gene = data.pop(0)

                    expression1_1 = list()
                    expression2_1 = list()

                    expression1_2 = list()
                    expression2_2 = list()

                    expression1_3 = list()
                    expression2_3 = list()

                    expression1_4 = list()
                    expression2_4 = list()

                    for values in itertools.izip(primary_data, data):
                        if values[0] != 'NaN' and values[1] != 'NaN':
                            if values[0] < lower:
                                expression1_1.append(float(values[0]))
                                expression2_1.append(float(values[1]))
                            elif lower <= values[0] < mid:
                                expression1_2.append(float(values[0]))
                                expression2_2.append(float(values[1]))
                            elif mid <= values[0] < upper:
                                expression1_3.append(float(values[0]))
                                expression2_3.append(float(values[1]))
                            elif values[0] >= upper:
                                expression1_4.append(float(values[0]))
                                expression2_4.append(float(values[1]))
                            else:
                                sys.stderr.write("ERROR: Value {val} did not fit within binned "
                                                 "quartiles\n".format(val=values[0]))

                    outfile.write("{s}\t{c}\t{p}\t{g1} - {g2}\t"
                                  "{min}\t{t1}\t{med}\t{t3}\t{max}".format(s=row[0], c=row[1], p=row[2],
                                                                           g1=prime_gene, g2=comp_gene,
                                                                           min=minimum, t1=lower, med=mid, t3=upper,
                                                                           max=maximum))
                    if len(expression1_1) > 0 and len(expression2_1) > 0:
                        rho, pvalue = scipy.stats.spearmanr(expression1_1, expression2_1)
                        outfile.write("{}, {}\t{}\t{}\t".format(len(expression1_1), len(expression2_1), rho, pvalue))
                    else:
                        outfile.write("0, 0\tn/a\tn/a\t")

                    if len(expression1_2) > 0 and len(expression2_2) > 0:
                        rho, pvalue = scipy.stats.spearmanr(expression1_2, expression2_2)
                        outfile.write("{}, {}\t{}\t{}\t".format(len(expression1_2), len(expression2_2), rho, pvalue))
                    else:
                        outfile.write("0, 0\tn/a\tn/a\t")

                    if len(expression1_3) > 0 and len(expression2_3) > 0:
                        rho, pvalue = scipy.stats.spearmanr(expression1_3, expression2_3)
                        outfile.write("{}, {}\t{}\t{}\t".format(len(expression1_3), len(expression2_3), rho, pvalue))
                    else:
                        outfile.write("0, 0\tn/a\tn/a\t")

                    if len(expression1_4) > 0 and len(expression2_4) > 0:
                        rho, pvalue = scipy.stats.spearmanr(expression1_4, expression2_4)
                        outfile.write("{}, {}\t{}\t{}\n".format(len(expression1_4), len(expression2_4), rho, pvalue))
                    else:
                        outfile.write("0, 0\tn/a\tn/a\n")
