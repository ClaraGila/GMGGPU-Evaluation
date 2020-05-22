import sys
smoother = "wrap_form0_cell_integral_otherwise"
inject = "wrap_loopy_kernel_inject"
prolong = "wrap_loopy_kernel_prolong"
restrict = "wrap_loopy_kernel_restrict"

def parse_f(filename, out_filename):
    with open(filename) as f:
        lines = [line.rstrip() for line in f]
        kernel_sum = 0.0
        smoother_sum = 0.0
        for line in lines:
            if prolong in line or restrict in line or inject in line:
                parts = line.split()
                time = float(parts[1][:-2])
                if parts[1][-2:] == "ms":
                    time = time * 1000
                kernel_sum = kernel_sum + time
                with open(out_filename, 'a') as fi:
                    fi.write(line + "\n")
            if smoother in line:
                parts = line.split()
                time = float(parts[1][:-2])
                if parts[1][-2:] == "ms":
                    time = time * 1000
                smoother_sum = smoother_sum + time
                with open(out_filename, 'a') as fi:
                    fi.write(line + "\n")
        with open(out_filename, 'a') as fi:
            fi.write("Kernels time: " + str(kernel_sum) + " smoother time" + str(smoother_sum) + " percentage "
                     + str(kernel_sum / smoother_sum * 100) + "%\n\n\n")


input_file = sys.argv[1]
output_file = sys.argv[2]
parse_f(input_file, output_file)