import pandas as pd
import requests
import re
import emoji
from pyarabic.araby import tokenize, is_arabicrange, strip_tashkeel, strip_tatweel, strip_diacritics, is_arabicword
import string


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
    data = list(df.iloc[458000:458198]['id'].map(str))
    print("id", data)
    tweet = requests.post(url, json=data)
    emojiHandlesRemoved = removeEmojisAndHandles(tweet.json())
    tweets.extend(emojiHandlesRemoved)

    # save result to CSV
    df.insert(1, "tweet", tweets, True)
    df.to_csv(r'tweet_dialect_dataset.csv')


def test():
    result = removeEmojisAndHandles({"3920270598136":"?.فلم DHOOM:3 ههههههه  ؟لما خلص الفلم ما عرفت شو قول فلم بايخ وفاشل ولا فلم رائع لكن اللي متأكد منوا ان الممثل #عامر_خان.. ادا الدور بشكل اكثر هههه  ، من رائع",
                            "392027059813646400":"#ياااحرية   بسام سليمان بكار مواليد 1978 _ حمص تير معلة اعتقلوه العفاريت الزرق بتاريخ  ؟ 18/5/2013 من حاجز"})


def remove_punctuations(text):
    arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
    english_punctuations = string.punctuation
    punctuations_list = arabic_punctuations + english_punctuations
    translator = str.maketrans('', '', punctuations_list)
    return text.translate(translator)


def removeEmojisAndHandles(tweets):
    cleanTweets = []
    pairs = tweets.items()
    for key, value in pairs:
        emojiRemoved = emoji.get_emoji_regexp().sub(u'', value)
        handleRemoved = re.sub('@[^\s]+', '', emojiRemoved)
        hashTagRemoved = re.sub("#[A-Za-z0-9_]+", "", handleRemoved)
        linksRemoved = re.sub(r'http\S+', '', hashTagRemoved)
        removeLaughs = re.sub("\sه*\s", '', linksRemoved)
        newLineRemoved = removeLaughs.replace('|', ' ')
        newLineRemoved = newLineRemoved.replace('\n', ' ')
        puncRemoved = remove_punctuations(newLineRemoved)
        trimTweet = puncRemoved.strip()
        nonArabicTextRemoved = ' '.join(tokenize(trimTweet, conditions=[is_arabicrange, is_arabicword], morphs=[strip_tashkeel, strip_tatweel]))
        removeTatweel = strip_tatweel(nonArabicTextRemoved)
        removedDiacritics = strip_diacritics(removeTatweel)
        print("after", removedDiacritics)
        cleanTweets.append(removedDiacritics)
    return cleanTweets


if __name__ == '__main__':
    main()
