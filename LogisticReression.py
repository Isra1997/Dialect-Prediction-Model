from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd


def main():
    data = pd.read_csv(r"tweet_dialect_dataset.csv")
    feature = data['tweet'].values.astype('U')
    target = data['dialect'].values.astype('U')
    X_train, X_text, Y_train, Y_test = train_test_split(feature, target, test_size=.2, random_state=100)

    pipe = make_pipeline(TfidfVectorizer(), LogisticRegression())
    param_grid = {'logisticregression__C' : [0.01, 0.1, 1, 10, 100]}

    model = GridSearchCV(pipe, param_grid, cv=5)
    model.fit(X_train, Y_train)

    prediction = model.predict(X_text)
    print(f"Accuracy Score is {accuracy_score(Y_test,prediction):.2f}")
    print(classification_report(Y_test,prediction))


if __name__ == '__main__':
    main()
