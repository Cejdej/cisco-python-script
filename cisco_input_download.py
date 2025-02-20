import paramiko
import time
import datetime
import getpass  # Secure password input
import os  # Used for folder creation

# Read switch IPs from a file
switch_file = "switches.txt"

# Get user credentials
username = input("Enter your username: ")
password = getpass.getpass("Enter your password: ")
command = input("Enter the command to run on all switches: ")

# Create "Outputs" folder if it doesn't exist
output_folder = "Outputs"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Create a timestamped output file inside "Outputs" folder
date_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_filename = os.path.join(output_folder, f"Switches_Output_{date_str}.txt")

# Open output file
with open(output_filename, "w") as output_file:
    # Read switches from file
    with open(switch_file, "r") as file:
        switches = file.readlines()

    # Loop through each switch
    for switch in switches:
        switch = switch.strip()  # Remove whitespace/newline

        if not switch:
            continue  # Skip empty lines

        try:
            print(f"Connecting to {switch}...")

            # Initialize SSH client
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=switch, username=username, password=password, look_for_keys=False, allow_agent=False)

            # Open an interactive shell session
            shell = ssh.invoke_shell()
            time.sleep(1)

            # Send command
            shell.send(command + "\n")
            time.sleep(2)  # Allow time for output

            # Read output
            output = shell.recv(65535).decode("utf-8")

            # Get switch hostname
            shell.send("show run | include hostname\n")
            time.sleep(1)
            hostname_output = shell.recv(65535).decode("utf-8")
            hostname = hostname_output.split()[-1] if "hostname" in hostname_output else switch

            # Write to file
            output_file.write(f"\n{'*' * 50}\n")
            output_file.write(f"Output from {hostname} ({switch})\n")
            output_file.write(f"{'*' * 50}\n")
            output_file.write(output)

            print(f"Output from {switch} saved!")

            # Close SSH connection
            ssh.close()

        except Exception as e:
            print(f"Failed to connect to {switch}: {e}")
            output_file.write(f"\n{'*' * 50}\n")
            output_file.write(f"Failed to connect to {switch}\n")
            output_file.write(f"{'*' * 50}\n")

print(f"\nAll outputs saved to {output_filename}")
