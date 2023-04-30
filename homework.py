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
    HR_IN_MIN: int = 60

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
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        spent_calories_run = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                              * self.get_mean_speed()
                              + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                              / self.M_IN_KM
                              * self.duration * self.HR_IN_MIN)
        return spent_calories_run


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_MEAN_HEIGHT_MULTIPLIER: float = 0.035
    CALORIES_MEAN_HEIGHT_SHIFT: float = 0.029
    CONST_SKM_HR_IN_M_SEC: float = 0.278
    CONST_SANT_IN_METR: int = 100

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        spent_calories_walk: float = ((self.CALORIES_MEAN_HEIGHT_MULTIPLIER
                * self.weight
                + ((self.get_mean_speed()
                 * self.CONST_SKM_HR_IN_M_SEC) ** 2
                 / (self.height / self.CONST_SANT_IN_METR))
                * self.CALORIES_MEAN_HEIGHT_SHIFT
                * self.weight) * (self.duration * self.HR_IN_MIN))
        return spent_calories_walk


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CONST_SWM: int = 2
    CALORIES_MEAN_SWM: float = 1.1

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed_pool: float = (self.length_pool * self.count_pool
                                  / self.M_IN_KM / self.duration)
        return mean_speed_pool

    def get_spent_calories(self) -> float:
        spent_calories_pool = ((self.get_mean_speed() + self.CALORIES_MEAN_SWM)
                               * self.CONST_SWM * self.weight * self.duration)
        return spent_calories_pool


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'SWM':
        swim: int = Swimming(data[0], data[1], data[2], data[3], data[4])
        return swim
    elif workout_type == 'RUN':
        run: int = Running(data[0], data[1], data[2])
        return run
    elif workout_type == 'WLK':
        walk: int = SportsWalking(data[0], data[1], data[2], data[3])
        return walk


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
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