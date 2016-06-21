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
            age_bin1 = list()
            age_bin2 = list()
            age_bin3 = list()
            age_bin4 = list()
            age_bin5 = list()
            i = 0

            for d, a in itertools.izip(data[gene], data['Age']):
                if int(a) <= 55:
                    age_bin1.append(d)
                if 55 < int(a) <= 65:
                    age_bin2.append(d)
                if 65 < int(a) <= 75:
                    age_bin3.append(d)
                if 75 < int(a) <= 55:
                    age_bin4.append(d)
                if int(a) > 85:
                    age_bin5.append(d)

            trace1 = go.Box(y=age_bin1,
                            name="Under 55")
            trace2 = go.Box(y=age_bin2,
                            name="55-65")
            trace3 = go.Box(y=age_bin3,
                            name="65-75")
            trace4 = go.Box(y=age_bin4,
                            name="75-85")
            trace5 = go.Box(y=age_bin5,
                            name="Over 85")

            traces = [trace1, trace2, trace3, trace4, trace5]

            layout = go.Layout(title="CNA Value By Age for Gene: {}".format(gene),
                               xaxis=dict(
                                   title="CNA Value"
                               ),
                               yaxis=dict(
                                   title="Age"
                               ))
            figure = go.Figure(data=traces, layout=layout)

            plotly.offline.plot(figure, filename="{}_correlations.html".format(gene))
