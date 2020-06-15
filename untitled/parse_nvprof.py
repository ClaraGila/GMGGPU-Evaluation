import sys
import os
import matplotlib.pyplot as plt
import numpy as np

smoother = "wrap_form0_cell_integral_otherwise"
inject = "wrap_loopy_kernel_inject"
prolong = "wrap_loopy_kernel_prolong"
restrict = "wrap_loopy_kernel_restrict"
wrap_kernel = "wrap_"
zero = "wrap_zero"
path_to_save = "/home/clara/GMGGPU-Evaluation/untitled/plots/test/"

def save_graphs(level, mesh_f, mesh_s, test_name, prolong_entries, restrict_entries):
    fig, ax = plt.subplots()
    x = np.linspace(prolong_entries[0], level - 1, 100) + 1
    y = 4 ** (x-level+1) * prolong_entries[-1]
    ax.set_yscale('log', basey=4)
    ax.grid(linestyle=':')
    plt.title('mesh coarse: (' + mesh_f + ', ' + mesh_s + ') and level: ' + str(level))
    plt.plot(list(range(1, len(prolong_entries) + 1)), prolong_entries, marker='o', label="prolong")
    plt.plot(list(range(1, len(restrict_entries) + 1)), restrict_entries, marker='o', label="restrict")
    plt.plot(x, y, linestyle=':', label="x^4")
    plt.legend()
    plt.ylabel('time(ms)')
    plt.xlabel('levels')
    plt.grid(True)
    # plt.show()
    plt.savefig(path_to_save + test_name + '.png')
    plt.clf()

def parse_time(line):
    parts = line.split()
    time = float(parts[1][:-2])
    if parts[1][-2:] == "us":
        time = time / 1000
    elif parts[1][-2:] == "ns":
        time = time / 1000000
    return time

def parse_f(test_no, level, counter, mesh_f, mesh_s, filename, out_filename):
    with open(filename) as f:
        lines = [line.rstrip() for line in f]
        prolong_values = []
        restrict_values = []
        inject_seen = 0
        restrict_seen = 0
        prolong_seen = 0
        for line in lines:
            if smoother in line:
                with open(out_filename, 'a') as fi:
                    smooth_max = parse_time(line)
                    fi.write(str(smooth_max) + " ")
                break
        for line in lines:
            if inject in line and inject_seen < 3 * level:
                inject_seen += 1
                continue
            elif inject_seen >= 3 * level:
                if restrict in line:
                    restrict_values.append(parse_time(line))
                    if restrict_seen == 0:
                        with open(out_filename, 'a') as fi:
                            restrict_max = parse_time(line)
                            fi.write(str(restrict_max) + " ")
                        restrict_seen = 1
                        continue
                if prolong in line:
                    prolong_values.append(parse_time(line))
                    prolong_seen += 1
                    if prolong_seen == level:
                        with open(out_filename, 'a') as fi:
                            prolong_max = parse_time(line)
                            fi.write(str(prolong_max) + "\n")
                        continue
        if test_no != 1:
            with open(out_filename, 'a') as fi:
                fi.write("Prolong values: ")
                for it in prolong_values:
                    fi.write(str(it) + " ")
                fi.write("\n Restrict values: ")
                for it in restrict_values:
                    fi.write(str(it) + " ")
                fi.write("\n\n\n\n\n")
            plot_file_name = str(level) + "-(" + mesh_f + "," + mesh_s + ")" + "-plot"
            save_graphs(level, mesh_f, mesh_s, plot_file_name, prolong_values, restrict_values[::-1])

def parse_all(level, mesh_f, mesh_s, filename, out_filename):
    restrict_sum = 0
    prolong_sum = 0
    inject_sum = 0
    smooth_sum = 0
    total_sum = 0

    with open(filename) as f:
        lines = [line.rstrip() for line in f]
        for line in lines:
            if wrap_kernel in line:
                total_sum += parse_time(line)
            if smoother in line:
                smooth_sum += parse_time(line)
            elif prolong in line:
                prolong_sum += parse_time(line)
            elif restrict in line:
                restrict_sum += parse_time(line)
            elif inject in line:
                inject_sum += parse_time(line)
        with open(out_filename, 'a') as fi:
            # fi.write("Level " + str(level) + " mesh (" + mesh_f + " , " + mesh_s + ")\n")
            # fi.write("Restrict " + str(restrict_sum) + " prolong: " + str(prolong_sum) + " inject: " + str(inject_sum) +
            #          " smooth" + str(smooth_sum) + " total: " + str(total_sum) + " percentage kernels " +
            #          str((restrict_sum + inject_sum + prolong_sum)/total_sum) + "\n")
            fi.write(str(restrict_sum) + " " + str(prolong_sum) + " " + str(inject_sum) +
                     " " + str(smooth_sum) + " " + str(total_sum) + "\n")

def calculate_memory_prolong(level, mesh_f, mesh_s):
    next = 2 ** level * 2 ** level * mesh_f * mesh_s * 4
    coarse = 2 ** (level - 1) * 2 ** (level - 1) * mesh_f * mesh_s * 4
    node_locations = next * 2
    coarse_coords = coarse / 2
    map_coord_field = 2 ** level * 2 ** level * mesh_f * mesh_s * 3
    map_global_dof_vec = 2 ** level * 2 ** level * mesh_f * mesh_s * 6
    sum = next + coarse + node_locations + coarse_coords + map_coord_field + map_global_dof_vec
    return sum * 8

def parse_one(level, mesh_f, mesh_s, filename, out_filename):
    with open(filename) as f:
        lines = [line.rstrip() for line in f]
        prolong_values = []
        mem = []
        restrict_values = []
        inject_seen = 0
        restrict_seen = 0
        prolong_seen = 0
        for line in lines:
            if inject in line and inject_seen < 3 * level:
                inject_seen += 1
                continue
            elif inject_seen >= 3 * level:
                # if restrict in line:
                #     restrict_values.append(parse_time(line))
                #     if restrict_seen == 0:
                #         with open(out_filename, 'a') as fi:
                #             restrict_max = parse_time(line)
                #             fi.write(str(restrict_max) + " ")
                #         restrict_seen = 1
                #         continue
                if prolong in line:
                    prolong_values.append(parse_time(line))
                    prolong_seen += 1
                    mem.append(calculate_memory_prolong(prolong_seen, int(mesh_f), int(mesh_s)))
        with open(out_filename, 'a') as fi:
            for idx, val in enumerate(prolong_values):
                fi.write(str(val) + " " + str(mem[idx]) + "\n")

def parse_line(line):
    parts = line.split()
    sum = float(parts[2])
    if(parts[1] == 'Kbyte'):
        sum /= 1000
    if(parts[1] == 'Gbyte'):
        sum *= 1000
    return sum


def parse_section(lines):
    read_sum ='dram__bytes_read.sum'
    write_sum = 'dram__bytes_write.sum'
    throughput = 'dram__throughput.avg.pct_of_peak_sustained_elapsed'
    sm_throughput = 'sm__pipe_fp64_cycles_active'
    flops = 'smsp__sass_thread_inst_executed_ops_dadd_dmul'
    flop_s = 'smsp__sass_thread_inst_executed_op_dfma_pred_on.sum'
    flop_rest = 'smsp__sass_thread_inst_executed_op'
    mbytes_sum = 0
    throughput_num = 0.0
    sm_num = 0.0
    flop_sum = 0.0
    flop_count = 0.0

    for idx, line in enumerate(lines):
        name = line.split()[0]
        if read_sum == name or write_sum == name:
            mbytes_sum += parse_line(line)
            continue
        if throughput in line:
            throughput_num = float(line.split()[2])
        if sm_throughput in line:
            sm_num = float(line.split()[2])
        if flops in line:
            flop_sum = float(line.split()[2])
        if flop_s in line:
            flop_count = flop_count + 2 * float(line.split()[2].replace(',', ''))
        elif flop_rest in line:
            flop_count += float(line.split()[2].replace(',', ''))


    return (mbytes_sum, throughput_num, sm_num, flop_sum, flop_count / 10**6)



def parse_nvc(level, mesh_f, mesh_s, input_file, output_file):
    start = '==PROF== Disconnected from process '
    start_seen = False
    inject_seen = 0
    restrict_total_dram = []
    restrict_throughput_dram = []
    sm_throughput= []
    flops = []
    flop_num = []

    with open(input_file) as f:
        lines = [line.rstrip() for line in f]
        it_list = iter(enumerate(lines))
        for idx, line in it_list:
            if start in line:
                start_seen = True
                continue
            if start_seen is False:
                continue
            if inject in line and inject_seen < 3 * level:
                inject_seen += 1
                continue
            elif inject_seen >= 3 * level:
                if restrict in line:
                    (mbytes_sum, throughput_num, sm_num, flop_sum, flop_count) = parse_section(lines[(idx+3):(idx+11)])
                    restrict_total_dram.append(mbytes_sum)
                    restrict_throughput_dram.append(throughput_num)
                    sm_throughput.append(sm_num)
                    flops.append(flop_sum)
                    flop_num.append(flop_count)
                    [next(it_list) for _ in range(10)]
    restrict_total_dram.reverse()
    restrict_throughput_dram.reverse()
    sm_throughput.reverse()
    flops.reverse()
    flop_num.reverse()
    with open(output_file, 'a') as fi:
        for idx, val in enumerate(restrict_total_dram):
            fi.write(str(val) + " ")
        fi.write("\n")
        for idx, val in enumerate(restrict_throughput_dram):
            fi.write(str(val) + " ")
        fi.write("\n")
        for idx, val in enumerate(sm_throughput):
            fi.write(str(val) + " ")
        fi.write("\n")
        for idx, val in enumerate(flops):
            fi.write(str(val) + " ")
        fi.write("\n")
        for idx, val in enumerate(flop_num):
            fi.write(str(val) + " ")
        fi.write("\n")



test_no = int(sys.argv[1])
level = int(sys.argv[2])
counter = int(sys.argv[3])
mesh_f = sys.argv[4]
mesh_s = sys.argv[5]
input_file = sys.argv[6]
output_file = sys.argv[7]
if test_no == 3:
    parse_all(level, mesh_f, mesh_s, input_file, output_file)
elif test_no == 4:
    parse_nvc(level, mesh_f, mesh_s, input_file, output_file)
else:
    parse_f(test_no, level, counter, mesh_f, mesh_s, input_file, output_file)