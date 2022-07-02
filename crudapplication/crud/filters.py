def make_user_filters(data):
    kwargs = {}
    email = data.get('email', '')
    first_name = data.get('first_name', '')
    last_name = data.get('last_name', '')

    if email:
        kwargs.update({'user__email__iexact': email})

    if first_name:
        kwargs.update({'user__first_name__iexact': first_name})

    if last_name:
        kwargs.update({'user__last_name__iexact': last_name})

    return kwargs