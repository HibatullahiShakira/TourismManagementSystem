from abc import ABC, abstractmethod


class TourServiceInterface(ABC):
    def create_tour(self, user, tour_data):
        pass

    def get_tour_by_id(self, tour_id):
        pass

    def get_tour_by_name(self, tour_name):
        pass

    def update_tour(self, tour_id, user, tour_update_data):
        pass

    def delete_tour(self, user, tour_id):
        pass

    def list_all_tour(self):
        pass

    def get_tour_by_location(self, location):
        pass
