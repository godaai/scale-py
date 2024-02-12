from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# tell MPI data type is int
# dtype='i', i is short for INT
if rank == 0:
    data = np.arange(10, dtype='i')
    comm.Send([data, MPI.INT], dest=1)
    print(f"Sended: {data}, from rank: {rank}.")
elif rank == 1:
    data = np.empty(10, dtype='i')
    comm.Recv([data, MPI.INT], source=0)
    print(f"Received: {data}, to rank: {rank}.")

# MPI detects data type
if rank == 0:
    data = np.arange(10, dtype=np.float64)
    comm.Send(data, dest=1)
    print(f"Sended: {data}, from rank: {rank}.")
elif rank == 1:
    data = np.empty(10, dtype=np.float64)
    comm.Recv(data, source=0)
    print(f"Received: {data}, to rank: {rank}.")