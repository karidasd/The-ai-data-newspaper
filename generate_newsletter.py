import feedparser
import datetime
import os

FEEDS = [
    "https://news.mit.edu/rss/topic/artificial-intelligence2",
    "https://towardsdatascience.com/feed",
    "https://www.kdnuggets.com/feed",
    "https://blog.google/technology/ai/rss/"
]

def get_recent_news(days=7):
    recent_news = []
    now = datetime.datetime.now(datetime.timezone.utc)
    
    for url in FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                # Some feeds might not have published_parsed, fallback to updated_parsed
                dt_parsed = entry.get('published_parsed') or entry.get('updated_parsed')
                if dt_parsed:
                    dt = datetime.datetime(*dt_parsed[:6], tzinfo=datetime.timezone.utc)
                    if (now - dt).days <= days:
                        source_title = feed.feed.title if hasattr(feed.feed, 'title') else url
                        recent_news.append({
                            'title': entry.title,
                            'link': entry.link,
                            'published': dt,
                            'source': source_title
                        })
        except Exception as e:
            print(f"Error parsing {url}: {e}")
            
    # Sort by date descending
    recent_news.sort(key=lambda x: x['published'], reverse=True)
    return recent_news

def generate_markdown(news_items):
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    md = f"# Εβδομαδιαία Εφημερίδα AI & Data Science - {date_str}\n\n"
    md += "Καλώς ήρθατε στο τεύχος της εβδομάδας! Εδώ συγκεντρώνονται τα πιο πρόσφατα νέα από το χώρο της Τεχνητής Νοημοσύνης.\n\n"
    
    if not news_items:
        md += "Δεν βρέθηκαν νέα άρθρα για αυτή την εβδομάδα.\n"
        return md

    for item in news_items:
        md += f"### [{item['title']}]({item['link']})\n"
        md += f"**Πηγή:** {item['source']} | **Ημερομηνία:** {item['published'].strftime('%d/%m/%Y')}\n\n"
        
    return md

def main():
    print("Fetching news...")
    news_items = get_recent_news(days=7)
    print(f"Found {len(news_items)} articles.")
    
    md_content = generate_markdown(news_items)
    
    # Create issues directory
    os.makedirs('issues', exist_ok=True)
    
    # Save file
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"issues/issue-{date_str}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(md_content)
        
    print(f"Newsletter generated: {filename}")
    
    # Update README to link the latest issue
    try:
        if os.path.exists('README.md'):
            with open('README.md', 'r', encoding='utf-8') as f:
                readme = f.read()
            
            # Simple insertion at the top of the issues list
            if "## Τελευταία Τεύχη" in readme:
                parts = readme.split("## Τελευταία Τεύχη")
                new_entry = f"\n- [{date_str}](issues/issue-{date_str}.md)"
                
                # Check if already added
                if new_entry not in parts[1]:
                    new_readme = parts[0] + "## Τελευταία Τεύχη" + new_entry + parts[1]
                    with open('README.md', 'w', encoding='utf-8') as f:
                        f.write(new_readme)
    except Exception as e:
        print(f"Could not update README: {e}")

if __name__ == "__main__":
    main()
