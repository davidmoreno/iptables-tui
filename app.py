import sys
from typing import Literal, Union

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Container
from textual.reactive import reactive

from iptablesboard import IpTablesBoard
from chaintable import ChainTable
from rule import load_tables

logs = []


class IpTablesTUIApp(App):
    TITLE = "iptables TUI"
    CSS_PATH = "iptables-tui.css"
    BINDINGS = [
        # ("Control+d", "toggle_dark", "Toggle Dark Mode"),
        # ("Control+S", "save", "Save"),
        # ("Control+L", "load", "Load"),
        ("escape", "switch", "Back"),
    ]

    tables = reactive(
        load_tables("/home/dmoreno/src/iptables-tui/examples/01.iptables")
    )
    # tables = reactive(load_tables(sys.argv[1]))
    tab = reactive(0)
    stack = reactive([])

    def compose(self) -> ComposeResult:
        yield Header()
        yield IpTablesBoard(self.tables)
        yield ChainTable(self.tables["filter"]["FORWARD"])
        yield Footer()

    def select_tab(self, tab: Literal["board", "chain"]):
        self.remove_class("board")
        self.remove_class("chain")
        self.add_class(tab)
        logs.append(f"Selected tab {tab}")

    def on_mount(self):
        self.select_tab("board")

    def on_ip_tables_board_select_table_chain(
        self, message: IpTablesBoard.SelectTableChain
    ):
        self.select_table(message.table, message.chain)

    def select_table(self, table, chain):
        logs.append(f"Select {table} / {chain}")
        self.title = f"iptables TUI - {table} {chain}"

        chaintable = self.query_one("ChainTable")
        chaintable.rows = self.tables.get(table, {}).get(chain, [])
        self.select_tab("chain")
        self.stack = [*self.stack, (table, chain)]

    def on_chain_table_select_rule(self, message: ChainTable.SelectRule):
        logs.append(f"CHAIN TABLE SELECT {message.rule}")
        self.select_table(self.stack[-1][0], message.rule.action)

    def action_switch(self):
        logs.append(f"POP {self.stack}")
        if len(self.stack) == 0:
            self.exit()
            return
        self.stack = self.stack[:-1]
        if len(self.stack) == 0:
            self.select_tab("board")
            return

        table, chain = self.stack[-1]
        chaintable = self.query_one("ChainTable")
        chaintable.rows = self.tables.get(table, {}).get(chain, [])


if __name__ == "__main__":
    app = IpTablesTUIApp()
    app.run()
    # print(load_tables())
    for line in logs:
        print(line)
