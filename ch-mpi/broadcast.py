import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD

comm.Barrier()

N = 5
if comm.rank == 0:
    A = np.arange(N, dtype=np.float64)    # rank 0 initializes data into variable A
else:
    A = np.empty(N, dtype=np.float64)     # As on other processes are empty

# Broadcast
comm.Bcast([A, MPI.DOUBLE])

# Print to verify
print("Rank:%2d, data:%s" % (comm.rank, A))