#! /usr/bin/env python3
# coding: utf-8
# branch: dev
# version: 1.0.2
# license: AGPLv3
# author: Yunfei Wang (yfwang0405@gmail.com)
#         Baochen Yang (yangbaochen1217@gmail.com)

import os
import pandas
import matplotlib
if not 'DISPLAY' in os.environ:
    matplotlib.use('Agg')  # if DISPLAY is not set
import pycircos
import matplotlib.pyplot as plt


def test():
    chroot = os.path.dirname(os.path.abspath(__file__))
    CNV = pandas.read_table(os.path.join(chroot, "data/scores.gistic"))
    CNV['chrom'] = 'chr' + CNV.Chromosome.astype(str)
    CNV = CNV.sort_values(['Chromosome', 'Start'])
    CNV.loc[CNV.Type == 'Del', 'frequency'] *= -1

    AMP = CNV.loc[CNV.Type == 'Amp', :]
    DEL = CNV.loc[CNV.Type == 'Del', :]

    chromsizes = pandas.read_table(os.path.join(chroot, "data/hg19.fa.sizes"), index_col=0, header=None, names=['length'])
    cg = pycircos.Circos(chromsizes, gap=2)

    # draw cytoband
    cg.draw_cytobands(8.1, 0.3, os.path.join(chroot, "data/cytoBand.txt.gz"))

    # draw chrom region
    cg.draw_scaffold(8.1, 0.3)
    cg.draw_ticks(8.1, 0.2, inside=True)
    cg.draw_scaffold_ids(9.2, inside=False, fontsize=15)

    # draw CNV
    cg.draw_scaffold(5.5, 0.01)
    cg.fill_between(5.5, AMP.iloc[:, :], start='Start', end='End', score='frequency', scale=2.0, facecolor='red', alpha=0.5)
    cg.fill_between(5.5, DEL.iloc[:, :], start='Start', end='End', score='frequency', scale=2.0, facecolor='blue', alpha=0.5)

    # draw links
    cg.draw_link(4.5, ['chr1', 'chr4'], [10000000, 10000000], [110000000, 110000000], color='purple', alpha=0.5)
    cg.draw_link(4.5, ['chr3', 'chr8'], [10000000, 10000000], [110000000, 110000000], color='lightblue', alpha=0.5)
    # save result to a png file
    plt.savefig(os.path.join(chroot, "./demo.png"))


if __name__ == "__main__":
    test()
