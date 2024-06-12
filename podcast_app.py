import streamlit as st
import requests
import xml.etree.ElementTree as ET

# Function to fetch the last two podcast episodes from RSS feed
def fetch_last_two_episodes(rss_url):
    response = requests.get(rss_url)
    if response.status_code != 200:
        st.error(f"Failed to fetch data from {rss_url}")
        return []
    
    root = ET.fromstring(response.content)
    episodes = []
    for item in root.findall('./channel/item')[:2]:
        title = item.find('title').text if item.find('title') is not None else 'No title'
        link = item.find('link').text if item.find('link') is not None else 'No link'
        pub_date = item.find('pubDate').text if item.find('pubDate') is not None else 'No publication date'
        description = item.find('description').text if item.find('description') is not None else 'No description'
        episodes.append({
            'title': title,
            'link': link,
            'published': pub_date,
            'description': description
        })
    return episodes

# RSS feed URLs
npr_rss = 'https://feeds.npr.org/500005/podcast.xml'
daily_rss = 'https://feeds.simplecast.com/54nAGcIl'

# Fetch the last two episodes
npr_episodes = fetch_last_two_episodes(npr_rss)
daily_episodes = fetch_last_two_episodes(daily_rss)

# Debugging information
st.write("NPR episodes fetched:", npr_episodes)
st.write("The Daily episodes fetched:", daily_episodes)

# Streamlit app
st.title("Latest Podcasts from NPR News Now and The Daily")

st.header("NPR News Now")
if not npr_episodes:
    st.write("No episodes found.")
else:
    for episode in npr_episodes:
        st.subheader(episode['title'])
        st.write(f"Published on: {episode['published']}")
        st.write(episode['description'], unsafe_allow_html=True)
        st.markdown(f"[Listen Here]({episode['link']})", unsafe_allow_html=True)

st.header("The Daily")
if not daily_episodes:
    st.write("No episodes found.")
else:
    for episode in daily_episodes:
        st.subheader(episode['title'])
        st.write(f"Published on: {episode['published']}")
        st.write(episode['description'], unsafe_allow_html=True)
        st.markdown(f"[Listen Here]({episode['link']})", unsafe_allow_html=True)
