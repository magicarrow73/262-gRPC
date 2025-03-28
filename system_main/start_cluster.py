"""
start_cluster.py

This script provides a convenient way to start a cluster of fault-tolerant
chat servers, either on a single machine or across multiple machines. Each
server runs as an independent process, using gRPC and Raft for communication.
"""

import sys
import os
import subprocess
import time
import argparse
import signal
import atexit

# List to track running processes
running_procs = []

def cleanup():
    """
    Terminate all running server processes on exit.

    This function is registered with atexit, so it is automatically called
    when the Python interpreter exits, or when the script is interrupted
    (e.g., via Ctrl+C). It attempts to terminate each server process gracefully,
    and if that fails, it forces a kill.
    """
    for proc in running_procs:
        try:
            proc.terminate()
            time.sleep(0.5)
            if proc.poll() is None:
                proc.kill()
        except Exception:
            pass

# Register cleanup handler
atexit.register(cleanup)

def start_server(server_id, num_servers, host='127.0.0.1', base_port=50051, base_raft_port=50100):
    """
    Start a single server in the cluster as a subprocess.

    :param server_id: An integer ID for this server (unique within the cluster).
    :param num_servers: The total number of servers in the cluster.
    :param host: The host/IP address on which the server should listen.
    :param base_port: The base port number for gRPC servers.
                      The actual gRPC port for this server is base_port + server_id.
    :param base_raft_port: The base port number for Raft consensus.
                           The actual Raft port for this server is base_raft_port + server_id.
    :return: A string containing the "host:grpc_port" address of this server.
    """
    # Calculate ports for this server
    grpc_port = base_port + server_id
    raft_port = base_raft_port + server_id
    
    # Generate the list of other servers for Raft consensus
    other_servers = []
    for i in range(num_servers):
        if i != server_id:
            other_servers.append(f"{host}:{base_raft_port + i}")
    
    # Command to start the server
    cmd = [
        sys.executable, "ft_server_grpc.py",
        "--host", host,
        "--port", str(grpc_port),
        "--node-id", str(server_id),
        "--raft-port", str(raft_port),  # Use the unique port
        "--cluster", ",".join(other_servers)
    ]
    
    # Start the server process
    print(f"Starting server {server_id} on {host}:{grpc_port} (Raft: {host}:{raft_port})")
    proc = subprocess.Popen(cmd)
    running_procs.append(proc)
    
    # Return the gRPC address of this server
    return f"{host}:{grpc_port}"

def main():
    """
    Main entry point to start a cluster of fault-tolerant chat servers.

    This script parses command-line arguments to determine how many servers
    to start, which host to bind them to, and the base ports for both gRPC
    and Raft. It then launches each server as a subprocess and monitors
    them. If any server crashes, it prints a warning message. The user can
    terminate the entire cluster with Ctrl+C.
    """
    parser = argparse.ArgumentParser(description="Start a cluster of fault-tolerant chat servers")
    parser.add_argument("--servers", type=int, default=5, help="Number of servers to start")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind servers to")
    parser.add_argument("--base-port", type=int, default=50051, help="Base port for gRPC servers")
    parser.add_argument("--base-raft-port", type=int, default=50100, help="Base port for Raft consensus")
    args = parser.parse_args()
    
    print(f"Starting a cluster of {args.servers} servers...")
    
    # Start each server and collect their addresses
    server_addresses = []
    for i in range(args.servers):
        addr = start_server(
            i, args.servers, args.host, args.base_port, args.base_raft_port
        )
        server_addresses.append(addr)
        time.sleep(1)  # Give each server a moment to start
    
    # Print the cluster information
    print("\nCluster started successfully!")
    print(f"Server addresses: {', '.join(server_addresses)}")
    print("\nTo start a client, run:")
    print(f"python ft_client_grpc.py --servers {','.join(server_addresses)}")
    print("\nPress Ctrl+C to stop the cluster...")
    
    # Keep the cluster running until interrupted
    crashed_set = set()
    try:
        while True:
            time.sleep(1)

            for i, proc in enumerate(running_procs):
                # If we already reported this server as crashed, skip
                if i in crashed_set:
                    continue
                
                if proc.poll() is not None:
                    print(f"Warning: Server {i} has crashed (exit code: {proc.returncode})")
                    crashed_set.add(i)

    except KeyboardInterrupt:
        print("\nStopping the cluster...")

if __name__ == "__main__":
    main()
