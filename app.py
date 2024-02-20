from flask import Flask, render_template, request
import pandas as pd
import numpy as np

popular_df = pd.read_csv("pop.csv")
similarity_score = pd.read_csv("similarity_score.csv")
pt = np.loadtxt("pt.csv")
books = pd.read_csv("books1.csv")



app = Flask(__name__)

@app.route('/')

def index():
    return render_template("index.html",
                           book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['Total_Votes'].values),
                           ratings=list(popular_df['Average_Rating'].values))


@app.route('/recommend_books',methods = ['POST'])

def recommend():
    user_input = request.form.get(user_input)
    return user_input


@app.route('/recommend')

def rec():
    return render_template("recommend.html")





if __name__ == '__main__':
    app.run(debug= True)


