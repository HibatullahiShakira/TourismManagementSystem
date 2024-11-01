from .interfaces import TourServiceInterface
from .models import Tour


class TourService(TourServiceInterface):
    def create_tour(self, user, tour_data):
        if not user.is_staff:
            raise PermissionError('Only staff members can create tour')
        required_field = ['name', 'availability', 'description', 'location', 'price']
        missed_field = [field for field in required_field if field not in tour_data or not tour_data]
        if missed_field:
            raise ValueError(f'Missing Fields: {', '.join(missed_field)}')

        if tour_data['price'] <= 0:
            raise ValueError('Price must not be less than zero')

        try:
            tour = Tour.objects.create(
                name=tour_data['name'],
                availability=tour_data['availability'],
                description=tour_data['description'],
                location=tour_data['location'],
                price=tour_data['price'],
            )
            tour.save()
            print('Tour created successfully')
            return tour
        except Exception as e:
            print('Error in creating tour:', str(e))
            raise ValueError('Creating a new Tour Failed')

    def update_tour(self, user, tour_id, tour_update_data):
        if not user.is_staff:
            raise PermissionError('Only staff member can update tour')
        try:
            tour = Tour.objects.get(id=tour_id)
            for field, value in tour_update_data.items():
                if hasattr(tour, field):
                    setattr(tour, field, value)
            tour.save()
            return tour
        except Tour.DoesNotExist:
            raise ValueError('Tour with the given ID does not exist')
        except Exception as e:
            raise ValueError('Updating the Tour Failed')

    def get_tour_by_id(self, tour_id):
        try:
            tour = Tour.objects.get(id=tour_id)
            return tour
        except Tour.DoesNotExist:
            raise ValueError('Tour with the given ID does not exist')
        except Exception as e:
            raise ValueError('An error Occurred fetching the Tour data')

    def delete_tour(self, user, tour_id):
        if not user.is_staff:
            raise PermissionError('Only staff members have permission to delete a tour')
        try:
            tour = Tour.objects.get(id=tour_id)
            tour.delete()
            return {'message': 'Tour deleted successfully'}
        except Tour.DoesNotExist:
            raise ValueError('Tour with the given ID does not exist')
        except Exception as e:
            raise ValueError('Deleting the Tour Failed')

    def list_all_tour(self):
        try:
            return Tour.objects.all()
        except Exception as e:
            raise ValueError('Getting all Tours Failed')

    def get_tour_by_name(self, tour_name):
        try:
            return Tour.objects.filter(name=tour_name)
        except Tour.DoesNotExist:
            raise ValueError(f'Tour with the name {tour_name} does not exist')
        except Exception as e:
            raise ValueError(f'Getting tour with name {tour_name} failed')

    def get_tour_by_location(self, location):
        try:
            return Tour.objects.get(location=location)
        except Tour.DoesNotExist:
            raise ValueError(f'Tour this {location} does exist yet')
        except Exception as e:
            raise ValueError(f'Getting Tours with the {location}')
