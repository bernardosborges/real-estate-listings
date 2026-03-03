from __future__ import annotations

class CreateUserInput:

    def __init__(
            self,
            *,
            email: str,
            password: str,
            public_id: str,
            is_superuser: bool = False
    ):

        self.email = email
        self.password = password
        self.public_id = public_id
        self.is_superuser = is_superuser
