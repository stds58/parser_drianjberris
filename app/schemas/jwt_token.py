from pydantic import BaseModel, Field
from typing import TypedDict,Dict,List, Optional


class RealmAccessDict(TypedDict):
    roles: List[str]

class ResourceAccessItem(TypedDict):
    roles: List[str]

class UserClaims(TypedDict):
    exp: int
    iat: int
    auth_time: int
    jti: str
    iss: str
    aud: str
    sub: str
    typ: str
    azp: str
    sid: str
    acr: str
    allowed_origins: List[str] = Field(default=None, validation_alias="allowed-origins")
    realm_access: RealmAccessDict
    resource_access: Dict[str, ResourceAccessItem] = {}
    scope: str
    email_verified: bool
    name: str
    preferred_username: str
    locale: str
    given_name: str
    family_name: str
    email: str
    exp_gumanize: str
    iat_gumanize: str
    exp_minutes_gumanize: int
    auth_time_gumanize: str



