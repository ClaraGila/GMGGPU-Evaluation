This project plots 4 types of graphs analysing the performance of transfer kernels of a matrix-free, geometric multigrid solver ran on GPUs in the Firedrake compiler (the Firedrake configuration used to test these is below).

The four types of plots are:
1. Time in s taken by smooth, restrict and prolong to be executed on the finest mesh with associated DoF
2. Time in s taken per level for prolong and restrict,compared to expected exponential time increase
3. Total times in s of GMG kernels ran for different problems of increasing DoF
4. Nsight Compute output for double precision GFLOP throughput and DRAM throughput (utilisation compared to theoretical peak) per GMG level for prolong, restrict and inject 

# Firedrake config 

{"firedrake": "5df0fe8a4ef45325351f7837b2fd7b3eab08a92f", \
"PyOP2": "3d2acf6ab88169c1a20550f677086164eccbd77f", \
"tsfc": "33bfbc1aa6c966bfdf6fade327a677a343e53bcd", \
"COFFEE": "72a4464aa18fd408de5304ac467db18d7af2b670", \
"ufl": "4516a6d5023eb5dfe62ec2431865e125aa6daf97", \
"FInAT": "2f0e0bd61fd5800920ed66a2c3347d4d916c0045", \
"fiat": "4ca7e9a0ace2540d6f6d1f844a96f4d6b9f553fc", \
"petsc":  "905158c6f9a6776daf927fe3564cfe0f0afe9e21", \
"petsc4py": "0db95a997847575cb29d419dce50be1016914253", \
"loopy": "83cb903d4f2d4df6a9dbfcdbd37b63bb3cfa54e1", \
"metarelease_info_file": null, \
"title": "GPU accelerated geometric multigrid in the Firedrake compiler"}

# Prerequisites
* Firedrake venv - https://www.firedrakeproject.org/zenodo.html
* nvprof running in the Firedrake venv - https://docs.nvidia.com/cuda/profiler-users-guide/index.html
* nv-nsight-cu-cli running in the Firedrake venv - https://docs.nvidia.com/nsight-compute/NsightComputeCli/index.html

# Zenodo to reference
@software{firedrake_zenodo_2020_3894682, \
  author       = {firedrake-zenodo}, \
  title        = {{Software used in 'GPU accelerated geometric 
                   multigrid in the Firedrake compiler'}}, \
  month        = jun,\
  year         = 2020,\
  publisher    = {Zenodo}, \
  version      = {Firedrake\_20200615.3},\
  doi          = {10.5281/zenodo.3894682}, \
  url          = { https://doi.org/10.5281/zenodo.3894682 } \
}

# Run simulations
To run the simulations, activate the firedrake venv and run:
``` python3 {installation-path/}GMGGPU-Evaluation/run.py ```

