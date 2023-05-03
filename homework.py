from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

TRAINING_INFO_MESSAGE = ('Тип тренировки: {training_type}; '
                             'Длительность: {duration:.3f} ч.; '
                             'Дистанция: {distance:.3f} км; '
                             'Ср. скорость: {speed:.3f} км/ч; '
                             'Потрачено ккал: {calories:.3f}.')

def get_message(self) -> str:
        return self.TRAINING_INFO_MESSAGE.format(training_type=self.training_type,
                                                 duration=self.duration,
                                                 distance=self.distance,
                                                 speed=self.speed,
                                                 calories=self.calories)

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
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    action: int
    duration: float
    weight: float

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        spent_calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                          * self.get_mean_speed()
                          + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                          / self.M_IN_KM
                          * self.duration * self.HR_IN_MIN)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    action: int
    duration: float
    weight: float
    height: float

    CALORIES_MEAN_HEIGHT_MULTIPLIER: float = 0.035
    CALORIES_MEAN_HEIGHT_SHIFT: float = 0.029
    CONST_SKM_HR_IN_M_SEC: float = 0.278
    CONST_SANT_IN_METR: int = 100

    def get_spent_calories(self) -> float:
        spent_calories: float = ((self.CALORIES_MEAN_HEIGHT_MULTIPLIER
                                 * self.weight
                                 + ((self.get_mean_speed()
                                  * self.CONST_SKM_HR_IN_M_SEC) ** 2
                                  / (self.height / self.CONST_SANT_IN_METR))
                                 * self.CALORIES_MEAN_HEIGHT_SHIFT
                                 * self.weight)
                                 * (self.duration * self.HR_IN_MIN))
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: int

    LEN_STEP: float = 1.38
    CONST_SWM: int = 2
    CALORIES_MEAN_SWM: float = 1.1

    def get_mean_speed(self) -> float:
        mean_speed: float = (self.length_pool * self.count_pool
                             / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        spent_calories = ((self.get_mean_speed() + self.CALORIES_MEAN_SWM)
                          * self.CONST_SWM * self.weight * self.duration)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    
    workouts = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
        }
    if workout_type in workouts:
        workout_class = workouts[workout_type]
        workout = workout_class(*data)
        return workout
    else:
        raise ValueError(f"Unknown workout type: {workout_type}")

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