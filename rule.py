from dataclasses import dataclass


@dataclass
class Rule:
    proto: str = "*"
    ip: str = "*"
    port: str = "*"
    iface: str = "*"
    action: str = "*"
    extra: str = "*"

    def parse_rule(self, args):
        while args:
            if args[0] == "-i":
                self.iface = args[1]
                args = args[2:]
            elif args[0] == "-p":
                self.proto = args[1]
                args = args[2:]
            elif args[0] == "-j":
                self.action = args[1]
                args = args[2:]
            elif args[0] == "-s":
                self.ip = args[1]
                args = args[2:]
            elif args[0] == "--dport":
                self.port = args[1]
                args = args[2:]
            else:
                self.extra += args[0] + " "
                args = args[1:]
        return self


def load_tables(filename):
    ret = {}

    table = ""
    chain = ""
    with open(filename) as fd:
        for line in fd:
            line = line.strip()
            if line.startswith("#"):
                continue
            elif line.startswith("*"):
                table = line[1:]
                ret[table] = {}
            elif line.startswith(":"):
                chain = line[1:].split()[0]
                ret[table][chain] = []
            elif line.startswith("-A"):
                args = line[3:].split()
                if args[0] not in ret[table]:
                    ret[table][args[0]] = []
                ret[table][args[0]].append(Rule().parse_rule(args))
            elif line == "COMMIT":
                continue

    return ret
