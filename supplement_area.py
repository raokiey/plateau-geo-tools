import argparse
import os

import geopandas as gpd
import yaml

from lib.supplement.roof_edge_area import supplement_area, reprojection
from lib.utils import is_exist_path, save_file


def main():
    parser = argparse.ArgumentParser(description="(str) Supplement roof edge area .")
    parser.add_argument("target_path", help="(str) Path of target file.")
    parser.add_argument("save_dir", help="(str) Path to save directory.")
    parser.add_argument("cfg_path", help="(str) Path of configurationyaml file.")
    parser.add_argument("--field_name", default="図形面積", help="(str) Name of roof edge area field.")
    parser.add_argument("--save_format", default="GeoJSON",
                        help="(str) Format of save file. Defaults to `GeoJSON`.")
    args = parser.parse_args()

    target_path = is_exist_path(args.target_path)
    config_path = is_exist_path(args.cfg_path)

    src_gdf = gpd.read_file(target_path)
    with open(config_path, mode="r") as f:
        cfg = yaml.safe_load(f)
    src_epsg = cfg["epsg"]
    if (src_epsg == 4326) or (src_epsg == 6668):
        src_gdf = reprojection(src_gdf, "EPSG:3857")

    supplement_gdf = supplement_area(src_gdf, field_name=args.field_name)

    if (src_epsg == 4326) or (src_epsg == 6668):
        src_crs = "EPSG:" + str(src_epsg)
        supplement_gdf = reprojection(supplement_gdf, src_crs)

    save_name = os.path.basename(target_path).split(".")[0]
    save_file(supplement_gdf, args.save_dir, save_name, args.save_format)


if __name__ == "__main__":
    main()
