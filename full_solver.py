from firedrake import *
from pyop2.gpu.cuda import cuda_backend as cuda
import sys

parameters = {"snes_type": "ksponly",
              "ksp_type": "preonly",
              "mat_type": "matfree",
              "pc_type": "mg",
              "pc_mg_type": "full",
              "mg_coarse_ksp_type": "gmres",
              "mg_coarse_pc_type": "jacobi",
              "mg_levels_ksp_type": "chebyshev",
              "mg_levels_ksp_max_it": 4,
              "mg_levels_pc_type": "jacobi",
              "pc_mg_log": True}

def warmupSolve(level = 2, mesh_arg=(10, 10)):
    ##Setup
    mesh = UnitSquareMesh(mesh_arg[0], mesh_arg[1])
    nlevel = level
    mh = MeshHierarchy(mesh, nlevel)
    V = FunctionSpace(mh[-1], 'CG', 2)
    u = function.Function(V)
    f = function.Function(V)
    v = TestFunction(V)
    F = dot(grad(u), grad(v)) * dx - f * v * dx
    bcs = DirichletBC(V, 0.0, (1, 2, 3, 4))
    x = SpatialCoordinate(V.mesh())
    with offloading(cuda):
        f.interpolate(-0.5 * pi * pi * (4 * cos(pi * x[0]) - 5 * cos(pi * x[0] * 0.5) + 2) * sin(pi * x[1]))
        solve(F == 0, u, bcs=bcs, solver_parameters=parameters)

def measureSolve(level = 2, mesh_arg=(10, 10)):
    ##Setup
    mesh = UnitSquareMesh(mesh_arg[0], mesh_arg[1])
    nlevel = level
    mh = MeshHierarchy(mesh, nlevel)
    V = FunctionSpace(mh[-1], 'CG', 2)
    u = function.Function(V)
    f = function.Function(V)
    v = TestFunction(V)
    F = dot(grad(u), grad(v)) * dx - f * v * dx
    bcs = DirichletBC(V, 0.0, (1, 2, 3, 4))
    x = SpatialCoordinate(V.mesh())
    with offloading(cuda):
        f.interpolate(-0.5 * pi * pi * (4 * cos(pi * x[0]) - 5 * cos(pi * x[0] * 0.5) + 2) * sin(pi * x[1]))
        solve(F == 0, u, bcs=bcs, solver_parameters=parameters)

    exact = Function(V[-1])
    exact.interpolate(sin(pi * x[0]) * tan(pi * x[0] * 0.25) * sin(pi * x[1]))
    a = norm(assemble(exact - u))
    print(a)

level = int(sys.argv[1])
mesh_f = int(sys.argv[2])
mesh_s = int(sys.argv[3])
measureSolve(level, (mesh_f, mesh_s))
