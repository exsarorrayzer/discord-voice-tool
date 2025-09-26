import json
import os
from typing import Dict, Any
from rich.console import Console

console = Console()

class ConfigManager:
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.default_config = {
            "tokens_file": "tokens.txt",
            "max_workers": 50,
            "timeout": 30,
            "default_server_id": "",
            "default_channel_id": "",
            "voice_settings": {
                "self_mute": False,
                "self_deaf": False,
                "self_stream": False,
                "self_video": False
            },
            "spammer_settings": {
                "join_duration": 1,
                "leave_duration": 1,
                "max_retries": 3
            }
        }
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    console.print(f"[green]✅ Config loaded from {self.config_file}[/green]")
                    return {**self.default_config, **config}  # Merge with defaults
            else:
                self.create_default_config()
                return self.default_config.copy()
        except Exception as e:
            console.print(f"[red]❌ Error loading config: {e}[/red]")
            console.print("[yellow]⚠️  Using default configuration[/yellow]")
            return self.default_config.copy()

    def create_default_config(self) -> None:
        """Create default configuration file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.default_config, f, indent=4)
            console.print(f"[green]✅ Default config created: {self.config_file}[/green]")
        except Exception as e:
            console.print(f"[red]❌ Error creating config file: {e}[/red]")

    def save_config(self) -> None:
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
            console.print(f"[green]✅ Config saved to {self.config_file}[/green]")
        except Exception as e:
            console.print(f"[red]❌ Error saving config: {e}[/red]")

    def get(self, key: str, default=None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k, {})
        return value if value != {} else default

    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self.save_config()

    def display_config(self) -> None:
        """Display current configuration"""
        from rich.table import Table
        from rich.panel import Panel
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Setting", style="green")
        table.add_column("Value", style="yellow")
        
        # Main settings
        table.add_row("Tokens File", self.config['tokens_file'])
        table.add_row("Max Workers", str(self.config['max_workers']))
        table.add_row("Default Server ID", self.config['default_server_id'] or "Not set")
        table.add_row("Default Channel ID", self.config['default_channel_id'] or "Not set")
        
        # Voice settings
        voice = self.config['voice_settings']
        table.add_row("Self Mute", "✅" if voice['self_mute'] else "❌")
        table.add_row("Self Deaf", "✅" if voice['self_deaf'] else "❌")
        table.add_row("Self Stream", "✅" if voice['self_stream'] else "❌")
        table.add_row("Self Video", "✅" if voice['self_video'] else "❌")
        
        console.print(Panel(table, title="📋 Current Configuration", border_style="blue"))