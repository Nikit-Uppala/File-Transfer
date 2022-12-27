# File Transfer

A simple command line application to send/receive files on LAN.

## Instructions

### To receive a file 
<ul>
    <li>Find your IPv4 address using ipconfig command in windows powershell or ip address command in linux.</li>
    <li>Run receiver.py with the following command</li>
        
        python receiver.py <IPv4 address>
</ul>

### To send a file
<ul>
    <li>Get the IPv4 address and the port of the receiver.</li>
    <li>Run sender.py with the following command:</li>

        python sender.py <IPv4 address> <PORT> <path_to_file_to_send>
</ul>
