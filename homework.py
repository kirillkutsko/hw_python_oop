from typing import Union, Type, List, Dict


class InfoMessage:
    """
    Возвращает информационное сообщение о тренировке.

    Атрибуты:
    duration: float
        Длительность тренировки
    distance: float
        Пройденная дистанция
    speed: float
        Скорость
    calories: float
        Потраченные калории.
    Методы:
    get_message()
        Вернуть информационное сообщение о тренировке.
    """

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
        """
        Принять данные о пройденной тренировке.

        Вернуть информационное сообщение.
        """
        return (
            f"Тип тренировки: {self.training_type}; "
            f"Длительность: {self.duration:.3f} ч.; "
            f"Дистанция: {self.distance:.3f} км; "
            f"Ср. скорость: {self.speed:.3f} км/ч; "
            f"Потрачено ккал: {self.calories:.3f}."
        )


class Training:
    """
    Базовый класс тренировки.

    Расчитать дистанцию и среднюю скорость.
    """

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    H_IN_M: int = 60

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
            f'{self.__class__.__name__} Определите get_spent_calories()'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )
        return message


class Running(Training):
    """
    Тренировка: бег.

    Наследуемый класс рассчитать калории для бега.
    """

    COEFF_CAL_1: int = 18
    COEFF_CAL_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для бега."""
        return (
            (self.COEFF_CAL_1 * self.get_mean_speed() - self.COEFF_CAL_2)
            * self.weight / self.M_IN_KM * (self.duration * self.H_IN_M)
        )


class SportsWalking(Training):
    """
    Тренировка: спортивная ходьба.

    Наследуемый класс рассчитать калории для спортивной ходьбы.
    """

    COEFF_CAL_1: float = 0.035
    COEFF_CAL_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.COEFF_CAL_1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.COEFF_CAL_2 * self.weight)
            * (self.H_IN_M * self.duration)
        )


class Swimming(Training):
    """Тренировка: плавание.

    Наследуемый класс рассчитать калории для плавания и
    среднюю скорость.
    """

    LEN_STEP: float = 1.38
    COEFF_1: float = 1.1
    COEFF_2: int = 2

    def __init__(
        self,
        action: int,
        duration: int,
        weight: float,
        length_pool: float,
        count_pool: int
    ) -> float:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для плавания."""
        return (
            (self.get_mean_speed() + self.COEFF_1)
            * self.COEFF_2 * self.weight
        )

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения для плавания."""
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )


def read_package(workout_type: str, data: List[Union[int, float]]) -> Training:
    """Прочитать данные полученные от датчиков."""
    trackers: Dict[str, Type[Training]] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking
    }
    if workout_type in trackers:
        return trackers[workout_type](*data)
    raise Exception(f'Неизвестный тип тренировки {workout_type}')


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
