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
## FUNCTIONALITIES HIGHLIGHTS

### RECOMMENDATIONS FEATURE
**Ned's Bayou** offers a points based system to suggest songs and artists to its users. 
The recommendation system works as follows: every interaction of the user with a song or an artist modifies a score related to the artist's genre, influencing the tastes of the user: liking a song will provide a score of +3 to all genres related to the song's artist, while adding a song to a playlist will provide a +2 score.
The favorite artist the user chooses at any time adds a +5 bonus to the artist's genres. Removing a song from a playlist or unliking it will result in the score being deducted from the total for the related genres.

The **"Suggested for you"** preview tab and the related **"Recommended for you"** template provides song and artist suggestions based on the score, using the following system: 
- The genres are ordered by score and the top three genres are selected;
- From the top three genres, the website gathers all related artists, ordered by number of common genres to the top three: from this list it extracts the top two artists and puts them in the template;
- Still based on scores, the website tries to find five songs from related artist to suggest to the user, excluding the ones the user already has in its likes (but not the ones in playlists): if the list doesn't reach the minimum number, it fills it with random recommendations;
- The website also provides a random artist and two random songs (excluding the ones already suggested) to extend the user interests to other genres and songs.

All scores are stored in a model that links each user to each genre, making them persist between sessions and influence future interactions.

-> The recommendation algorithm is also used to order results when searching for any term: if results from various genres are present, they get ordered using the *Recommendations* model table with genre scores.

### FILTERING FEATURE
On the **Search Results** page, the website offers a few filters to sort through query results: you can always choose a tab between *Songs*, *Artists*, *Playlists* and *Users*, on which you will also find a **Genre filtering** when looking at the first two tabs, a **Playlist length** filter for the third one and a **Number of likes** feature for the last one.

### IMAGE AND AUDIO MANAGEMENT
On **Ned's Bayou**, the user is able to choose between personalising their profile and playlists or to leave a default cover and default profile picture. Removing an added picture will at any time change it to the default one. For *Curators*, an artist or song pictures can be left blank and will be replaced by the default ones; to be coherent, the only space that can not be left blank is the audio file for a song, since it'd be counterproductive to add a song with a default audio file on a streaming platform!

___________
## HOW TO USE NED'S BAYOU
**Ned's Bayou** uses primarily its modular toolbar to allow users to navigate through pages. Clicking on the website's name on the toolbar will always **bring you to the homepage**, while on the right side you will see a varying amount of buttons depending on your log situation:
- If you're not logged in, the toolbar will feature two buttons to allow users to **Create an account** or **Login**;
- If you're a Listener, the toolbar will feature a welcome message and a link to your user profile, a button to access the **Create a playlist** form and a button to **Log out** of your account;
- If you're a Curator, your toolbar will have all previously listed Listener buttons, a small icon to show your different account status and a button to access the **Curator Dashboard**.

You can search and find anything that is on the website using the **Search Bar** on the homepage. The full song catalogue, ordered by artist with links to all individual artist pages, can be accessed through a dedicated section at the bottom of the homepage. If you want to see personalised recommendations, you can also access the "Suggested for you" box at the top of the homepage and its related page.
From the **Profile** page you will be able to edit or delete all your playlists, change your user data like name, favourite artist and bio and unlike liked songs. You won't be allowed to do these actions on any other user profile than your own and only if you are logged in.
By using the **Song and Artist Cards** featured on all the website pages, you will always be able to access the artist page by clicking on their name, playing the audio related to the song, quick adding the song to one of your playlists that *does not already feature it* and liking/unliking it. If all your playlists feature a song, the *quick add* feature will provide a link to the **"Add a playlist"** page instead.
From the **Playlist details** page, you will also be able to click the *Share this playlist* button to get the playlist's link copied. Using the **Playlist Cards** featured in one's profile or on the search bar you will also be able to get a link by using the quick share button.

#### NOTES ON CURATOR DASHBOARD FOR CURATORS
If your account is from the *Curator group*, you will be able to access the **Curator Dashboard**. On the dashboard page, a Curator will find three forms, made to **Add a Genre, an Artist or a Song** to the database. Under all three forms the user will find three tables featuring all currently present genres, artists and songs in the database, with two buttons: one to **Edit** and one to **Delete** the item in question.
When the Curator edits an element, the editing form will appear at the top of the page from the already existing ones, changing the writing to "Update" from "Add". When you delete an item instead, no confirmation button will appear and the action will have immediate consequences. As state before, these are the actions that will happen when deleting objects:
1. **Deleting a song** will result in all scores associated with that song to be deducted from the Recommendations table for all users involved; this means that anyone who liked the song or added the song to a playlist will lose 3 and 2 (x Playlist) points respectfully;
2. **Deleting an artist** will result in all songs associated with that artist to be deleted (hence the score deduction), and 5 more points deducted from scores of all users who had that artist as their favorite;
3. **Deleting a genre** will result in all Recommendations rows associated to be deleted and in all artists which only have that single genre associated to be deleted (and scores will disappear).

> On the db.sqlite3 database provided I left one Curator account with the following credentials, as to allow testing of the Curator Dashboard:
 
_**Username: alice
Password: alice
Can also access /admin of Django Administration.**_

___________
### FINAL NOTES AND INDICATIONS
This website was created for a University project (as stated above) and its style is heavily inspired by [Ned Bayou LTD](https://europe.nedbayou.com/gb/), a website for merch by Twenty One Pilots. I would like to clarify that all the icons and images I am using are used for a fake website that will be up for a limited amount of time and are used for personal use only (with no income to the website or me). 
All artists and songs featured in this project are among my favorite of all time and all mentions, pictures and icons used are just a tribute to them, coming from my heart.
No copyright or company associated with this website!