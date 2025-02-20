from netmiko import ConnectHandler
import datetime
import getpass
import os

# Read switch list from file
switch_file = "switches.txt"

# Ask for device type (Cisco or Aruba)
while True:
    device_type = input("Is this a Cisco or Aruba device? (cisco/aruba): ").strip().lower()
    if device_type in ["cisco", "aruba"]:
        break
    print("Invalid input. Please enter 'cisco' or 'aruba'.")

# Map user input to Netmiko device types
device_mapping = {
    "cisco": "cisco_ios",
    "aruba": "aruba_osswitch"
}
netmiko_device_type = device_mapping[device_type]

# Ask for credentials
username = input("Enter your username: ")
password = getpass.getpass("Enter your password: ")

# Ask for the command to execute
command = input(f"Enter the command to run on all {device_type} devices: ")

# Create "Outputs" folder if it doesn't exist
output_folder = "Outputs"
os.makedirs(output_folder, exist_ok=True)

# Create a timestamped output file
date_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_filename = os.path.join(output_folder, f"Switches_Output_{date_str}.txt")

# Open output file
with open(output_filename, "w") as output_file:
    with open(switch_file, "r") as file:
        switches = file.readlines()

    for switch in switches:
        switch = switch.strip()  # Remove spaces/new lines
        if not switch:
            continue  # Skip empty lines

        try:
            print(f"Connecting to {switch} ({device_type})...")

            device = {
                "device_type": netmiko_device_type,
                "host": switch,
                "username": username,
                "password": password,
                "fast_cli": False,
            }

            net_connect = ConnectHandler(**device)

            # Get the hostname
            hostname_output = net_connect.send_command("show run | include hostname")
            hostname = hostname_output.split()[-1] if "hostname" in hostname_output else switch

            # Run the specified command
            output = net_connect.send_command(command)

            # Save output
            output_file.write(f"\n{'*' * 50}\n")
            output_file.write(f"Output from {hostname} ({switch}) - {device_type}\n")
            output_file.write(f"{'*' * 50}\n")
            output_file.write(output)

            net_connect.disconnect()

        except Exception as e:
            print(f"Failed to connect to {switch}: {e}")
            output_file.write(f"\n{'*' * 50}\n")
            output_file.write(f"Failed to connect to {switch}\n")
            output_file.write(f"{'*' * 50}\n")

# Print final output location
print(f"\nAll outputs saved to {output_filename}")
