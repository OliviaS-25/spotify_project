from apis import spotify
from apis import sendgrid
from urllib.request import urlopen


def print_menu():
    print('''
---------------------------------------------------------------------
Settings / Browse Options
---------------------------------------------------------------------
1 - Select your favorite genres  
2 - Select your favorite artists 
3 - Discover new music
4 - Quit
---------------------------------------------------------------------
    ''')


genres = []
artist = []
artist_ids = []

template = '''
    <h1>{artist_name}</h1>
    <p>More info <a href="{share_url}">here...</a></p>
    <img src="{image_url}" />
    {tracks_table}
'''

def handle_genre_selection():
    global genres
    all_genre = spotify.get_genres_abridged()
    count = 1
    for genre in all_genre:
        print(count, genre)
        count += 1

    user_select = input(
        'Plese select two genres as a comma-delimited lsit of numbers. Type "clear" to clear out genres ')
    ids_select = user_select.split(",")
    for id in ids_select:
        id_clean = int(id) - 1
        genres.append(all_genre[id_clean])
    return (genres)


def handle_artist_selection():
    print('Handle artist selection here...')
    # 1. Allow user to search for an artist using
    #    spotify.get_artists() function
    # 2. Allow user to store / modify / retrieve artists
    #    in order to get song recommendations
    global artist
    global artist_ids
    artist_1 = str(input('Enter the name of the artist '))
    lookup_artist = spotify.get_artists(artist_1)
    for dictionary in range(len(lookup_artist)):
        list_of_artists = lookup_artist[dictionary].get('name')
        print(str(dictionary + 1) + "." + list_of_artists)
    user_select = input(
        'Plese select two artist as a comma-delimited lsit of numbers. Type "clear" to clear out artist ')

    ids_select = user_select.split(",")
    for id in ids_select:
        id_clean = int(id) - 1
        artist.append(lookup_artist[id_clean])
    for art in artist:
        artist_ids.append(art['id'])

    # print(artist)
    return(artist_ids)


def get_recommendations():
    print('Handle retrieving a list of recommendations here...')
    # 1. Allow user to retrieve song recommendations using the
    #    spotify.get_similar_tracks() function
    # 2. List them below
    # handle_artist_selection()

    # for _id in artist_ids:
    related_tracks = spotify.get_similar_tracks(handle_artist_selection())  # , genres= genres, simplify =True)
    print(related_tracks)
    email_choice = input('Do you want to send an email (y/n)? ')
    if email_choice == 'y':
        from_email = input('What is your email ')
        to_emails = input('Who would you like to send the email to?')
        subject = input('What is your subject line ')
        html_content = related_tracks
        
        html_text = template.format(
        #artist_name=artist['name'],
        #image_url=artist['image_url_small'],
        # name= 'name',
        artist_name='name',
        image_url='image_url_small',
        share_url='share_url',
        tracks_table=spotify.get_formatted_tracklist_table_html(html_content)
        )
        print('Sending the email...')
        sendgrid.send_mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        html_content = '<br><br>' + html_text)


# Begin Main Program Loop:
while True:
    print_menu()
    choice = input('What would you like to do? ')
    if choice == '1':
        handle_genre_selection()
    elif choice == '2':
        handle_artist_selection()
    elif choice == '3':
        get_recommendations()
        # In addition to showing the user recommendations, allow them
        # to email recommendations to one or more of their friends using
        # the sendgrid.send_mail() function.
    elif choice == '4':
        print('Quitting...')
        break
    else:
        print(choice, 'is an invalid choice. Please try again.')
    print()
    input('Press enter to continue...')
