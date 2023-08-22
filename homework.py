from __future__ import annotations
from dataclasses import asdict, dataclass


class TrainingsError(Exception):
    def __init__(self, text: str) -> None:
        self.txt = text


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    TYPE_OF_TRAINING = 'Тип тренировки: '
    DUARATION = 'Длительность: '
    DISTANCE = 'Дистанция: '
    MEAN_SPEAD = 'Ср. скорость: '
    SPENT_CALORIES = 'Потрачено ккал: '
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return ('{5}{0}; {6}{1:.3f} ч.; {7}{2:.3f} км; {8}{3:.3f} км/ч; '
                '{9}{4:.3f}.').format(*asdict(self).values(),
                                      self.TYPE_OF_TRAINING,
                                      self.DUARATION,
                                      self.DISTANCE,
                                      self.MEAN_SPEAD,
                                      self.SPENT_CALORIES)


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    M_IN_HOUR: int = 60

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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        mean_speed: float = (self.CALORIES_MEAN_SPEED_MULTIPLIER
                             * self.get_mean_speed()
                             + self.CALORIES_MEAN_SPEED_SHIFT)
        duration_in_minutes: float = self.duration * super().M_IN_HOUR
        return (mean_speed * self.weight / super().M_IN_KM
                * duration_in_minutes)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_HIEGHT_MULTIPLIER: float = 0.029
    HOUR_IN_SEC: int = 3600
    CM_IN_METRE: int = 100
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 0.278

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        duration_in_minutes: float = self.duration * super().M_IN_HOUR
        mean_speed: float = (self.get_mean_speed()
                             * self.CALORIES_MEAN_SPEED_MULTIPLIER)
        height_in_meters: float = self.height / self.CM_IN_METRE
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + (mean_speed**2 / height_in_meters)
                * self.CALORIES_HIEGHT_MULTIPLIER * self.weight)
                * duration_in_minutes)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / super().M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        mean_speed: float = ((self.get_mean_speed()
                             + self.CALORIES_MEAN_SPEED_SHIFT)
                             * self.CALORIES_MEAN_SPEED_MULTIPLIER)
        return mean_speed * self.weight * self.duration


#  Такое решение элегантнее?
#  Или лучше аннотировать data через from typing import Union;
#  data: list[Union[float, int]]????
def read_package(workout_type: str, data: list[float | int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainings: dict[str, type[Training]] = {'SWM': Swimming,
                                            'RUN': Running,
                                            'WLK': SportsWalking}
    if workout_type not in trainings:
        #  А такой вариант использования исключения
        #  будет правильнее?
        raise TrainingsError('Код тренировки не существует')
    return trainings[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list[tuple[str, list[int]]] = [('SWM', [720, 1, 80, 25, 40]),
                                             ('RUN', [15000, 1, 75]),
                                             ('WLK', [9000, 1, 75, 180])
                                             ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
