class IsNotValidObjIdEx(Exception):
    def __init__(self, msg='Not Valid ObjectId', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_NOT_VALID_OBJECT_ID'

    pass