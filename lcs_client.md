<h1 id="lcs_client">lcs_client</h1>


This is intended to be a serverside client to help with hackru services that biggie back
on lcs login ang user data

<h2 id="lcs_client.set_root_url">set_root_url</h2>

```python
set_root_url(url)
```
sets root url. defaults to `https://api.hackru.org`
<h2 id="lcs_client.set_testing">set_testing</h2>

```python
set_testing(testing)
```
weather or not to use test endpoint, defaults to `False`
<h2 id="lcs_client.User">User</h2>

```python
User(self, email, password=None, token=None)
```

a user object to easily call other endpoints on behalf of a user
constructor logs the user and gets a handle. requires you to pass a token OR a password

<h3 id="lcs_client.User.profile">profile</h3>

```python
User.profile(self)
```
call lcs to get the user's profile
<h3 id="lcs_client.User.dm_link_for">dm_link_for</h3>

```python
User.dm_link_for(self, other_user)
```
get a dm link for another user's slack __NOT IMPLMIMENTED YET__
<h2 id="lcs_client.ResponseError">ResponseError</h2>

```python
ResponseError(self, response)
```
error with an attached http Response
<h2 id="lcs_client.RequestError">RequestError</h2>

```python
RequestError(self, response)
```
ideally you shouldn't receve this. there was an issue with the input to the api
<h2 id="lcs_client.CredentialError">CredentialError</h2>

```python
CredentialError(self, response)
```
there was an issue login in with that credential, or a token is invalid
<h2 id="lcs_client.on_login">on_login</h2>

```python
on_login(f)
```

decorator. call the decorated function whenever we find a new user
use case: get their profile and update local db.
function should take in the user object as the first param

```python
@lcs_client.on_login
def your_func(user_profile):
    # updating the user profile or something
```

<h2 id="lcs_client.validate_token">validate_token</h2>

```python
validate_token(email, token)
```
validates an lcs token and email pair
<h2 id="lcs_client.login">login</h2>

```python
login(email, password)
```
gets a token for a user
<h2 id="lcs_client.get_profile">get_profile</h2>

```python
get_profile(email, token, auth_email=None)
```

gets the profile of a user. add auth_email if you are looking at the users profile
from a different account

<h2 id="lcs_client.get_dm_for">get_dm_for</h2>

```python
get_dm_for(email, token, other_user)
```

get a dm link to talk with another user on slack. __NOT YET IMPLEMENTED__

<h2 id="lcs_client.base_url">base_url</h2>

```python
base_url()
```
get the lcs base url
<h2 id="lcs_client.get">get</h2>

```python
get(endpoint, *args, **kwargs)
```
does get request to lcs endpoint
<h2 id="lcs_client.post">post</h2>

```python
post(endpoint, *args, **kwargs)
```
does post request to lcs endpoint
