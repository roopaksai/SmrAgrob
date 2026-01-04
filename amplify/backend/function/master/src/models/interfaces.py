from dataclasses import dataclass, field

@dataclass
class HelloWorldInput:
    name: str

@dataclass
class Output:
    output_message: str = field(default_factory=lambda: "")
    output_details: dict = field(default_factory=lambda: {})
    output_status: str = field(default_factory=lambda: "SUCCESS")