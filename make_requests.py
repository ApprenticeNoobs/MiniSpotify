import requests


BASE_URL = 'http://localhost:5000'
USER_API_URL = BASE_URL + '/user'
DELIMITER = '&'


# Example request url:
# http://127.0.0.1:5000/create_user?name=Randy%20%email=randy@gmail.com%20%password=12345
def create_user(name, email, password):
    params = {
        'name': name,
        'email': email,
        'password': password
    }
    return requests.get(url=USER_API_URL, params=params)


def delete_user(email):
    params = {
        'email': email
    }
    return requests.delete(url=USER_API_URL, params=params)


def update_user_email(name, password, new_email):
    params = {
        'name': name,
        'password': password,
        'email': new_email
    }
    return requests.put(url=USER_API_URL, params=params)


if __name__ == '__main__':
    name = 'randy'
    email = 'randy@gmail.com'
    password = '12345'
    new_email = 'randy12345@gmail.com'

    print("creating user....")
    response = create_user(name=name, email=email, password=password)
    print(response)
    print('updating user email....')
    response = update_user_email(name=name, password=password, new_email=new_email)
    print(response)
    print('deleting user....')
    response = delete_user(email=new_email)
    print(response)

    # TODO: need to fix response in Flask router so that we can call `response.json()`.
