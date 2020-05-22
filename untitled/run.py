import subprocess

test_dir = "/home/clara/PycharmProjects/untitled/"
output_file_name = "output_test.txt"

def runScript(test_file, pyop2_out, out_file, level, mesh_f, mesh_s):
    f = open(pyop2_out, 'w')
    subprocess.call(['python3', test_file, level, mesh_f, mesh_s, '-log_view'], stdout=f)
    f.close()
    subprocess.call(['python3', '/home/clara/PycharmProjects/untitled/parse_pyop2.py', pyop2_out, out_file])

def runNvp(test_file, nvp_out, out_file, level, mesh_f, mesh_s):
    # f = open(nvp_out, 'w')
    subprocess.call(['nvprof', '--log-file', nvp_out, 'python3', test_file, level, mesh_f, mesh_s])
    # f.close()
    subprocess.call(['python3', '/home/clara/PycharmProjects/untitled/parse_nvprof.py', nvp_out, out_file])

def runTest(output_dir, test_file):
    counter = 0
    output_file = output_dir + output_file_name
    open(output_file, 'w').close()
    params = {1: [(10, 10), (20, 20), (30, 30), (40, 40), (50, 50), (60, 60)],
              2: [(10, 10), (20, 20), (30, 30), (40, 40), (50, 50), (60, 60)],
              3: [(10, 10), (20, 20), (30, 30), (40, 40), (50, 50), (60, 60)],
              4: [(10, 10), (20, 20), (30, 30), (40, 40), (50, 50), (60, 60)],
              5: [(10, 10), (20, 20)]}
    params_mesh = {(10, 10): [1, 2, 3, 4, 5, 6],
                   (20, 20): [1, 2, 3, 4, 5],
                   (30, 30): [1, 2, 3, 4],
                   (40, 40): [1, 2, 3, 4],
                   (50, 50): [1, 2, 3],
                   (60, 60): [1, 2, 3]}
    params_prob_1 = [[((32, 32), 1), ((16, 16), 2), ((8, 8), 3), ((4, 4), 4), ((2, 2), 5), ((1, 1), 6)],
    [((64, 64), 1), ((32, 32), 2), ((16, 16), 3), ((8, 8), 4), ((4, 4), 5), ((2, 2), 6), ((1, 1), 7)],
    [((128, 128), 1), ((64, 64), 2), ((32, 32), 3), ((16, 16), 4), ((8, 8), 5), ((4, 4), 6), ((2, 2), 7), ((1, 1), 8)],
    [((256, 256), 1),((128, 128), 2), ((64, 64), 3), ((32, 32), 4), ((16, 16), 5), ((8, 8), 6), ((4, 4), 7), ((2, 2), 8), ((1, 1), 9)],
    [((512, 512), 1), ((256, 256), 2),((128, 128), 3), ((64, 64), 4), ((32, 32), 5), ((16, 16), 6)]]
    levels = [1, 2, 3, 4, 5]
    meshes = [(10, 10), (20, 20), (30, 30), (40, 40)]
    count = 0
    for case in params_prob_1:
        for ((i, j), k) in case:
        # for n in params_mesh[(i, j)]:
            counter += 1
            pyop2_out = output_dir + "output_" + str(counter) + ".txt"
            with open(output_file, 'a') as fi:
                fi.write("Trying level: " + str(k) + " with mesh: (" + str(i) + "," + str(j) + ")\n")
            runScript(test_dir + test_file, pyop2_out, output_file, str(k), str(i), str(j))
        count += 1
        with open(output_file, 'a') as fi:
            fi.write("Finished case: " + str(count) + "\n")

def runNvpTest(output_dir, test_file):
    counter = 0
    output_file = output_dir + output_file_name
    open(output_file, 'w').close()
    params_prob_1 = [[((32, 32), 1), ((16, 16), 2), ((8, 8), 3), ((4, 4), 4), ((2, 2), 5), ((1, 1), 6)],
                     [((64, 64), 1), ((32, 32), 2), ((16, 16), 3), ((8, 8), 4), ((4, 4), 5), ((2, 2), 6), ((1, 1), 7)],
                     [((128, 128), 1), ((64, 64), 2), ((32, 32), 3), ((16, 16), 4), ((8, 8), 5), ((4, 4), 6),
                      ((2, 2), 7), ((1, 1), 8)],
                     [((256, 256), 1), ((128, 128), 2), ((64, 64), 3), ((32, 32), 4), ((16, 16), 5), ((8, 8), 6),
                      ((4, 4), 7), ((2, 2), 8), ((1, 1), 9)],
                     [((512, 512), 1), ((256, 256), 2), ((128, 128), 3), ((64, 64), 4), ((32, 32), 5), ((16, 16), 6)]]
    count = 0
    for case in params_prob_1:
        for ((i, j), k) in case:
            # for n in params_mesh[(i, j)]:
            counter += 1
            nvp_out = output_dir + "output_" + str(counter) + ".txt"
            with open(output_file, 'a') as fi:
                fi.write("Trying level: " + str(k) + " with mesh: (" + str(i) + "," + str(j) + ")\n")
            runNvp(test_dir + test_file, nvp_out, output_file, str(k), str(i), str(j))
        count += 1
        with open(output_file, 'a') as fi:
            fi.write("Finished case: " + str(count) + "\n")

runNvpTest("/home/clara/PycharmProjects/untitled/results/nvp_test/", "test.py")

#runTest("/home/clara/PycharmProjects/untitled/results/test/", "test.py")
#runTest("/home/clara/PycharmProjects/untitled/results/harder_solver/", "harder_solver.py")
#runTest("/home/clara/PycharmProjects/untitled/results/diff_meshes/", "diff_meshes.py")
#runTest("/home/clara/PycharmProjects/untitled/results/3D/", "3D.py")
