import socket
import urllib
import sys
from worker_pool import WorkerPool


def main():
	worker_pool = WorkerPool('134.226.32.10', 8235)
	worker_pool.run()

if __name__ == "__main__":
    main()
