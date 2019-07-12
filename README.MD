# Gerenciagram API Challenge
 
## Given challenge:
Create an API that has:
1. Endpoint to load information from a profile as profile data and last 10 posts (username will have to be passed in the URL) using the installoader lib and sending that data to the s3 in a private bucket;
Bonus: if you make it work asynchronously.
2. Endpoint to download a s3 post from a given profile by its index (for example, username = test and index = 0 would be the last post made by the profile);
 
3. Endpoint to download s3 profile data (return json containing the data that the installer saves in the file).


Application Setup
=================

Recommended way is to clone repository and use poetry do manage dependencies, but you can use `pip install -r requirements.txt`.

