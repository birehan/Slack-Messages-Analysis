import pandas as pd
import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine

# Connection parameters
connection_params = {
    "host": "localhost",
    "user": "birehan",
    "password": "password",
    "port": "5432",
    "database": "slackdbs"
}


def top_and_bottom_users_mention_count():

    conn = psycopg2.connect(**connection_params)
    cursor = conn.cursor()

    # Query to get users and their mention counts
    query = """
        SELECT u.user_id, u.real_name, COUNT(m.mentioned_user_id) as mention_count
        FROM Users u
        LEFT JOIN MessageMentions m ON u.user_id = m.mentioned_user_id
        GROUP BY u.user_id, u.real_name
        ORDER BY mention_count DESC
    """

    # Execute the query and fetch the results into a Pandas DataFrame
    df = pd.read_sql_query(query, conn)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Display the top and bottom 10 users by mention count
    top_10_users = df.head(10)
    bottom_10_users = df.tail(10)

    return top_10_users, bottom_10_users



def top_and_bottom_users_reply_count():

    conn = psycopg2.connect(**connection_params)
    cursor = conn.cursor()

    # Query to get users and their reply counts
    query = """
        SELECT u.user_id, u.real_name, COUNT(r.reply_id) as reply_count
        FROM Users u
        LEFT JOIN Replies r ON u.user_id = r.user_id
        GROUP BY u.user_id, u.real_name
        ORDER BY reply_count DESC
    """

    # Execute the query and fetch the results into a Pandas DataFrame
    df = pd.read_sql_query(query, conn)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Display the top and bottom 10 users by reply count
    top_10_users = df.head(10)
    bottom_10_users = df.tail(10)

    return top_10_users, bottom_10_users

def top_and_bottom_users_message_count():

    conn = psycopg2.connect(**connection_params)
    cursor = conn.cursor()

    # Query to get users and their message counts
    query = """
        SELECT u.user_id, u.real_name, COUNT(m.msg_id) as message_count
        FROM Users u
        LEFT JOIN Messages m ON u.user_id = m.user_id
        GROUP BY u.user_id, u.real_name
        ORDER BY message_count DESC
    """

    # Execute the query and fetch the results into a Pandas DataFrame
    df = pd.read_sql_query(query, conn)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Display the top and bottom 10 users by message count
    top_10_users = df.head(10)
    bottom_10_users = df.tail(10)

    return top_10_users, bottom_10_users

def top_and_bottom_users_reaction_count():

    conn = psycopg2.connect(**connection_params)
    cursor = conn.cursor()

    # Query to get users and their reaction counts
    query = """
        SELECT u.user_id, u.real_name, COUNT(reaction_id) as reaction_count
        FROM Users u
        JOIN ReactionUsers ru ON u.user_id = ru.user_id
        GROUP BY u.user_id, u.real_name
        ORDER BY reaction_count DESC
    """

    # Execute the query and fetch the results into a Pandas DataFrame
    df = pd.read_sql_query(query, conn)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Display the top and bottom 10 users by reaction count
    top_10_users = df.head(10)
    bottom_10_users = df.tail(10)

    return top_10_users, bottom_10_users


def top_10_messages_by_replies():

    conn = psycopg2.connect(**connection_params)
    cursor = conn.cursor()

    # Query to get messages and their reply counts
    query = """
        SELECT m.ts, m.text, COUNT(r.reply_id) as reply_count
        FROM Messages m
        LEFT JOIN Replies r ON m.ts = r.message_ts
        GROUP BY m.ts, m.text
        ORDER BY reply_count DESC
        LIMIT 10
    """

    # Execute the query and fetch the results into a Pandas DataFrame
    df = pd.read_sql_query(query, conn)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return df

def top_10_messages_by_reactions():

    conn = psycopg2.connect(**connection_params)
    cursor = conn.cursor()

    # Query to get messages and their reaction counts
    query = """
        SELECT m.ts, m.text, COUNT(r.reaction_id) as reaction_count
        FROM Messages m
        LEFT JOIN Reactions r ON m.ts = r.message_ts
        GROUP BY m.ts, m.text
        ORDER BY reaction_count DESC
        LIMIT 10
    """

    # Execute the query and fetch the results into a Pandas DataFrame
    df = pd.read_sql_query(query, conn)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return df

def top_10_messages_by_mentions():

    conn = psycopg2.connect(**connection_params)
    cursor = conn.cursor()

    # Query to get messages and their mention counts
    query = """
        SELECT m.ts, m.text, COUNT(mm.mentioned_user_id) as mention_count
        FROM Messages m
        LEFT JOIN MessageMentions mm ON m.ts = mm.message_ts
        GROUP BY m.ts, m.text
        ORDER BY mention_count DESC
        LIMIT 10
    """

    # Execute the query and fetch the results into a Pandas DataFrame
    df = pd.read_sql_query(query, conn)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return df


def get_channel_stats():
    # Create a connection to PostgreSQL
    conn = psycopg2.connect(**connection_params)
    cursor = conn.cursor()

    # Query to get channel-wise data for scatter plot
    query = """
        SELECT
            c.name AS channel_name,
            COUNT(DISTINCT m.ts) AS channel_total_messages,
            COUNT(DISTINCT r.reply_id) + COUNT(DISTINCT re.reaction_id) AS replies_reactions_sum
        FROM
            Channels c
            LEFT JOIN Messages m ON c.channel_id = m.channel_id
            LEFT JOIN Replies r ON m.ts = r.message_ts
            LEFT JOIN Reactions re ON m.ts = re.message_ts
        GROUP BY
            c.name
        ORDER BY
            channel_total_messages DESC
    """

    # Execute the query and fetch the results into a Pandas DataFrame
    df = pd.read_sql_query(query, conn)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return df


# def get_reply_time_differences():
    # # Create a connection to PostgreSQL
    # conn = psycopg2.connect(**connection_params)
    # cursor = conn.cursor()

    # # Query to get messages and their corresponding replies with Unix timestamp conversion
    # query = """
    #     SELECT
    #         m.ts AS message_ts,
    #         m.text AS message_text,
    #         m.channel_id,
    #         r.ts AS reply_ts
    #     FROM
    #         Messages m
    #         LEFT JOIN Replies r ON m.ts = r.message_ts
    #     WHERE
    #         r.ts IS NOT NULL
    #     ORDER BY
    #         m.ts
    # """

    # # Execute the query and fetch the results into a Pandas DataFrame
    # df = pd.read_sql_query(query, conn)

    # # Close the cursor and connection
    # cursor.close()
    # conn.close()

    # # Convert Unix timestamps to datetime objects
    # df['message_ts'] = pd.to_datetime(df['message_ts'], unit='s')
    # df['reply_ts'] = pd.to_datetime(df['reply_ts'], unit='s')

    # # Compute time differences
    # df['time_difference'] = (df['reply_ts'] - df['message_ts']).dt.total_seconds() / 60.0

    # # Extract the time of the day in 24hr format
    # df['time_of_day'] = df['message_ts'].dt.hour + df['message_ts'].dt.minute / 60.0

    # return df

# print(get_reply_time_differences().head())



def get_reply_time_differences():
    # Create a connection to PostgreSQL
    conn = psycopg2.connect(**connection_params)
    cursor = conn.cursor()

    # Query to get messages and their corresponding replies with Unix timestamp conversion
    query = """
        SELECT
            m.ts AS message_ts,
            m.text AS message_text,
        m.channel_id,
            c.name AS channel_name,  -- Include channel_name in the SELECT statement
            r.ts AS reply_ts
        FROM
            Messages m
            LEFT JOIN Channels c ON m.channel_id = c.channel_id  -- Join Channels table
            LEFT JOIN Replies r ON m.ts = r.message_ts
        WHERE
            r.ts IS NOT NULL
        ORDER BY
            m.ts
    """

    # Execute the query and fetch the results into a Pandas DataFrame
    df = pd.read_sql_query(query, conn)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Convert Unix timestamps to datetime objects
    df['message_ts'] = pd.to_datetime(df['message_ts'], unit='s')
    df['reply_ts'] = pd.to_datetime(df['reply_ts'], unit='s')

    # Compute time differences
    df['time_difference'] = (df['reply_ts'] - df['message_ts']).dt.total_seconds() / 60.0

    # Extract the time of the day in 24hr format
    df['time_of_day'] = df['message_ts'].dt.hour + df['message_ts'].dt.minute / 60.0

    return df
