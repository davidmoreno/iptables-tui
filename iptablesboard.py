from textual.widgets import Button, Static, DataTable, Label
from textual.containers import Container, Horizontal
from textual.scroll_view import ScrollView
from textual.message import Message, MessageTarget


class IpTablesBoard(Static):
    def compose(self):
        yield ScrollView(
            Horizontal(
                Label("Incoming", classes="choice"),
                Static(),
                Static(),
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
                Button("raw | PREROUTING", classes="raw", id="raw-PREROUTING"),
                Static(),
                Static(),
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
                Button("raw | OUTPUT", classes="raw", id="raw-OUTPUT"),
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
                Label("Connection (State) Tracking", classes="choice"),
            ),
            Horizontal(Label("↓"), Static(), Static(), Label("↓"), classes="h1"),
            Horizontal(
                Label("localhost source?", classes="choice h3"),
                Label("→", classes="w1 h3"),
                Button("nat | PREROUTING", classes="nat", id="nat-PREROUTING"),
                Static(),
                Button("mangle | OUTPUT", classes="mangle", id="mangle-OUTPUT"),
            ),
            Horizontal(
                Label("↓"),
                Label("↓"),
                Static(),
                Label("↓"),
                classes="h1",
            ),
            Horizontal(
                Label("↓"),
                Label("Routing Decision", classes="choice"),
                Static(),
                Button("nat | OUTPUT", classes="nat", id="nat-OUTPUT"),
            ),
            Horizontal(
                Label("↓"),
                Label("↓"),
                Static(),
                Label("↓"),
                classes="h1",
            ),
            Horizontal(
                Label("↓"),
                Label("→", classes="w1 h3"),
                Label("For this host?", classes="choice"),
                Label("→", classes="w1 h3"),
                Button("mangle | FORWARD", classes="mangle", id="mangle-FORWARD"),
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
                Button("mangle | INPUT", classes="mangle", id="mangle-INPUT"),
                Button("filter | FORWARD", classes="filter", id="filter-FORWARD"),
                Button("filter | OUTPUT", classes="filter", id="filter-OUTPUT"),
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
                Button("filter | INPUT", classes="filter", id="filter-INPUT"),
                Button("security | FORWARD", classes="security", id="security-FORWARD"),
                Button("security | OUTPUT", classes="security", id="security-OUTPUT"),
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
                Button("security | INPUT", classes="security", id="security-INPUT"),
                Label("Release to outbound", classes="choice"),
                Label("←", classes="w1 h3"),
                Label("←"),
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
                Button("nat | INPUT", classes="nat", id="nat-INPUT"),
                Button(
                    "mangle | POSTROUTING", classes="mangle", id="mangle-POSTROUTING"
                ),
                Static(),
            ),
            Horizontal(
                Static(),
                Static(),
                Label("↓"),
                Static(),
                classes="h1",
            ),
            Horizontal(
                Static(),
                Static(),
                Label("Dest Localhost", classes="choice"),
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
                Static(),
                Label("Outgoing packet", classes="choice"),
                Label("←"),
            ),
        )

    class SelectTableChain(Message):
        def __init__(self, sender: MessageTarget, table: str, chain: str):
            self.table = table
            self.chain = chain
            super().__init__(sender)

    async def on_button_pressed(self, event: Button.Pressed):
        table, chain = event.button.id.split("-")
        await self.post_message(self.SelectTableChain(self, table, chain))
