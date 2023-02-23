from textual.widgets import Button, Static, DataTable, Label
from textual.containers import Container


class IpTablesBoard(Static):
    def compose(self):
        yield Button("Incoming")
        yield Static()
        yield Static()
        yield Button("Local Generated")

        yield Label("↓")
        yield Static()
        yield Static()
        yield Label("↓")

        yield Button("raw | PREROUTING", classes="raw")
        yield Static()
        yield Static()
        yield Button("Routing Decision")

        yield Label("↓")
        yield Static()
        yield Static()
        yield Label("↓")

        yield Button("Connection (state) Tracking")
        yield Static()
        yield Static()
        yield Button("raw | OUTPUT", classes="raw")

        yield Label("↓")
        yield Static()
        yield Static()
        yield Label("↓")

        yield Button("mangle | PREROUTING", classes="mangle")
        yield Static()
        yield Static()
        yield Button("Connection (State) Tracking")

        yield Label("↓")
        yield Static()
        yield Static()
        yield Label("↓")

        yield Button("localhost source?")
        yield Button("nat | PREROUTING", classes="nat")
        yield Static()
        yield Button("mangle | OUTPUT", classes="mangle")

        yield Label("↓")
        yield Static()
        yield Static()
        yield Label("↓")

        yield Static()
        yield Button("Routing Decision")
        yield Static()
        yield Button("nat | OUTPUT", classes="nat")

        yield Static()
        yield Button("For this host?")
        yield Button("mangle | FORWARD", classes="mangle")
        yield Button("Routing Decision")

        yield Static()
        yield Button("mangle | INPUT", classes="mangle")
        yield Button("filter | FORWARD", classes="filter")
        yield Button("filter | FORWARD Decision", classes="filter")

        yield Static()
        yield Button("filter | INPUT", classes="filter")
        yield Button("security | FORWARD")
        yield Button("security | OUTPUT")
