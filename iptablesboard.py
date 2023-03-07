from textual.widgets import Button, Static, DataTable, Label
from textual.containers import Container, Horizontal
from textual.scroll_view import ScrollView
from textual.message import Message, MessageTarget
from textual.reactive import reactive


class IpTablesBoard(Static):
    def __init__(self, tables):
        self.tables = tables
        super().__init__()

    def compose(self):
        tables = self.tables
        yield ScrollView(
            Horizontal(
                Label("Incoming", classes="choice"),
                Static(),
                Static(),
                Label(" ", classes="w1 h3"),
                Label("Local Generated", classes="choice"),
            ),
            Horizontal(
                Label("↓"),
                Static(),
                Static(),
                Label("↓"),
                classes="h1",
            ),
            Horizontal(
                self.get_button("raw", "PREROUTING"),
                Static(),
                Static(),
                Label(" ", classes="w1 h3"),
                Label("Routing Decision", classes="choice"),
            ),
            Horizontal(
                Label("↓"),
                Static(),
                Static(),
                Label("↓"),
                classes="h1",
            ),
            Horizontal(
                Label("Connection (state) Tracking", classes="choice"),
                Static(),
                Static(),
                Label(" ", classes="w1 h3"),
                self.get_button("raw", "OUTPUT"),
            ),
            Horizontal(
                Label("↓"),
                Static(),
                Static(),
                Label("↓"),
                classes="h1",
            ),
            Horizontal(
                Button(
                    "mangle | PREROUTING",
                    classes="mangle",
                    id="mangle-PREROUTING",
                ),
                Static(),
                Static(),
                Label(" ", classes="w1 h3"),
                Label("Connection (State) Tracking", classes="choice"),
            ),
            Horizontal(Label("↓"), Static(), Static(), Label("↓"), classes="h1"),
            Horizontal(
                Label("localhost source?", classes="choice h3"),
                Label("→", classes="w1 h3"),
                self.get_button("nat", "PREROUTING"),
                Static(),
                self.get_button("mangle", "OUTPUT"),
            ),
            Horizontal(
                Label("↓"),
                Label("↓"),
                Static(),
                Label("↓"),
                classes="h1",
            ),
            Horizontal(
                Label("↓\n↓\n↓"),
                Label(" ", classes="w1 h3"),
                Label("Routing Decision", classes="choice"),
                Static(),
                Label(" ", classes="w1 h3"),
                self.get_button("nat", "OUTPUT"),
            ),
            Horizontal(
                Label("↓"),
                Label("↓"),
                Static(),
                Label("↓"),
                classes="h1",
            ),
            Horizontal(
                Label("      ↓\n      ↓→→→→→"),
                Label("→", classes="w1 h3"),
                Label("For this host?", classes="choice"),
                Label("→", classes="w1 h3"),
                self.get_button("mangle", "FORWARD"),
                Label(" ", classes="w1 h3"),
                Label("Routing Decision", classes="choice"),
            ),
            Horizontal(
                Static(),
                Label("↓"),
                Label("↓"),
                Label("↓"),
                classes="h1",
            ),
            Horizontal(
                Static(),
                Label(" ", classes="w1 h3"),
                self.get_button("mangle", "INPUT"),
                Label(" ", classes="w1 h3"),
                self.get_button("filter", "FORWARD"),
                Label(" ", classes="w1 h3"),
                self.get_button("filter", "OUTPUT"),
            ),
            Horizontal(
                Static(),
                Label("↓"),
                Label("↓"),
                Label("↓"),
                classes="h1",
            ),
            Horizontal(
                Static(),
                Label(" ", classes="w1 h3"),
                self.get_button("filter", "INPUT"),
                Label(" ", classes="w1 h3"),
                self.get_button("security", "FORWARD"),
                Label(" ", classes="w1 h3"),
                self.get_button("security", "OUTPUT"),
            ),
            Horizontal(
                Static(),
                Label("↓"),
                Label("↓"),
                Label("↓"),
                classes="h1",
            ),
            Horizontal(
                Static(),
                Label(" ", classes="w1 h3"),
                self.get_button("security", "INPUT"),
                Label(" ", classes="w1 h3"),
                Label("Release to outbound", classes="choice"),
                Label("←", classes="w1 h3"),
                Label("←       "),
            ),
            Horizontal(
                Static(),
                Label("↓"),
                Label("↓"),
                Static(),
                classes="h1",
            ),
            Horizontal(
                Static(),
                Label(" ", classes="w1 h3"),
                self.get_button("nat", "INPUT"),
                Label(" ", classes="w1 h3"),
                Button(
                    "mangle | POSTROUTING", classes="mangle", id="mangle-POSTROUTING"
                ),
                Static(),
            ),
            Horizontal(
                Static(),
                Label("↓"),
                Label("↓"),
                Static(),
                classes="h1",
            ),
            Horizontal(
                Static(),
                Label(" ", classes="w1 h3"),
                Label("Local processing", classes="choice"),
                Label(" ", classes="w1 h3"),
                Label("Dest Localhost?", classes="choice"),
                Label("→", classes="w1 h3"),
                Button("nat | POSTROUTING", classes="nat", id="nat-POSTROUTING"),
            ),
            Horizontal(
                Static(),
                Static(),
                Label("↓"),
                Label("↓"),
                classes="h1",
            ),
            Horizontal(
                Static(),
                Label(" ", classes="w1 h3"),
                Static(),
                Label(" ", classes="w1 h3"),
                Label("Outgoing packet", classes="choice"),
                Label(" ", classes="w1 h3"),
                Label("←       "),
            ),
        )

    def get_button(self, table, chain):
        count = len(self.tables.get(table, {}).get(chain, []))
        if count:
            suffix = f" ({count})"
        else:
            suffix = ""
        return Button(
            f"{table} | {chain}{suffix}",
            classes=table,
            id=f"{table}-{chain}",
        )

    class SelectTableChain(Message):
        def __init__(self, sender: MessageTarget, table: str, chain: str):
            self.table = table
            self.chain = chain
            super().__init__(sender)

    async def on_button_pressed(self, event: Button.Pressed):
        table, chain = event.button.id.split("-")
        await self.post_message(self.SelectTableChain(self, table, chain))
