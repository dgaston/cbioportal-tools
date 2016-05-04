#!/usr/bin/env python

import argparse
import csv
import sys
import itertools
import numpy as np

import cbioportal

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cases', help="Input file with study, case, and profile ids [Required]")
    parser.add_argument('-g', '--genes', help="Text file with list of genes to evaluate for correlations. The first "
                                              "listed gene will control the binning")
    parser.add_argument('-o', '--output', help='Output file name. Will overwrite existing.')

    args = parser.parse_args()

    with open(args.genes, 'rU') as genefile:
        genes = genefile.read().splitlines()
