import requests


BASE_URL = 'http://localhost:5000'
DELIMITER = '&'


# Example request url:
# http://127.0.0.1:5000/create_user?name=Randy%20%email=randy@gmail.com%20%password=12345
def create_user(name, email, password):
    route = '/user'
    params = {
        'name': name,
        'email':email,
        'password': password
    }
    return requests.get(url=BASE_URL + route, params=params)
    

if __name__ == '__main__':
    response = create_user(name='randy', email='randy@gmail.com', password='12345')
    print(response)
