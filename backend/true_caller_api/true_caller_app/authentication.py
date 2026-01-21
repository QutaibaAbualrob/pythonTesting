from rest_framework.authentication import TokenAuthentication


class BearerTokenAuthentication(TokenAuthentication):
    """
    Custom TokenAuthentication that accepts both 'Token' and 'Bearer' keywords.
    This allows clients to use 'Authorization: Bearer <token>' or 'Authorization: Token <token>'.
    """
    keyword = 'Bearer'
