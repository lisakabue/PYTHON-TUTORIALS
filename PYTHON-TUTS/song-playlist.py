artist_songs = {
    "The Beatles": ["Hey Jude", "Let It Be", "Yesterday"],
    "Taylor Swift": ["Shake It Off", "Love Story", "Blank Space"],
    "Ed Sheeran": ["Perfect", "Thinking Out Loud", "Photograph"]
}


def get_user_input():
    artist = input('Enter your favorite artist: ').title()
    return artist

def main():
    artist = get_user_input()
    if artist in artist_songs: 
        print(f"Hey nice that you're here, we recommend the following songs by $ {artist}")
        for songs in artist_songs[artist]:
            print(songs)
    
    else:
        print(f"There was no match for the artist: $ {artist}, try:") 
        for artist in artist_songs:
            print(f"Songs by: {artist}")
            for songs in artist_songs[artist]:
                print(songs)
                   


main()
