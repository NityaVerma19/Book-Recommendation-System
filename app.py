from flask import Flask, render_template, request
import pandas as pd
import numpy as np


popular_df = pd.read_csv("pop.csv")
similarity_score = pd.read_csv("final_ss.csv")
pt = pd.read_csv("pt.csv")
books = pd.read_csv("books1.csv")
suggestions = pd.read_csv("suggestions.csv")
#index = np.where(pt.index == "Animal Farm")[0]  # fetching the index
app = Flask(__name__)

@app.route('/')

def index():
    return render_template("index.html",
                           book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['Total_Votes'].values),
                           ratings=list(popular_df['Average_Rating'].values))


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)