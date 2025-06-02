def user_group_context(request):
    is_curator = False
    if request.user.is_authenticated:
        is_curator = request.user.groups.filter(name='Curator').exists()
    return {
        'req_user_is_curator': is_curator
    }