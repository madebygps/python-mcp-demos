"""Keycloak authentication provider for FastMCP.

This module provides KeycloakAuthProvider - a complete authentication solution that integrates
with Keycloak's OAuth 2.1 and OpenID Connect services, supporting Dynamic Client Registration (DCR)
for seamless MCP client authentication.

Based on proposed FastMCP PR: https://github.com/jlowin/fastmcp/pull/1937

Note: Requires Keycloak 26.6.0 or later, which properly honors the `token_endpoint_auth_method`
parameter in DCR requests. See: https://github.com/keycloak/keycloak/issues/44403
"""

from __future__ import annotations

from fastmcp.server.auth import RemoteAuthProvider
from fastmcp.server.auth.providers.jwt import JWTVerifier
from pydantic import AnyHttpUrl


class KeycloakAuthProvider(RemoteAuthProvider):
    """Keycloak authentication provider with Dynamic Client Registration (DCR) support.

    This provider integrates FastMCP with Keycloak by configuring the appropriate JWT
    verification settings and pointing MCP clients directly to Keycloak's OAuth endpoints.

    All OAuth operations go directly to Keycloak:
    - Authorization flows (users authenticate directly with Keycloak)
    - Token issuance (tokens come directly from Keycloak)
    - Token validation (JWT signatures verified against Keycloak's keys)
    - Dynamic Client Registration (DCR requests go directly to Keycloak)

    Requires Keycloak 26.6.0+ which properly honors `token_endpoint_auth_method: client_secret_post`
    in DCR responses (fixed in https://github.com/keycloak/keycloak/pull/45309).

    Example:
        ```python
        from fastmcp import FastMCP
        from keycloak_provider import KeycloakAuthProvider

        keycloak_auth = KeycloakAuthProvider(
            realm_url="http://localhost:8080/realms/fastmcp",
            base_url="http://localhost:8000",
            required_scopes=["openid", "profile"],
        )

        mcp = FastMCP("My App", auth=keycloak_auth)
        ```
    """

    def __init__(
        self,
        *,
        realm_url: AnyHttpUrl | str,
        base_url: AnyHttpUrl | str,
        required_scopes: list[str] | None = None,
        audience: str | list[str] | None = None,
        token_verifier: JWTVerifier | None = None,
    ):
        """Initialize Keycloak authentication provider.

        Args:
            realm_url: Your Keycloak realm URL (e.g., "https://keycloak.example.com/realms/myrealm")
            base_url: Public URL of this FastMCP server
            required_scopes: Optional list of scopes to require for all requests
            audience: Optional audience(s) for JWT validation. If not specified and no custom
                verifier is provided, audience validation is disabled. For production use,
                it's recommended to set this to your resource server identifier or base_url.
            token_verifier: Optional token verifier. If None, creates JWT verifier for Keycloak
        """
        self.base_url = AnyHttpUrl(str(base_url).rstrip("/"))
        self.realm_url = str(realm_url).rstrip("/")

        # Create default JWT verifier if none provided
        if token_verifier is None:
            # Keycloak uses specific URL patterns (not the standard .well-known paths)
            token_verifier = JWTVerifier(
                jwks_uri=f"{self.realm_url}/protocol/openid-connect/certs",
                issuer=self.realm_url,
                algorithm="RS256",
                required_scopes=required_scopes,
                audience=audience,
            )

        # Initialize RemoteAuthProvider with Keycloak as the authorization server
        # MCP clients will be directed to Keycloak for all OAuth operations
        super().__init__(
            token_verifier=token_verifier,
            authorization_servers=[AnyHttpUrl(self.realm_url)],
            base_url=self.base_url,
        )
