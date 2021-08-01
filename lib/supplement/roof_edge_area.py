def reprojection(gdf, tgt_crs):
    """Reproject in given the GeoDataFrame.
    Args:
        gdf (geopandas.GeoDataFrame): GeoDataFrame of reprojection target.
        tgt_crs (int): EPSG code of target crs.

    Returns:
        geopandas.GeoDataFrame: Reprojected GeoDataFrame.
    """
    gdf = gdf.to_crs(tgt_crs)

    return gdf


def supplement_area(gdf, field_name):
    """Supplement roof edge area attribute.
    Args:
        gdf (geopandas.GeoDataFrame): Target GeoDataFrame.
        field_name (str, optional): Roof edge area field's name.

    Returns:
        geopandas.GeoDataFrame: GeoDataFrame of complement area attribute.
    """
    area_list = []
    for _, row in gdf.iterrows():
        if (field_name == "None") or (float(row[field_name]) == 0.0):
            area_list.append(str(int(row["geometry"].area)))
        else:
            area_list.append(str(row[field_name]))
    if field_name == "None":
        gdf["図形面積"] = area_list
    else:
        gdf[field_name] = area_list

    return gdf
