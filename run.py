import subprocess

test_dir = "/home/clara/GMGGPU-Evaluation/"
output_file_name = "output_test.txt"

def runNvp(test_no, test_file, nvp_out, out_file, level, mesh_f, mesh_s, counter):
    subprocess.call(['nvprof', '--print-gpu-trace', '--log-file', nvp_out, 'python3', test_file, level, mesh_f, mesh_s])
    subprocess.call(['python3', '/home/clara/GMGGPU-Evaluation/parse_nvprof.py', str(test_no), level, counter, mesh_f,
                     mesh_s, nvp_out, out_file])


def runNvc(output_file, out_file, level, mesh_f, mesh_s, counter):
    metrics = ['dram__throughput.avg.pct_of_peak_sustained_elapsed,dram__bytes_read.sum,'
               'dram__bytes_write.sum,smsp__sass_thread_inst_executed_op_dadd_pred_on.sum,'
               'smsp__sass_thread_inst_executed_ops_dadd_dmul_dfma_pred_on.avg.pct_of_peak_sustained_elapsed,'
               'sm__pipe_fp64_cycles_active.avg.pct_of_peak_sustained_elapsed,'
               'smsp__sass_thread_inst_executed_op_dmul_pred_on.sum,'
               'smsp__sass_thread_inst_executed_op_dfma_pred_on.sum']

    with open(output_file, 'w') as fi:
        subprocess.call(['nv-nsight-cu-cli', '--metrics'] + metrics + ['python3',
                                                                       '/home/clara/GMGGPU-Evaluation/test_w_args.py'],
                        stdout=fi)
    subprocess.call(['python3', '/home/clara/GMGGPU-Evaluation/parse_nvprof.py', str(4), level, counter, mesh_f, mesh_s,
                     output_file, out_file])

def runNvpTest(output_dir, test_file):
    counter = 0
    output_file = output_dir + output_file_name
    open(output_file, 'w').close()
    params_prob_1 = [[((32, 32), 1), ((16, 16), 2), ((8, 8), 3), ((4, 4), 4), ((2, 2), 5), ((1, 1), 6)],
                     [((64, 64), 1), ((32, 32), 2), ((16, 16), 3), ((8, 8), 4), ((4, 4), 5), ((2, 2), 6), ((1, 1), 7)],
                     [((128, 128), 1), ((64, 64), 2), ((32, 32), 3), ((16, 16), 4), ((8, 8), 5), ((4, 4), 6),
                      ((2, 2), 7), ((1, 1), 8)],
                     [((256, 256), 1), ((128, 128), 2), ((64, 64), 3), ((32, 32), 4), ((16, 16), 5), ((8, 8), 6),
                      ((4, 4), 7), ((2, 2), 8), ((1, 1), 9)]]
    new_prob = [[((1, 1), 6), ((7, 7), 4), ((1, 1), 7), ((1, 1), 8), ((9, 9), 5), ((5, 5), 6), ((7, 7), 6), ((1, 1), 9),
                 ((1, 1), 10)]]

    count = 0
    for case in new_prob:
        for ((i, j), k) in case:
            # for n in params_mesh[(i, j)]:
            counter += 1
            nvp_out = output_dir + "output_" + str(counter) + ".txt"
            with open(output_file, 'a') as fi:
                fi.write("Trying level: " + str(k) + " with mesh: (" + str(i) + "," + str(j) + ")\n")
            runNvp(2, test_dir + test_file, nvp_out, output_file, str(k), str(i), str(j), str(counter))
        count += 1
        with open(output_file, 'a') as fi:
            fi.write("Finished case: " + str(count) + "\n")

def runTestOne(output_dir, test_file, output_file_name):
    counter = 0
    output_file = output_dir + output_file_name
    open(output_file, 'w').close()
    new_prob = [[((1, 1), 6), ((7, 7), 4), ((1, 1), 7), ((1, 1), 8), ((9, 9), 5), ((5, 5), 6), ((7, 7), 6), ((1, 1), 9)]]

    count = 0
    for case in new_prob:
        for ((i, j), k) in case:
            counter += 1
            nvp_out = output_dir + "output_test1_" + str(counter) + ".txt"
            with open(output_file, 'a') as fi:
                fi.write(str(2**k * i * 2**k * j * 4) + " ")
            runNvp(1, test_dir + test_file, nvp_out, output_file, str(k), str(i), str(j), str(counter))
        count += 1
        import plots
        plots.plot_graph_test1(output_dir, output_file_name)


def runTestThree(output_dir, test_file, output_file_name):
    counter = 0
    output_file = output_dir + output_file_name
    open(output_file, 'w').close()
    new_prob = [[((1, 1), 6), ((7, 7), 4), ((1, 1), 7), ((1, 1), 8), ((9, 9), 5), ((5, 5), 6), ((1, 1), 9)]]

    count = 0
    for case in new_prob:
        for ((i, j), k) in case:
            counter += 1
            nvp_out = output_dir + "output_test3_" + str(counter) + ".txt"
            with open(output_file, 'a') as fi:
                fi.write(str(2**k * i * 2**k * j * 4) + " ")
            runNvp(3, test_dir + test_file, nvp_out, output_file, str(k), str(i), str(j), str(counter))
        count += 1
        import plots
        plots.plot_graph_test3(output_dir, output_file_name)

def runTestFour(output_dir, test_file, output_file_name):
    counter = 0
    output_file = output_dir + output_file_name
    open(output_file, 'w').close()
    # new_prob = [((1, 1), 10)]
    nvc_out = output_dir + "nvc_out.txt"
    runNvc(nvc_out, output_file, str(10), str(1), str(1), str(0))
    import plots
    plots.plot_graph_test4(output_dir, output_file_name)


#runTestOne("/home/clara/GMGGPU-Evaluation/results/nvp_test/test1/", "test.py", "output_test.txt")
#runNvpTest("/home/clara/GMGGPU-Evaluation/results/nvp_test/", "test.py")
#runTestThree("/home/clara/GMGGPU-Evaluation/results/nvp_test/test3/", "full_solver.py", "output_test.txt")
runTestFour("/home/clara/GMGGPU-Evaluation/results/nvp_test/test4/", "test.py", "output_test.txt")
