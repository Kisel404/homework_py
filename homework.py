



class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    def get_message(self):
        _str = ("Тип тренировки: " + str(self.training_type) +
                "; Длительность: " + str(self.duration) +
                " ч.; Дистанция: " + str(self.distance) +
                " км; Ср. скорость: " + str(self.speed) +
                " км/ч; Потрачено ккал: " + str(self.calories)+".")
        return _str
    def __init__(self,
                 training_type,
                 duration,
                 distance,
                 speed,
                 calories) -> None:
        self.training_type = training_type
        self.duration = format(duration, '.3f')
        self.distance = format(distance, '.3f')
        self.speed = format(speed, '.3f')
        self.calories = format(calories, '.3f')

class Training:
    """Базовый класс тренировки."""

    action: float
    duration: float
    weight: float
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = float(action)
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM


    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        _res = self.get_distance() / self.duration
        return _res

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        infoMessage = InfoMessage(
                self.__class__.__name__,
                 self.duration,
                 self.get_distance(),
                 self.get_mean_speed(),
                 self.get_spent_calories())
        return infoMessage


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ):
        super().__init__(action, duration, weight)
    def get_spent_calories(self) -> float:
        return (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_HOUR



class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_MULTIPLIER1: float = 0.035
    CALORIES_MULTIPLIER2: float = 0.029
    KMH_TO_MS: float = 0.278
    METR_TO_SM: int = 100
    height: float
    def __init__(self,
                 action:int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height / self.METR_TO_SM
    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MULTIPLIER1 * self.weight + ((self.KMH_TO_MS * self.get_mean_speed())**2 / self.height) * self.CALORIES_MULTIPLIER2 * self.weight) * self.duration * self.MIN_IN_HOUR)

class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    action: int
    count_pool: int
    LEN_STEP: float = 1.38
    SPEED_KOEF: float = 1.1
    SPEED_MULTIPLIER: int = 2
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        self.length_pool = length_pool
        self.count_pool = count_pool
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.SPEED_KOEF) * self.SPEED_MULTIPLIER * self.weight * self.duration)
    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM / self.duration)

trainingTypes: dict[str, tuple[type[Training], int]] = {
    'SWM': (Swimming, 5),
    'RUN': (Running, 3),
    'WLK': (SportsWalking, 4),
    }

def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type not in trainingTypes:
        raise ValueError('Неизвестный тип тренировки: {workout_type}')

    class_, expected = trainingTypes[workout_type]
    if len(data) != expected:
        raise ValueError(f'Некорректное количество аргументов {data}')

    return class_(*data)

def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())
    return


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

