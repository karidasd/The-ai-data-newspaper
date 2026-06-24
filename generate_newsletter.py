import feedparser
import datetime
import os
import re

FEEDS = [
    "https://news.mit.edu/rss/topic/artificial-intelligence2",
    "https://towardsdatascience.com/feed",
    "https://www.kdnuggets.com/feed",
    "https://blog.google/technology/ai/rss/"
]

def clean_html(raw_html):
    if not raw_html: return ""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext[:180] + "..." if len(cleantext) > 180 else cleantext

def get_recent_news(days=7):
    recent_news = []
    now = datetime.datetime.now(datetime.timezone.utc)
    
    for url in FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                dt_parsed = entry.get('published_parsed') or entry.get('updated_parsed')
                if dt_parsed:
                    dt = datetime.datetime(*dt_parsed[:6], tzinfo=datetime.timezone.utc)
                    if (now - dt).days <= days:
                        source_title = feed.feed.title if hasattr(feed.feed, 'title') else url
                        
                        summary = entry.get('summary', '')
                        if not summary:
                            summary = entry.get('description', '')
                        summary_clean = clean_html(summary)
                        
                        import html
                        
                        recent_news.append({
                            'title': html.escape(entry.title),
                            'link': entry.link,
                            'published': dt,
                            'source': html.escape(source_title),
                            'summary': html.escape(summary_clean)
                        })
        except Exception as e:
            print(f"Error parsing {url}: {e}")
            
    recent_news.sort(key=lambda x: x['published'], reverse=True)
    return recent_news

def generate_html(news_items):
    date_str = datetime.datetime.now().strftime("%d %b %Y")
    
    html = f"""<!DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI & Data Science News</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #38bdf8;
            --accent-glow: rgba(56, 189, 248, 0.5);
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
        }}
        
        body {{
            background-color: var(--bg-color);
            color: var(--text-main);
            line-height: 1.6;
            min-height: 100vh;
            background-image: 
                radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(139, 92, 246, 0.15) 0px, transparent 50%);
            background-attachment: fixed;
        }}
        
        header {{
            text-align: center;
            padding: 4rem 1rem;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }}
        
        h1 {{
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(to right, #38bdf8, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }}
        
        .date-badge {{
            display: inline-block;
            background: rgba(255,255,255,0.1);
            padding: 0.5rem 1.5rem;
            border-radius: 50px;
            font-size: 0.9rem;
            color: var(--text-muted);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.05);
        }}
        
        main {{
            max-width: 1200px;
            margin: 3rem auto;
            padding: 0 1.5rem;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 2rem;
        }}
        
        .card {{
            background: var(--card-bg);
            border-radius: 16px;
            padding: 1.5rem;
            border: 1px solid rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            display: flex;
            flex-direction: column;
            text-decoration: none;
            color: inherit;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
            border-color: rgba(56, 189, 248, 0.3);
            box-shadow: 0 10px 30px -10px var(--accent-glow);
        }}
        
        .card-source {{
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--accent);
            margin-bottom: 0.5rem;
            font-weight: 600;
        }}
        
        .card-title {{
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1rem;
            line-height: 1.4;
        }}
        
        .card-summary {{
            color: var(--text-muted);
            font-size: 0.95rem;
            flex-grow: 1;
            margin-bottom: 1.5rem;
        }}
        
        .card-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.85rem;
            color: var(--text-muted);
            border-top: 1px solid rgba(255,255,255,0.05);
            padding-top: 1rem;
        }}
        
        .hero-card {{
            grid-column: 1 / -1;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            align-items: center;
            background: linear-gradient(135deg, rgba(30,41,59,0.9), rgba(15,23,42,0.9));
            padding: 3rem;
        }}
        
        @media (max-width: 768px) {{
            .hero-card {{
                grid-template-columns: 1fr;
                padding: 1.5rem;
            }}
            h1 {{ font-size: 2.2rem; }}
        }}
        
        footer {{
            text-align: center;
            padding: 3rem;
            color: var(--text-muted);
            border-top: 1px solid rgba(255,255,255,0.05);
            margin-top: 4rem;
        }}
    </style>
</head>
<body>
    <header>
        <h1>The AI & Data Newspaper</h1>
        <div class="date-badge">Τελευταία Ενημέρωση: {date_str}</div>
    </header>
    
    <main>
"""
    if not news_items:
        html += '<p style="text-align:center;">Δεν βρέθηκαν νέα άρθρα για αυτή την εβδομάδα.</p>'
    else:
        html += '<div class="grid">'
        for i, item in enumerate(news_items):
            card_class = "card hero-card" if i == 0 else "card"
            
            # Simple fallback layout for hero card footer
            html += f"""
            <a href="{item['link']}" target="_blank" class="{card_class}">
                <div>
                    <div class="card-source">{item['source']}</div>
                    <h2 class="card-title">{item['title']}</h2>
                    <p class="card-summary">{item['summary']}</p>
                </div>
                <div class="card-footer" style="{'grid-column: 1 / -1;' if i==0 else ''}">
                    <span>{item['published'].strftime('%d %b %Y')}</span>
                    <span style="color: var(--accent)">Διάβασε περισσότερα &rarr;</span>
                </div>
            </a>
            """
        html += '</div>'
        
    html += """
    </main>
    
    <footer>
        <p>Αυτοματοποιημένο περιοδικό δημιουργημένο με Python & GitHub Actions.</p>
    </footer>
</body>
</html>
"""
    return html

def main():
    print("Fetching news...")
    news_items = get_recent_news(days=7)
    print(f"Found {len(news_items)} articles.")
    
    html_content = generate_html(news_items)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print("Website generated: index.html")

if __name__ == "__main__":
    main()
