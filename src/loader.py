import argparse
import copy
import glob
import io
import json
import os
import shutil
from datetime import datetime
from time import sleep

import pandas as pd

# from pick import pick


# Create wrapper classes for using slack_sdk in place of slacker
class SlackDataLoader:
    '''
    Slack exported data IO class.

    When you open slack exported ZIP file, each channel or direct message 
    will have its own folder. Each folder will contain messages from the 

    conversation, organised by date in separate JSON files.

    You'll see reference files for different kinds of conversations: 
    users.json files for all types of users that exist in the slack workspace
    channels.json files for public channels, 
    
    These files contain metadata about the conversations, including their names and IDs.

    For secruity reason, we have annonymized names - the names you will see are generated using faker library.
    
    '''
    def __init__(self, path):
        '''
        path: path to the slack exported data folder
        '''
        self.path = path
        self.channels = self.get_channels()
        self.users = self.get_users()
    

    def get_users(self):
        '''
        write a function to get all the users from the json file
        '''
        with open(os.path.join(self.path, 'users.json'), 'r') as f:
            users = json.load(f)

        return users
    
    def get_channels(self):
        '''
        write a function to get all the channels from the json file
        '''
        with open(os.path.join(self.path, 'channels.json'), 'r') as f:
            channels = json.load(f)

        return channels

    def get_channel_messages(self, channel_name):
        
        '''
        write a function to get all the messages from a channel
        
        '''

        messages = []
        base_path = "../data/" + channel_name

        json_files = [
        f"{base_path}/{pos_json}" 
        for pos_json in os.listdir(base_path) 
        if pos_json.endswith('.json')
        ]    

        combined = []

        for json_file in json_files:
            with open(json_file, 'r', encoding="utf8") as slack_data:
                json_content = json.load(slack_data)
            combined.extend(json_content)
        


        for msg in combined:
            if "subtype" not in msg:
                text = msg.get("text", None)
                ts = msg.get("ts", None)

                messages.append((text, ts))
                
        return messages

    

    def get_all_channels_messages(self):
        messages = []
        for channel in self.channels:
            base_path = "../data/" + channel["name"]

            json_files = [
            f"{base_path}/{pos_json}" 
            for pos_json in os.listdir(base_path) 
            if pos_json.endswith('.json')
            ]    

            combined = []

            for json_file in json_files:
                with open(json_file, 'r', encoding="utf8") as slack_data:
                    json_content = json.load(slack_data)
                combined.extend(json_content)
            


            for msg in combined:
                if "subtype" not in msg:
                    text = msg.get("text", None)
                    ts = msg.get("ts", None)

                    messages.append((text, ts))
            
        
        return messages
            

    def get_user_map(self):
        '''
        write a function to get a map between user id and user name
        '''
        userNamesById = {}
        userIdsByName = {}
        for user in self.users:
            userNamesById[user['id']] = user['name']
            userIdsByName[user['name']] = user['id']
        return userNamesById, userIdsByName

    
     # combine all json file in all-weeks8-9
    def slack_parser(self, path_channel):
        """ parse slack data to extract useful informations from the json file
            step of execution
            1. Import the required modules
            2. read all json file from the provided path
            3. combine all json files in the provided path
            4. extract all required informations from the slack data
            5. convert to dataframe and merge all
            6. reset the index and return dataframe
        """

        # specify path to get json files

        
        json_files = [f"{path_channel}/{pos_json}" for pos_json in os.listdir(path_channel) if pos_json.endswith('.json')]
        combined = []

        for json_file in json_files:
            with open(json_file, 'r', encoding="utf8") as slack_data:
                json_content = json.load(slack_data)
                combined.append(json_content)
        


        # loop through all json files and extract required informations
        dflist = []

        for slack_data in combined:
          
            msg_type, msg_content, sender_id, time_msg, msg_dist, time_thread_st, reply_users, \
            reply_count, reply_users_count, tm_thread_end = [],[],[],[],[],[],[],[],[],[]
            
            for row in slack_data:
                if 'bot_id' in row.keys():
                    continue
                else:
                    msg_type.append(row['type'])
                    msg_content.append(row['text'])
                    if 'user_profile' in row.keys(): sender_id.append(row['user_profile']['real_name'])
                    else: sender_id.append('Not provided')
                    time_msg.append(row['ts'])
                    if 'blocks' in row.keys() and len(row['blocks'][0]['elements'][0]['elements']) != 0 :
                        msg_dist.append(row['blocks'][0]['elements'][0]['elements'][0]['type'])
                    else: msg_dist.append('reshared')
                    if 'thread_ts' in row.keys():
                        time_thread_st.append(row['thread_ts'])
                    else:
                        time_thread_st.append(0)
                    if 'reply_users' in row.keys():
                        reply_users.append(",".join(row['reply_users']))                        
                    else:    
                        reply_users.append(0)
                    if 'reply_count' in row.keys():

                        reply_count.append(row['reply_count'])
                        reply_users_count.append(row['reply_users_count'])
                        tm_thread_end.append(row['latest_reply'])
                    else:
                        reply_count.append(0)
                        reply_users_count.append(0)
                        tm_thread_end.append(0)
            

            data = zip(msg_type, msg_content, sender_id, time_msg, msg_dist, time_thread_st,
            reply_count, reply_users_count, reply_users, tm_thread_end)
            columns = ['msg_type', 'msg_content', 'sender_name', 'msg_sent_time', 'msg_dist_type',
            'time_thread_start', 'reply_count', 'reply_users_count', 'reply_users', 'tm_thread_end']

            df = pd.DataFrame(data=data, columns=columns)
            df = df[df['sender_name'] != 'Not provided']
            dflist.append(df)
        


        dfall = pd.concat(dflist, ignore_index=True)
        dfall['channel'] = path_channel.split('/')[-1].split('.')[0]        
        dfall = dfall.reset_index(drop=True)
        
        return dfall


    def parse_slack_reaction(self, path, channel):
        """get reactions"""
        dfall_reaction = pd.DataFrame()
        combined = []

        json_files = [f"{path}/{pos_json}" for pos_json in os.listdir(path) if pos_json.endswith('.json')]
        combined = []

        for json_file in json_files:
            with open(json_file, 'r', encoding="utf8") as slack_data:
                json_content = json.load(slack_data)
                combined.append(json_content)
    



        reaction_name, reaction_count, reaction_users, msg, user_id = [], [], [], [], []

        for slack_data in combined:            
            for i_count, i in enumerate(slack_data):
                if 'reactions' in i.keys():
                    for j in range(len(i['reactions'])):
                        msg.append(i['text'])
                        user_id.append(i['user'])
                        reaction_name.append(i['reactions'][j]['name'])
                        reaction_count.append(i['reactions'][j]['count'])
                        reaction_users.append(",".join(i['reactions'][j]['users']))
                    
        data_reaction = zip(reaction_name, reaction_count, reaction_users, msg, user_id)
        columns_reaction = ['reaction_name', 'reaction_count', 'reaction_users_count', 'message', 'user_id']
        df_reaction = pd.DataFrame(data=data_reaction, columns=columns_reaction)
        df_reaction['channel'] = channel
        return df_reaction

    def get_community_participation(self, path):
        """ specify path to get json files"""

        json_files = [f"{path}/{pos_json}" for pos_json in os.listdir(path) if pos_json.endswith('.json')]
        combined = []

        for json_file in json_files:
            with open(json_file, 'r', encoding="utf8") as slack_data:
                json_content = json.load(slack_data)
                combined.append(json_content)
        

        combined = []
        comm_dict = {}
     
        # print(f"Total json files is {len(combined)}")
        for a in combined:
            for msg in a:
                if 'replies' in msg.keys():
                    for i in msg['replies']:
                        comm_dict[i['user']] = comm_dict.get(i['user'], 0)+1
        return comm_dict





if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='Export Slack history')
    # parser.add_argument('--zip', help="Name of a zip file to import")
    # args = parser.parse_args()
    pass
