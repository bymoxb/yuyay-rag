from flask import g


class AuthUser:

    @staticmethod
    def username():
        return g.user.get("preferred_username")
