class Parser:

    def parse_procs(self, raw_procs, target_user):
        break_lines = raw_procs.split("\n")
        semi_parse = []
        i = 0x0

        # Itera cada salto de linea
        for line in break_lines:

            if i > 0x0:
                # Itera cada elemento por linea
                for un_spacio in line.split(" "):
                    if len(un_spacio) > 0x0 and un_spacio is not " ":
                        semi_parse.append(un_spacio)

                if len(semi_parse) > 0:
                    user = semi_parse[0]

                    if user == target_user:
                        return True

                semi_parse.clear()

            i += 1

        return False