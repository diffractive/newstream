def extras(request):
    if '_auth_user_id' in request.session:
        print("Auth user id: " +
              str(request.session['_auth_user_id']), flush=True)
        return {
            'auth_user_id': request.session['_auth_user_id']
        }
    else:
        print("No Auth user id in session", flush=True)
    return {}
