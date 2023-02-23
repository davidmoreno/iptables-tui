from dataclasses import dataclass
import sys
from time import monotonic

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.containers import Container
from textual.reactive import reactive

from iptablesboard import IpTablesBoard
from chaintable import ChainTable


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


class IpTablesTUIApp(App):
    TITLE = "iptables TUI"
    CSS_PATH = "iptables-tui.css"
    BINDINGS = [
        ("Control+d", "toggle_dark", "Toggle Dark Mode"),
        ("Control+S", "save", "Save"),
        ("Control+L", "load", "Load"),
        ("escape", "switch", "Switch Mode"),
    ]

    tables = reactive(load_tables(sys.argv[1]))
    tab = reactive(0)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Container(IpTablesBoard())
        yield ChainTable(self.tables["filter"]["INPUT"])
        # yield Container(
        #     TableTree(),
        #     Button("TEST", id="test"),
        #     id="main",
        # )

    def on_mount(self):
        self.add_class("tab-0")

    def on_ip_tables_board_select_table_chain(
        self, message: IpTablesBoard.SelectTableChain
    ):
        self.add_class("tab-1")
        self.remove_class("tab-0")
        self.title = f"iptables TUI - {message.table} {message.chain}"

        chaintable = self.query_one("ChainTable")
        chaintable.rows = self.tables.get(message.table, {}).get(message.chain, [])

    def action_switch(self):
        if "tab-0" in self.classes:
            self.add_class("tab-1")
            self.remove_class("tab-0")
        else:
            self.add_class("tab-0")
            self.remove_class("tab-1")

    #     yield Container(ChainTable())


if __name__ == "__main__":
    app = IpTablesTUIApp()
    app.run()
    # print(load_tables())
