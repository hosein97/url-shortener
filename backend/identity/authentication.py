from rest_framework.authentication import BaseAuthentication

import jwt

from django.conf import settings

from jwt import PyJWKClient

from django.contrib.auth import get_user_model

User = get_user_model()

JWKS_URL = (
    f"{settings.KEYCLOAK_INTERNAL_URL}"
    f"/realms/{settings.KEYCLOAK_REALM}"
    "/protocol/openid-connect/certs"
)


ISSUER = (
    f"{settings.KEYCLOAK_PUBLIC_URL}"
    f"/realms/{settings.KEYCLOAK_REALM}"
)

jwk_client = PyJWKClient(JWKS_URL)


class KeycloakAuthentication(BaseAuthentication):

    def authenticate(self, request):

        auth_header = request.headers.get(
            "Authorization"
        )

        if not auth_header:
            return None


        parts = auth_header.split()

        if len(parts) != 2:
            return None


        scheme, token = parts


        if scheme.lower() != "bearer":
            return None


        try:

            signing_key = (
                jwk_client
                .get_signing_key_from_jwt(token)
            )


            payload = jwt.decode(

                token,

                signing_key.key,

                algorithms=["RS256"],

                audience=settings.KEYCLOAK_API_AUDIENCE,

                issuer=ISSUER,

            )


        except jwt.PyJWTError:

            return None



        keycloak_sub = payload["sub"]


        user, created = User.objects.get_or_create(

            keycloak_sub=keycloak_sub,
    
            defaults={
                "username": payload.get(
                    "preferred_username"
                ),
                "email": payload.get(
                    "email"
                ),
            }

        )


        return (
            user,
            token
        )