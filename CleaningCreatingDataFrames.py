import pandas as pd
import requests
import re
import emoji


def main():
    df = pd.read_csv(r'dialect_dataset.csv')
    url = "https://recruitment.aimtechnologies.co/ai-tasks"
    tweets = []
    stop = df.shape[0]-196

    for row in range(1000, stop, 1000):
        data = list(df.iloc[row-1000:row]['id'].map(str))
        print("id", data)
        tweet = requests.post(url, json=data)
        emojiHandlesRemoved = removeEmojisAndHandles(tweet.json())
        tweets.extend(emojiHandlesRemoved)
        print(emojiHandlesRemoved)

    # finish last 197 rows
    data = list(df.iloc[458001:458198]['id'].map(str))
    print("id", data)
    tweet = requests.post(url, json=data)
    emojiHandlesRemoved = removeEmojisAndHandles(tweet.json())
    tweets.extend(emojiHandlesRemoved)

    # save result to CSV
    df.insert(1, "tweet", tweets, True)
    df.to_csv(r'tweet_dialect_dataset.csv')

    df


def removeEmojisAndHandles(tweets):
    removeEmojiTweets = []
    pairs = tweets.items()
    for key, value in pairs:
        emojiRemoved = emoji.get_emoji_regexp().sub(u'', value)
        handleRemoved = re.sub('@[^\s]+', '', emojiRemoved)
        hashTagRemoved = re.sub("#[A-Za-z0-9_]+", "", handleRemoved)
        linksRemoved = re.sub(r'http\S+', '', hashTagRemoved)
        puncRemoved = re.sub('[()!?]', ' ', linksRemoved)
        puncRemoved = re.sub('\[.*?\]', ' ', puncRemoved)
        removeEmojiTweets.append(puncRemoved)
    return removeEmojiTweets


if __name__ == '__main__':
    main()
