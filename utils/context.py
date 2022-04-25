class context:
    @staticmethod
    def content():
        return {key: value for key, value in context.__dict__.items()
                if not key.startswith('_') and key != 'content'}
