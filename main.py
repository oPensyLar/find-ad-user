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


ipaddr = "127.0.0.1"
user = "you-ad-user"
password = "you-ad-password"
user_target = "ad-user-to-find"

user_found = False
ssh = ssh_client.SshClient(ipaddr, 22, user, password)
ret_data = ssh.ssh_exec("ps uax")

if ret_data is None:
    try:
        # Is Windows host?
        wmi_object = wmi.WMI(ipaddr, user=user, password=password)
        user_found = check_user_process(wmi_object, user_target)

    except wmi.x_access_denied:
        print("[!] auth Windows access denied")

else:
    p = _parser.Parser()
    user_found = p.parse_procs(ret_data["stdout"], user_target)

if user_found is True:
    headers = ["username", "logged_on"]
    data = [[user_target, ipaddr]]
    csv = csv_writer.CsvWriter("output.csv", headers, data)
    csv.create_csv()