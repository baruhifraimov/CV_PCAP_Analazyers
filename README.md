# CV_PCAP_Analyzers

This is a simple script that is built with AI to provide easy analysis and visualization of network traffic from Wireshark PCAP files and firewall logs.

## Features

- Analyze PCAP files and display:
  - Packets per second
  - Variance
  - Expected value

- Analyze firewall CSV logs and generate:
  - Statistical graph of distinct IP addresses per second

## Usage

1. To analyze a Wireshark PCAP file:
    ```bash
    python wireshark_analysis_script.py -f <path_to_pcap_file>
    ```

2. To analyze a firewall log CSV file:
    ```bash
    python firewall_analyze.py -l <path_to_log_file>
    ```

## Output
- Graphs representing packet distribution and IP activity.
- Statistical summaries for traffic analysis.

## License
This project is **free to use and modify**. Feel free to contribute or adapt it for your own use.
