from music.models import Recommendation


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