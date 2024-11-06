import re
import sys
import os
import uuid
import ipaddress
import argparse

# Regular expressions for different MAC and IP address formats
MAC_REGEX = r'\b(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}\b|\b[0-9A-Fa-f]{4}:[0-9A-Fa-f]{4}:[0-9A-Fa-f]{4}\b|\b[0-9A-Fa-f]{4}\.[0-9A-Fa-f]{4}\.[0-9A-Fa-f]{4}\b'
IPV4_REGEX = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
IPV6_REGEX = r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b|\b(?:[0-9a-fA-F]{1,4}:){1,7}:[0-9a-fA-F]{0,4}\b'

# Function to generate an artificial MAC address
def generate_fake_mac():
    return ':'.join(format(x, '02x') for x in uuid.uuid4().bytes[:6])

# Function to generate an artificial IPv4 address within the private range
def generate_fake_ipv4():
    return str(ipaddress.IPv4Address(int(ipaddress.IPv4Address("10.0.0.0")) + uuid.uuid4().int % 0xFFFFFF))

# Function to generate an artificial IPv6 address within the unique local address (ULA) range
def generate_fake_ipv6():
    return str(ipaddress.IPv6Address("fd00::") + uuid.uuid4().int % (1 << 64))

# Stage 1: Analyze and generate swap.map
def analyze_files(input_files):
    unique_addresses = {}
    replacement_dict = {}

    for filename in input_files:
        with open(filename, 'r') as file:
            content = file.read()

            # Find all MAC, IPv4, and IPv6 addresses
            mac_addresses = re.findall(MAC_REGEX, content)
            ipv4_addresses = re.findall(IPV4_REGEX, content)
            ipv6_addresses = re.findall(IPV6_REGEX, content)

            # Filter valid IPv4 addresses
            ipv4_addresses = [ip for ip in ipv4_addresses if all(0 <= int(octet) < 256 for octet in ip.split('.'))]

            # Store unique MACs and IPs
            for mac in mac_addresses:
                if mac not in unique_addresses:
                    unique_addresses[mac] = generate_fake_mac()
            for ip in ipv4_addresses:
                if ip not in unique_addresses:
                    unique_addresses[ip] = generate_fake_ipv4()
            for ip in ipv6_addresses:
                if ip not in unique_addresses:
                    unique_addresses[ip] = generate_fake_ipv6()

    # Write the mapping to swap.map
    with open('swap.map', 'w') as map_file:
        for original, replacement in unique_addresses.items():
            map_file.write(f"{original} {replacement}\n")
            replacement_dict[original] = replacement

    print("swap.map has been created with artificial addresses.")
    return replacement_dict

# Stage 2: Replace original addresses using swap.map
def sanitize_files(input_files, dictionary_file):
    # Load the replacement dictionary
    replacement_dict = {}
    with open(dictionary_file, 'r') as map_file:
        for line in map_file:
            original, replacement = line.strip().split()
            replacement_dict[original] = replacement

    for filename in input_files:
        with open(filename, 'r') as file:
            content = file.read()

        # Replace each original address with its replacement
        for original, replacement in replacement_dict.items():
            content = content.replace(original, replacement)

        # Write the modified content to a new file
        modified_filename = f"{filename}.modified"
        with open(modified_filename, 'w') as modified_file:
            modified_file.write(content)

        print(f"{modified_filename} has been created with sanitized addresses.")

def main():
    parser = argparse.ArgumentParser(description="Script to anonymize MAC and IP addresses in text files.")
    parser.add_argument('-analyze', action='store_true', help="Run analysis and generate swap.map")
    parser.add_argument('-sanitize', action='store_true', help="Sanitize files using swap.map")
    parser.add_argument('-input', nargs='+', help="Input files for analysis or sanitization")
    parser.add_argument('-dictionary', help="Dictionary file (swap.map) for sanitization")

    args = parser.parse_args()

    if args.analyze and args.input:
        analyze_files(args.input)
    elif args.sanitize and args.input and args.dictionary:
        sanitize_files(args.input, args.dictionary)
    else:
        print("Invalid arguments. Please use -analyze -input <files> for analysis or -sanitize -dictionary swap.map -input <files> for sanitization.")

if __name__ == "__main__":
    main()
