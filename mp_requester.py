import os
import time
import datetime
import logging
import socket
import multiprocessing


# Defining the path to the current directory
current_directory = os.getcwd()

# Defining logging filename
log_path = current_directory + '/mp_requester.log'

# Defining open sockets filename
open_sockets = current_directory + '/open_sockets.txt'

# Installing the application output
logging.basicConfig(filename=log_path, level=logging.INFO)


def ip_generator(queue):
    '''
    Generates an ip address with a port

    Args:
        None
    Return:
        None
    '''
    try:
        # Install the ports we want to check
        ports_list = [22, 23, 25, 80, 137, 138, 139, 443, 445, 3306, 5432]

        # Creating an IP address string
        for el0 in range(1, 191):
            for el1 in range(1, 256):
                for el2 in range(1, 256):
                    for el3 in range(1, 256):
                        for port in ports_list:
                            ip = f'{el0}.{el1}.{el2}.{el3}'
                            queue.put((ip, port))

    # Catching an error in the function
    except Exception as e:
        # Getting the current time
        current_time = datetime.datetime.now()
        # Format the time
        formatted_time = current_time.strftime('%H:%M:%S')
        # Fix error in the log
        logging.error(f'{formatted_time} ERR ip_generator: {e}')
        # Continue generation
        pass


def ip_checker(queue):
    '''
    Checks the port of the received address for openness
    If the port is open, it fixes the address in open_sockets.txt

    Args:
        None
    Returns:
        None
    '''
    try:
        # Creating a client socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Setting the waiting period for a response from the server
        client_socket.settimeout(1)

        # Extract IP and port
        count = 0
        while not queue.empty():
            ip, port = queue.get()
            count += 1

            if count % 10_000_000 == 0:
                # Forming the current time
                current_time = datetime.datetime.now()
                # Format the time
                formatted_time = current_time.strftime('%H:%M:%S')
                # Format count
                formatted_count = '{:,}'.format(count)
                # Fix it in the logs
                logging.info(
                    f"{formatted_time} {formatted_count} ip's was checked "
                    f"by ip_checker, current IP = {ip}:{port}")

            try:
                # Establishing a connection to the server
                server_answer = client_socket.connect_ex((ip, port))
                # If there is an answer
                if server_answer == 0:
                    # Output the address
                    print(f'{ip}:{port} is open')
                    # Fixing the status of the port
                    with open(open_sockets, 'a+') as f:
                        f.write(f'{ip}:{port} is open\n')
            except socket.timeout:
                pass

        # Closing the socket
        client_socket.close()

    # Catching an error in the function
    except Exception as e:
        # Extracting IP and PORT from the queue
        ip, port = queue.get()
        # Forming the current time
        current_time = datetime.datetime.now()
        # Format the time
        formatted_time = current_time.strftime('%H:%M:%S')
        # Fix it in the logs
        logging.error(f'{formatted_time} ERR ip_checker: {e}, {ip}:{port}')
        # Continue scanning
        pass

if __name__ == '__main__':
    # Determine the number of processes
    num_processes = 10
    processes = []

    # Creating queue
    queue = multiprocessing.Queue()

    # Creating a process to fill the queue
    generator_process = multiprocessing.Process(target=ip_generator, args=(queue, ))
    generator_process.start()

    # Waiting for the queue to fill
    time.sleep(1)

    # Starting the list of processes
    for _ in range(num_processes):
        process = multiprocessing.Process(target=ip_checker, args=(queue, ))
        process.start()
        processes.append(process)

    # Completing the generation process
    generator_process.join()

    # Completing the checking processes
    for process in processes:
        process.join()

    print('all processes has been finished')
