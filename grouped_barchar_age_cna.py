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
            count_bin1 = 0.0000001
            count_bin2 = 0.0000001
            count_bin3 = 0.0000001
            count_bin4 = 0.0000001
            count_bin5 = 0.0000001

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

                if 75 < int(a) <= 85:
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

            trace1 = go.Bar(x=['Under 55', '55-65', '65-75', '75-85', '85 and Over'],
                            y=[num_neg2_bin1 / count_bin1,
                               num_neg2_bin2 / count_bin2,
                               num_neg2_bin3 / count_bin3,
                               num_neg2_bin4 / count_bin4,
                               num_neg2_bin5 / count_bin5],
                            name="Deep Loss")

            trace2 = go.Bar(x=['Under 55', '55-65', '65-75', '75-85', '85 and Over'],
                            y=[num_neg1_bin1 / count_bin1,
                               num_neg1_bin2 / count_bin2,
                               num_neg1_bin3 / count_bin3,
                               num_neg1_bin4 / count_bin4,
                               num_neg1_bin5 / count_bin5],
                            name="Shallow Loss")

            trace3 = go.Bar(x=['Under 55', '55-65', '65-75', '75-85', '85 and Over'],
                            y=[num_zero_bin1 / count_bin1,
                               num_zero_bin2 / count_bin2,
                               num_zero_bin3 / count_bin3,
                               num_zero_bin4 / count_bin4,
                               num_zero_bin5 / count_bin5],
                            name="Copy Neutral")

            trace4 = go.Bar(x=['Under 55', '55-65', '65-75', '75-85', '85 and Over'],
                            y=[num_pos1_bin1 / count_bin1,
                               num_pos1_bin2 / count_bin2,
                               num_pos1_bin3 / count_bin3,
                               num_pos1_bin4 / count_bin4,
                               num_pos1_bin5 / count_bin5],
                            name="Gain")

            trace5 = go.Bar(x=['Under 55', '55-65', '65-75', '75-85', '85 and Over'],
                            y=[num_pos2_bin1 / count_bin1,
                               num_pos2_bin2 / count_bin2,
                               num_pos2_bin3 / count_bin3,
                               num_pos2_bin4 / count_bin4,
                               num_pos2_bin5 / count_bin5],
                            name="Strong Gain")

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
