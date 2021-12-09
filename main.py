import wmi
import ping3
import _parser
import csv_writer
import pyad.adquery

enable_ssh_find = False

if enable_ssh_find:
	import ssh_client

def check_user_process(wmi_obj, user):
	for s in wmi_obj.Win32_Process():
		owner = s.GetOwner()

		if owner[0] is not None:
			index=owner[2].find(user)
			if index >= 0x0:
				return {"found": True, "user": owner[2]}

	return {"found": False, "user": None}


user = ""
password = ""
file_users = "users-to-find.txt"

q = pyad.adquery.ADQuery()
q.execute_query(attributes=["distinguishedName", "description"],
	where_clause="objectClass = 'computer'")

for row in q.get_results():
    str_split = row["distinguishedName"].split(",")
    str_split = str_split[0].split("=")
    print("Checking on " + str_split[1])

    ping_result = ping3.ping(str_split[1])

    if ping_result is False:
        print("[!] Host " + str_split[1] + " is down")
        continue

    with open(file_users, "r") as handle_user:
    	ret_data = None
    	for c_user in handle_user:
            c_user = c_user.replace("\n", "")
            c_user = c_user.replace("\r", "")

            if enable_ssh_find:
            	user_found = False
            	ssh = ssh_client.SshClient(str_split[1], 22, user, password)
            	ret_data = ssh.ssh_exec("ps uax")
            	p = _parser.Parser()
            	user_found = p.parse_procs(ret_data["stdout"], c_user)

            if ret_data is None:
                try:
                    # Is Windows host?
                    wmi_object = wmi.WMI(str_split[1], user=user, password=password)
                    user_found = check_user_process(wmi_object, c_user)

                    if user_found["found"] is True:
                    	headers = ["username", "logged_on"]
                    	data = [[user_found["user"], str_split[1]]]
                    	csv = csv_writer.CsvWriter("output.csv", headers, data)
                    	csv.create_csv()

#                except wmi.x_wmi:
#                    print("[!] Host is down? on " + str_split[1] + "\n")

                except wmi.x_access_denied:
                    print("[!] x_access_denied on " + str_split[1])

                except wmi.x_wmi_authentication:
                    print("[!] x_wmi_authentication on " + str_split[1])

                if ret_data is None:
                	continue