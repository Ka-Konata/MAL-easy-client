class UnknownStatusGiven(Exception):
    '''Raised when an invalid status is entered
    
    params:
    (str) status: The entered status'''
    
    def __init__(self, status: str) -> None:
        message = f'\'{status}\' must be one of these: (\'watching\', \'completed\', \'on_hold\', \'dropped\', \'plan_to_watch\')'
        super().__init__(message)


class UnknownOrderedbyGiven(Exception):
    '''Raised when an invalid sortedby is entered
    
    params:
    (str) sortedby: The entered sortedby'''
    
    def __init__(self, sortedby: str) -> None:
        message = f'\'{sortedby}\' must be one of these for ANIMES: (\'list_score\', \'list_updated_at\', \'anime_title\', \'anime_start_date\', \'plan_to_watch\'). or one of these for MANGAS (\'list_score\', \'list_updated_at\', \'manga_title\', \'manga_start_date\', \'manga_id\')'
        super().__init__(message)


class LimiteOver1000(Exception):
    '''Raised when the limit entered is over than 1000
    
    params:
    (str) limit: The entered limit'''
    
    def __init__(self, limit: str) -> None:
        message = f'\'{limit}\' can\'t be over than 1000'
        super().__init__(message)


class UnknownListType(Exception):
    '''Raised when an invaid list type is entered
    
    params:
    (str) type: the list type'''

    def __init__(self, type: str) -> None:
        message = f'\'{type}\' must be one of these: (user, anime, manga)'
        super().__init__(message)


class Unauthorized(Exception):
    '''Raised when an invaid token/client_id is entered'''

    def __init__(self) -> None:
        message = 'Connection Unauthorized. Token or Client ID is invalid'
        super().__init__(message)


class AtLeastOneMethod(Exception):
    '''Raised when an both username and id arguments are missing'''

    def __init__(self) -> None:
        message = 'You must insert one of these arguments: username or id'
        super().__init__(message)
