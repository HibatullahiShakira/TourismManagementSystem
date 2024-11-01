from abc import ABC, abstractmethod


class AuthenticationServiceInterface(ABC):
    @abstractmethod
    def register(self, user_data):
        pass

    @abstractmethod
    def login(self, login_data, request):
        pass

    @abstractmethod
    def logout(self, request):
        pass

    @abstractmethod
    def update_user_profile(self, user_id, user_update_data):
        pass

    @abstractmethod
    def delete_account(self, user_id):
        pass

    @abstractmethod
    def get_all_users(self, user_id):
        pass

    @abstractmethod
    def get_user_by_id(self, user_id):
        pass
