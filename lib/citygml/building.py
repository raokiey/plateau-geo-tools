from lib.citygml.city_object import CityObject


class Building(CityObject):
    """Parse attribute and geometry of object in the given building module CityGML.

    Attributes:
        config_path (str): Path of configuration yaml file.
        gml_path (str): Path of target CityGML file.
    """
    def __init__(self, config_path, gml_path):
        super().__init__(config_path, gml_path)

    def parse_attribute(self, root, nsmap):
        """Parse attribute information in the given building module CityGML.

        Args:
            root (lxml.etree._Element): The root of CityGML as a tree structure.
            nsmap (dict): Dictonary of name space in used target CityGML.

        Returns:
            list: List of attrbiute information each building.
        """
        city_objects = root.xpath('.//core:cityObjectMember', namespaces=nsmap)

        num_of_objects = len(city_objects)
        objects_list = []
        for i in range(0, num_of_objects):
            object_member_list = []
            for attr in self.cfg["attribute"]:
                if isinstance(attr, str):
                    try:
                        obj = city_objects[i].xpath(attr, namespaces=nsmap)
                        object_member_list.append(obj[0].text)
                    except IndexError:
                        object_member_list.append(None)
                elif isinstance(attr, list):
                    j = 0
                    while isinstance(attr[1], list):
                        obj = city_objects[i].xpath(attr[j], namespaces=nsmap)
                        attr = attr[1:]
                        j += 1
                    else:
                        try:
                            obj = city_objects[i].xpath(attr[j], namespaces=nsmap)
                            for child in attr[j+1:]:
                                object_member_list.append(obj[0].xpath(child, namespaces=nsmap)[0].text)
                        except IndexError:
                            object_member_list.append(None)
                else:
                    object_member_list.append(None)

            objects_list.append(object_member_list)

        return objects_list
