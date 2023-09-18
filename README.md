# Multiprocessing Port Scanner

This Python script scans multiple IP addresses and ports using multiprocessing, making it useful for checking the accessibility of various ports on a range of IP addresses simultaneously.

## Features

- Scans a wide range of IP addresses and ports concurrently.
- Logs scan results, including open ports, to a specified log file.
- Utilizes multiprocessing for improved scan speed.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your system.
- Required Python modules: `datetime`, `socket`, `logging`, `multiprocessing`, `time`, `os`.

## Usage

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/Surfer-liner/global_port_hunter.git

2. Modify the script settings (optional):

You can customize the script by modifying the following settings in the script itself:

- log_path: The path to the log file where scan results will be recorded.
- open_sockets: The path to the file where open ports will be recorded.

3. Run the script:

   ```bash
   python3 mp_requester.py

4. Monitor the progress:
The script will start scanning IP addresses and ports, displaying open ports in the terminal. The progress will also be logged in the specified log file.

5. Check the results:
After the scan is complete, you can review the log file to see the list of open ports on the scanned IP addresses.

## Contributing

Contributions are welcome! If you find any issues or want to enhance the script, please create a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

Thanks to the Python community for creating and maintaining the necessary libraries.
