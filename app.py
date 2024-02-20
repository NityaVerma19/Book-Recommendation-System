from flask import Flask, render_template
import pandas as pd

popular_df = pd.read_csv("popularity.csv")

app = Flask(__name__)

@app.route('/')

def index():
    return render_template("index.html",
                           book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['Total_Votes'].values),
                           ratings = list(popular_df['Average_Rating'].values))




if __name__ == '__main__':
    app.run(debug= True)


