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
        """Форматирование данных о тренировке в виде строки для вывода."""
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {"{:.3f}".format(self.duration)} ч.; '
            f'Дистанция: {"{:.3f}".format(self.distance)} км; '
            f'Ср. скорость: {"{:.3f}".format(self.speed)} км/ч; '
            f'Потрачено ккал: {"{:.3f}".format(self.calories)}.'
        )

class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # Расстояние за один шаг в метрах
    M_IN_KM: int = 1000  # Константа для перевода значений из метров в километры
    KMH_IN_MSEC: float = 0.278  # Коэффициент перевода скорости из км/ч в м/с
    MIN_IN_H: int = 60  # Количество минут в часе

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action  #  Количество шагов или гребков
        self.duration = duration  # Продолжительность тренировки в часах
        self.weight = weight  # Вес пользователя

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        training_distance = self.get_distance()
        mean_speed = training_distance / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Рассчитывание количества потраченных калорий.
        Метод реализуется в классах-наследниках."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Возвращение информационного сообщения о выполненной тренировке."""
        training_type = type(self).__name__  # Динамическое получение типа тренировки
        duration = self.duration
        distance = self.get_distance()
        mean_speed = self.get_mean_speed()
        spent_calories = self.get_spent_calories()
        return InfoMessage(training_type, duration, distance, mean_speed, spent_calories)

class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18  # Коэффициент для расчета калорий
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79  # Смещение для расчета калорий

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_spent_calories(self) -> float:
        """Рассчитывание количества калорий, затраченных при беге."""
        mean_speed = Training.get_mean_speed(self)
        calories_spent = (((self.CALORIES_MEAN_SPEED_MULTIPLIER * mean_speed)
                           + self.CALORIES_MEAN_SPEED_SHIFT)
                          * self.weight / self.M_IN_KM * (self.duration * self.MIN_IN_H))
        return calories_spent

class SportsWalking(Training):
    """Класс для тренировки: спортивная ходьба."""
    KMH_IN_MSEC: float = 0.278  # Коэффициент перевода скорости из км/ч в м/с
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035  # Коэффициент веса для расчета калорий
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029  # Коэффициент роста
    CM_IN_M: int = 100  # Количество сантиметров в метре

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.height = height
        self.height = height  # Рост спортсмена в см

    def get_mean_speed(self) -> float:
        """Рассчитывание средней скорости движения в км/ч."""
        mean_speed = Training.get_mean_speed(self)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Рассчитывание количества калорий, потраченных при спортивной ходьбе."""
        mean_speed = self.get_mean_speed() * self.KMH_IN_MSEC
        training_time_in_minutes = self.duration * self.MIN_IN_H
        height_in_meters = self.height / self.CM_IN_M
        calories_spent = ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                           + (mean_speed ** 2 / height_in_meters)
                           * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
                          * training_time_in_minutes)
        return calories_spent

class Swimming(Training):
    """Класс для тренировки: плавание."""
    LEN_STEP: float = 1.38  # Расстояние за один гребок в метрах
    SWIMMING_MEAN_SPEED_SHIFT: float = 1.1  # Смещение для средней скорости
    SWIMMING_MEAN_SPEED_MULTIPLIER: int = 2  # Коэффициент для расчета калорий

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.length_pool = length_pool  # Длина бассейна в метрах
        self.count_pool = count_pool  # Сколько раз пользователь переплыл бассейн

    def get_mean_speed(self) -> float:
        """Рассчитывание средней скорости плавания в км/ч."""
        mean_speed = ((self.length_pool * self.count_pool)
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Рассчитывание количества калорий, потраченных при плавании."""
        mean_speed = self.get_mean_speed()
        calories_spent = ((mean_speed + self.SWIMMING_MEAN_SPEED_SHIFT)
                          * self.SWIMMING_MEAN_SPEED_MULTIPLIER
                          * self.weight * self.duration)
        return calories_spent

def read_package(workout_type: str, data: list) -> Training:
    """Создание объекта тренировки на основе данные полученные от датчиков."""
    workout_codes = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    #  Динамическое создание экземпляра класса, соответствующего типу тренировки
    return workout_codes[workout_type](*data)

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