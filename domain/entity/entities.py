from dataclasses import dataclass


@dataclass()
class SigningPolicy:
    name: str
    path: str
    value: str
    expires: int

    def __iter__(self):
        yield 'name', self.name
        yield 'path', self.path
        yield 'value', self.value
        yield 'expires', self.expires
