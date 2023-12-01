import uuid
from .loader import SlackDataLoader
from .utils import get_messages__detail_from_channel


class Helper:
    def __init__(self):
        self.loader = SlackDataLoader("../data")
        
    def get_all_users(self):
        all_users = []
        for user in self.loader.users:
            cur_user = {"user_id": user["id"], "real_name": user["real_name"]}
            all_users.append(cur_user)
        
        return all_users

    def get_all_channels(self):
        all_channels = []
        for channel in self.loader.channels:
            cur_channel = {"channel_id": channel["id"], "name": channel["name"]}
            all_channels.append(cur_channel)
        
        return all_channels

    def get_all_messages(self):
        all_messages = []
        for channel in self.loader.channels:
            channel_messages = get_messages__detail_from_channel(f"../data/{channel['name']}")
            
            formatted_messages = channel_messages.apply(lambda msg: {
                "msg_id": msg.get("msg_id") or str(uuid.uuid4()),
                "text": msg.get("text", ""),
                "cleaned_text": msg.get("cleaned_text", ""),

                "user_id": msg.get("user", ""),
                "mentions": msg.get("mentions", []) or [],
                "reactions": msg.get("reactions", []) or [],
                "replies": msg.get("replies", []) or [],
                "ts": msg.get("ts", ""),
                "channel_id": channel["id"]
            }, axis=1)

            all_messages.extend(formatted_messages.to_list())
                
        return all_messages