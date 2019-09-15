'''an example of using lcs_client for an api'''
from functools import wraps

from flask import Flask, jsonify, request
import lcs_client

app = Flask(__name__)

class DB:
    '''
    a fake database for example purposes.
    stores our information and caches lcs info for easy retreval.
    you don't really have to store lcs data locally, you could
    technically call get_profile() every time you need data
    '''
    _data = {'lcs': {}, 'our': {}}

    def get(self, collection, email):
        '''access cached lcs or our info'''
        return self._data[collection].get('email', None)

    def set(self, collection, email, data):
        '''update lcs cache or set our info'''
        self._data[collection]['email'] = data

    def __str__(self):
        return str(self._data)

db = DB()
@lcs_client.on_login
def update_profile(profile):
    '''
    update their profile. if they don't have a profile then fill stuff in
    and make note that we need more info
    '''
    first_time = db.get('lcs', profile['email']) == None
    db.set('lcs', profile['email'], profile)
    if first_time:
        db.set('our', profile['email'], {
            'needs_additional_info': True,
            'todos': [],
            'favorite_food': None
        })

def require_user(f):
    '''a decorator that gets a user object and passes it to the handler'''
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'json body required'
            }), 400
        body = request.json
        user = lcs_client.User(body['email'], token=body['token'])
        return f(*args, user=user, **kwargs)
    return wrapper


@app.route('/profile', methods=['POST'])
@require_user
def profile(user=None):
    lcs = db.get('lcs', user.email)
    our = db.get('our', user.email)
    return jsonify({
        'success': True,
        'profile': {
            'email': lcs['email'],
            'needs_additional_info': our['needs_additional_info'],
            'todos': our['todos'],
            'favorite_food': our['favorite_food'],
        }
    })

@app.route('/additional_info', methods=['POST'])
@require_user
def set_additional_info(user=None):
    '''
    the idea is that when the ui first loads the profile it will check if
    we need to collect additional info. if we do
    '''
    our = db.get('our', user.email)
    our['favorite_food'] = request.json['favorite_food']
    our['needs_additional_info'] = False
    db.set('our', user.email, our)
    return jsonify({'success': True})

@app.route('/todo', methods=['POST'])
@require_user
def new_todo(user=None):
    todo = request.json
    our = db.get('our', user.email)
    our['todos'].append({
        'text': todo['text']
    })
    db.set('our', user.email, our)
    return jsonify({'success': True, '_id': len(our['todos']) - 1})

@app.route('/todo', methods=['DELETE'])
@require_user
def resolve(user=None):
    _id = request.json['_id']
    our = db.get('our', user.email)
    if len(our['todos']) <= _id:
        return jsonify({'success': False, 'error': '_id does not exist'})
    del our['todos'][_id]
    db.set('our', user.email, our)
    return jsonify({'success': True})

@app.errorhandler(lcs_client.CredentialError)
def unauth(e):
    return jsonify({
        'success': False,
        'error': 'invalid credentials: ' + str(e),
    }), 403

@app.errorhandler(Exception)
def handler(e):
    print(type(e))
    # idealy you'd also get the correct response code
    return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run()
