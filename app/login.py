from flask_login import login_user
from flask import make_response

def loginUser(user):
    try: 
        l = login_user(user)
        if not l:
            print("Login failed")
            raise Exception("Login failed")
        response = make_response("User logged in successfully", 200)
        response.headers["Content-Type"] = "text/plain"
        response.set_cookie(key = "authenticated", value = "true", samesite="none", secure=True)
        return response
    except Exception as e: 
        print(e)
        return "An error ocurred while configuring the user session", 500