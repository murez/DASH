# ssh-agent.py
import paramiko


def V100():
    pass


def Titan():
    pass


def Test():
    _private_key = paramiko.RSAKey.from_private_key_file(
        "C:\\Users\\Nyove\\OneDrive\\Server\\.ssh\\sist_hpc_key")
    _client = paramiko.SSHClient()
    _client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    _client.connect(hostname="10.15.89.192", port=22112,
                    username="qinfr", pkey=_private_key)
    stdin, stdout, stderr = _client.exec_command('df -h ')
    print(stdout.read().decode('utf-8'))
    _client.close()


if __name__ == '__main__':
    Test()
