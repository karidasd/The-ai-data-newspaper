import feedparser
import datetime
import os
import re
import html
import requests
from bs4 import BeautifulSoup
import shutil

FEEDS = {
    "Industry News": [
        "https://blog.google/technology/ai/rss/"
    ],
    "Research & Papers": [
        "https://news.mit.edu/rss/topic/artificial-intelligence2"
    ],
    "Tutorials & Data Science": [
        "https://towardsdatascience.com/feed",
        "https://www.kdnuggets.com/feed"
    ]
}

def clean_html(raw_html):
    if not raw_html: return ""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext[:150] + "..." if len(cleantext) > 150 else cleantext

def extract_image_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            og_image = soup.find('meta', property='og:image')
            if og_image and og_image.get('content'):
                return og_image['content']
            tw_image = soup.find('meta', name='twitter:image')
            if tw_image and tw_image.get('content'):
                return tw_image['content']
    except Exception as e:
        pass
    return ""

def get_recent_news(days=7):
    all_news = []
    now = datetime.datetime.now(datetime.timezone.utc)
    
    print("Fetching RSS feeds...")
    for category, urls in FEEDS.items():
        for url in urls:
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
                            
                            all_news.append({
                                'title': html.escape(entry.title),
                                'link': entry.link,
                                'published': dt,
                                'source': html.escape(source_title),
                                'summary': html.escape(summary_clean),
                                'category': category
                            })
            except Exception as e:
                print(f"Error parsing {url}: {e}")
                
    all_news.sort(key=lambda x: x['published'], reverse=True)
    
    print("Extracting images (this may take a minute)...")
    for item in all_news:
        item['image'] = extract_image_url(item['link'])
        
    return all_news

def get_archives():
    if not os.path.exists('archive'):
        return []
    files = [f for f in os.listdir('archive') if f.endswith('.html')]
    files.sort(reverse=True)
    return files

def generate_html(news_items, archives):
    date_str = datetime.datetime.now().strftime("%d %B %Y")
    
    top_story = news_items[0] if news_items else None
    other_news = news_items[1:] if len(news_items) > 1 else []
    
    categorized = {cat: [] for cat in FEEDS.keys()}
    for item in other_news:
        categorized[item['category']].append(item)
    
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
        body {{ background-color: var(--bg); color: var(--text-main); font-family: 'Source Sans Pro', sans-serif; line-height: 1.6; padding: 0 1rem; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        
        header {{ text-align: center; padding: 3rem 0 1rem 0; margin-bottom: 2rem; border-bottom: 4px solid var(--text-main); }}
        .masthead-title {{ font-family: 'Playfair Display', serif; font-size: clamp(3rem, 8vw, 6rem); font-weight: 900; text-transform: uppercase; letter-spacing: -2px; line-height: 1; margin-bottom: 1rem; color: var(--text-main); }}
        .masthead-info {{ display: flex; justify-content: space-between; border-top: 1px solid var(--text-main); border-bottom: 1px solid var(--text-main); padding: 0.5rem 0; font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }}
        
        a {{ text-decoration: none; color: inherit; display: block; }}
        
        /* TOP STORY */
        .top-story {{ display: grid; grid-template-columns: 2fr 1.5fr; gap: 2rem; padding-bottom: 2rem; border-bottom: 2px solid var(--text-main); margin-bottom: 3rem; }}
        .top-story-content {{ display: flex; flex-direction: column; justify-content: center; }}
        .top-story-image {{ min-height: 350px; background-size: cover; background-position: center; border-radius: 4px; border: 1px solid var(--border-color); }}
        
        .article-category {{ font-weight: 700; color: var(--accent); text-transform: uppercase; font-size: 0.8rem; letter-spacing: 1px; margin-bottom: 0.5rem; }}
        .top-story-title {{ font-family: 'Playfair Display', serif; font-size: 3.5rem; font-weight: 900; line-height: 1.1; margin-bottom: 1rem; }}
        .top-story-summary {{ font-size: 1.2rem; color: var(--text-muted); margin-bottom: 1.5rem; }}
        
        /* CATEGORY SECTIONS */
        .category-section {{ margin-bottom: 4rem; }}
        .category-header {{ font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 700; border-bottom: 2px solid var(--border-color); padding-bottom: 0.5rem; margin-bottom: 2rem; }}
        
        .articles-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 2rem; }}
        .article {{ padding-bottom: 1.5rem; border-bottom: 1px solid var(--border-color); }}
        .article-image {{ height: 200px; background-size: cover; background-position: center; margin-bottom: 1rem; border-radius: 4px; border: 1px solid var(--border-color); }}
        .article-title {{ font-family: 'Playfair Display', serif; font-size: 1.5rem; font-weight: 700; line-height: 1.2; margin-bottom: 0.5rem; }}
        .article-summary {{ font-size: 0.95rem; color: var(--text-muted); }}
        
        .article:hover .article-title, .top-story:hover .top-story-title {{ color: var(--accent); text-decoration: underline; }}
        
        /* ARCHIVE & ABOUT */
        .sidebar-section {{ background: #f0f0f0; padding: 2rem; border-radius: 4px; margin-bottom: 4rem; }}
        .sidebar-title {{ font-family: 'Playfair Display', serif; font-size: 1.5rem; margin-bottom: 1rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem; }}
        .archive-list {{ list-style: none; }}
        .archive-list li {{ margin-bottom: 0.5rem; }}
        .archive-list a {{ color: var(--text-main); text-decoration: underline; }}
        .archive-list a:hover {{ color: var(--accent); }}
        
        .subscribe-section {{ margin: 4rem 0; padding: 4rem 2rem; background: #111; color: #fff; text-align: center; border-radius: 8px; }}
        .subscribe-title {{ font-family: 'Playfair Display', serif; font-size: 2.5rem; margin-bottom: 1rem; }}
        .subscribe-form {{ display: flex; justify-content: center; max-width: 500px; margin: 0 auto; }}
        .subscribe-input {{ padding: 1rem; flex-grow: 1; border: none; border-radius: 4px 0 0 4px; outline: none; font-size: 1rem; }}
        .subscribe-btn {{ padding: 1rem 2rem; background: var(--accent); color: white; border: none; border-radius: 0 4px 4px 0; font-weight: 600; cursor: pointer; font-size: 1rem; }}
        
        @media (max-width: 900px) {{
            .top-story {{ grid-template-columns: 1fr; }}
            .top-story-image {{ min-height: 250px; order: -1; }}
            .masthead-info {{ flex-direction: column; gap: 0.5rem; text-align: center; }}
            .subscribe-form {{ flex-direction: column; }}
            .subscribe-input {{ border-radius: 4px; margin-bottom: 1rem; }}
            .subscribe-btn {{ border-radius: 4px; }}
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
        html_out += '<div style="text-align: center; padding: 3rem; font-family: \'Playfair Display\', serif; font-size: 1.5rem;">Δεν βρέθηκαν νέα άρθρα για αυτή την εβδομάδα.</div>'
    else:
        # TOP STORY
        ts_date = top_story['published'].strftime('%d %b %Y')
        ts_img_style = f"background-image: url('{top_story['image']}');" if top_story['image'] else "background: linear-gradient(135deg, #cbd5e1, #94a3b8);"
        html_out += f"""
            <a href="{top_story['link']}" target="_blank" class="top-story">
                <div class="top-story-content">
                    <div class="article-category">{top_story['source']} &bull; {ts_date}</div>
                    <h2 class="top-story-title">{top_story['title']}</h2>
                    <p class="top-story-summary">{top_story['summary']}</p>
                </div>
                <div class="top-story-image" style="{ts_img_style}"></div>
            </a>
        """
        
        # CATEGORIES
        for category, articles in categorized.items():
            if articles:
                html_out += f"""
                <section class="category-section">
                    <h2 class="category-header">{category}</h2>
                    <div class="articles-grid">
                """
                for item in articles:
                    img_style = f"background-image: url('{item['image']}');" if item['image'] else "background: linear-gradient(135deg, #e2e8f0, #cbd5e1);"
                    html_out += f"""
                        <a href="{item['link']}" target="_blank" class="article">
                            <div class="article-image" style="{img_style}"></div>
                            <div class="article-category">{item['source']}</div>
                            <h3 class="article-title">{item['title']}</h3>
                            <p class="article-summary">{item['summary']}</p>
                        </a>
                    """
                html_out += """
                    </div>
                </section>
                """
                
    # ARCHIVE & SUBSCRIBE
    html_out += """
        </main>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
            <section class="sidebar-section">
                <h3 class="sidebar-title">Προηγούμενα Τεύχη / Archive</h3>
                <ul class="archive-list">
    """
    if archives:
        for arch in archives:
            name = arch.replace('issue-', '').replace('.html', '')
            html_out += f'<li><a href="archive/{arch}">{name}</a></li>'
    else:
         html_out += '<li>Κανένα παλαιότερο τεύχος.</li>'
         
    html_out += """
                </ul>
            </section>
            
            <section class="sidebar-section">
                <h3 class="sidebar-title">Σχετικά με την Εφημερίδα</h3>
                <p style="margin-bottom: 1rem;"><strong>The AI & Data Newspaper</strong> είναι μια πλήρως αυτοματοποιημένη προσπάθεια συγκέντρωσης των κορυφαίων ειδήσεων. Curated by Code &mdash; Powered by GitHub Actions.</p>
                <p><strong>About the Newspaper:</strong> A fully automated initiative to aggregate top news. Curated by Code.</p>
            </section>
        </div>
        
        <section class="subscribe-section">
            <h2 class="subscribe-title">Subscribe to our Newsletter</h2>
            <p style="margin-bottom: 2rem; font-size: 1.1rem; opacity: 0.8;">Get the latest AI & Data Science news delivered directly to your inbox every week.</p>
            <form action="#" method="POST" class="subscribe-form">
                <input type="email" placeholder="Your email address" class="subscribe-input" required>
                <button type="submit" class="subscribe-btn">Subscribe</button>
            </form>
            <p style="margin-top: 1rem; font-size: 0.8rem; opacity: 0.5;">* Insert your Mailchimp or Substack form action URL here to activate.</p>
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
    news_items = get_recent_news(days=7)
    
    # Create archive directory if it doesn't exist
    os.makedirs('archive', exist_ok=True)
    
    # Get list of archives for the sidebar
    archives = get_archives()
    
    # Generate HTML
    html_content = generate_html(news_items, archives)
    
    # Save as index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    # Save a copy to the archive
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    archive_path = f"archive/issue-{date_str}.html"
    shutil.copy('index.html', archive_path)
        
    print(f"Website generated: index.html and {archive_path}")

if __name__ == "__main__":
    main()
