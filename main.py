import streamlit as st
import requests
from datetime import datetime, timedelta

NEWS_API_KEY = 'f3bb4ac82fd24206915af669fe8be001'
NEWS_API_URL = 'https://newsapi.org/v2/everything'

def fetch_external_news(date, genre):
    try:
        params = {
            'from': date,
            'to': date,
            'sortBy': 'publishedAt',
            'language': 'en',
            'apiKey': NEWS_API_KEY,
            'domains': 'timesofindia.indiatimes.com,indiatoday.in,thehindu.com,ndtv.com,bbc.com,cnn.com,reuters.com,forbes.com,theguardian.com,nytimes.com,washingtonpost.com,aljazeera.com,huffpost.com,buzzfeed.com,usatoday.com,nbcnews.com,abcnews.go.com,bloomberg.com,businessinsider.com,marketwatch.com,wsj.com,theverge.com,techcrunch.com,cnbc.com,thetimes.co.uk,theeconomicstimes.indiatimes.com,livemint.com,thewire.in,hindustantimes.com,deccanherald.com,firstpost.com,tribuneindia.com,newindianexpress.com,business-standard.com,dailyexcelsior.com,outlookindia.com,pressinformationbureau.gov.in,financialexpress.com,mintlounge.in,vogue.in,elle.in,harpersbazaarindia.com,gqindia.com,sports.ndtv.com,cricbuzz.com,espncricinfo.com,filmfare.com,bollywoodhungama.com,scoopwhoop.com,manoramaonline.com',
            'pageSize': 100
        }

        if genre != 'all':
            params['q'] = genre

        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        articles = response.json().get('articles', [])

        summaries = []
        for article in articles:
            summary = summarize_article(article.get('description', '') or article.get('content', ''))
            summaries.append({
                'title': article['title'],
                'summary': summary,
                'url': article['url'],
                'publishedAt': article['publishedAt']
            })

        # Sort summaries by date
        summaries.sort(key=lambda x: x['publishedAt'], reverse=True)

        return summaries
    except Exception as e:
        print(f"Error fetching external news: {e}")
        return []

def summarize_article(text):
    if not text:
        return "No summary available."
    words = text.split()
    return ' '.join(words[:100])

def main():
    st.set_page_config(layout="wide")

    st.title('Newsbot')

    max_date = datetime.today().strftime('%Y-%m-%d')
    min_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')

    date = st.date_input('Choose a date', value=datetime.today(), min_value=datetime.today() - timedelta(days=30), max_value=datetime.today())
    genre = st.selectbox('Choose a genre', ['all', 'technology', 'sports', 'business', 'entertainment', 'health', 'science', 'general', 'fashion'])

    if st.button('Submit'):
        summaries = fetch_external_news(date.strftime('%Y-%m-%d'), genre)

        if summaries:
            cols_per_row = 4  # Number of columns per row
            rows = len(summaries) // cols_per_row + int(len(summaries) % cols_per_row > 0)
            for row in range(rows):
                cols = st.columns(cols_per_row)
                for col_idx in range(cols_per_row):
                    idx = row * cols_per_row + col_idx
                    if idx < len(summaries):
                        with cols[col_idx]:
                            st.markdown(f"""
                            <div style="background-color: #fff; padding: 15px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                                <h2 style="font-size: 18px; margin-bottom: 10px; color: #333;">{summaries[idx]['title']}</h2>
                                <p style="font-size: 14px; color: #666; margin-bottom: 10px;">{summaries[idx]['summary']}</p>
                                <a href="{summaries[idx]['url']}" target="_blank" style="color: #007bff; text-decoration: none; font-weight: bold;">Read more</a>
                            </div>
                            """, unsafe_allow_html=True)
        else:
            st.write("No articles found for the selected date and genre.")

if __name__ == '__main__':
    main()
