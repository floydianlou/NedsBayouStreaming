import random

from music.models import Recommendation, Artist, Song


def update_recommendations(user, song, delta):
    """
    BASIS FOR RECOMMENDATION SYSTEM: delta can be positive or negative and can assume
    different values depending on the action taken (liking a song or adding to playlist)
    if no row for the artist's genres exists it creates one and adds the score starting from
    0, can both go in negative and positive values.
    """
    if user.is_authenticated:
        for genre in song.artist.genres.all():
            rec, created = Recommendation.objects.get_or_create(user=user, genre=genre)
            rec.score += delta
            rec.save()


def get_random_recommendations(user):
    print("🎲 Returning random recommendations.")

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
