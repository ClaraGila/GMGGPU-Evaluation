import matplotlib.pyplot as plt

def plot_graph_test1(output_dir, output_file_name):
    file = output_dir + output_file_name
    with open(file) as f:
        lines = [line.rstrip() for line in f]
        x_axis = []
        smooth = []
        restrict = []
        prolong = []
        for line in lines:
            parts = line.split()
            x_axis.append(float(parts[0]))
            smooth.append(float(parts[1]))
            restrict.append(float(parts[2]))
            prolong.append(float(parts[3]))

        plt.title("DoF and kernel times")
        fig, ax = plt.subplots()
        ax.grid(linestyle=':')
        plt.plot(x_axis, smooth, marker='x', label="smooth")
        plt.plot(x_axis, restrict, marker='+', label="restrict")
        plt.plot(x_axis, prolong, marker='o', label="prolong")
        plt.legend()
        plt.ylabel('time(ms)')
        plt.xlabel('DoF')
        plt.grid(True)
        plt.savefig(output_dir + 'DoFTime.png')
        plt.clf()

def plot_graph_test3(output_dir, output_file_name):
    file = output_dir + output_file_name
    with open(file) as f:
        lines = [line.rstrip() for line in f]
        inject = []
        smooth = []
        restrict = []
        prolong = []
        total = []
        x_axis = []
        for line in lines:
            parts = line.split()
            x_axis.append(float(parts[0]) / 1000)
            restrict.append(float(parts[1]) / 1000)
            prolong.append(float(parts[2]) / 1000)
            inject.append(float(parts[3]) / 1000)
            smooth.append(float(parts[4]) /1000)
            total.append(float(parts[5]) / 1000)

        plt.title("DoF and kernel times")
        fig, ax = plt.subplots()
        ax.grid(linestyle=':')
        plt.plot(x_axis, smooth, marker='x', label="smooth")
        plt.plot(x_axis, restrict, marker='+', label="restrict")
        plt.plot(x_axis, prolong, marker='o', label="prolong")
        plt.plot(x_axis, inject, marker='*', label="inject")
        plt.plot(x_axis, total, marker='o', label="total", linestyle='dashed')
        plt.legend()
        plt.ylabel('time(s)')
        plt.xlabel('DoF')
        plt.grid(True)
        plt.savefig(output_dir + 'DoFTime.png')
        plt.clf()

def plot_graph_test4(output_dir, output_file_name):
    file = output_dir + output_file_name
    with open(file) as f:
        lines = [line.rstrip() for line in f]
        total_dram = [float(i) for i in lines[0].split()]
        throughput = [float(i) / 100 * 128 for i in lines[1].split()]
        sm_throughput = [float(i) for i in lines[2].split()]
        flops = [float(i) for i in lines[3].split()]
        flop_num = [float(i) for i in lines[4].split()]
        fig, ax = plt.subplots()
        ax.grid(linestyle=':')
        # plt.plot(list(range(1, len(total_dram) + 1)), sm_throughput, marker='x', label="SM throughput(%)")
        plt.plot(list(range(1, len(throughput) + 1)), throughput, marker='x', label="DRAM throughput(%)")
        plt.plot(list(range(1, len(flops) + 1)), flops, marker='x', label="FLOPs throughput(%)")
        plt.legend()
        plt.xlabel('level')
        plt.ylabel('% of BabelStream')
        plt.grid(True)
        plt.savefig(output_dir + 'bottleneck.png')
        plt.clf()