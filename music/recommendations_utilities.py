import random

from music.models import Recommendation, Artist, Song


def update_recommendations(user, song, delta):

    # BASIS FOR RECOMMENDATION SYSTEM: delta can be positive or negative and can assume
    # different values depending on the action taken (liking a song or adding to playlist)
    # if no row for the artist's genres exists it creates one and adds the score starting from
    # 0, can both go in negative and positive values.

    if user.is_authenticated:
        for genre in song.artist.genres.all():
            rec, created = Recommendation.objects.get_or_create(user=user, genre=genre)
            rec.score += delta
            rec.save()


def get_random_recommendations(user):
    print("Returning random recommendations.")

    random_artists = list(Artist.objects.all())
    random.shuffle(random_artists)

    random_songs = list(Song.objects.all())
    random.shuffle(random_songs)

    return {
        "related_artists": random_artists[:2],
        "recommended_songs": random_songs[:5],
        "random_artist": random_artists[2] if len(random_artists) > 2 else None,
        "random_songs": random_songs[5:7]
    }

def get_random_songs(user, count, exclude_song_ids=None):
    print(f"🎲 get_random_songs(user, count={count})")

    # gets a list of exlcuded song ids
    excluded_song_ids = list(user.liked_songs.values_list('id', flat=True))
    if exclude_song_ids:
        excluded_song_ids.extend(exclude_song_ids)

    # removes the excluded songs and shuffles them
    available_songs = Song.objects.exclude(id__in=excluded_song_ids)
    available_songs_list = list(available_songs)

    random.shuffle(available_songs_list)
    selected_songs = available_songs_list[:count]

    # if they're not enough, it fills the selected songs with random ones, excluding the ones already in list
    if len(selected_songs) < count:
        missing = count - len(selected_songs)
        print(f"Only {len(selected_songs)} unseen songs available. Filling {missing} more with fallback.")

        fallback_exclude_ids = [s.id for s in selected_songs] + excluded_song_ids
        fallback_candidates = list(Song.objects.exclude(id__in=fallback_exclude_ids))
        random.shuffle(fallback_candidates)

        if not fallback_candidates:
            print("Fallback candidates empty. Using final fallback from full catalog excluding recommended.")
            final_fallback_exclude_ids = exclude_song_ids if exclude_song_ids else []
            fallback_candidates = list(Song.objects.exclude(id__in=final_fallback_exclude_ids))
            random.shuffle(fallback_candidates)

        selected_songs.extend(fallback_candidates[:missing])

    print(f"Selected {len(selected_songs)} random song(s):", [s.title for s in selected_songs])

    return selected_songs

def is_curator(user):
    return user.groups.filter(name='Curator').exists()