from time import monotonic

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.widgets import Button, Static, DataTable, Label, Tree
from textual.containers import Container
from textual.reactive import reactive
from textual import events

from iptablesboard import IpTablesBoard

ROWS = [
    ("#", "IFACE", "PROTO", "IP", "PORT", "ACTION", "EXTRA"),
    (1, "eth0", "*", "127.0.0.1", "80", "DROP"),
    (2, "*", "*", "127.0.0.1", "22", "ACCEPT"),
    (3, "eth0", "*", "127.0.0.1", "80", "DROP"),
    (4, "*", "*", "127.0.0.1", "22", "ACCEPT"),
    (5, "eth0", "*", "127.0.0.1", "80", "DROP"),
    (6, "*", "*", "127.0.0.1", "22", "ACCEPT"),
    (7, "eth0", "*", "127.0.0.1", "80", "DROP"),
    (8, "*", "*", "127.0.0.1", "22", "ACCEPT"),
    (9, "eth0", "*", "127.0.0.1", "80", "DROP"),
    (10, "*", "*", "127.0.0.1", "22", "ACCEPT"),
    (11, "eth0", "*", "127.0.0.1", "80", "DROP"),
    (12, "*", "*", "127.0.0.1", "22", "ACCEPT"),
    (13, "eth0", "*", "127.0.0.1", "80", "DROP"),
    (14, "*", "*", "127.0.0.1", "22", "ACCEPT"),
]


class ChainTable(Static):
    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self):
        table = self.query_one(DataTable)
        rows = iter(ROWS)
        table.add_columns(*next(rows))
        table.add_rows(rows)


class TableTree(Static):
    def compose(self):
        tree = Tree("Tables")
        filter = tree.root.add("filter")
        filter.add_leaf("INPUT")
        filter.add_leaf("OUTPUT")
        filter.add_leaf("FORWARD")
        nat = tree.root.add("nat")
        nat.add_leaf("INPUT")
        nat.add_leaf("OUTPUT")
        nat.add_leaf("FORWARD")
        yield tree


class IpTablesTUIApp(App):
    TITLE = "iptables TUI"
    CSS_PATH = "iptables-tui.css"
    BINDINGS = [
        ("Control+d", "toggle_dark", "Toggle Dark Mode"),
        ("Control+S", "save", "Save"),
        ("Control+L", "load", "Load"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Container(IpTablesBoard())
        # yield Container(
        #     TableTree(),
        #     ChainTable(),
        #     Button("TEST", id="test"),
        #     id="main",
        # )

    #     yield Container(ChainTable())


if __name__ == "__main__":
    app = IpTablesTUIApp()
    app.run()
