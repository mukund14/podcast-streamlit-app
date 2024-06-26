import streamlit as st
import requests
import xml.etree.ElementTree as ET

# Function to fetch the last two podcast episodes from RSS feed
def fetch_last_two_episodes(rss_url):
    try:
        response = requests.get(rss_url)
        response.raise_for_status()
        content_type = response.headers.get('Content-Type', '').lower()
        if 'xml' not in content_type:
            st.error(f"Invalid content type: {content_type} for URL: {rss_url}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch data from {rss_url}")
        st.error(str(e))
        return []
    
    try:
        root = ET.fromstring(response.content)
    except ET.ParseError as e:
        st.error(f"Failed to parse XML from {rss_url}")
        st.error(str(e))
        return []

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

# RSS feed URLs with reliable alternatives
podcasts = {
    'Productivity': [
        {'name': 'The Tony Robbins Podcast', 'rss': 'https://tonyrobbins.libsyn.com/rss'},
        {'name': 'Beyond the To-Do List - Productivity for Work & Life', 'rss': 'https://feeds.beyondthetodolist.com/beyondthetodolist'}
    ],
    'Finance': [
        {'name': 'Planet Money', 'rss': 'https://feeds.npr.org/510289/podcast.xml'},
        {'name': 'Freakonomics Radio', 'rss': 'https://feeds.megaphone.fm/ADL9840290619'}
    ],
    'Data Science': [
        {'name': 'Data Skeptic', 'rss': 'https://dataskeptic.com/feed.rss'},
        {'name': 'Not So Standard Deviations', 'rss': 'https://feeds.simplecast.com/tOjNXec5'}
    ]
}

# Streamlit app
st.set_page_config(page_title="Podcast Dashboard", page_icon="🎧", layout="wide")

st.title("🎧 Podcast Dashboard on Productivity, Finance, and Data Science")
st.markdown("---")

# Function to display episodes
def display_episodes(podcast_name, episodes):
    st.subheader(podcast_name)
    if not episodes:
        st.write("No episodes found.")
    else:
        for episode in episodes:
            st.markdown(f"**{episode['title']}**")
            st.write(f"Published on: {episode['published']}")
            st.write(episode['description'] if episode['description'] else "No description available", unsafe_allow_html=True)
            st.markdown(f"[Listen Here]({episode['link']})", unsafe_allow_html=True)
            st.markdown("---")

# Display podcast sections
for category, feeds in podcasts.items():
    st.header(category)
    col1, col2 = st.columns(2)
    
    for i, feed in enumerate(feeds):
        episodes = fetch_last_two_episodes(feed['rss'])
        with col1 if i % 2 == 0 else col2:
            display_episodes(feed['name'], episodes)
