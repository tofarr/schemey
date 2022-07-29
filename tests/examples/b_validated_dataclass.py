from typing import Optional

from schemey.validated import validated

# We can create a validated dataclass that prevents bad data being inserted


@validated
class Greeter:
    first_name: str
    last_name: Optional[str] = None

    def greet(self):
        return f"Hello {self.first_name} {self.last_name or ''}".strip()


greeter = Greeter("Developer")
print(greeter.first_name)
print(greeter.last_name)
greeter.last_name = "McDeveloperFace"  # Set without issue because this is a string
print(greeter.greet())
# greeter.last_name = 10 # raises ValidationError
# Greeter(10) # Also raises ValidationError
