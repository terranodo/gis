Opinionated Python + Postgis GIS.

Features:

- [ ] PostGIS Geography columns
- [ ] HTTP2 only
- [ ] Async I/O
- [ ] jsonb storage
- [ ] TopoJSON sequences output
- [ ] OpenAPI 3.0 compliant
- [ ] Provides access to features
- [ ] Provides access to layers (collection of features)
- [ ] Provides access to datasets (collection of layers)
- [ ] Provides access to maps (collection of datasets)
- [ ] Supports access to cloud optimized geotiffs


/dataset/<id>
/map/<id>
/api
/<layer_name>/<id>
/precipitation/ <- stac catlog of folders
/precipitation/<folder>/LC08_20171112_120012/ <- stac item for this dataset with overviews, etc and links to the actual geotiff.
/precipitation/<folder>/LC08_20171112_120012/ <- stac item for this dataset with overviews, etc and links to the actual geotiff.
/precipitation/<folder>/LC08_20171112_120012/1.tif <- cloud optimized geotiff

