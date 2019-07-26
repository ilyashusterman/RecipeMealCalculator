class UpdateRecipeException(Exception):

    def __init__(self, missing_keys, existing_keys):
        message = 'Missing keys %s was not found at %s' % (missing_keys, existing_keys)
        super().__init__(message)
