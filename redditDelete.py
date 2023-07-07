#!/usr/bin/env python

import praw
import time
import argparse
import csv
import yaml
from getpass import getpass

# Parse command line argument
parser = argparse.ArgumentParser(description='Edit or restore Reddit comments.')
parser.add_argument('--restore', type=str, help='CSV file to restore comments from')
args = parser.parse_args()

# Load data from YAML configuration file
with open('config.yml', 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

# Create a Reddit instance
reddit = praw.Reddit(
    client_id=cfg['client_id'],
    client_secret=cfg['client_secret'],
    password=getpass("Enter your Reddit password:"),
    user_agent="praw script to edit or restore all my comments",
    username=cfg['username'],
)

print("Reddit object created")

# If the --restore argument is provided, restore comments from the CSV file
if args.restore:
    with open(args.restore, newline='') as csvfile:
        comment_data = csv.DictReader(csvfile)
        for row in comment_data:
            comment = reddit.comment(id=row['id'])
            try:
                print("Restoring ", row)
                comment.edit(row['body'])
            except praw.exceptions.PRAWException as e:
                print(f"Could not edit comment {row['id']}: {e}")
            time.sleep(3)
else:  # Otherwise, replace all comments with the message from the YAML file
    message = cfg['message']
    for comment in reddit.user.me().comments.new(limit=None):
        print("Revising ", comment)
        comment.edit(message)
        time.sleep(3)
