import unittest
from src.loader import SlackDataLoader


class TestSlackDataLoader(unittest.TestCase):
    def setUp(self):
        self.loader = SlackDataLoader("data")

    def test_slack_parser_columns(self):
        # Replace 'your_path_channel' with the actual path to your test JSON files
        path_channel = "data/all-week1"
        df = self.loader.slack_parser(path_channel)

        expected_columns = [
            'msg_type', 'msg_content', 'sender_name', 'msg_sent_time', 'msg_dist_type',
            'time_thread_start', 'reply_count', 'reply_users_count', 'reply_users', 'tm_thread_end', 'channel'
        ]

        self.assertEqual(list(df.columns), expected_columns)

    def test_slack_parser_not_empty(self):
        # Replace 'your_path_channel' with the actual path to your test JSON files
        path_channel = "data/all-week1"
        df = self.loader.slack_parser(path_channel)

        self.assertFalse(df.empty)

    # Add more tests as needed...

if __name__ == '__main__':
    unittest.main()
