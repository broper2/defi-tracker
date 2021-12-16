from abc import ABC, abstractmethod


class ValidatorAdapterBase(ABC):

    @abstractmethod
    def get_chart_data(self):
        raise NotImplementedError

    def get_display_names(self):
        raise NotImplementedError

    def get_x_axis_labels(self):
        raise NotImplementedError
