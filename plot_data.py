#!/usr/bin/env python

import argparse
import csv
import numpy as np
import plotly
import plotly.graph_objs as go

from collections import defaultdict


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input file name.')

    args = parser.parse_args()

    data = defaultdict(list)

    with open(args.input, 'r') as infile:
        reader = csv.reader(infile, dialect='tab-excel')
        header = reader.next()
        header.pop()

        for row in reader:
            i = 0
            row.pop()
            for element in row:
                data[header[i]].append(element)
            i += 1

    traces = list()
    for gene in data:
        if gene != 'Age':
            trace = go.Scatter(
                x=data[gene],
                y=data['Age'],
                mode='markers'
            )

    plotly.offline.plot(traces, filename="correlations.html")
