import functools
from typing import Callable


def _if_can_wash(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(self: "CarWashStation", *args, **kwargs) -> None:
        if isinstance(args[0], Car):
            if self.clean_power > args[0].clean_mark:
                return func(self, *args, **kwargs)
        elif isinstance(args[0], list):
            cars = args[0]
            filtered_cars = [
                car for car in cars if car.clean_mark < self.clean_power
            ]
            return func(self,
                        filtered_cars,
                        *args[1:], **kwargs)
        return None

    return wrapper


class Car:
    def __init__(self,
                 comfort_class: int,
                 clean_mark: int,
                 brand: str) -> None:
        self.comfort_class = comfort_class
        self.clean_mark = clean_mark
        self.brand = brand


class CarWashStation:
    def __init__(self,
                 distance_from_city_center: float,
                 clean_power: int,
                 average_rating: float,
                 count_of_ratings: int) -> None:
        self.distance_from_city_center = distance_from_city_center
        self.clean_power = clean_power
        self.average_rating = average_rating
        self.count_of_ratings = count_of_ratings

    @_if_can_wash
    def serve_cars(self, cars: list[Car]) -> float:
        income = 0.0
        for car in cars:
            income += self.calculate_washing_price(car)
            self.wash_single_car(car)
        return round(income, 1)

    @_if_can_wash
    def calculate_washing_price(self, car: Car) -> float:
        delta_car_wash = self.clean_power - car.clean_mark
        price = (car.comfort_class * delta_car_wash
                 * self.average_rating / self.distance_from_city_center)
        return round(price, 1)

    @_if_can_wash
    def wash_single_car(self, car: Car) -> None:
        if self.clean_power > car.clean_mark:
            car.clean_mark = self.clean_power

    def rate_service(self, rating: float) -> None:
        sum_current_rating = self.average_rating * self.count_of_ratings
        sum_rating_new = sum_current_rating + rating
        count_ratings_new = self.count_of_ratings + 1
        self.average_rating = round(sum_rating_new / count_ratings_new, 1)
        self.count_of_ratings = count_ratings_new
