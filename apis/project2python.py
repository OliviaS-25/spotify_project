from apis import spotify
from apis import utilities
from pprint import pprint
from IPython.core.display import HTML

# some formatting:
HTML(utilities.get_jupyter_styling())

genre_1 = input('Select a genre ')
another_genre = str(input('Would you like to select another genre y/n? Type clear to reselect genres '))

while True:
    if another_genre == 'y':
        genre_2= input('Select a genre ')
        genres=[genre_1, genre_2]
    elif another_genre == 'n':
        genres= [genre_1] 
    else: 
        genres= []
print(genres)