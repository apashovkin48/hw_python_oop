class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.trainig_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f"Тип тренировки: {self.trainig_type}; "
                f"Длительность: {format(self.duration, '.3f')} ч.; "
                f"Дистанция: {format(self.distance, '.3f')} км; "
                f"Ср. скорость: {format(self.speed, '.3f')} км/ч; "
                f"Потрачено ккал: {format(self.calories, '.3f')}.")


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    TRAIN_NAME = "ОФП"
    MIN_IN_H = 60
    SEC_IN_MIN = 60

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
        """Получить среднюю скорость движения в км/ч"""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.TRAIN_NAME,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    TRAIN_NAME = "Running"
    LEN_STEP = 0.65
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_H
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    TRAIN_NAME = "SportsWalking"
    LEN_STEP = 0.65
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (
            (
                self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight
                + (
                    (self.get_mean_speed() * self.KMH_IN_MSEC)**2
                    / (self.height / self.CM_IN_M)
                )
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight
            )
            * self.duration * self.MIN_IN_H
        )


class Swimming(Training):
    """Тренировка: плавание."""
    TRAIN_NAME = "Swimming"
    LEN_STEP = 1.38
    CALORIES_WEIGHT_MULTIPLIER = 2
    CALORIES_MEAN_SPEED_SHIFT = 1.1

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
        return (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.CALORIES_WEIGHT_MULTIPLIER
            * self.weight
            * self.duration
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_names: dict[str, Training] = {
        'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking
    }
    return training_names[workout_type](*data)


def main(training: Training) -> None:
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
