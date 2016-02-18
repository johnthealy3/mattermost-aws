# Mattermost AWS Status Bot

This bot grabs all AWS N. Virginia (us-east-1) status updates since the last run,
up to 12 hours ago, and posts them to the specified Mattermost webhook.

### Installation

Install dependencies:
```sh
	sudo pip install feedparser BeautifulSoup
```
Set environment variables:
```sh
	export AWSBOT_WEBHOOK_URL=<URL goes here>
	export AWSBOT_USERNAME=<Username>
```
