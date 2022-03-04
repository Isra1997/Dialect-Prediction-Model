import pandas as pd
import requests
import re


def main():
    df = pd.read_csv(r'dialect_dataset.csv')
    url = "https://recruitment.aimtechnologies.co/ai-tasks"
    tweets = []
    test_df = df.iloc[0:10]
    stop = df.shape[0]-197

    for row in range(1000, stop+1, 1000):
        data = list(df.iloc[row-1000:row]['id'].map(str))
        print("id", data)
        tweet = requests.post(url, json=data)
        emojiHandlesRemoved = removeEmojiAndHandles(tweet.json())
        tweets.extend(emojiHandlesRemoved)
        print(emojiHandlesRemoved)

    test_df.insert(2, "tweet", tweets, True)
    test_df.to_csv(r'tweet_dialect_dataset.csv')

    print(test_df)


def removeEmojiAndHandles(tweets):
    removeEmojiTweets = []
    pairs = tweets.items()
    for key, value in pairs:
        regrex_pattern = re.compile(pattern="["
                                            u"\U0001F600-\U0001F64F"  # emoticons
                                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                            "]+", flags=re.UNICODE)
        emojiRemoved = regrex_pattern.sub(r'', value)
        removeEmojiTweets.append(re.sub('@[^\s]+', '', emojiRemoved))
    return removeEmojiTweets


if __name__ == '__main__':
    main()
