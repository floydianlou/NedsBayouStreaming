# *NED'S BAYOU - MUSIC STREAMING SERVICE*

**Ned's Bayou** is a simulated music streaming service made with Django for a [University project](https://www.ing-inl.unifi.it/vp-130-terzo-anno.html#).
The website takes inspiration from all the currently famous streaming platforms for styling and main functionalities and tries to replicate the most common features: making, creating and editing an account, liking songs, creating playlists and browsing a catalogue either by seeing personalised recommendations, a full list of songs or by searching a term on the search bar.
On Ned's Bayou you automatically start with a Listener role, which can do all previously listed activities; if you're not logged in, you'll still be able to browse the website and see other people's profiles and playlist creations, but you won't be able to like songs or create your own playlists.
By using the Django Administration Panel, some accounts can also cover a Curator role and access the "Curator Dashboard" to add, edit or delete all songs, artists and genres.

> All songs use the same track as to not violate any copyright laws. I used an instrumental version of [Heavydirtysoul by Twenty One Pilots](https://www.youtube.com/watch?v=lzXRdS9cynQ) which I found for free on multiple Reddit threads and online.

## WEBSITE FUNCTIONALITIES
**Ned's Bayou** offers the following functionalities, listed in no particular order:

- **Creating a personalised account** with a profile picture, a small bio, a possible favorite artist and an international phone number;
- Viewing your profile, editing some of the associated data, viewing and managing your likes and your playlist creations;
- Viewing other people's profiles and playlists;
- Browsing the app's full catalogue sorted by artist, searching for a specific song or artist and viewing personalised recommendations;
- Viewing an artist page, their provided biography, their entire music catalogue on the app and some randomly selected highlights;
- Seeing the top five most used songs in playlists at the moment and the latest playlist creations;
- Searching for terms and filtering by genre, playlist length or user likes to find what you are really looking for;
- Playing a song from the song player, liking it or adding it with the quick add feature to a playlist you already created;
- Creating a playlist from scratch, with customising options like a title, a description and a playlist cover.

*For Curators only:*
- Adding, editing or deleting a music genre, with a unique name and an optional description (**NOTE: deleting a genre will result in the loss of all artists with that one single genre associated**);
- Adding, editing or deleting an artist, with options for a name, a biography, up to three music genres associated and a 16:9 picture for the artist page (**NOTE: deleting an artist will result in the loss of the artist's full catalogue of songs**);
- Adding, editing or deleting songs, with options for a song name, cover and audio file, other than associating it with an artist from the catalogue.

**All editing, creating and personalised actions are uniquely reserved to logged-in users, while a guest can still browse the website.**

___________

## RECOMMENDATIONS FEATURE
**Ned's Bayou** offers a points based system to suggest songs and artists to its users. 
The recommendation system works as follows: every interaction of the user with a song or an artist modifies a score related to the artist's genre, influencing the tastes of the user: liking a song will provide a score of +3 to all genres related to the song's artist, while adding a song to a playlist will provide a +2 score.
The favorite artist the user chooses at any time adds a +5 bonus to the artist's genres. Removing a song from a playlist or unliking it will result in the score being deducted from the total for the related genres.

The **"Suggested for you"** preview tab and the related **"Recommended for you"** template provides song and artist suggestions based on the score, using the following system: 
- The genres are ordered by score and the top three genres are selected;
- From the top three genres, the website gathers all related artists, ordered by number of common genres to the top three: from this list it extracts the top two artists and puts them in the template;
- Still based on scores, the website tries to find five songs from related artist to suggest to the user, excluding the ones the user already has in its likes (but not the ones in playlists): if the list doesn't reach the minimum number, it fills it with random recommendations;
- The website also provides a random artist and two random songs (excluding the ones already suggested) to extend the user interests to other genres and songs.

All scores are stored in a model that links each user to each genre, making them persist between sessions and influence future interactions.

TODO scrivere della ricerca personalizzata