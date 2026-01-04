from models.interfaces import HelloWorldInput as Input, Output

class Compute:
    def __init__(self, input: Input):
        self.input = input

    def compute(self) -> Output:
        output_message = f"Hello, {self.input.name}!"
        output_details = {"length_of_name": len(self.input.name)}
        return Output(
            output_message=output_message,
            output_details=output_details
        )