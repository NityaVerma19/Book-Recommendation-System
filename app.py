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

def home():
    return render_template("index.html",
                           book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['Total_Votes'].values),
                           ratings=list(popular_df['Average_Rating'].values))


@app.route('/recommend')
def recommend_ui():
    return render_template('recommendations.html')

def recommend(book_name):
    try:
        # fetch index
        index = np.where(pt.index == book_name)[0][0]
        similar_items = sorted(list(enumerate(similarity_score[0])), key=lambda x: x[1], reverse=True)[
                        1:5]  # sorting based on the similarity score
        print(similar_items)

        data = []
        for i in similar_items:
            items = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            items.extend(temp_df.drop_duplicates('Book-Title')['Book-Title'].values)
            items.extend(temp_df.drop_duplicates('Book-Title')['Book-Author'].values)
            items.extend(temp_df.drop_duplicates('Book-Title')['Book-Title'].values)

            data.append(items)
        return data

    except IndexError:
        # Handle the case where the book name is not found in the index
        return ["Book not found in the dataset"]

book_recommendations = recommend("The Notebook")
print("Recommendations:", book_recommendations)

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    if request.method == 'POST':
        book_name = request.form['book_name']
        recommendations = recommend(book_name)
        return render_template('recommendations.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)

