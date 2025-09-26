# Discord Voice Tool

A professional Discord voice channel utility tool with mass joining and voice channel spamming capabilities.

✨ Features

· Mass Voice Join - Join voice channels with multiple tokens simultaneously
· Voice Spammer - Automated join/leave spam with customizable timing
· Config Management - JSON-based configuration system
· Rich UI - Beautiful terminal interface with colors and progress indicators
· Token Management - Easy token management from external file
· Rate Limit Protection - Built-in protection against Discord rate limits

🚀 Quick Start

Prerequisites

· Python 3.7 or higher
· Discord account(s) with valid token(s)

Installation

1. Clone the repository

```bash
git clone https://github.com/exsarorrayzer/discord-voice-tool.git
cd discord-voice-tool
```

1. Install dependencies

```bash
pip install -r requirements.txt
```

1. Configure your tokens
   · Create tokens.txt in the main directory
   · Add your Discord tokens (one per line)
2. Run the tool

```bash
python main.py
```

⚙️ Configuration

The tool uses config.json for all settings:

Default Configuration

```json
{
    "tokens_file": "tokens.txt",
    "max_workers": 50,
    "timeout": 30,
    "default_server_id": "",
    "default_channel_id": "",
    "voice_settings": {
        "self_mute": false,
        "self_deaf": false,
        "self_stream": false,
        "self_video": false
    },
    "spammer_settings": {
        "join_duration": 1,
        "leave_duration": 1,
        "max_retries": 3
    }
}
```

Configuration Options

Setting Description Default
tokens_file Path to tokens file tokens.txt
max_workers Maximum concurrent connections 50
default_server_id Default server ID for quick access ""
default_channel_id Default channel ID for quick access ""
voice_settings.self_mute Join voice muted false
voice_settings.self_deaf Join voice deafened false
spammer_settings.join_duration Seconds to stay in voice 1
spammer_settings.leave_duration Seconds to wait between joins 1

🎮 Usage

Main Menu Options

1. Mass Join Voice Channel
   · Join a voice channel with all tokens
   · Uses WebSocket connections for stability
   · Maintains connection until interrupted
2. Voice Channel Spammer
   · Automated join/leave cycling
   · Customizable timing intervals
   · Configurable voice settings
3. Configuration Menu
   · View current settings
   · Set default Server/Channel IDs
   · Configure voice and spammer settings
4. Check Tokens
   · View loaded tokens (first 5 with masking)
   · Verify token count and validity

Getting Server and Channel IDs

To get Server and Channel IDs in Discord:

1. Enable Developer Mode:
   · Settings → Advanced → Developer Mode (ON)
2. Get Server ID:
   · Right-click server icon → "Copy ID"
3. Get Channel ID:
   · Right-click voice channel → "Copy ID"

📁 Project Structure

```
discord-voice-tool/
├── main.py                 # Main application
├── config.json            # Configuration file
├── tokens.txt             # Discord tokens (create this)
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── utils/
    ├── banner.py          # ASCII art banner
    ├── creds.py          # Developer credits
    └── config_manager.py # Configuration management
```

🛠️ Technical Details

Dependencies

· rich: Beautiful terminal formatting
· websockets: WebSocket client implementation
· colorama: Cross-platform colored terminal text

Architecture

· Async/Await: For non-blocking WebSocket connections
· ThreadPoolExecutor: For concurrent token management
· Modular Design: Separated concerns for maintainability
· Error Handling: Comprehensive exception handling

⚠️ Disclaimer

This tool is intended for educational and development purposes only. Users are responsible for complying with Discord's Terms of Service. Misuse may result in account suspension or termination.

Responsible Usage Guidelines

· ✅ Use on servers you own or have permission to test on
· ✅ Respect rate limits and server resources
· ✅ Use for legitimate testing and development
· ❌ Do not use for harassment or disruption
· ❌ Do not use on servers without permission
· ❌ Do not use for malicious purposes

🐛 Troubleshooting

Common Issues

"tokens.txt not found"

· Create tokens.txt file in the main directory
· Add your Discord tokens (one per line)

"No tokens found"

· Ensure tokens are properly formatted in tokens.txt
· Remove empty lines and comments

Connection errors

· Verify token validity
· Check internet connection
· Ensure Discord service is accessible

Rate limiting

· Reduce max_workers in configuration
· Increase delays between operations

Debug Mode

For detailed debugging, enable verbose logging by modifying the source code or checking the console output for specific error messages.

👨‍💻 Developer

exsarorrayzer

· GitHub: exsarorrayzer
· Instagram: exsarorrayzer
· Discord: noinfonocontext
· YouTube: exsarorrayzer

🙏 Acknowledgments

· Discord API community for documentation
· Rich library developers for amazing terminal UI
· Python community for excellent WebSocket support

---

Remember: Always use tools responsibly and respect platform terms of service. Happy coding! 🚀