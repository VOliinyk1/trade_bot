import requests
import feedparser
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
from typing import List, Dict
import re

class NewsAggregator:
    def __init__(self):
        self.news_sources = {
            'coindesk': {
                'rss': 'https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml',
                'base_url': 'https://www.coindesk.com'
            },
            'cointelegraph': {
                'rss': 'https://cointelegraph.com/rss',
                'base_url': 'https://cointelegraph.com'
            },
            'decrypt': {
                'rss': 'https://decrypt.co/feed',
                'base_url': 'https://decrypt.co'
            },
            'bitcoinist': {
                'rss': 'https://bitcoinist.com/feed/',
                'base_url': 'https://bitcoinist.com'
            },
            'cryptonews': {
                'rss': 'https://cryptonews.com/news/feed/',
                'base_url': 'https://cryptonews.com'
            }
        }
        
        self.crypto_keywords = [
            'bitcoin', 'btc', 'ethereum', 'eth', 'crypto', 'cryptocurrency',
            'blockchain', 'defi', 'nft', 'altcoin', 'trading', 'market',
            'binance', 'coinbase', 'regulation', 'adoption', 'institutional'
        ]
        
        self.cache = {}
        self.cache_duration = 600  # 10 хвилин
    
    def fetch_rss_news(self, source_name: str) -> List[Dict]:
        """Отримати новини з RSS джерела"""
        if source_name not in self.news_sources:
            return []
        
        try:
            rss_url = self.news_sources[source_name]['rss']
            feed = feedparser.parse(rss_url)
            
            news_items = []
            for entry in feed.entries[:10]:  # Останні 10 новин
                # Перевіряємо чи новина актуальна (останні 24 години)
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6])
                    if datetime.now() - pub_date > timedelta(hours=24):
                        continue
                
                # Перевіряємо чи новина стосується крипто
                if self._is_crypto_related(entry.title + ' ' + entry.get('summary', '')):
                    news_item = {
                        'title': entry.title,
                        'link': entry.link,
                        'summary': entry.get('summary', ''),
                        'published': entry.get('published', ''),
                        'source': source_name
                    }
                    news_items.append(news_item)
            
            return news_items
            
        except Exception as e:
            print(f"Помилка отримання новин з {source_name}: {e}")
            return []
    
    def fetch_reddit_news(self) -> List[Dict]:
        """Отримати новини з Reddit (r/cryptocurrency, r/bitcoin)"""
        try:
            reddit_news = []
            subreddits = ['cryptocurrency', 'bitcoin', 'ethereum', 'CryptoCurrency']
            
            for subreddit in subreddits:
                url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=5"
                headers = {'User-Agent': 'CryptoBot/1.0'}
                
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    
                    for post in data['data']['children']:
                        post_data = post['data']
                        
                        # Перевіряємо чи пост актуальний
                        post_time = datetime.fromtimestamp(post_data['created_utc'])
                        if datetime.now() - post_time > timedelta(hours=12):
                            continue
                        
                        # Перевіряємо чи пост стосується крипто
                        if self._is_crypto_related(post_data['title'] + ' ' + post_data.get('selftext', '')):
                            news_item = {
                                'title': post_data['title'],
                                'link': f"https://reddit.com{post_data['permalink']}",
                                'summary': post_data.get('selftext', '')[:200] + '...' if post_data.get('selftext') else '',
                                'published': post_time.strftime('%Y-%m-%d %H:%M:%S'),
                                'source': f'reddit/{subreddit}',
                                'score': post_data.get('score', 0),
                                'comments': post_data.get('num_comments', 0)
                            }
                            reddit_news.append(news_item)
                
                time.sleep(1)  # Затримка між запитами
            
            return reddit_news
            
        except Exception as e:
            print(f"Помилка отримання новин з Reddit: {e}")
            return []
    
    def fetch_twitter_trends(self) -> List[Dict]:
        """Отримати тренди з Twitter (симуляція через API)"""
        # Це базова реалізація, в реальності потрібен Twitter API
        try:
            # Симулюємо отримання трендів
            trends = [
                {
                    'title': 'Bitcoin Price Analysis',
                    'link': 'https://twitter.com/search?q=bitcoin',
                    'summary': 'Bitcoin trending on Twitter',
                    'published': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'source': 'twitter/trends',
                    'mentions': 15000
                },
                {
                    'title': 'Ethereum Network Update',
                    'link': 'https://twitter.com/search?q=ethereum',
                    'summary': 'Ethereum network updates trending',
                    'published': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'source': 'twitter/trends',
                    'mentions': 8500
                }
            ]
            return trends
            
        except Exception as e:
            print(f"Помилка отримання трендів Twitter: {e}")
            return []
    
    def _is_crypto_related(self, text: str) -> bool:
        """Перевірити чи текст стосується криптовалют"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.crypto_keywords)
    
    def get_all_news(self) -> List[Dict]:
        """Отримати всі новини з усіх джерел"""
        all_news = []
        
        # Перевіряємо кеш
        cache_key = 'all_news'
        if cache_key in self.cache:
            cached_time, cached_news = self.cache[cache_key]
            if time.time() - cached_time < self.cache_duration:
                return cached_news
        
        # Отримуємо новини з RSS джерел
        for source in self.news_sources.keys():
            try:
                news = self.fetch_rss_news(source)
                all_news.extend(news)
                time.sleep(1)  # Затримка між запитами
            except Exception as e:
                print(f"Помилка отримання новин з {source}: {e}")
        
        # Отримуємо новини з Reddit
        try:
            reddit_news = self.fetch_reddit_news()
            all_news.extend(reddit_news)
        except Exception as e:
            print(f"Помилка отримання новин з Reddit: {e}")
        
        # Отримуємо тренди з Twitter
        try:
            twitter_trends = self.fetch_twitter_trends()
            all_news.extend(twitter_trends)
        except Exception as e:
            print(f"Помилка отримання трендів Twitter: {e}")
        
        # Сортуємо за часом публікації
        all_news.sort(key=lambda x: x.get('published', ''), reverse=True)
        
        # Кешуємо результат
        self.cache[cache_key] = (time.time(), all_news)
        
        return all_news[:20]  # Повертаємо топ 20 новин
    
    def get_news_summary(self) -> str:
        """Отримати короткий звіт про новини"""
        news = self.get_all_news()
        
        if not news:
            return "Новини не знайдено"
        
        summary = "📰 **Останні новини крипто ринку:**\n\n"
        
        for i, item in enumerate(news[:5], 1):
            title = item['title'][:100] + '...' if len(item['title']) > 100 else item['title']
            source = item['source']
            summary += f"{i}. **{title}**\n"
            summary += f"   📍 {source}\n\n"
        
        return summary
    
    def get_sentiment_analysis(self) -> Dict:
        """Простий аналіз сентименту новин"""
        news = self.get_all_news()
        
        positive_keywords = ['bullish', 'moon', 'pump', 'surge', 'rally', 'adoption', 'institutional', 'positive']
        negative_keywords = ['bearish', 'crash', 'dump', 'fall', 'decline', 'regulation', 'ban', 'negative']
        
        positive_count = 0
        negative_count = 0
        
        for item in news:
            text = (item['title'] + ' ' + item.get('summary', '')).lower()
            
            for keyword in positive_keywords:
                if keyword in text:
                    positive_count += 1
            
            for keyword in negative_keywords:
                if keyword in text:
                    negative_count += 1
        
        total = positive_count + negative_count
        if total == 0:
            sentiment = 'NEUTRAL'
            score = 0
        else:
            score = (positive_count - negative_count) / total
            if score > 0.1:
                sentiment = 'POSITIVE'
            elif score < -0.1:
                sentiment = 'NEGATIVE'
            else:
                sentiment = 'NEUTRAL'
        
        return {
            'sentiment': sentiment,
            'score': score,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'total_news': len(news)
        }
