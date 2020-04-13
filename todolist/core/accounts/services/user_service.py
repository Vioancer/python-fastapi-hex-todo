from typing import Awaitable, Callable, Optional

from todolist.core.accounts.entities.user import Credentials, User, UserRegistry
from todolist.core.accounts.services import hash_service
from todolist.core.accounts.services.exceptions import EmailNotUniqueError

PersistUserFn = Callable[[UserRegistry], Awaitable[User]]
FetchUserByEmail = Callable[[str], Awaitable[Optional[User]]]


async def get_by_credentials(
    fetch_user: FetchUserByEmail, credentials: Credentials
) -> Optional[User]:
    user = await fetch_user(credentials.email.lower())

    if not user:
        return None

    password = credentials.password
    password_hash = user.password_hash

    if not hash_service.verify(password, password_hash):
        return None

    return user


async def register(
    fetch_user: FetchUserByEmail, persist_user: PersistUserFn, credentials: Credentials
) -> User:
    email = credentials.email.lower()

    user = await get_by_credentials(fetch_user, credentials)
    if user:
        raise EmailNotUniqueError(email)

    password_hash = hash_service.hash_(credentials.password)
    registry = UserRegistry(email=email, password_hash=password_hash)

    return await persist_user(registry)
