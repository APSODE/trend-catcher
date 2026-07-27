class IllegalSaltException(Exception):
    def __init__(self, **kwargs):
        param_amount = len(kwargs.keys())

        if param_amount == 1:
            error_message = f"The provided salt length {kwargs.get('length')} is outside the allowed range."

        elif param_amount == 3:
            error_message = (
                f"The salt length {kwargs.get('length')} is invalid. "
                f"It must be between {kwargs.get('min_length')} and {kwargs.get('max_length')} characters."
            )

        else:
            error_message = f"An unexpected error occurred during salt generation."


        super().__init__(error_message)