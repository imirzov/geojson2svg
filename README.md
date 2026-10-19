# GEOJSON2SVG

Convert GeoJSON file to SVG and save.
CR map have proportions 2000x1155.
All parameters are set in Land child classes.

Conventions:
    mp - multipolygon
    pg - polygon
    pt - point

NOTE Call all images convertion at once (for correct inheritance):
    MapObj(State)
    MapObj(Region)
    MapObj(District)

NOTE Maps could be merged:
    MapObj(District) + MapObj(CityPart)

NOTE Apply style to see sublands in merged maps:
<style>
    path {fill: transparent; stroke: black; stroke-width: 1px}
    path#ceska-republika {fill: lightgray;}
    path#hlavni-mesto-praha {fill: pink;}
</style>
<style>
    path {stroke: red; stroke-width: 0.2px}
</style>

NOTE Граница области - это упорядоченный контур из точек.
Две области имеют одну общую границу, т.е. два склеенных контура.
Количество точек на общей границе с каждой стороны может быть разное.
Пограничный контур с каждой стороны должен иметь одинаковое число точек.
Точки на пограничных контурах должны иметь одинаковые координаты
(должны "склеиваться"). Не должно быть повторяющихся точек.

TODO Read svg_code from a file.