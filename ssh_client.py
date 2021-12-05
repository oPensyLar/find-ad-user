import paramiko
import time
import _parser


class SshClient:

    host = None
    prt = None
    usr = None
    pwd = None

    def __init__(self, hst, port, user, password):
        self.host = hst
        self.prt = port
        self.usr = user
        self.pwd = password

    def ssh_exec(self, cmd):
        repeat = True

        while repeat:
            client = paramiko.client.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.load_system_host_keys()
            time.sleep(1)
            repeat = False

            try:
                client.connect(self.host, port=self.prt, username=self.usr, password=self.pwd)

            except ConnectionError:
                print("[!] ConnectionError")
                continue

            except TimeoutError:
                return None

            except EOFError:
                print("[!] EOFError")
                continue

            except paramiko.ssh_exception.AuthenticationException:
                return None

            except paramiko.ssh_exception.NoValidConnectionsError:
                print("[!] SSH AUTH ERROR?")
                continue

            try:
                stdin, stdout, stderr = client.exec_command(cmd)

            except ConnectionResetError:
                print("[!] exec_command() ERROR")
                continue

            except paramiko.ssh_exception.SSHException:
                print("[!] SSHException ERROR")
                continue

            stdout = stdout.readlines()
            stderr = stderr.readlines()
            # stdin = stdin.readlines()
            client.close()

            str_output = ''.join(str(e) for e in stdout)
            str_err_output = ''.join(str(e) for e in stderr)

            return {"stdout": str_output, "stderr": str_err_output}

        return None

    def send_query(self, ip_addr, port, usr, passwd, payload):
        ssh_parser = _parser.Parser()
        raw_data = self.ssh_exec(ip_addr, port, usr, passwd, payload)

        if raw_data is not None:
            ssh_parser.set_error(0x0)
            ssh_parser.parse_output(raw_data)

        else:
            ssh_parser.set_error(0x1)

        return ssh_parser