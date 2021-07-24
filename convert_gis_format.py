import argparse
import os
import warnings

import numpy as np

from lib.utils import is_exist_path, save_file

warnings.resetwarnings()
warnings.simplefilter('ignore', DeprecationWarning)


def main():
    # set arguments
    parser = argparse.ArgumentParser(description="Convert CityGML on PLATEAU to other GIS file format.")
    parser.add_argument("module", type=str, help="(str) Thematic module of target CityGML.")
    parser.add_argument("gml_path", type=str, help="(str) Path of target CityGML.")
    parser.add_argument("save_dir", type=str, help="(str) Path to save directory.")
    parser.add_argument("--cfg_path", type=str, help="(str) Path of config yaml file.")
    parser.add_argument("--save_format", type=str, default="GeoJSON",
                        help="(str) Format of save file. Defaults to `GeoJSON`.")
    args = parser.parse_args()

    if args.module == "bldg":
        from lib.citygml.building import Building as object_parser
        if args.cfg_path is None:
            args.cfg_path = "./config/building_config.yaml"
    elif args.module == "tran":
        from lib.citygml.transportation import Transportation as object_parser
        if args.cfg_path is None:
            args.cfg_path = "./config/transportation_config.yaml"

    # load CityGML
    cfg_path = is_exist_path(args.cfg_path)
    gml_path = is_exist_path(args.gml_path)
    city_objects = object_parser(cfg_path, gml_path)
    root, nsmap = city_objects.load_gml()

    # parse information
    geom_list = city_objects.parse_geometry(root, nsmap)

    if args.module == "bldg":
        attr_list = city_objects.parse_attribute(root, nsmap)
        element_array = np.hstack([np.array(attr_list), np.array(geom_list)])

    elif args.module == "tran":
        element_array = np.array(geom_list)

    # convert GeoDataFrame
    gdf = city_objects.convert_gdf(element_array)

    # save file
    save_name = os.path.basename(gml_path).split(".")[0]
    save_name = "_".join(save_name.split("_")[:2] + [str(city_objects.cfg["epsg"])])
    save_file(gdf, args.save_dir, save_name, args.save_format)


if __name__ == "__main__":
    main()
