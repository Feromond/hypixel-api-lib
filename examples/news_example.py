from hypixel_api_lib import SkyBlockNews 
from dotenv import load_dotenv
import os

load_dotenv()

try:
    skyblock_news = SkyBlockNews(api_key=os.getenv("HYPIXEL_API_KEY"))
except PermissionError as e:
    print(f"Permission error: {e}")
    exit()
except ConnectionError as e:
    print(f"Connection error: {e}")
    exit()

# Latest news
latest_news = skyblock_news.get_latest_news()
if latest_news:
    print("Latest News:")
    print(f"Title: {latest_news.title}")
    print(f"Date: {latest_news.date_str}")
    print(f"Material: {latest_news.material}")
    print(f"Link: {latest_news.link}")
else:
    print("No news available.")

# Get all news items
all_news = skyblock_news.get_all_news()
print(f"\nTotal News Items: {len(all_news)}")
for news_item in all_news:
    date_display = news_item.date.strftime('%d %B %Y') if news_item.date else news_item.date_str
    print(f"- {news_item.title} ({date_display})")


# Get news by specific date
from datetime import date

specific_date = date(2024, 10, 15)
news_on_date = skyblock_news.get_news_by_date(specific_date)

print(f"\nNews items on {specific_date.strftime('%d %B %Y')}:")
for news_item in news_on_date:
    print(f"- {news_item.title}")
