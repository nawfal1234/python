from tkinter import *
from tkinter import messagebox
from datetime import datetime
import pytz
import requests
from awesometkinter.bidirender import add_bidi_support, render_text
import pyarabic.araby as araby
import PyQt5.QtCore

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import string
import requests
from bs4 import BeautifulSoup

import pyarabic.araby as araby
from nltk.corpus import stopwords # arabic stopwords
import arabicstopwords.arabicstopwords as stp # arabic stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.snowball import ArabicStemmer # Arabic Stemmer gets rot word
import qalsadi.lemmatizer

st = ArabicStemmer()
lemmer = qalsadi.lemmatizer.Lemmatizer()

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_colwidth', None)
sns.set()

app = Tk()

UTC = pytz.utc
app.geometry("1200x480+600+300")
app.title(f"Search word in quran")
app.resizable(False,True)
app.config(background = '#293241')

frame1 = Frame(app,height =120, width = 900,bg="#5c4ce1",bd=1,relief=FLAT)
frame1.place(x=0,y=0)

frame2 = Frame(app,height =120, width = 1200,bg='#867ae9',bd=1,relief=FLAT)
frame2.place(x=900,y=0)

frame2 = Frame(app,height =30, width = 2000,bg='black',bd=1,relief=RAISED)
frame2.place(x=0,y=120)
label_date_now = Label(text="Current Date", bg ="#5c4ce1", font = 'Verdana 12 bold')
label_date_now.place(x=20, y=40)

label_time_now = Label(text="Current Time", bg ="#5c4ce1", font = 'Verdana 12')
label_time_now.place(x=20, y=60)

label_word = Label(text="كلمة", bg ='#867ae9', font = 'Verdana 11',anchor='center')
label_word.place(x=1100, y=15)
label_search = Label(text="Search \nAvailable word", bg = '#867ae9', font = 'Verdana 8')
label_search.place(x=1780, y=70)
word_text_var = StringVar()
word_text = Entry(app,width=11,bg='#eaf2ae',fg='black',font='verdana 11',textvariable= word_text_var)
word_text.place(x=1100,y=40)
word_text['textvariable']= word_text_var

result_box_surratName = Text(app, height = 1000, width = 8, bg='#293241',fg='#ecfcff', relief=FLAT,font=('verdana 10',10))
result_box_surratName.place(x=20 , y= 152)


result_box_ayaNum = Text(app, height = 1000, width = 30, bg='#293241',fg='#ecfcff', relief=FLAT, font=('verdana 10',10))
result_box_ayaNum.place(x= 150, y= 152)

result_box_ayaTxt = Text(app, height = 3000, width = 2100, bg='#293241',fg='#ecfcff', relief=FLAT, font=('verdana 10',10))
result_box_ayaTxt.place(x= 260 , y= 152)


search_word_image = PhotoImage(file = "C:/Users/Faical Sebti/Documents/khalid cherkani projet/icons/search-icon.png")
def search_in_quran():
    print('nawfal cherkani')
    
         



label_head_result = Label(text="  الصورة إسم        \t الأية رقم \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t              الأية", bg = 'black', fg='white', font = 'Verdana 8 bold',anchor='nw')
label_head_result.place(x=10, y=125)

def update_clock():
    raw_TS = datetime.now(UTC)
    date_now = raw_TS.strftime("%d %b %Y")
    time_now = raw_TS.strftime("%H:%M:%S %p")
    label_date_now.config(text = date_now)
    label_time_now.config(text = time_now)
    label_time_now.after(1000, update_clock)

update_clock()

################### Training


df = pd.read_csv("C:/Users/Faical Sebti/Documents/khalid cherkani projet/Quran/Quran.csv")

df.info()

corpus = df["clean_txt"]
vectorizer = TfidfVectorizer(ngram_range=(1, 2))
corpus_vectorized = vectorizer.fit_transform(corpus)
print(corpus_vectorized.shape)

print(vectorizer.get_feature_names_out()[:20])
def listToString(s):
 
    # initialize an empty string
    str1 = "\b"
 
    # traverse in the string
    for i in range(len(s)):
        str1=str1+" "+s[i]
 
    # return string
    return str1
# retrieve the top_n ayah with the highest scores and show them
def show_best_results(df_quran, scores_array, top_n=20):
    sorted_indices = scores_array.argsort()[::-1]
    for position, idx in enumerate(sorted_indices[:top_n]):
           row = df_quran.iloc[idx]
           score = scores_array[idx]
           ayah = row["ayah_txt"].split(' ')
           ayah_num = row["ayah_num"]
           surah_name = row["surah_name"]
           if score > 0:
             print(ayah)
             print(f'أيه رقم {ayah_num}  سورة {surah_name}')
             print("====================================")
             result_box_surratName.insert(END,f"{surah_name}")
             result_box_surratName.insert(END,"\n")
             result_box_ayaNum.insert(END,f"{ayah_num}")
             result_box_ayaNum.insert(END,"\n")
             result_box_ayaTxt.insert(END,f"{listToString(ayah[::])}",RIGHT)
             result_box_ayaTxt.insert(END,"\n")
    result_box_ayaTxt.config(state = "disabled")
def run_tfidf(query):
    query_vectorized = vectorizer.transform([query])
    scores = query_vectorized.dot(corpus_vectorized.transpose())
    scores_array = scores.toarray()[0]
    show_best_results(df, scores_array)
search_word_button = Button(app, image=search_word_image, bg ="#5c4ce1", command = show_best_results, relief= RAISED)
search_word_button.place(x=1800,y=25)
query = word_text.get().strip()
query = "الصلاة "
run_tfidf(query)
###############################################

#text box for displaying result
app.attributes('-fullscreen', True)
app.mainloop()