import pandas as pd
import os
from random import choice
from flask import Flask, render_template, request, redirect

app = Flask(__name__, static_url_path='/static')

# Charger le fichier CSV
df = pd.read_csv(
        os.path.join('train.csv', 'train_200.csv')
    )
comments = df['texte'].tolist() 
random_comment = choice(comments) 
    
@app.route('/')
def index():
    return render_template('index.html', comment=random_comment)

@app.route('/submit', methods=['POST'])
def submit():
    comment_row = df.iloc[df[df['texte'] == random_comment].index, 2:]

    comment_row_html = comment_row.to_html(index=False)
    
    toxique = request.form.get('toxic')
    insulte = request.form.get('insult')
    obscene = request.form.get('obscene')
    menace = request.form.get('threatening')
    
    toxique = 1 if toxique == 'yes' else 0
    insulte = 1 if insulte == 'yes' else 0
    obscene = 1 if obscene == 'yes' else 0
    menace = 1 if menace == 'yes' else 0
    
    correct_toxic = comment_row['toxique'].values[0]
    correct_obscene = comment_row['obscene'].values[0]
    correct_threatening = comment_row['menace'].values[0]
    correct_insult = comment_row['insulte'].values[0]

    is_toxic_correct = toxique == correct_toxic
    is_obscene_correct = obscene == correct_obscene
    is_threatening_correct = menace == correct_threatening
    is_insult_correct = insulte == correct_insult

    return render_template('index.html', 
                           toxique=toxique,
                           insulte=insulte,
                           obscene=obscene,
                           menace=menace,
                           is_toxic_correct=is_toxic_correct, 
                           is_insult_correct=is_insult_correct,
                           is_obscene_correct=is_obscene_correct,
                           is_threatening_correct=is_threatening_correct,
                           comment_row_html=comment_row_html)

@app.route('/replay', methods=['GET'])
def replay():
    random_comment = choice(comments)
    return render_template('index.html', comment=random_comment)

@app.route('/generate_new_comment', methods=['POST'])
def generate_new_comment():
    global random_comment
    random_comment = choice(comments)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

