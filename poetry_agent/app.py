import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.markdown import Markdown
from rich.box import ROUNDED, DOUBLE

console = Console()
load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-2.0-flash"
)

# === Sub Agents ===
iqbal_agent = Agent(
    name="Iqbal_Agent",
    model=model,
    instructions="""You MUST respond with this EXACT format:
🌟 [Name]: Allama Muhammad Iqbal (1877-1938)
📖 [Ghazal]: 
"Lab pe aati hai dua ban ke tamanna meri
Zindagi shama ki soorat ho Khudaya meri
Zindagi teri zulfon ki narm chhaon mein
Kat-e-waqt guzre ya Rab ilm-o-hikmat mein
Ae khuda shikwa-e-arbab-e-wafa bhi sun le
Khugar-e-hamd se thora sa gila bhi sun le"

🔍 [Tashreeh]: This ghazal is a spiritual prayer expressing:
- A child's innocent supplication 🧒
- Yearning for divine guidance 🕌  
- Balance between praise and complaint
- Quest for knowledge and wisdom 📚

🏰 [History]: Known as 'Poet of the East', Iqbal:
- Inspired Pakistan's creation 🇵🇰
- Revolutionized Islamic philosophy
- Wrote in both Urdu and Persian
- Knighted by British Empire (later returned title) 🏅"""
)

ghalib_agent = Agent(
    name="Ghalib_Agent",
    model=model,
    instructions="""You MUST respond with this EXACT format:
🌟 [Name]: Mirza Asadullah Khan Ghalib (1797-1869)
📖 [Ghazal]:
"Dil-e-nadan tujhe hua kya hai
Aakhir is dard ki dawa kya hai
Hum hain mushtaq aur woh be-zar
Ya ilahi ye maajra kya hai
Main bhi munh mein zaban rakhta hoon
Kaash pucho ke muddaa kya hai"

🔍 [Tashreeh]: Ghalib's masterpiece explores:
- Paradox of unrequited love 💔  
- Philosophical questions about suffering
- Lover's frustration with beloved
- Each couplet is a complete thought 💭

🏰 [History]: The last great Mughal poet:
- Witnessed Delhi's decline 🏛️
- Master of Urdu and Persian
- Transformed ghazal into philosophical form
- Known for wit and complex imagery 🎭"""
)

faiz_agent = Agent(
    name="Faiz_Agent",
    model=model,
    instructions="""You MUST respond with this EXACT format:
🌟 [Name]: Faiz Ahmed Faiz (1911-1984)
📖 [Ghazal]:
"Gulon mein rang bhare baad-e-naubahar chale
Chale bhi aao ke gulshan ka karobar chale
Qafas udaas hai yaaron saba se kuch to kaho
Kaheen to beher-e-khuda aaj zikr-e-yaar chale
Mat kar alam ae dil-e-naadaan tujhe
Dekh ke tere ham-nashinon ka shumaar chale"

🔍 [Tashreeh]: Faiz's revolutionary work blends:
- Beauty of nature 🌸 with political metaphors
- Prison imagery symbolizing oppression ⛓️
- Hope for social change ✊
- Traditional form with modern themes

🏰 [History]: Nobel-nominated revolutionary:
- Blended Marxism with ghazal tradition
- Works banned by dictatorships 🚫
- Inspired South Asian progressives
- Won Lenin Peace Prize ☮️"""
)

# === Master Agent ===
master_agent = Agent(
    name="Urdu_Poetry_Master",
    model=model,
    instructions="""
You MUST route requests EXACTLY:
- "iqbal" → Iqbal_Agent
- "ghalib" → Ghalib_Agent  
- "faiz" → Faiz_Agent
NEVER modify the original poetry""",
    handoffs=[iqbal_agent, ghalib_agent, faiz_agent]
)

# === Heading Banner ===
def print_heading():
    heading = """[bold bright_cyan]
╔════════════════════════════════════════════════════════════════════════════════╗
║████████████████████████████████████████████████████████████████████████████████
╭───────────────────────────────✦ ♛ ✦───────────────────────────────╮
│                                                                     |
│        ░▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒░           
│        █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█           
│        █               U R D U   P O E T R Y               █       
│        █████████████████████████████████████████████████████       
│                                                                   
│        "Khudi ko kar buland itna, ke har taqdeer se pehle         
│         Khuda bande se khud pooche, bata teri raza kya hai"         
│                                                                    
╰───────────────────────────────✦ ♛ ✦───────────────────────────────╯
████████████████████████████████████████████████████████████████████████████████
╚═══════════════════════════ Explore the treasures of Urdu poetry ══════════════╝
[/bold bright_cyan]"""
    console.print(heading)
    console.print(Panel.fit(
        "[bold cyan]Available Poets:[/bold cyan]\n"
        "• [bold yellow]Allama Iqbal[/bold yellow] - Spiritual & Philosophical Poetry\n"
        "• [bold yellow]Mirza Ghalib[/bold yellow] - Classical Ghazals\n"
        "• [bold yellow]Faiz Ahmed Faiz[/bold yellow] - Revolutionary Verses\n\n"
        "Type 'exit' to quit",
        title="📜 Urdu Poets Collection",
        border_style="bright_magenta",
        box=ROUNDED
    ))

# === Beautified Display Function ===
def display_formatted_poet_info(info):
    sections = {
        "🌟 [Name]": "",
        "📖 [Ghazal]": "",
        "🔍 [Tashreeh]": "",
        "🏰 [History]": ""
    }

    current = None
    for line in info.split("\n"):
        line = line.strip()
        for key in sections:
            if line.startswith(key):
                current = key
                sections[key] = line[len(key):].strip() + "\n"
                break
        else:
            if current:
                sections[current] += line + "\n"

    console.rule("[bold bright_magenta]📚 Urdu Poetry Archive[/bold bright_magenta]")
    console.print(Panel(
        sections["🌟 [Name]"],
        title="🌟 Poet Name",
        border_style="bright_yellow",
        box=DOUBLE,
        padding=(1, 2)
    ))

    console.print(Columns([
        Panel(
            sections["📖 [Ghazal]"],
            title="📖 Ghazal",
            border_style="cyan",
            box=ROUNDED,
            padding=(1, 2)
        ),
        Panel(
            Markdown(sections["🔍 [Tashreeh]"]),
            title="🔍 Tashreeh (Explanation)",
            border_style="green",
            box=ROUNDED,
            padding=(1, 2)
        )
    ], equal=True))

    console.print(Panel(
        Markdown(sections["🏰 [History]"]),
        title="🏰 Historical Background",
        border_style="blue",
        box=DOUBLE,
        padding=(1, 2)
    ))

# === App Runner ===
print_heading()

# User input with flexible matching
poet_input = input("📜 Enter poet name (iqbal / ghalib / faiz): ").lower().strip()

# Map longer inputs to keys
if "iqbal" in poet_input:
    poet = "iqbal"
elif "ghalib" in poet_input:
    poet = "ghalib"
elif "faiz" in poet_input:
    poet = "faiz"
elif poet_input == "exit":
    console.print("[bold green]👋 Exiting...[/bold green]")
    exit()
else:
    console.print("[bold red]❌ Invalid poet name! Please choose: iqbal / ghalib / faiz[/bold red]")
    exit()

result = Runner.run_sync(master_agent, poet)
text_output = result.output if hasattr(result, "output") else str(result)
display_formatted_poet_info(text_output)
