from textual.app import App, ComposeResult
from textual.widgets import Button, Static, DataTable, Label, Tree, Input
from textual.reactive import reactive
from textual.containers import Container, Horizontal
from textual.message import Message, MessageTarget

from rule import Rule

HEADERS = ["#", "IFACE", "PROTO", "IP", "PORT", "ACTION", "EXTRA"]


class ChainTable(Static):
    rows = reactive([])
    chains = reactive({})

    def __init__(self, rows):
        super().__init__()
        # self.rows = rows

    def compose(self) -> ComposeResult:
        yield Container(
            DataTable(fixed_columns=7, id="table"),
            Container(
                Label("Interface"),
                Label("Address / Netwok"),
                Input(placeholder="Interface", id="iface"),
                Input(placeholder="Address/Network", id="ip"),
                Label("Port"),
                Label("Protocol"),
                Input(placeholder="Port", id="port"),
                Input(placeholder="Protocol", id="proto"),
                id="form",
            ),
            Container(
                Label("Action"),
                Input(placeholder="Action", id="action"),
                Label("Extra"),
                Input(placeholder="Extra", id="extra"),
                Label("---", id="description"),
            ),
        )

    def on_mount(self):
        table = self.query_one(DataTable)
        table.add_columns(*HEADERS)
        self.watch_rows(self.rows)

    def set_chain(self, rows, chains):
        self.chains = chains
        self.rows = rows
        table = self.query_one(DataTable)
        table.focus()

    def watch_rows(self, rows):
        table = self.query_one(DataTable)
        table.clear()

        def action(x):
            if x.action in Rule.BUILTIN:
                return x.action
            rules = self.chains.get(x.action, None)
            if rules is None:
                return x.action
            return f"{x.action} ({len(rules)})"

        rows = (
            (n + 1, x.iface, x.proto, x.ip, x.port, action(x), x.extra)
            for n, x in enumerate(self.rows)
        )
        table.add_rows(rows)
        table.focus()

    class SelectRule(Message):
        def __init__(self, sender: MessageTarget, rule: Rule):
            self.rule = rule
            super().__init__(sender)

    async def on_data_table_cell_selected(self, msg):
        rule: Rule = self.rows[msg.coordinate.row]
        if rule.action in rule.BUILTIN:
            return
        await self.post_message(self.SelectRule(self, rule))

    async def on_data_table_cell_highlighted(self, msg):
        rule: Rule = self.rows[msg.coordinate.row]

        self.query_one("#iface").value = rule.iface
        self.query_one("#proto").value = rule.proto
        self.query_one("#ip").value = rule.ip
        self.query_one("#port").value = rule.port
        self.query_one("#action").value = rule.action
        self.query_one("#extra").value = rule.extra
        self.query_one("#description").update(rule.description())
