class User:
    """Пользователь, арендующий виртуальные ресурсы."""

    def __init__(self, user_id: int, name: str, email: str) -> None:
        self.id = user_id
        self.name = name
        self.email = email

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать пользователя из словаря данных."""
        return cls(data["id"], data["name"], data["email"])

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"


def add_user(users: list[User], name: str, email: str) -> User:
    """Создать объект User и добавить его в коллекцию."""
    user_id = max((u.id for u in users), default=0) + 1
    user = User(user_id, name, email)
    users.append(user)
    return user


def find_user(users: list[User], query: str) -> list[User]:
    """Найти пользователей по имени или адресу электронной почты."""
    query = query.lower()
    return [
        u for u in users
        if query in u.name.lower() or query in u.email.lower()
    ]


def find_user_by_id(users: list[User], user_id: int) -> User | None:
    """Найти пользователя по идентификатору."""
    for user in users:
        if user.id == user_id:
            return user
    return None
