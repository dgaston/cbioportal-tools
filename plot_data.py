#!/usr/bin/env python

import argparse
import csv
import numpy as np
import scipy.stats
import plotly
import plotly.graph_objs as go

from collections import defaultdict


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input file name.')

    args = parser.parse_args()

    data = defaultdict(list)

    with open(args.input, 'r') as infile:
        reader = csv.reader(infile, dialect='excel-tab')
        header = reader.next()
        header.pop(0)

        for row in reader:
            i = 0
            row.pop(0)
            for element in row:
                data[header[i]].append(element)
                i += 1

    traces = list()
    for gene in data:
        if gene != 'Age':
            trace = [go.Scatter(
                x=data[gene],
                y=data['Age'],
                mode='markers'
            )]
            rho, pvalue = scipy.stats.spearmanr(data[gene], data['Age'])
            traces.append(trace)

            layout = go.Layout(title="CNA Value vs Age for Gene: {}".format(gene),
                               xaxis=dict(
                                   title="CNA Value"
                               ),
                               yaxis=dict(
                                   title="Age"
                               ),
                               annotations=[
                                   dict(
                                       text="R = {}<br>P = {}".format(rho, pvalue),
                                       x=1,
                                       xref="paper",
                                       y=1,
                                       yref="paper"
                                   )
                               ])
            figure = go.Figure(data=trace, layout=layout)

            plotly.offline.plot(figure, filename="{}_correlations.html".format(gene))
