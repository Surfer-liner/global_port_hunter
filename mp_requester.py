import os
import time
import datetime
import logging
import socket
import multiprocessing


current_directory = os.getcwd()
log_path = current_directory + '/mp_requester.log'
open_sockets = current_directory + '/open_sockets.txt'
logging.basicConfig(filename=log_path, level=logging.INFO)


def ip_generator(queue):
    '''Generates an ip address with a port'''
    try:
        ports_list = [22, 23, 25, 80, 137, 138, 139, 443, 445, 3306, 5432]
        for el0 in range(1, 191):
            for el1 in range(1, 256):
                for el2 in range(1, 256):
                    for el3 in range(1, 256):
                        for port in ports_list:
                            ip = f'{el0}.{el1}.{el2}.{el3}'
                            queue.put((ip, port))
    except Exception as e:
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime('%H:%M:%S')
        logging.error(f'{formatted_time} ERR ip_generator: {e}')
        pass


def ip_checker(queue):
    '''Checks the port of the received address for openness
    If the port is open, it fixes the address in open_sockets.txt'''
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(1)
        count = 0
        while not queue.empty():
            ip, port = queue.get()
            count += 1
            if count % 10_000_000 == 0:
                current_time = datetime.datetime.now()
                formatted_time = current_time.strftime('%H:%M:%S')
                formatted_count = '{:,}'.format(count)
                logging.info(
                    f"{formatted_time} {formatted_count} ip's was checked "
                    f"by ip_checker, current IP = {ip}:{port}")
            try:
                server_answer = client_socket.connect_ex((ip, port))
                if server_answer == 0:
                    print(f'{ip}:{port} is open')
                    with open(open_sockets, 'a+') as f:
                        f.write(f'{ip}:{port} is open\n')
            except socket.timeout:
                pass
        client_socket.close()
    except Exception as e:
        ip, port = queue.get()
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime('%H:%M:%S')
        logging.error(f'{formatted_time} ERR ip_checker: {e}, {ip}:{port}')
        pass

if __name__ == '__main__':
    num_processes = 10
    processes = []
    queue = multiprocessing.Queue()
    generator_process = multiprocessing.Process(target=ip_generator, args=(queue, ))
    generator_process.start()
    time.sleep(1)
    for _ in range(num_processes):
        process = multiprocessing.Process(target=ip_checker, args=(queue, ))
        process.start()
        processes.append(process)
    generator_process.join()
    for process in processes:
        process.join()
