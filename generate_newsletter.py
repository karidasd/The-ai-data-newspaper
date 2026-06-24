import feedparser
import datetime
import os
import re
import html

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
    date_str = datetime.datetime.now().strftime("%d %B %Y")
    
    html_out = f"""<!DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The AI & Data Newspaper</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Source+Sans+Pro:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #f9f8f6;
            --text-main: #1a1a1a;
            --text-muted: #555555;
            --accent: #b91c1c;
            --border-color: #d1d1d1;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            background-color: var(--bg);
            color: var(--text-main);
            font-family: 'Source Sans Pro', sans-serif;
            line-height: 1.6;
            padding: 0 1rem;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        /* MASTHEAD (HEADER) */
        header {{
            text-align: center;
            padding: 3rem 0 1rem 0;
            margin-bottom: 2rem;
            border-bottom: 4px solid var(--text-main);
        }}
        
        .masthead-title {{
            font-family: 'Playfair Display', serif;
            font-size: clamp(3rem, 8vw, 6rem);
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: -2px;
            line-height: 1;
            margin-bottom: 1rem;
            color: var(--text-main);
        }}
        
        .masthead-info {{
            display: flex;
            justify-content: space-between;
            border-top: 1px solid var(--text-main);
            border-bottom: 1px solid var(--text-main);
            padding: 0.5rem 0;
            font-size: 0.9rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        /* MAGAZINE GRID */
        main {{
            display: grid;
            grid-template-columns: repeat(12, 1fr);
            gap: 2rem;
        }}
        
        a {{ text-decoration: none; color: inherit; display: block; }}
        
        /* TOP STORY (HERO) */
        .top-story {{
            grid-column: span 12;
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 2rem;
            padding-bottom: 2rem;
            border-bottom: 2px solid var(--border-color);
        }}
        
        .top-story-content {{
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        
        .article-category {{
            font-weight: 700;
            color: var(--accent);
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 1px;
            margin-bottom: 0.5rem;
        }}
        
        .top-story-title {{
            font-family: 'Playfair Display', serif;
            font-size: 3.5rem;
            font-weight: 900;
            line-height: 1.1;
            margin-bottom: 1rem;
        }}
        
        .top-story-summary {{
            font-size: 1.2rem;
            color: var(--text-muted);
            margin-bottom: 1.5rem;
        }}
        
        .hero-image-block {{
            background: var(--text-main);
            color: var(--bg);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
            text-align: center;
            border-radius: 4px;
        }}
        
        /* STANDARD ARTICLES */
        .article {{
            grid-column: span 4;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid var(--border-color);
        }}
        
        .article-title {{
            font-family: 'Playfair Display', serif;
            font-size: 1.5rem;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 0.5rem;
        }}
        
        .article-summary {{
            font-size: 0.95rem;
            color: var(--text-muted);
        }}
        
        .article:hover .article-title, .top-story:hover .top-story-title {{
            color: var(--accent);
            text-decoration: underline;
        }}
        
        /* RESPONSIVE */
        @media (max-width: 900px) {{
            .top-story {{ grid-template-columns: 1fr; }}
            .article {{ grid-column: span 6; }}
            .masthead-info {{ flex-direction: column; gap: 0.5rem; }}
        }}
        
        @media (max-width: 600px) {{
            .article {{ grid-column: span 12; }}
            .masthead-title {{ font-size: 3.5rem; }}
        }}
        
        footer {{
            text-align: center;
            padding: 3rem 0;
            margin-top: 2rem;
            border-top: 4px solid var(--text-main);
            font-family: 'Playfair Display', serif;
            font-style: italic;
        }}
        
        .about-section {{
            margin-top: 4rem;
            padding: 3rem;
            background: var(--text-main);
            color: var(--bg);
            border-radius: 8px;
            text-align: center;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }}
        .about-title {{
            font-family: 'Playfair Display', serif;
            font-size: clamp(1.8rem, 5vw, 2.5rem);
            margin-bottom: 1rem;
            line-height: 1.2;
        }}
        .about-text {{
            max-width: 800px;
            margin: 0 auto 1.5rem auto;
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        .about-footer {{
            font-family: 'Playfair Display', serif;
            font-style: italic;
            opacity: 0.8;
        }}
        @media (max-width: 600px) {{
            .about-section {{
                padding: 1.5rem;
                margin-top: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="masthead-title">The AI News</div>
            <div class="masthead-info">
                <span>ΤΕΥΧΟΣ: {date_str}</span>
                <span>DATA SCIENCE & ARTIFICIAL INTELLIGENCE</span>
                <span>ΔΩΡΕΑΝ ΕΚΔΟΣΗ</span>
            </div>
        </header>
        
        <main>
"""
    if not news_items:
        html_out += '<div style="grid-column: span 12; text-align: center; padding: 3rem; font-family: \'Playfair Display\', serif; font-size: 1.5rem;">Δεν βρέθηκαν νέα άρθρα για αυτή την εβδομάδα.</div>'
    else:
        for i, item in enumerate(news_items):
            date_formatted = item['published'].strftime('%d %b %Y')
            
            if i == 0:
                html_out += f"""
                <a href="{item['link']}" target="_blank" class="top-story">
                    <div class="top-story-content">
                        <div class="article-category">{item['source']} &bull; {date_formatted}</div>
                        <h2 class="top-story-title">{item['title']}</h2>
                        <p class="top-story-summary">{item['summary']}</p>
                    </div>
                    <div class="hero-image-block">
                        <span style="font-family: 'Playfair Display', serif; font-size: 2rem; font-style: italic;">"The biggest story of the week."</span>
                    </div>
                </a>
                """
            else:
                html_out += f"""
                <a href="{item['link']}" target="_blank" class="article">
                    <div class="article-category">{item['source']}</div>
                    <h3 class="article-title">{item['title']}</h3>
                    <p class="article-summary">{item['summary']}</p>
                </a>
                """
                
    html_out += """
        </main>
        
        <section class="about-section">
            <h2 class="about-title">Σχετικά με την Εφημερίδα</h2>
            <p class="about-text">
                Το <strong>The AI & Data Newspaper</strong> είναι μια πλήρως αυτοματοποιημένη προσπάθεια συγκέντρωσης των κορυφαίων ειδήσεων γύρω από την Τεχνητή Νοημοσύνη και την Επιστήμη Δεδομένων. Η συλλογή των άρθρων, η σελιδοποίηση και η έκδοση του περιοδικού πραγματοποιούνται αυτόματα κάθε εβδομάδα, αντλώντας δεδομένα από κορυφαίες πηγές παγκοσμίως.
            </p>
            <h2 class="about-title" style="margin-top: 3rem;">About the Newspaper</h2>
            <p class="about-text">
                <strong>The AI & Data Newspaper</strong> is a fully automated initiative to aggregate top news around Artificial Intelligence and Data Science. The collection of articles, formatting, and publishing are performed automatically every week, pulling data from top global sources.
            </p>
            <p class="about-footer" style="margin-top: 2rem;">
                Curated by Code &mdash; Powered by GitHub Actions
            </p>
        </section>
        
        <footer>
            <p>Αυτοματοποιημένο ψηφιακό περιοδικό &mdash; Δημιουργημένο με Python & GitHub Actions.</p>
        </footer>
    </div>
</body>
</html>
"""
    return html_out

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
