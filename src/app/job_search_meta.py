class JobSearchAppMeta(type):
    """
    Метакласс для приложения по поиску работы.
    """

    def __call__(cls, *args, **kwargs):
        """
        Создает экземпляр класса, и вызывает взаимодействие с пользователем.
        :param args: Аргументы для создания экземпляра класса.
        :param kwargs: Ключевые аргументы для создания экземпляра класса.
        :return: Экземпляр класса.
        """
        instance = super().__call__(*args, **kwargs)
        instance._interact_with_user()
        return instance
