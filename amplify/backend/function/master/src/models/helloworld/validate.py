from models.interfaces import HelloWorldInput as Input

class Validator:
    def __init__(self, input: Input):
        self.input = input

    def validate_input(self):
        
        return True,""