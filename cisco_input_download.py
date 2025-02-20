import paramiko
import getpass
import datetime


# Function to connect to the Cisco switch and execute a command
def execute_command(hostname, username, password, command):
    try:
        # Create an SSH client instance
        ssh = paramiko.SSHClient()

        # Automatically add the switch to known hosts
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the switch using SSH
        ssh.connect(hostname, username=username, password=password)

        # Execute the command
        stdin, stdout, stderr = ssh.exec_command(command)

        # Fetch the output
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        # If there is an error, set the output to the error message
        if error:
            output = f"Error: {error}"

        # Get the current date and time to append to the filename
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d_%H-%M-%S")

        # Construct the output file name (hostname_date.txt)
        output_file = f"{hostname}_{date_str}.txt"

        # Save the command output to the specified file
        with open(output_file, 'w') as f:
            f.write(output)

        # Close the SSH connection
        ssh.close()

    except Exception as e:
        # If any exception occurs, write the exception to the file
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        output_file = f"{hostname}_{date_str}.txt"

        with open(output_file, 'w') as f:
            f.write(f"An error occurred: {e}")


# Main function to get user input and call the function
if __name__ == "__main__":
    # Get credentials and command
    hostname = input("Enter the switch hostname or IP address: ")
    username = input("Enter the SSH username: ")
    password = getpass.getpass("Enter the SSH password: ")  # Use getpass for secure password input
    command = input("Enter the command to execute (e.g., show version): ")

    # Execute the command and save the output to the file
    execute_command(hostname, username, password, command)
