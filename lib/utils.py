import os
import sys


def is_exist_path(path):
    """Chek the given path is exist.

    Args:
        path (str): Path of check exist target.

    Returns:
        str: The given path, if path is exist.
    """
    try:
        os.path.exists(path)
        return path
    except FileNotFoundError:
        print("{} is not found.".format(os.path.abspath(path)))
        sys.exit(1)


def save_file(gdf, save_dir, save_name, format="GeoJSON"):
    """Save to file the given GeoDataframe.

    Args:
        gdf (geopandas.GeoDataFrame): GeoDataFrame of save target.
        save_dir (str): Path of save directory.
        save_name (str): Name of save file.
        format (str, optional): Format of save file. Defaults to "GeoJSON".
    """
    # extract raw has valid geometry
    save_gdf = gdf[~(gdf["geometry"].is_empty | gdf["geometry"].isna())].reset_index(drop=True)

    if format == "GeoJSON":
        save_path = os.path.join(save_dir, save_name + ".geojson")
        save_gdf.to_file(save_path, driver="GeoJSON")

    elif format == "shp":
        save_path = os.path.join(save_dir, save_name + ".shp")
        save_gdf.to_file(save_path)

    elif format == "gpkg":
        save_path = os.path.join(save_dir, save_name + ".gpkg")
        save_gdf.to_file(save_path, layer=save_name, driver="GPKG")
