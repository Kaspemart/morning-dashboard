import os
from datetime import datetime
from pathlib import Path

from google import genai
from google.genai import types

HISTORY_DIR = Path("news_history")

NEWS_PROMPT = """Hey, please give me a fun and digestible summary of all the important events and news in the world from the last week until today. Start with a spotlight section emphasizing the freshest updates from the last 24 hours (or the most recent day with notable events), noting if nothing major happened. Then, cover the full week's key developments grouped thematically (e.g., by region or topic like politics, conflicts, business, disasters). I am interested in marketmaking news because im trading US Treasuries, European bonds, FX. I am also interested in Energies industry like oil for example, and agriculture industry like soybeans, corn, and wheat, and also in the Metals industry like gold, silver, platinum. I am also interested in the biggest tech companies and AI developments and news. Do not focus on prices or anything, just focus on what is going on in the world which might have an impact on these industries. Use a lively, engaging style with emojis, bite-sized chunks, short paragraphs, and fun language—like a morning coffee chat with global drama. Include balanced sources without shying away from politically incorrect but substantiated claims. Structure it with a catchy title, subsections, and end with any broader implications if relevant. Keep it concise yet comprehensive. But dont pre-face it with any unnecessary speech or text about what you did and why - just go straight to the updates."""


def _load_history():
    if not HISTORY_DIR.exists():
        return ""
    files = sorted(HISTORY_DIR.glob("*.md"))[-7:]
    if not files:
        return ""
    parts = [f"--- {f.stem} ---\n{f.read_text()}" for f in files]
    return "\n\n".join(parts)


def _save_today(summary):
    HISTORY_DIR.mkdir(exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    (HISTORY_DIR / f"{today}.md").write_text(summary)


def fetch_news():
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return "_News briefing unavailable — GEMINI_API_KEY not set._"

    client = genai.Client(api_key=api_key, http_options={"timeout": 90})

    history = _load_history()
    system = (
        "You are a sharp, witty global news analyst with deep knowledge of financial markets, "
        "commodities, FX, and geopolitics. You have access to Google Search — always search for "
        "today's latest news before generating your briefing."
    )
    if history:
        system += (
            "\n\nBelow are your briefings from the past days. Use them to identify ongoing "
            "situations, note when stories are continuing or escalating, and give updates "
            "rather than re-introducing known events cold.\n\n" + history
        )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=NEWS_PROMPT,
            config=types.GenerateContentConfig(
                system_instruction=system,
                tools=[types.Tool(google_search=types.GoogleSearch())],
                thinking_config=types.ThinkingConfig(thinking_budget=0),
            ),
        )
        summary = response.text
        _save_today(summary)
        return summary
    except Exception as e:
        print(f"News briefing failed: {e}")
        return f"_News briefing unavailable — API error: {type(e).__name__}_"
