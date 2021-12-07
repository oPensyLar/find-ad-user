import wmi
import _parser
import csv_writer
import pyad.adquery


def check_user_process(wmi_obj, user):
    for s in wmi_obj.Win32_Process():
        owner = s.GetOwner()

        if owner[0] is not None:
            if owner[2] == user:
                return True

    return False


user = "you-ad-user"
password = "you-ad-password"
file_users = "users-to-find.txt"

q = pyad.adquery.ADQuery()
q.execute_query(attributes=["distinguishedName", "description"], where_clause="objectClass = 'computer'")

for row in q.get_results():
    str_split = row["distinguishedName"].split(",")
    str_split = str_split[0].split("=")
    print("Checking on.. " + str_split[1])

    with open(file_users, "r") as handle_user:
        for c_user in handle_user:
            c_user = c_user.replace("\n", "")
            c_user = c_user.replace("\r", "")

            user_found = False
            try:
                # Is Windows host?
                wmi_object = wmi.WMI(str_split[1], user=user, password=password)
                user_found = check_user_process(wmi_object, c_user)

            except wmi.x_access_denied:
                print("[!] x_access_denied on " + str_split[1])

            except wmi.x_wmi_authentication:
                print("[!] x_wmi_authentication on " + str_split[1])

            p = _parser.Parser()
            user_found = p.parse_procs(ret_data["stdout"], c_user)

            if user_found is True:
                headers = ["username", "logged_on"]
                data = [[c_user, str_split[1]]]
                csv = csv_writer.CsvWriter("output.csv", headers, data)
                csv.create_csv()
