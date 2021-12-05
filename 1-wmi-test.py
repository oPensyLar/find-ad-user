import wmi


def wmi_local():
    conn = wmi.WMI()

    for class_name in conn.Win32_Process.properties.keys():
        print(class_name)


def wmi_remote():
    host = "you_ip_server"
    usr = "you_user_doamin"
    pwd = "you_password"
    conn = wmi.WMI(host, user=usr, password=pwd)

    for class_name in conn.Win32_Process.properties.keys():
        print(class_name)


wmi_remote()
