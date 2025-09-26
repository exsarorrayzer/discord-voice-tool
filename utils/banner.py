from rich.console import Console
from rich.panel import Panel

console = Console()

def banner() -> None:
    art = r'''


'''

    # Mor tonları (RGB)
    purple_shades = [
        (102, 0, 153),
        (128, 0, 192),
        (153, 51, 255),
        (178, 102, 255),
        (153, 51, 255),
        (128, 0, 192),
        (102, 0, 153)
    ]

    art_lines = art.strip("\n").split("\n")
    colored_lines = []

    for i, line in enumerate(art_lines):
        color = purple_shades[i % len(purple_shades)]
        hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
        colored_lines.append(f"[{hex_color}]{line}[/{hex_color}]")

    console.print("\n".join(colored_lines))

if __name__ == "__main__":
    banner()