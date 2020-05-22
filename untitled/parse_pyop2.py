import sys
prolong = "wrap_loopy_kernel_prolong"
restrict = "wrap_loopy_kernel_restrict"
inject = "wrap_loopy_kernel_inject"
mult = "MatMult"
transp = "MatMultTranspose"
solve = "KSPSolve"
coarsen = "DMCoarsen"
interp = "DMCreateInterp"
injn = "DMCreateInject"
smooth = "wrap_form0_cell_integral_otherwise"

prolong_entries = []
restrict_entries = []

start = "--- Event Stage 2: benchmark"

def parse_f(filename, out_filename):
    seen = False
    with open(filename) as f:
        total_time = 0.0
        kernels_time = 0.0
        w_mat_mult = 0.0
        dm_time = 0.0
        smooth_sum = 0.0
        lines = [line.rstrip() for line in f]
        for line in lines:
            if start in line:
                seen = True
                continue
            if (prolong in line or restrict in line or inject in line) and seen:
                parts = line.split()
                name = parts[0]
                with open(out_filename, 'a') as fi:
                    kernels_time = kernels_time + float(parts[3])
                    fi.write(name + " Count_max: " + parts[1] + " Count_ratio: " + parts[2] + " Time_max: " + parts[3] + " Time_ratio: " + parts[4] + " Global time: " + parts[10] + "\n")
            if (mult in line or transp in line) and seen:
                parts = line.split()
                w_mat_mult = w_mat_mult + float(parts[3])
            if (solve in line) and seen:
                parts = line.split()
                ksp_solve = float(parts[3])
            if smooth in line and seen:
                parts = line.split()
                smooth_sum = float(parts[3])
            if (coarsen in line or injn in line or interp in line) and seen:
                parts = line.split()
                dm_time = dm_time + float(parts[3])
            if "------------------" in line and seen:
                break
            if seen:
                parts = line.split()
                if len(parts) > 0:
                    total_time = total_time + float(parts[3])
    with open(out_filename, 'a') as fi:
        # fi.write("------------Total time: " + str(total_time) + "-----percentage kernels: " +
        #          str((kernels_time / total_time) * 100) + "---------div by solve:" +
        #          str(((kernels_time) / ksp_solve) * 100) +"-------with DM:" +
        #          str(((kernels_time + dm_time) / ksp_solve) * 100) + "---\n")
        fi.write("------------Total time: " + str(total_time) + "-----total kernels: " +
                 str(kernels_time) + "---------smooth:" +
                 str(smooth_sum) + "-------percentange: " +
                 str((kernels_time / smooth_sum) * 100) + "---\n")


input_file = sys.argv[1]
output_file = sys.argv[2]
parse_f(input_file, output_file)
