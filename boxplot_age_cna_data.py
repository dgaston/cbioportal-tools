#!/usr/bin/env python

import csv
import argparse
import itertools
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
            cna_neg2 = list()
            cna_neg1 = list()
            cna_zero = list()
            cna_pos1 = list()
            cna_pos2 = list()
            i = 0

            for d, a in itertools.izip(data[gene], data['Age']):
                if int(d) == -2:
                    cna_neg2.append(a)
                if int(d) == -1:
                    cna_neg1.append(a)
                if int(d) == -0:
                    cna_zero.append(a)
                if int(d) == -1:
                    cna_pos1.append(a)
                if int(d) == 2:
                    cna_pos2.append(a)

            trace_neg2 = go.Box(y=cna_neg2,
                                name="Deep Deletion")
            trace_neg1 = go.Box(y=cna_neg1,
                                name="Hemizygous Deletion")
            trace_zero = go.Box(y=cna_zero,
                                name="Neutral")
            trace_pos1 = go.Box(y=cna_pos1,
                                name="Amplification")
            trace_pos2 = go.Box(y=cna_pos2,
                                name="Strong Amplification")

            traces = [trace_neg2, trace_neg1, trace_zero, trace_pos1, trace_pos2]

            layout = go.Layout(title="Ages by CNA value for Gene: {}".format(gene),
                               xaxis=dict(
                                   title="CNA Value"
                               ),
                               yaxis=dict(
                                   title="Age"
                               ))
            figure = go.Figure(data=traces, layout=layout)

            plotly.offline.plot(figure, filename="{}_correlations.html".format(gene))
