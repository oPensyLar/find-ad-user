import wmi
import ssh_client
import _parser
import csv_writer


def check_user_process(wmi_obj, user):
    for s in wmi_obj.Win32_Process():
        owner = s.GetOwner()

        if owner[0] is not None:
            if owner[2] == user:
                return True

    return False


user = "you-ad-user"
password = "you-ad-password"
user_target = "ad-user-to-find"
file_servers = "srv.txt"
file_users = "users-to-find.txt"

with open(file_servers, "r") as handle_servers:
    for c_addr in handle_servers:
        c_addr = c_addr.replace("\n", "")
        c_addr = c_addr.replace("\r", "")

        with open(file_users, "r") as handle_user:
            for c_user in handle_user:
                c_user = c_user.replace("\n", "")
                c_user = c_user.replace("\r", "")

                user_found = False
                ssh = ssh_client.SshClient(c_addr, 22, user, password)
                ret_data = ssh.ssh_exec("ps uax")

                if ret_data is None:
                    try:
                        # Is Windows host?
                        wmi_object = wmi.WMI(c_addr, user=user, password=password)
                        user_found = check_user_process(wmi_object, user_target)

                    except wmi.x_access_denied:
                        print("[!] auth Windows access denied on " + c_addr)

                else:
                    if ret_data is None:
                        continue

                    p = _parser.Parser()
                    user_found = p.parse_procs(ret_data["stdout"], user_target)

            if user_found is True:
                headers = ["username", "logged_on"]
                data = [[user_target, c_addr]]
                csv = csv_writer.CsvWriter("output.csv", headers, data)
                csv.create_csv()
