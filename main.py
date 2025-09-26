#!/usr/bin/env python3

import asyncio
import json
import os
import sys
from typing import List, Dict, Any
from websockets import connect as websockets_connect
from websocket import WebSocket
from concurrent.futures import ThreadPoolExecutor
import time

from rich.console import Console
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.table import Table

from utils.banner import banner
from utils.creds import creds
from utils.config_manager import ConfigManager

console = Console()

class DiscordVoiceTool:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.tokens = []
        self.load_tokens()
    
    def load_tokens(self) -> None:
        try:
            tokens_file = self.config_manager.get('tokens_file')
            
            if not os.path.exists(tokens_file):
                console.print(f"[red]❌ {tokens_file} not found![/red]")
                console.print("Please create tokens.txt and add your Discord tokens.")
                sys.exit(1)
            
            with open(tokens_file, 'r', encoding='utf-8') as f:
                self.tokens = [line.strip() for line in f.readlines() if line.strip()]
            
            if not self.tokens:
                console.print("[red]❌ No tokens found in tokens file![/red]")
                sys.exit(1)
                
            console.print(f"[green]✅ Loaded {len(self.tokens)} tokens[/green]")
            
        except Exception as e:
            console.print(f"[red]❌ Error loading tokens: {e}[/red]")
            sys.exit(1)

    async def connect_voice(self, token: str, server_id: str, channel_id: str) -> None:
        try:
            voice_settings = self.config_manager.get('voice_settings')
            
            async with websockets_connect('wss://gateway.discord.gg/?v=9&encoding=json') as websocket:
                hello = await websocket.recv()
                hello_json = json.loads(hello)
                heartbeat_interval = hello_json['d']['heartbeat_interval'] / 1000
                
                identify_payload = {
                    "op": 2,
                    "d": {
                        "token": token,
                        "properties": {
                            "$os": "linux",
                            "$browser": "chrome",
                            "$device": "chrome"
                        },
                        "presence": {
                            "status": "online",
                            "afk": False
                        }
                    }
                }
                await websocket.send(json.dumps(identify_payload))
                
                voice_payload = {
                    "op": 4,
                    "d": {
                        "guild_id": server_id,
                        "channel_id": channel_id,
                        "self_mute": voice_settings['self_mute'],
                        "self_deaf": voice_settings['self_deaf'],
                        "self_stream": voice_settings['self_stream'],
                        "self_video": voice_settings['self_video']
                    }
                }
                await websocket.send(json.dumps(voice_payload))
                
                console.print(f"[green]✅ Token connected to voice channel[/green]")
                
                while True:
                    await asyncio.sleep(heartbeat_interval)
                    await websocket.send(json.dumps({"op": 1, "d": None}))
                    
        except Exception as e:
            console.print(f"[red]❌ Connection error: {e}[/red]")

    async def mass_join_voice(self, server_id: str = None, channel_id: str = None) -> None:
        if not server_id:
            server_id = self.config_manager.get('default_server_id')
        if not channel_id:
            channel_id = self.config_manager.get('default_channel_id')
        
        if not server_id or not channel_id:
            console.print("[red]❌ Server ID and Channel ID are required![/red]")
            return
        
        console.print(f"\n[blue]🚀 Starting mass voice join...[/blue]")
        console.print(f"[yellow]• Server ID: {server_id}[/yellow]")
        console.print(f"[yellow]• Channel ID: {channel_id}[/yellow]")
        console.print(f"[yellow]• Tokens: {len(self.tokens)}[/yellow]")
        
        tasks = []
        for i, token in enumerate(self.tokens):
            task = asyncio.create_task(self.connect_voice(token, server_id, channel_id))
            tasks.append(task)
            
            if i % 5 == 0:
                await asyncio.sleep(0.1)
        
        await asyncio.gather(*tasks, return_exceptions=True)

    def voice_spammer(self, server_id: str = None, channel_id: str = None) -> None:
        if not server_id:
            server_id = self.config_manager.get('default_server_id')
        if not channel_id:
            channel_id = self.config_manager.get('default_channel_id')
        
        if not server_id or not channel_id:
            console.print("[red]❌ Server ID and Channel ID are required![/red]")
            return
        
        console.print(f"\n[red]🔊 Starting voice spammer...[/red]")
        
        voice_settings = self.config_manager.get('voice_settings')
        spammer_settings = self.config_manager.get('spammer_settings')
        
        def spam_token(token: str):
            try:
                ws = WebSocket()
                ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
                
                identify = {
                    "op": 2,
                    "d": {
                        "token": token,
                        "properties": {
                            "$os": "windows",
                            "$browser": "chrome",
                            "$device": "chrome"
                        }
                    }
                }
                ws.send(json.dumps(identify))
                
                while True:
                    join_payload = {
                        "op": 4,
                        "d": {
                            "guild_id": server_id,
                            "channel_id": channel_id,
                            "self_mute": voice_settings['self_mute'],
                            "self_deaf": voice_settings['self_deaf'],
                            "self_stream": voice_settings['self_stream'],
                            "self_video": voice_settings['self_video']
                        }
                    }
                    ws.send(json.dumps(join_payload))
                    time.sleep(spammer_settings['join_duration'])
                    
                    leave_payload = {
                        "op": 4,
                        "d": {
                            "guild_id": server_id,
                            "channel_id": None,
                            "self_mute": voice_settings['self_mute'],
                            "self_deaf": voice_settings['self_deaf']
                        }
                    }
                    ws.send(json.dumps(leave_payload))
                    time.sleep(spammer_settings['leave_duration'])
                    
            except Exception as e:
                console.print(f"[red]❌ Spammer error: {e}[/red]")
        
        max_workers = min(len(self.tokens), self.config_manager.get('max_workers'))
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for token in self.tokens:
                executor.submit(spam_token, token)
                time.sleep(0.1)

    def configuration_menu(self) -> None:
        from rich.prompt import Prompt
        
        while True:
            console.print("\n[bold cyan]🔧 Configuration Menu[/bold cyan]")
            console.print("1. View current configuration")
            console.print("2. Set default Server ID")
            console.print("3. Set default Channel ID")
            console.print("4. Configure voice settings")
            console.print("5. Configure spammer settings")
            console.print("6. Back to main menu")
            
            choice = Prompt.ask("Select option", choices=["1", "2", "3", "4", "5", "6"])
            
            if choice == "1":
                self.config_manager.display_config()
            elif choice == "2":
                server_id = Prompt.ask("Enter default Server ID")
                self.config_manager.set('default_server_id', server_id)
            elif choice == "3":
                channel_id = Prompt.ask("Enter default Channel ID")
                self.config_manager.set('default_channel_id', channel_id)
            elif choice == "4":
                self.configure_voice_settings()
            elif choice == "5":
                self.configure_spammer_settings()
            elif choice == "6":
                break

    def configure_voice_settings(self) -> None:
        voice_settings = self.config_manager.get('voice_settings')
        
        voice_settings['self_mute'] = Confirm.ask("Self Mute?", default=voice_settings['self_mute'])
        voice_settings['self_deaf'] = Confirm.ask("Self Deaf?", default=voice_settings['self_deaf'])
        voice_settings['self_stream'] = Confirm.ask("Self Stream?", default=voice_settings['self_stream'])
        voice_settings['self_video'] = Confirm.ask("Self Video?", default=voice_settings['self_video'])
        
        self.config_manager.set('voice_settings', voice_settings)

    def configure_spammer_settings(self) -> None:
        spammer_settings = self.config_manager.get('spammer_settings')
        
        join_duration = IntPrompt.ask("Join duration (seconds)", default=spammer_settings['join_duration'])
        leave_duration = IntPrompt.ask("Leave duration (seconds)", default=spammer_settings['leave_duration'])
        
        spammer_settings['join_duration'] = max(1, join_duration)
        spammer_settings['leave_duration'] = max(1, leave_duration)
        
        self.config_manager.set('spammer_settings', spammer_settings)

    def display_menu(self) -> None:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Option", style="cyan", width=10)
        table.add_column("Description", style="white")
        
        table.add_row("1", "Mass Join Voice Channel")
        table.add_row("2", "Voice Channel Spammer")
        table.add_row("3", "Configuration Menu")
        table.add_row("4", "Check Tokens")
        table.add_row("5", "Exit")
        
        console.print(Panel(table, title="🎮 Main Menu", border_style="blue"))

    async def run(self) -> None:
        banner()
        creds()
        
        console.print("\n")
        
        while True:
            self.display_menu()
            
            choice = Prompt.ask(
                "\n[bold yellow]Select an option[/bold yellow]",
                choices=["1", "2", "3", "4", "5"],
                default="1"
            )
            
            if choice == "1":
                server_id = Prompt.ask("[bold cyan]Server ID[/bold cyan]", 
                                      default=self.config_manager.get('default_server_id'))
                channel_id = Prompt.ask("[bold cyan]Channel ID[/bold cyan]", 
                                       default=self.config_manager.get('default_channel_id'))
                
                if Confirm.ask("\n[bold red]Start mass join?[/bold red]"):
                    await self.mass_join_voice(server_id, channel_id)
            
            elif choice == "2":
                server_id = Prompt.ask("[bold cyan]Server ID[/bold cyan]", 
                                      default=self.config_manager.get('default_server_id'))
                channel_id = Prompt.ask("[bold cyan]Channel ID[/bold cyan]", 
                                       default=self.config_manager.get('default_channel_id'))
                
                if Confirm.ask("\n[bold red]Start voice spammer?[/bold red]"):
                    self.voice_spammer(server_id, channel_id)
            
            elif choice == "3":
                self.configuration_menu()
            
            elif choice == "4":
                console.print(f"\n[green]✅ Loaded tokens: {len(self.tokens)}[/green]")
                for i, token in enumerate(self.tokens[:5]):
                    console.print(f"[yellow]{i+1}. {token[:20]}...[/yellow]")
                if len(self.tokens) > 5:
                    console.print(f"[yellow]... and {len(self.tokens) - 5} more[/yellow]")
            
            elif choice == "5":
                console.print("[green]👋 Goodbye![/green]")
                break
            
            console.print("\n")

async def main():
    try:
        tool = DiscordVoiceTool()
        await tool.run()
    except KeyboardInterrupt:
        console.print("\n[red]⚠️  Interrupted by user[/red]")
    except Exception as e:
        console.print(f"[red]❌ Fatal error: {e}[/red]")

if __name__ == "__main__":
    if sys.version_info < (3, 7):
        console.print("[red]❌ Python 3.7 or higher required![/red]")
        sys.exit(1)
    
    asyncio.run(main())