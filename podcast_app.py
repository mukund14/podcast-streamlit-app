import streamlit as st
import requests
import xml.etree.ElementTree as ET

# Function to fetch the last two podcast episodes from RSS feed
def fetch_last_two_episodes(rss_url):
    response = requests.get(rss_url)
    root = ET.fromstring(response.content)
    episodes = []
    for item in root.findall('./channel/item')[:2]:
        title = item.find('title').text
        link = item.find('link').text
        pub_date = item.find('pubDate').text
        description = item.find('description').text
        episodes.append({
            'title': title,
            'link': link,
            'published': pub_date,
            'description': description
        })
    return episodes

# RSS feed URLs
jenna_rss = 'https://feeds.simplecast.com/8vqw4qK_'
amy_rss = 'https://feeds.simplecast.com/DBvwNlgY'

# Fetch the last two episodes
jenna_episodes = fetch_last_two_episodes(jenna_rss)
amy_episodes = fetch_last_two_episodes(amy_rss)

# Streamlit app
st.title("Latest Podcasts from Jenna Kutcher and Amy Porterfield")

st.header("Jenna Kutcher - [Goal Digger Podcast](https://podcasts.apple.com/us/podcast/the-goal-digger-podcast/id1178704872)")
for episode in jenna_episodes:
    st.subheader(episode['title'])
    st.write(f"Published on: {episode['published']}")
    st.write(episode['description'], unsafe_allow_html=True)
    st.markdown(f"[Listen Here]({episode['link']})", unsafe_allow_html=True)

st.header("Amy Porterfield - [Online Marketing Made Easy](https://podcasts.apple.com/us/podcast/online-marketing-made-easy-with-amy-porterfield/id594703545)")
for episode in amy_episodes:
    st.subheader(episode['title'])
    st.write(f"Published on: {episode['published']}")
    st.write(episode['description'], unsafe_allow_html=True)
    st.markdown(f"[Listen Here]({episode['link']})", unsafe_allow_html=True)
