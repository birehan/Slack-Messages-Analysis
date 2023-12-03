import streamlit as st
import subprocess

# Run the pip install command
subprocess.run(["pip", "install", "psycopg2-binary"])

import analysis_queries as analysis


# Add a little margin to the layout
st.markdown(
    """
    <style>
        .main {
            padding: 20px;
        }
        .sidebar {
            padding: 10px;
            background-color: #f4f4f4;
            border-right: 1px solid #d3d3d3;
        }
        .sidebar-item {
            margin-bottom: 10px;
        }
        .st-emotion-cache-13ejsyy{
             width: 100%;
          }
    </style>
    """,
    unsafe_allow_html=True,
)

# Define the sections of your dashboard
sections = ["Top 10 Users by Reply Count", "Bottom 10 Users by Reply Count",
            "Top 10 Users by Mention Count", "Bottom 10 Users by Mention Count",
            "Top 10 Users by Message Count", "Bottom 10 Users by Message Count",
            "Top 10 Users by Reaction Count", "Bottom 10 Users by Reaction Count",
            "Top 10 Messages by Reply Count", "Top 10 Messages by Mention Count",
            "Top 10 Messages by Reaction Count", "Channel Statistics", "Message Reply Analysis"]

# Sidebar menu as buttons
st.sidebar.header("User Engagement Analysis")
button1 = st.sidebar.button("Top 10 Users by Reply Count")
button2 = st.sidebar.button("Bottom 10 Users by Reply Count")
button3 = st.sidebar.button("Top 10 Users by Mention Count")
button4 = st.sidebar.button("Bottom 10 Users by Mention Count")
button5 = st.sidebar.button("Top 10 Users by Message Count")
button6 = st.sidebar.button("Bottom 10 Users by Message Count")
button7 = st.sidebar.button("Top 10 Users by Reaction Count")
button8 = st.sidebar.button("Bottom 10 Users by Reaction Count")
st.sidebar.header("Message Analysis")
button9 = st.sidebar.button("Top 10 Messages by Reply Count")
button10 = st.sidebar.button("Top 10 Messages by Mention Count")
button11 = st.sidebar.button("Top 10 Messages by Reaction Count")

st.sidebar.header("Channel Activity Analysis")
button12 = st.sidebar.button("Channel Statistics")

st.sidebar.header("Message Replies Time Analysis")
button13 = st.sidebar.button("Message Reply Analysis")

# Main content
st.title("Slack Message Analysis Dashboard")
st.text("Explore various metrics and statistics on messages and user engagement")


# Call the function from the notebook to get top and bottom users by reply count
top_ten_reply_users, bottom_ten_reply_users = analysis.top_and_bottom_users_reply_count()

# Call the function from the notebook to get top and bottom users by mention count
top_ten_mention_users, bottom_ten_mention_users = analysis.top_and_bottom_users_mention_count()

# Call the function from the notebook to get top and bottom users by message count
top_ten_message_users, bottom_ten_message_users = analysis.top_and_bottom_users_message_count()

# Call the function from the notebook to get top and bottom users by reaction count
top_ten_reaction_users, bottom_ten_reaction_users = analysis.top_and_bottom_users_reaction_count()

# Call the function from the notebook to get top messages by reply count, mention count, and reaction count
top_messages_by_reply_count= analysis.top_10_messages_by_replies()
top_messages_by_mention_count= analysis.top_10_messages_by_mentions()
top_messages_by_reaction_count = analysis.top_10_messages_by_reactions()

table = st.container()
bar = st.container()


# Function to generate content based on the selected button
def generate_content(selected_button, count_col, users):
    with table:
        # Display top users table in the first column
        st.subheader(f"Table - {selected_button}")
        st.table(users)

    with bar:
        st.subheader(f"Bar Chart - {selected_button}")
        st.bar_chart(users.set_index("real_name")[count_col])

# Function to generate content for top messages
def generate_top_messages_content(selected_button, messages):
    with table:
        # Display top messages table
        st.subheader(f"Table - {selected_button}")
        st.table(messages)

# Function to generate content for channel statistics
def generate_channel_statistics():
    # Get channel statistics
    channel_stats = analysis.get_channel_stats()

    # Display scatter plot
    st.subheader("Scatter Plot: Total Messages vs Replies + Reactions")
    st.scatter_chart(channel_stats, x='channel_total_messages', y='replies_reactions_sum', color='channel_name')

    # Determine the channel with the highest activity
    most_active_channel = channel_stats.loc[channel_stats['channel_total_messages'].idxmax(), 'channel_name']
    st.subheader(f"Channel with the Highest Activity: {most_active_channel}")

# Function to generate content for message reply analysis
def generate_message_reply_analysis():
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
        color='channel_name',
    )

    return scatter_chart





# Display content based on the selected button
if button1:
    generate_content("Top 10 Users by Reply Count", "reply_count", top_ten_reply_users)

elif button2:
    generate_content("Bottom 10 Users by Reply Count", "reply_count", bottom_ten_reply_users)

elif button3:
    generate_content("Top 10 Users by Mention Count", "mention_count", top_ten_mention_users)

elif button4:
    generate_content("Bottom 10 Users by Mention Count", "mention_count", bottom_ten_mention_users)

elif button5:
    generate_content("Top 10 Users by Message Count", "message_count", top_ten_message_users)

elif button6:
    generate_content("Bottom 10 Users by Message Count", "message_count", bottom_ten_message_users)

elif button7:
    generate_content("Top 10 Users by Reaction Count", "reaction_count", top_ten_reaction_users)

elif button8:
    generate_content("Bottom 10 Users by Reaction Count", "reaction_count", bottom_ten_reaction_users)

elif button9:
    generate_top_messages_content("Top 10 Messages by Reply Count", top_messages_by_reply_count)

elif button10:
    generate_top_messages_content("Top 10 Messages by Mention Count", top_messages_by_mention_count)

elif button11:
    generate_top_messages_content("Top 10 Messages by Reaction Count", top_messages_by_reaction_count)

elif button12:
    generate_channel_statistics()

elif button13:
    generate_message_reply_analysis()
else:
    generate_content("Top 10 Users by Reply Count", "reply_count", top_ten_reply_users)



