from textual.app import App, ComposeResult
from textual.widgets import Button, Static, DataTable, Label, Tree
from textual.reactive import reactive

HEADERS = ["#", "IFACE", "PROTO", "IP", "PORT", "ACTION", "EXTRA"]


class ChainTable(Static):
    rows = reactive([])

    def __init__(self, rows):
        super().__init__()
        # self.rows = rows

    def compose(self) -> ComposeResult:
        yield DataTable(fixed_columns=7)

    def on_mount(self):
        table = self.query_one(DataTable)
        table.add_columns(*HEADERS)
        rows = (
            (n, x.iface, x.proto, x.ip, x.port, x.action, x.extra)
            for n, x in enumerate(self.rows)
        )
        table.add_rows(rows)

    def watch_rows(self, rows):
        table = self.query_one(DataTable)
        table.clear()

        rows = (
            (n, x.iface, x.proto, x.ip, x.port, x.action, x.extra)
            for n, x in enumerate(self.rows)
        )
        table.add_rows(rows)