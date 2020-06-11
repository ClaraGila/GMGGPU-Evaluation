import sys
prolong_entries = []
restrict_entries = []

start = "--- Event Stage 1: MG Apply"
interp = "MGInterp Level"

def parse_f(filename, out_filename):
    seen = False
    with open(filename) as f:
        lines = [line.rstrip() for line in f]
        for line in lines:
            if start in line:
                seen = True
                continue
            if interp in line and seen:
                parts = line.split()
                with open(out_filename, 'a') as fi:
                    fi.write(parts[23] + " ")
            if "------------------" in line and seen:
                break

input_file = sys.argv[1]
output_file = sys.argv[2]
parse_f(input_file, output_file)
