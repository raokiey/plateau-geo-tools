import geopandas as gpd
import yaml
from lxml import etree
from shapely import wkt
from shapely.geometry import MultiPolygon, Polygon


class CityObject(object):
    """Parse attribute and geometry of object in the given CityGML.

    Attributes:
        config_path (str): Path of configuration yaml file.
        gml_path (str): Path of target CityGML file.
    """
    def __init__(self, config_path, gml_path):
        self.config_path = config_path
        self.gml_path = gml_path

        with open(self.config_path, mode="r") as f:
            self.cfg = yaml.safe_load(f)

    def load_gml(self):
        """Load CityGML as XML format.

        Returns:
            lxml.etree._Element: The root of CityGML as a tree structure.
            dict: Dictonary of name space in used target CityGML.
        """
        tree = etree.parse(self.gml_path, parser=None)
        root = tree.getroot()
        nsmap = root.nsmap

        return root, nsmap

    def parse_geometry(self, root, nsmap):
        """Parse geometry information in the given CityGML.

        Args:
            root (lxml.etree._Element): The root of CityGML as a tree structure.
            nsmap (dict): Dictionary of name space in used target CityGML.

        Returns:
            list: List of merge MultiPolygon geometry object and WKT.
        """
        city_objects = root.xpath(".//core:cityObjectMember", namespaces=nsmap)
        num_of_objects = len(city_objects)
        geometry_list = []
        for i in range(0, num_of_objects):
            lod_geoms = city_objects[i].xpath(self.cfg["geometry"][0][0], namespaces=nsmap)
            if len(lod_geoms) != 0:
                pos_lists = lod_geoms[0].xpath(self.cfg["geometry"][0][1], namespaces=nsmap)
                lod0_geometry = self._convert_geometry_2d(pos_lists)
                geometry_list.append([lod0_geometry])
            else:
                geometry_list.append([None])

        return geometry_list

    def parse_attribute(self, root, nsmap):
        pass

    def convert_gdf(self, element_array):
        """Convert parse result to GeoDataFrame.
        Args:
            cfg (dict): Dictionary of loaded config yaml.
            element_array (numpy.array): Array of DataFrame element.
            epsg (int, optional): EPSG code of target crs. Defaults to 6668.
        Returns:
            geopandas.GeoDataFrame: GeoDataFrame of parse result.
        """
        column_names = self.cfg["column"]
        epsg = self.cfg["epsg"]
        target_crs = "EPSG:" + str(epsg)
        gdf = gpd.GeoDataFrame(element_array, columns=column_names, crs="EPSG:6668")
        if epsg != 6668:
            gdf = gdf.to_crs(target_crs)
        return gdf

    def _convert_geometry_2d(self, pos_lists):
        """Convert LOD0 poslist to MultiPolygon object.

        Args:
            pos_lists (list): List of position list in CityGML.

        Returns:
            shapely.geometry.MultiPoltgon: Object of MultiPolygon geometry.
        """
        multi_polygon_list = []
        for p in pos_lists:
            polygon_list = []
            pos_text = p.text
            pos_list = pos_text.split(' ')
            # extract x, y coordinate value
            for i in range(len(pos_list) // 3):
                polygon_list.append((float(pos_list[3*i+1]), float(pos_list[3*i])))
            multi_polygon_list.append(Polygon(polygon_list))

        return MultiPolygon(multi_polygon_list).buffer(0)

    def _convert_wkt(self, geometry):
        """Convert MultiPolygon object to Well-known text(WKT) format.

        Args:
            geometry (shapely.geometry.MultiPoltgon): Object of MultiPolygon geometry.

        Returns:
            str: Well-known text format of given MultiPolygon geometry.
        """
        lod_wkt = wkt.dumps(geometry.convex_hull)

        return lod_wkt
