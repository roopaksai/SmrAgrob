import traceback
from models.constants import OutputStatus
from models.helloworld.compute import Compute
from models.helloworld.validate import Validator
from models.interfaces import HelloWorldInput as Input, Output


class HelloWorld:
    def __init__(self, Input: Input) -> None:
        self.input = Input

    def process(self) -> Output:
        input = self.input
        valid_input, error_message = self._validate(input)

        if not valid_input:
            return Output(
                output_message=f"INVALID_INPUT: {error_message}",
                output_status=OutputStatus.FAILURE
            )

        try:
            output = self._compute(input)
        except Exception as e:
            traceback.print_exc()
            output = Output(
                output_message=f"COMPUTE_FAILED: {str(e)}",
                output_status=OutputStatus.FAILURE
            )

        return output
    
    def _validate(self, input: Input) -> tuple[bool, str]:
        validator = Validator(input)
        return validator.validate_input()

    def _compute(self, input: Input) -> Output:
        compute = Compute(input)
        return compute.compute()