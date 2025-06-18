def get_profile_picture_url(user):
    default_url = "https://res.cloudinary.com/dliev5zuy/image/upload/f_auto/v1750204693/defaultPicture_z9uqh8"

    try:
        url = user.profile_picture.url
    except Exception:
        url = default_url
    if '/upload/' in url and 'f_auto' not in url:
           url = url.replace('/upload/', '/upload/f_auto/')
    return url

def get_cover_url(cover_field):
    default_url = "https://res.cloudinary.com/dliev5zuy/image/upload/f_auto,c_fill,g_auto,w_100,h_100/v1750248957/defaultPlaylistCover_elb8ew.jpg"

    try:
        url = cover_field.url
    except:
        return default_url

    if '/upload/' in url:
        return url.replace('/upload/', '/upload/f_auto,c_fill/')
    return url

def get_artist_photo_url(artist):
    default_url = "https://res.cloudinary.com/dliev5zuy/image/upload/v1750249305/default_artist_vtyuz5.png"

    try:
        url = artist.photo.url
    except Exception:
        url = default_url
    if '/upload/' in url and 'f_auto' not in url:
        url = url.replace('/upload/', '/upload/f_auto/')
    return url

def get_song_cover_url(song):
    default_url = "https://res.cloudinary.com/dliev5zuy/image/upload/v1750249400/default_cover_td9qhw.png"

    try:
        url = song.cover.url
    except Exception:
        url = default_url

    if '/upload/' in url and 'f_auto' not in url:
        url = url.replace('/upload/', '/upload/f_auto/')
    return url

def get_song_audio_url(song):
    default_url = "https://res.cloudinary.com/dliev5zuy/video/upload/v1750267041/HDS_-_DEMO_ldyoty.mp3"

    try:
        url = song.audio_file.url
    except Exception:
        url = default_url

    if '/upload/' in url and 'f_auto' not in url:
        url = url.replace('/upload/', '/upload/f_auto/')
    return url