M_IN_KM = 1000


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type,
                 duration,
                 distance,
                 speed,
                 calories) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration: .3f} ч.; '
                f'Дистанция: {self.distance: .3f} км; '
                f'Ср. скорость: {self.speed: .3f} км/ч; '
                f'Потрачено ккал: {self.calories: .3f}. ')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65

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
        dist = self.action * self.LEN_STEP / M_IN_KM
        return dist

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avrg_speed = self.get_distance() / self.duration
        return avrg_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        info_msg = InfoMessage(training_type,
                                self.duration,
                                distance,
                                speed,
                                calories)
        return info_msg


class Running(Training):
    """Тренировка: бег."""

    CLRS_AVRG_SPEED = 18
    CLRS_AVRG_SPEED_SHIFT = 1.79

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_distance(self):
        return super().get_distance()

    def get_mean_speed(self) -> float:
        return super().get_mean_speed()


    def get_spent_calories(self):
        spent_clrs = ((self.CLRS_AVRG_SPEED * super().get_mean_speed()
                      + self.CLRS_AVRG_SPEED_SHIFT)
                      * self.weight / M_IN_KM * self.duration)
        return spent_clrs


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CLRS_AVRG_WEIGTH = 0.035
    CLRS_AVRG_HIEGTH = 0.029

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 heigth: float) -> None:
        super().__init__(action, duration, weight)
        self.heigth = heigth

    def get_distance(self):
        super().get_distance(self.action)

    def get_spent_calories(self):
        spent_clrs = ((self.CLRS_AVRG_WEIGTH * self.weight
                       + (super().get_mean_speed()**2 / self.heigth)
                       * self.CLRS_AVRG_HIEGTH * self.weight) * self.duration)
        return spent_clrs


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CLRS_AVRG_SPEED = 1.1
    CLRS_AVRG_WEIGTH = 1.79

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool,
                 count_pool) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self):
        super().get_distance(self.action)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avrg_speed = (self.length_pool * self.count_pool / M_IN_KM
                      / self.duration)
        return avrg_speed

    def get_spent_calories(self):
        spent_clrs = ((self.get_mean_speed() + self.CLRS_AVRG_SPEED)
                      * self.CLRS_AVRG_WEIGTH * self.weight * self.duration)
        return spent_clrs


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    if workout_type == training_dict['SWM']:
        swm = training_dict['SWM'](*data)
        return swm
    elif workout_type == training_dict['RUN']:
        run = training_dict['RUN'](*data)
        return run
    else:
        wlk = training_dict['WLK'](*data)
        return wlk


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
