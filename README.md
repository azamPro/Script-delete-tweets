# 🗑️ Twitter/X Tweet Deleter (Selenium)

A Python script to automatically delete your latest tweets using Selenium and ChromeDriver.

---

## 🔧 Environment Variables

Create a `.env` file in the same directory with the following credentials:

```env
TWITTER_EMAIL=Azzam@gmail.com
TWITTER_USERNAME=AzamPro_
TWITTER_PASSWORD=AzamPass

```


## 📦 Installation

Make sure you have Python 3.9+ installed.

Install required packages:

```bash
pip install -r requirements.txt

```



## 🚀 Run the Script

To run the script:

```bash
python deleteTweets.py

```

By default, the script will:

Delete up to 100 tweets

Wait 60 seconds after every 5 tweets

Run in headless (invisible) mode

Log all actions to delete_tweet_log.txt



## ⚙️ Customization

You can edit the top of deleteTweets.py to configure:

```python
MAX_TWEETS = 100         # How many tweets to delete
SLEEP_EVERY = 5          # Pause after every N tweets
SLEEP_SECONDS = 60       # Pause duration in seconds
HEADLESS = True          # Set to False to show the browser

```



## 📄 Log File

All actions are logged in:

```bash
delete_tweet_log.txt
```

Example:

```csharp
[2025-06-10 05:01:24] Deleted tweet #3
[2025-06-10 05:01:32] Failed to delete tweet #4: TimeoutException - ...
```

## ✅ Features

- Works with the latest Twitter/X UI

- Uses login cookies to avoid logging in every time

- Headless mode supported for silent automation

- Easy to customize limits and delays


