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

# Streamlit app
st.set_page_config(page_title="Podcast Aggregator", page_icon="🎧", layout="wide")

st.title("🎧 Latest Podcasts from NPR News Now and The Daily")
st.markdown("---")

def display_episodes(podcast_name, episodes):
    st.header(podcast_name)
    if not episodes:
        st.write("No episodes found.")
    else:
        for episode in episodes:
            st.subheader(episode['title'])
            st.write(f"Published on: {episode['published']}")
            st.write(episode['description'], unsafe_allow_html=True)
            st.markdown(f"[Listen Here]({episode['link']})", unsafe_allow_html=True)
            st.markdown("---")

# Display episodes
col1, col2 = st.columns(2)

with col1:
    display_episodes("NPR News Now", npr_episodes)

with col2:
    display_episodes("The Daily", daily_episodes)
