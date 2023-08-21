from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


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

    SPEED_COEF: int = 18
    SPEED_SHIFT_COEF: float = 1.79

    def get_spent_calories(self) -> float:
        average_speed: float = (self.SPEED_COEF * self.get_mean_speed()
                                + self.SPEED_SHIFT_COEF)
        duaration_in_minutes: float = self.duration * super().M_IN_HOUR
        return (average_speed * self.weight / super().M_IN_KM
                * duaration_in_minutes)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WEIGTH_COEFF: float = 0.035
    HIEGTH_COEFF: float = 0.029
    HOUR_IN_SEC: int = 3600
    CM_IN_METRE: int = 100
    SPEED_COEFF: float = 0.278

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        duaration_in_minutes: float = self.duration * super().M_IN_HOUR
        average_speed: float = self.get_mean_speed() * self.SPEED_COEFF
        height_in_meters: float = self.height / self.CM_IN_METRE
        return ((self.WEIGTH_COEFF * self.weight
                + (average_speed**2 / height_in_meters)
                * self.HIEGTH_COEFF * self.weight)
                * duaration_in_minutes)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SPEED_SHIFT_COEF: float = 1.1
    SPEED_COEF: int = 2

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
        average_speed: float = ((self.get_mean_speed() + self.SPEED_SHIFT_COEF)
                                * self.SPEED_COEF)
        return average_speed * self.weight * self.duration


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainings: dict[str, type(Training)] = {'SWM': Swimming,
                                            'RUN': Running,
                                            'WLK': SportsWalking}
    if workout_type not in trainings:
        raise Exception('Код тренировки не существует')
    return trainings[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()

    print(info.get_message())  # TODO.


if __name__ == '__main__':
    packages: list[tuple[str, list[int]]] = [('SWM', [720, 1, 80, 25, 40]),
                                             ('RUN', [15000, 1, 75]),
                                             ('WLK', [9000, 1, 75, 180])
                                             ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
