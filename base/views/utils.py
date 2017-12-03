def get_layer(dumpsters):
    features = []
    lat = 0
    long = 0
    for dumpster in dumpsters:
        fill = dumpster.percent_fill
        d_lat = dumpster.coordinates[0]
        d_long = dumpster.coordinates[1]
        lat += d_lat
        long += d_long
        if fill < 30:
            color = "green"
        elif fill > 50:
            color = "red"
        else:
            color = "yellow"
        features.append({
            "type": "Feature",
            "properties": {
                "description": f'{dumpster.address}<br/>'
                               f'<center>{str(fill)}% full</center>',
                "color": color
            },
            "geometry": {
                "type": "Point",
                "coordinates": [d_long, d_lat]
            }
        })
    layer = {
        "type": "FeatureCollection",
        "features": features
    }
    try:
        lat = lat / len(features)
        long = long / len(features)
    except ZeroDivisionError:
        pass
    return layer, lat, long