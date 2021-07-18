from lib.citygml.city_object import CityObject


class Transportation(CityObject):
    def __init__(self, config_path, gml_path):
        super().__init__(config_path, gml_path)
