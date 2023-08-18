class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

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
        dist: float = self.action * self.LEN_STEP / self.M_IN_KM
        return dist

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avrg_speed: float = self.get_distance() / self.duration
        return avrg_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        info_msg: InfoMessage = InfoMessage(self.__str__(), self.duration,
                                            self.get_distance(),
                                            self.get_mean_speed(),
                                            self.get_spent_calories())
        return info_msg

    def __str__(self) -> str:
        return 'Training'


class Running(Training):
    """Тренировка: бег."""

    SPEED_COEF: int = 18
    SPEED_SHIFT_COEF: float = 1.79

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_distance(self) -> float:
        return super().get_distance()

    def get_mean_speed(self) -> float:
        return super().get_mean_speed()

    def get_spent_calories(self) -> float:
        avrg_speed: float = (self.SPEED_COEF * self.get_mean_speed()
                             + self.SPEED_SHIFT_COEF)
        duaration_in_minutes: float = self.duration * super().M_IN_HOUR
        spent_clrs: float = (avrg_speed * self.weight / super().M_IN_KM
                             * duaration_in_minutes)
        return spent_clrs

    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()

    def __str__(self) -> str:
        return 'Running'


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

    def get_distance(self) -> float:
        return super().get_distance()

    def get_mean_speed(self) -> float:
        return super().get_mean_speed()

    def get_spent_calories(self) -> float:
        duaration_in_minutes: float = self.duration * super().M_IN_HOUR
        avr_speed: float = self.get_mean_speed() * self.SPEED_COEFF
        height_in_meters: float = self.height / self.CM_IN_METRE
        spent_clrs: float = ((self.WEIGTH_COEFF * self.weight
                              + (avr_speed**2 / height_in_meters)
                              * self.HIEGTH_COEFF * self.weight)
                             * duaration_in_minutes)
        return spent_clrs

    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()

    def __str__(self) -> str:
        return 'SportsWalking'


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

    def get_distance(self) -> float:
        return super().get_distance()

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avrg_speed: float = (self.length_pool * self.count_pool
                             / super().M_IN_KM
                             / self.duration)
        return avrg_speed

    def get_spent_calories(self) -> float:
        avrg_speed: float = ((self.get_mean_speed() + self.SPEED_SHIFT_COEF)
                             * self.SPEED_COEF)
        spent_clrs: float = avrg_speed * self.weight * self.duration
        return spent_clrs

    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()

    def __str__(self) -> str:
        return 'Swimming'


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict: dict = {'SWM': Swimming,
                           'RUN': Running,
                           'WLK': SportsWalking}
    for key in training_dict.keys():
        if workout_type == key:
            trn: Training = training_dict[key](*data)
            return trn


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: tuple = [('SWM', [720, 1, 80, 25, 40]),
                       ('RUN', [15000, 1, 75]),
                       ('WLK', [9000, 1, 75, 180])
                       ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
