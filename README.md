# GEOJSON2SVG

Convert GeoJSON file to SVG and save.

Model supports entities:

    pt - point
    ls - linestring
    pg - polygon
    mpt - mulipoint
    mls - multilinestring
    mpg - multipolygon

CR map have proportions 2000x1155.

All parameters are set in Land classes.

Call all images convertion at once (for correct inheritance):

    MapObj(State)
    MapObj(Region)
    MapObj(District)

Maps could be merged:

    MapObj(District) + MapObj(CityPart)

NOTE Граница области - это упорядоченный контур из точек. Две области имеют одну общую границу, т.е. два склеенных контура. Количество точек на общей границе с каждой стороны может быть разное. Пограничный контур с каждой стороны должен иметь одинаковое число точек. Точки на пограничных контурах должны иметь одинаковые координаты (должны "склеиваться"). Не должно быть повторяющихся точек.
