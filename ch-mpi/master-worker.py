from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank < size - 1:
    # Worker process
    np.random.seed(rank)
    # Generate random data
    data_count = np.random.randint(100)
    data = np.random.randint(100, size=data_count)
    comm.send(data, dest=size - 1)
    print(f"Worker: worker ID: {rank}; count: {len(data)}")
else:
    # Master process
    for i in range(size - 1):
        status = MPI.Status()
        data = comm.recv(source=MPI.ANY_SOURCE, status=status)
        print(f"Master: worker ID: {status.Get_source()}; count: {len(data)}")

comm.Barrier()