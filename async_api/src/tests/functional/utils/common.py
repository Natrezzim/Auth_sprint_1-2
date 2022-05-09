

class UtilsCommon:

    def create_params(self, **kwargs):
        """
        создаём словарь с параметрами для запроса
        :param kwargs:
        :return:
        """
        params = {}
        for key, val in kwargs.items():
            if val is not None:
                params[key] = val
        return params
