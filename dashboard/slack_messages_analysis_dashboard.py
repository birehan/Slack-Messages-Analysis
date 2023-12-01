import os
import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

rpath = os.path.abspath('..')
if rpath not in sys.path:
    sys.path.insert(0, rpath)

# import src.data_analysis as analysis
import dashboard.analysis_queries as analysis

# st.set_page_config(page_title="Slack Data Analysis", page_icon=":tada:", layout="wide")

st.set_page_config(page_title="Slack Data Analysis", page_icon=":tada:", layout="wide", initial_sidebar_state="collapsed")

# Add a little margin to the layout
st.markdown(
    """
    <style>
        .main {
            padding: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Slack Message Analysis Dashboard")
st.text('Channel Members Analysis')



# Call the function from the notebook to get top and bottom users
top_ten_reply_users, bottom_ten_reply_users =  analysis.top_and_bottom_users_reply_count()   

container = st.container()

with container:

    top_container = st.container()

    with top_container:
        # Create two columns within the container
        top_table_col, top_chart_col = st.columns(2)

        # Display top users table in the first column
        with top_table_col:
            st.subheader("Table - Top 10 Users by Reply Count")
            st.table(top_ten_reply_users)


        with top_chart_col:
            st.subheader("Bar Chart - Top 10 Users by Reply Count")
            st.bar_chart(top_ten_reply_users.set_index("real_name")["reply_count"])

    # Container for Bottom 10 Users
    bottom_container = st.container()

    # Display bottom users table and bar chart in the same row
    with bottom_container:
        # Create two columns within the container
        bottom_table_col, bottom_chart_col = st.columns(2)

        # Display bottom users table in the first column
        with bottom_table_col:
            st.subheader("Table - Bottom 10 Users by Reply Count")
            st.table(bottom_ten_reply_users)

        # Display bar chart for bottom users in the second column
        with bottom_chart_col:
            st.subheader("Bar Chart - Bottom 10 Users by Reply Count")
            st.bar_chart(bottom_ten_reply_users.set_index("real_name")["reply_count"])



# Call the function from the notebook to get top and bottom users by mention count
top_ten_mention_users, bottom_ten_mention_users = analysis.top_and_bottom_users_mention_count()

# Container for Mention Count
mention_container = st.container()

with mention_container:
    # Create two columns within the container
    mention_table_col, mention_chart_col = st.columns(2)

    # Display top users table in the first column
    with mention_table_col:
        st.subheader("Table - Top 10 Users by Mention Count")
        st.table(top_ten_mention_users)

    # Display bar chart for top users in the second column
    with mention_chart_col:
        st.subheader("Bar Chart - Top 10 Users by Mention Count")
        st.bar_chart(top_ten_mention_users.set_index("real_name")["mention_count"])

# Container for Bottom 10 Users by Mention Count
bottom_mention_container = st.container()

# Display bottom users table and bar chart in the same row
with bottom_mention_container:
    # Create two columns within the container
    bottom_mention_table_col, bottom_mention_chart_col = st.columns(2)

    # Display bottom users table in the first column
    with bottom_mention_table_col:
        st.subheader("Table - Bottom 10 Users by Mention Count")
        st.table(bottom_ten_mention_users)

    # Display bar chart for bottom users in the second column
    with bottom_mention_chart_col:
        st.subheader("Bar Chart - Bottom 10 Users by Mention Count")
        st.bar_chart(bottom_ten_mention_users.set_index("real_name")["mention_count"])


# Call the function from the notebook to get top and bottom users by message count
top_ten_message_users, bottom_ten_message_users = analysis.top_and_bottom_users_message_count()

# Container for Message Count
message_container = st.container()

with message_container:
    # Create two columns within the container
    message_table_col, message_chart_col = st.columns(2)

    # Display top users table in the first column
    with message_table_col:
        st.subheader("Table - Top 10 Users by Message Count")
        st.table(top_ten_message_users)

    # Display bar chart for top users in the second column
    with message_chart_col:
        st.subheader("Bar Chart - Top 10 Users by Message Count")
        st.bar_chart(top_ten_message_users.set_index("real_name")["message_count"])

# Container for Bottom 10 Users by Message Count
bottom_message_container = st.container()

# Display bottom users table and bar chart in the same row
with bottom_message_container:
    # Create two columns within the container
    bottom_message_table_col, bottom_message_chart_col = st.columns(2)

    # Display bottom users table in the first column
    with bottom_message_table_col:
        st.subheader("Table - Bottom 10 Users by Message Count")
        st.table(bottom_ten_message_users)

    # Display bar chart for bottom users in the second column
    with bottom_message_chart_col:
        st.subheader("Bar Chart - Bottom 10 Users by Message Count")
        st.bar_chart(bottom_ten_message_users.set_index("real_name")["message_count"])


# Call the function to get top and bottom users by reaction count
top_ten_reaction_users, bottom_ten_reaction_users = analysis.top_and_bottom_users_reaction_count()

# Container for Reaction Count
reaction_container = st.container()

with reaction_container:
    # Create two columns within the container
    reaction_table_col, reaction_chart_col = st.columns(2)

    # Display top users table in the first column
    with reaction_table_col:
        st.subheader("Table - Top 10 Users by Reaction Count")
        st.table(top_ten_reaction_users)

    # Display bar chart for top users in the second column
    with reaction_chart_col:
        st.subheader("Bar Chart - Top 10 Users by Reaction Count")
        st.bar_chart(top_ten_reaction_users.set_index("real_name")["reaction_count"])

# Container for Bottom 10 Users by Reaction Count
bottom_reaction_container = st.container()

# Display bottom users table and bar chart in the same row
with bottom_reaction_container:
    # Create two columns within the container
    bottom_reaction_table_col, bottom_reaction_chart_col = st.columns(2)

    # Display bottom users table in the first column
    with bottom_reaction_table_col:
        st.subheader("Table - Bottom 10 Users by Reaction Count")
        st.table(bottom_ten_reaction_users)

    # Display bar chart for bottom users in the second column
    with bottom_reaction_chart_col:
        st.subheader("Bar Chart - Bottom 10 Users by Reaction Count")
        st.bar_chart(bottom_ten_reaction_users.set_index("real_name")["reaction_count"])


# Call the function to get top 10 messages by replies
top_10_messages_by_replies = analysis.top_10_messages_by_replies()

# Container for Top 10 Messages by Replies
top_messages_by_replies_container = st.container()

with top_messages_by_replies_container:
    # Create two columns within the container
    top_messages_table_col, top_messages_chart_col = st.columns(2)

    # Display top messages table in the first column
    with top_messages_table_col:
        st.subheader("Table - Top 10 Messages by Replies")
        st.table(top_10_messages_by_replies)

    # Display bar chart for top messages in the second column
    with top_messages_chart_col:
        st.subheader("Bar Chart - Top 10 Messages by Replies")
        st.bar_chart(top_10_messages_by_replies.set_index("ts")["reply_count"])


# Call the function to get top 10 messages by reactions count
top_10_messages_by_reactions = analysis.top_10_messages_by_reactions()

# Container for Top 10 Messages by Reactions
top_messages_by_reactions_container = st.container()

with top_messages_by_reactions_container:
    # Create two columns within the container
    top_messages_table_col, top_messages_chart_col = st.columns(2)

    # Display top messages table in the first column
    with top_messages_table_col:
        st.subheader("Table - Top 10 Messages by Reactions")
        st.table(top_10_messages_by_reactions)

    # Display bar chart for top messages in the second column
    with top_messages_chart_col:
        st.subheader("Bar Chart - Top 10 Messages by Reactions")
        st.bar_chart(top_10_messages_by_reactions.set_index("ts")["reaction_count"])


# Call the function to get top 10 messages by mentions
top_10_messages_by_mentions = analysis.top_10_messages_by_mentions()

# Function to limit characters in each cell
def limit_characters(cell, limit=120):
    return cell[:limit] + '...' if len(cell) > limit else cell

# Apply the character limit to the relevant columns
top_10_messages_by_mentions["text"] = top_10_messages_by_mentions["text"].apply(lambda x: limit_characters(x))

# Container for Top 10 Messages by Mentions
top_messages_by_mentions_container = st.container()

with top_messages_by_mentions_container:
    # Create two columns within the container
    top_messages_mentions_table_col, top_messages_mentions_chart_col = st.columns(2)

    # Display top messages table by mentions in the first column
    with top_messages_mentions_table_col:
        st.subheader("Table - Top 10 Messages by Mentions")
        st.table(top_10_messages_by_mentions)

    # Display bar chart for top messages by mentions in the second column
    with top_messages_mentions_chart_col:
        st.subheader("Bar Chart - Top 10 Messages by Mentions")
        st.bar_chart(top_10_messages_by_mentions.set_index("ts")["mention_count"])


# Get channel statistics
channel_stats = analysis.get_channel_stats()

# Streamlit dashboard
st.title("Channel Statistics Dashboard")

# Display scatter plot
st.subheader("Scatter Plot: Total Messages vs Replies + Reactions")
st.scatter_chart(channel_stats, x='channel_total_messages', y='replies_reactions_sum', color='channel_name')


# Determine the channel with the highest activity
most_active_channel = channel_stats.loc[channel_stats['channel_total_messages'].idxmax(), 'channel_name']
st.subheader(f"Channel with the Highest Activity: {most_active_channel}")



def plot_scatter():
    # Get reply time differences
    df = analysis.get_reply_time_differences()

    # Calculate the fraction of messages replied within the first 5 minutes
    total_messages = len(df)
    replied_within_5mins = len(df[df['time_difference'] <= 5.0])
    fraction_replied_within_5mins = replied_within_5mins / total_messages

    # Display fraction replied within 5 minutes
    st.write(f"Fraction of messages replied within the first 5 minutes: {fraction_replied_within_5mins:.2%}")

    # Create a scatter plot using Streamlit
    st.subheader("2D Scatter Plot")
    scatter_chart = st.scatter_chart(
        data=df,
        x='time_difference',
        y='time_of_day',
        color='channel_id',
    )

    return scatter_chart


st.title("Message Reply Analysis")
plot_scatter()