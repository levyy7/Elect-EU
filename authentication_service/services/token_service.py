from repositories.token_repository import TokenRepository


class TokenService:
    def __init__(self, token_repository: TokenRepository):
        self.token_repository = token_repository
    
    def store_token(self, email, token):
        self.token_repository.store_token(email, token)
        
    def get_token(self, email):
        return self.token_repository.get_token(email)
              
    

    