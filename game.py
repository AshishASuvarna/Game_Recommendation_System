import pandas as pd
                                  
df=pd.read_csv("C:/Users/lenovo/Desktop/recommendation/Video_Games.csv")
df.columns
features=['Platform','Genre','Publisher','Developer']

df=df.rename_axis('Index').reset_index()

for feature in features:
    df[feature] = df[feature].fillna('')
    
def combine_features(row):
    try:
        return row['Platform']+" "+row['Genre']+" "+row['Publisher']+" "+row['Developer']
    except:
        print ("Error:", row)
        
df["combined_features"] = df.apply(combine_features,axis=1)

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
cv = CountVectorizer()
count_matrix = cv.fit_transform(df["combined_features"])

cosine_sim = cosine_similarity(count_matrix)
cosine_sim.shape

df.head()

def get_title_from_index(index):
    return df[df.Index == index]["Name"].values[0]

def get_index_from_title(name):
    return df[df.Name == name]["Index"].values[0]

from tkinter import *
from tkinter import ttk
from hdpitkinter import HdpiTk

def show_game():
    game_user_likes = e1.get() 
    game_index = get_index_from_title(game_user_likes)
            
                    
    i=int(game_index)
    Similar_games = list( enumerate(cosine_sim[i]))
    sorted_similar_games = sorted(Similar_games,key = lambda x:x[1], reverse = True)
                    
    i=0
    List =[None]*10
    for element in sorted_similar_games:
        s=get_title_from_index(element[0])
        List[i]=s
        i=i+1
        if i>=10:
            break
                
                
    for x in range(len(List) -1, -1, -1):
            t="\n"
            txt.insert(0.0, List[x])
            txt.insert(0.0, t)
        
top=HdpiTk()  
top.title("Game Recommendation Application")
top.resizable(0,0)
top.geometry("750x500+370+150")
top.configure(bg="#d1c4e9")

lab0=Label(top, text="Game Recommendation App",font=("times new roman",25,"bold"),fg="floralwhite",
           bg="#512da8",relief="sunken",bd=5).place(x=0,y=0,relwidth=1)

lab1=Label(top,text="Enter Your Favorite Game",bg="#d1c4e9",fg="#5d00ff",
               font=("times new roman",15,"bold"))
lab1.place(x=80,y=100)

e1=Entry(top,width="30",font=("times new roman",15,"bold"))
e1.place(x=350,y=100)

tot=Button(top,text="Search",command=show_game,fg="floralwhite",
           bg="#5d00ff",font=("times new roman",15,"bold"),bd=5).place(x=320,y=140)

lab2=Label(top,text="Top 10 Suggested Games for You",bg="#d1c4e9",fg="#5d00ff",
               font=("times new roman",15,"bold"))
lab2.place(x=220,y=180)

txt=Text(top,width=57,height=13, wrap=WORD)
txt.place(x=80,y=220)

top.mainloop()
