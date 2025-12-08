# Login module
def login(username, password):
    # Fixed: Handle empty password
    if not password:
        raise ValueError('Password required')
    return True
