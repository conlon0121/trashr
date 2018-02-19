import ast
import json

import numpy
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point, MultiPoint
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import View
from django_tables2 import RequestConfig
from sklearn.cluster import KMeans

from base.forms import DumpsterSelectForm, RouteDateForm
from base.models import Dumpster, Route
from base.tables import RouteTable
from base.views.utils import get_layer


@method_decorator(login_required, name='dispatch')
class RouteView(View):
    template_name = "logged_in/route.html"
    invalid_template_name = "logged_in/dashboard.html"
    form_class_select = DumpsterSelectForm
    form_class_date = RouteDateForm

    def get(self, request):
        routes = Route.objects.filter(date=Route.objects.latest('date').date)
        table = RouteTable(routes)
        route_geometries = [{'coordinates': [], 'type': 'LineString'} for _ in range(routes.count())]
        dumpsters = []
        for i, route in enumerate(routes):
            route_geometries[i]['coordinates'].extend([list(coords) for coords in route.coordinates.coords])
            dumpsters.extend(route.dumpsters.all())
        layer, lat, long = get_layer(dumpsters)

        return render(request, self.template_name, {'table': table,
                                                    'layer': json.dumps(layer),
                                                    'route_geometries': json.dumps(route_geometries),
                                                    'lat': lat,
                                                    'long': long,
                                                    'colors': route_colors(),
                                                    'date_form': RouteDateForm(),
                                                    'date': timezone.localtime().date().strftime("%m/%d/%Y"),
                                                    })

    def post(self, request):
        Route.objects.filter(date=timezone.localtime().date()).delete()
        form = DumpsterSelectForm(request.POST)
        if form.is_valid():
            form_vals = form.cleaned_data
            drivers = int(form_vals['drivers'][0][:1])
            dumpster_ids = ast.literal_eval(form_vals['dumpsters'])
            dumpsters = Dumpster.objects.filter(id__in=dumpster_ids)
            layer, lat, long = get_layer(dumpsters)
            clusters = k_means(drivers, dumpsters)
            route_geometries = []
            routes = []
            drivers = ['Samuel Adams', 'James Moriarty', 'Alex Hamilton', 'Mark Hamill', 'Zach Sharp',
                       'Shaun Jacobs', 'Nick Conlon', 'Goutham Subramanian', 'Nick Sischo', 'Hartley LeRoy']
            errors = 0
            for i, cluster in enumerate(clusters):
                route = mapbox_api_call([35.789500, -78.684436], cluster[1])
                if route:
                    route_geometries.append(route['geometry'])
                    route = Route.objects.create(time_estimate=round(route['duration'] / 60),
                                                 number_of_dumpsters=len(cluster[0]),
                                                 driver=drivers[i],
                                                 coordinates=MultiPoint(
                                                     [Point(*coords) for coords in route['geometry']['coordinates']]
                                                 ))
                    route.dumpsters.add(*cluster[0])
                    routes.append(route)
                else:
                    errors += 1
            table = RouteTable(routes)
            args = {'table': table,
                    'layer': json.dumps(layer),
                    'route_geometries': json.dumps(route_geometries),
                    'lat': lat,
                    'long': long,
                    'colors': route_colors(),
                    'date_form': RouteDateForm(),
                    'date': timezone.localtime().date().strftime("%m/%d/%Y"),
                    }
            if errors:
                args.update({'errors': f'There was an error calculating {errors} route(s)'})
            return render(request, self.template_name, args)
        return render(request, self.template_name, {'errors': 'Invalid form submission'})


class RouteUpdateView(View):
    form_class = RouteDateForm
    template_name = 'route_view.html'

    def post(self, request):
        form = RouteDateForm(request.POST)
        if form.is_valid():
            form_vals = form.cleaned_data
            routes = Route.objects.filter(date=form_vals['date'])
            if routes:
                table = RouteTable(routes)
                RequestConfig(request).configure(table)
                route_geometries = [{'coordinates': [], 'type': 'LineString'} for _ in range(routes.count())]
                dumpsters = []
                for i, route in enumerate(routes):
                    route_geometries[i]['coordinates'].extend([list(coords) for coords in route.coordinates.coords])
                    dumpsters.extend(route.dumpsters.all())
                layer, lat, long = get_layer(dumpsters)
            return render(request, self.template_name,
                          {'table': table,
                           'layer': json.dumps(layer),
                           'route_geometries': json.dumps(route_geometries),
                           'lat': lat,
                           'long': long,
                           'colors': route_colors(),
                           'date_form': RouteDateForm(),
                           'date': form_vals['date'].strftime("%m/%d/%Y"),
                           })



def k_means(num_drivers, dumpsters):
    features = []
    for dumpster in dumpsters:
        features.append([*dumpster.coordinates])
    features = numpy.array(features)
    kmeans = KMeans(n_clusters=num_drivers).fit(features)
    count = 0
    clusters = [[[], []] for _ in range(num_drivers)]
    for i in kmeans.labels_:
        clusters[i][0].append(dumpsters[count])
        clusters[i][1].append(Point(*features[count]))
        count += 1
    return clusters

def route_colors():
    light_red_color = '#AB0F0F'
    light_green_color = '#196F3D'
    dark_blue_color = '#1A5276'
    dark_red_color = '#873600'
    purple_color = '#5B2C6F'
    pink_color = '#A2079B'
    light_blue_color = '#069C91'
    dark_green_color = '#3B8711'
    black_color = '#000000'
    yellow_color = '#9A7D0A'
    return [light_red_color, light_green_color, pink_color, dark_red_color,
            purple_color, dark_green_color, light_blue_color,
            dark_blue_color, black_color, yellow_color]


def mapbox_api_call(home, cluster):
    lat_long_string = str(home[1]) + ',' + str(home[0]) + ';'
    for coordinates in cluster:
        lat_long_string += str(coordinates[1]) + ',' + str(coordinates[0]) + ';'
    url = f'https://api.mapbox.com/optimized-trips/v1/mapbox/driving/{lat_long_string[:-1]}?geometries=geojson' \
          '&source=first' \
          '&access_token=pk.eyJ1IjoidHJhc2hyIiwiYSI6ImNqOHJ3MDBzZjAyZTgzNG1yNHpmZDl3Y2sifQ.q574EBc3GMSMHBH2sPGM6w'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response = response.json()
            return response['trips'][0]
    except requests.exceptions.ConnectionError:
        pass
    return False
