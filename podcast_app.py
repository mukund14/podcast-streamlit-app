# RSS feed URLs with reliable alternatives
podcasts = {
    'Productivity': [
        {'name': 'The Tony Robbins Podcast', 'rss': 'https://tonyrobbins.libsyn.com/rss'},
        {'name': 'The Tim Ferriss Show', 'rss': 'https://tim.blog/feed/podcast/'}
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
