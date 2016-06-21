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
            count_bin1 = 0
            count_bin2 = 0
            count_bin3 = 0
            count_bin4 = 0
            count_bin5 = 0

            num_neg2_bin1 = 0
            num_neg1_bin1 = 0
            num_zero_bin1 = 0
            num_pos1_bin1 = 0
            num_pos2_bin1 = 0

            num_neg2_bin2 = 0
            num_neg1_bin2 = 0
            num_zero_bin2 = 0
            num_pos1_bin2 = 0
            num_pos2_bin2 = 0

            num_neg2_bin3 = 0
            num_neg1_bin3 = 0
            num_zero_bin3 = 0
            num_pos1_bin3 = 0
            num_pos2_bin3 = 0

            num_neg2_bin4 = 0
            num_neg1_bin4 = 0
            num_zero_bin4 = 0
            num_pos1_bin4 = 0
            num_pos2_bin4 = 0

            num_neg2_bin5 = 0
            num_neg1_bin5 = 0
            num_zero_bin5 = 0
            num_pos1_bin5 = 0
            num_pos2_bin5 = 0

            for d, a in itertools.izip(data[gene], data['Age']):
                if int(a) <= 55:
                    count_bin1 += 1

                    if int(d) == -2:
                        num_neg2_bin1 += 1
                    elif int(d) == -1:
                        num_neg1_bin1 += 1
                    elif int(d) == 0:
                        num_zero_bin1 += 1
                    elif int(d) == 1:
                        num_pos1_bin1 += 1
                    elif int(d) == 2:
                        num_pos2_bin1 += 1

                if 55 < int(a) <= 65:
                    count_bin2 += 1

                    if int(d) == -2:
                        num_neg2_bin2 += 1
                    elif int(d) == -1:
                        num_neg1_bin2 += 1
                    elif int(d) == 0:
                        num_zero_bin2 += 1
                    elif int(d) == 1:
                        num_pos1_bin2 += 1
                    elif int(d) == 2:
                        num_pos2_bin2 += 1

                if 65 < int(a) <= 75:
                    count_bin3 += 1

                    if int(d) == -2:
                        num_neg2_bin3 += 1
                    elif int(d) == -1:
                        num_neg1_bin3 += 1
                    elif int(d) == 0:
                        num_zero_bin3 += 1
                    elif int(d) == 1:
                        num_pos1_bin3 += 1
                    elif int(d) == 2:
                        num_pos2_bin3 += 1

                if 75 < int(a) <= 55:
                    count_bin4 += 1

                    if int(d) == -2:
                        num_neg2_bin4 += 1
                    elif int(d) == -1:
                        num_neg1_bin4 += 1
                    elif int(d) == 0:
                        num_zero_bin4 += 1
                    elif int(d) == 1:
                        num_pos1_bin4 += 1
                    elif int(d) == 2:
                        num_pos2_bin4 += 1

                if int(a) > 85:
                    count_bin5 += 1

                    if int(d) == -2:
                        num_neg2_bin5 += 1
                    elif int(d) == -1:
                        num_neg1_bin5 += 1
                    elif int(d) == 0:
                        num_zero_bin5 += 1
                    elif int(d) == 1:
                        num_pos1_bin5 += 1
                    elif int(d) == 2:
                        num_pos2_bin5 += 1

            trace1 = go.Bar(x=['-2', '-1', '0', '+1', '+2'],
                            y=[float(num_neg2_bin1) / float(count_bin1),
                               float(num_neg1_bin1) / float(count_bin1),
                               float(num_zero_bin1) / float(count_bin1),
                               float(num_pos1_bin1) / float(count_bin1),
                               float(num_pos2_bin1) / float(count_bin1)],
                            name="Under 55")

            trace2 = go.Bar(x=['-2', '-1', '0', '+1', '+2'],
                            y=[float(num_neg2_bin2) / float(count_bin2),
                               float(num_neg1_bin2) / float(count_bin2),
                               float(num_zero_bin2) / float(count_bin2),
                               float(num_pos1_bin2) / float(count_bin2),
                               float(num_pos2_bin2) / float(count_bin2)],
                            name="55-65")

            trace3 = go.Bar(x=['-2', '-1', '0', '+1', '+2'],
                            y=[float(num_neg2_bin3) / float(count_bin3),
                               float(num_neg1_bin3) / float(count_bin3),
                               float(num_zero_bin3) / float(count_bin3),
                               float(num_pos1_bin3) / float(count_bin3),
                               float(num_pos2_bin3) / float(count_bin3)],
                            name="65-75")

            trace4 = go.Bar(x=['-2', '-1', '0', '+1', '+2'],
                            y=[float(num_neg2_bin4) / float(count_bin4),
                               float(num_neg1_bin4) / float(count_bin4),
                               float(num_zero_bin4) / float(count_bin4),
                               float(num_pos1_bin4) / float(count_bin4),
                               float(num_pos2_bin4) / float(count_bin4)],
                            name="75-85")

            trace5 = go.Bar(x=['-2', '-1', '0', '+1', '+2'],
                            y=[float(num_neg2_bin5) / float(count_bin5),
                               float(num_neg1_bin5) / float(count_bin5),
                               float(num_zero_bin5) / float(count_bin5),
                               float(num_pos1_bin5) / float(count_bin5),
                               float(num_pos2_bin5) / float(count_bin5)],
                            name="Over 85")

            traces = [trace1, trace2, trace3, trace4, trace5]

            layout = go.Layout(title="Proportion of CNA Values per Age Group for Gene: {}".format(gene),
                               xaxis=dict(
                                   title="Age Group"
                               ),
                               yaxis=dict(
                                   title="Proportion of Samples"
                               ))
            figure = go.Figure(data=traces, layout=layout)

            plotly.offline.plot(figure, filename="{}_CNA_Proportions_Age_Group.html".format(gene))
