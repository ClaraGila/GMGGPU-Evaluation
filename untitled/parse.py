import numpy as np
import matplotlib.pyplot as plt
import re

prolong = "wrap_loopy_kernel_prolong_TIME"
restrict = "wrap_loopy_kernel_restrict_TIME"
inject = "wrap_loopy_kernel_inject_TIME"
smooth = "wrap_form0_cell_integral_otherwise_TIME"

file = "/home/clara/multigrid_logs.txt"
prolong_entries = []
restrict_entries = []
test_start = "test_poisson.py::test_poisson_gmg_gpu["
out = "out='"
path_to_save = '/home/clara/multigrid_logs/'

def save_graphs(test_name, prolong_entries, restrict_entries):
    nums = list(range(0, len(prolong_entries)))
    height = prolong_entries
    bars = nums
    y_pos = np.arange(len(bars))
    plt.figure(1)
    graph1 = plt.bar(y_pos, height)
    # Custom Axis title
    plt.xlabel('prolong_' + test_name, fontweight='bold', color='orange', fontsize='17', horizontalalignment='center')
    plt.savefig(path_to_save + 'prolong_' + test_name + '.png')
    plt.clf()

    nums = list(range(0, len(restrict_entries)))
    height = restrict_entries
    bars = nums
    y_pos = np.arange(len(bars))
    plt.figure(2)
    graph2 = plt.bar(y_pos, height)

    # Custom Axis title
    plt.xlabel('restrict_' + test_name, fontweight='bold', color='orange', fontsize='17', horizontalalignment='center')
    plt.savefig(path_to_save + 'restrict_' + test_name + '.png')
    plt.clf()

def parse_pycharm():
    with open(file) as f:
        prolong_sum = 0.0
        restrict_sum = 0.0
        inject_sum = 0.0
        others_sum = 0.0
        first = True
        lines = [line.rstrip() for line in f]
        remaining = ""
        count = 1
        for line in lines:
            if test_start in line:
                test = re.search('test_poisson.py::test_poisson_gmg_gpu\[(.*)\] ##teamcity', line)
                if test is not None:
                    test_name = test.group(1)
                else:
                    test_name = None
            if out in line:
                line = line.split(out, 1)[1]
                parts = line.split('|n')
                # parts.pop(0)
                if first:
                    first = False
                    remaining = parts[len(parts) - 1].split('\'')[0]
                    parts.pop(len(parts) - 1)
                    #parts[len(parts) - 1] = parts[len(parts) - 1].split('\'')[0]]
                else:
                    count += 1
                    parts[0] = remaining + parts[0]
                    remaining = parts[len(parts) - 1].split('\'')[0]
                    parts.pop(len(parts) - 1)

                for part in parts:
                    sections = part.split('=')
                    if sections[0] == prolong:
                        prolong_entries.append(float(sections[1]))
                        prolong_sum += float(sections[1])
                        # print("\n", sections[0])
                        # print("\n", sections[1])
                    elif sections[0] == restrict:
                        restrict_entries.append(float(sections[1]))
                        restrict_sum += float(sections[1])
                        # print("\n", sections[0])
                        # print("\n", sections[1])
                    elif sections[0] == inject:
                        inject_sum += float(sections[1])
                    else:
                        # print("\n", sections[0])
                        # print("\n", sections[1])
                        others_sum += float(sections[1])
                # save_graphs(test_name, prolong_entries, restrict_entries)
                # prolong_entries = []
                # restrict_entries = []
        total_sum = prolong_sum + restrict_sum + inject_sum + others_sum
        print("Prolong: {0}, restrict: {1}, others: {2}, percent {3}% count {4}".format(prolong_sum, restrict_sum, others_sum, (
                    prolong_sum + restrict_sum + inject_sum) / total_sum * 100, count))
def parse_f(file, filename):
    with open(file) as f:
        prolong_sum = 0.0
        restrict_sum = 0.0
        others_sum = 0.0
        inject_sum = 0.0
        smooth_sum = 0.0
        lines = [line.rstrip() for line in f]
        lines.pop(len(lines) - 1)
        for line in lines:
            sections = line.split('=')
            if sections[0] == prolong:
                prolong_entries.append(float(sections[1]))
                prolong_sum += float(sections[1])
            elif sections[0] == restrict:
                restrict_entries.append(float(sections[1]))
                restrict_sum += float(sections[1])
            elif sections[0] == inject:
                inject_sum += float(sections[1])
            elif sections[0] == smooth:
                smooth_sum += float(sections[1])
            else:
                others_sum += float(sections[1])
        total_sum = prolong_sum + restrict_sum + inject_sum + others_sum
        print("File: {6} -- Prolong: {0}, restrict: {1}, inject:{2}, others: {3}, smooth: {4}, percent {5}%".
              format(prolong_sum, restrict_sum, inject_sum,others_sum, smooth_sum, (prolong_sum + restrict_sum + inject_sum) / total_sum * 100,
                    filename))

def parse_files():
    dir = '/home/clara/mg_results/'
    import os
    for filename in os.listdir(dir):
            parse_f(os.path.join(dir, filename), filename)

parse_files()
#parse_pycharm()