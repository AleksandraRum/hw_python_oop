from dataclasses import dataclass

from typing import Type, Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type};'
            f' Длительность: {self.duration:.3f} ч.;'
            f' Дистанция: {self.distance:.3f} км;'
            f' Ср. скорость: {self.speed:.3f} км/ч;'
            f' Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: float = 1000
    LEN_STEP: float = 0.65
    IN_MIN: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f'Определите get_spent_calories в'
            f'{self.__class__.__name__}'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFF_KCAL_1: float = 18
    COEFF_KCAL_2: float = 20

    def get_spent_calories(self) -> float:
        calories = ((self.COEFF_KCAL_1 * self.get_mean_speed()
                    - self.COEFF_KCAL_2)
                    * self.weight / self.M_IN_KM
                    * (self.duration * self.IN_MIN))
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_KCAL_W_1: float = 0.035
    COEFF_KCAL_W_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calories_w = ((self.COEFF_KCAL_W_1 * self.weight
                      + (self.get_mean_speed() ** 2 // self.height)
                      * self.COEFF_KCAL_W_2 * self.weight)
                      * (self.duration * self.IN_MIN))
        return calories_w


class Swimming(Training):
    LEN_STEP: float = 1.38
    COEFF_KCAL_SW_1: float = 1.1
    COEFF_KCAL_SW_2: float = 2
    """Тренировка: плавание."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                + self.COEFF_KCAL_SW_1)
                * self.COEFF_KCAL_SW_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_training: Dict[str, Type[Training]] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming,
    }
    if workout_type not in type_training:
        raise ValueError("неизвестный тип тренировки")
    else:
        return type_training[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
