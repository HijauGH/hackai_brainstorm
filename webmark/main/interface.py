import warnings
from typing import Tuple, List, Any, Optional

import geopandas as gpd
import numpy as np
import osmnx as ox
# DEV
import pandas as pd
from catboost import CatBoostRegressor
from geopy.distance import geodesic
from scipy.spatial import cKDTree
from shapely.geometry import Point, MultiPoint
from tqdm import tqdm

from .const import ALL_POINT
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

warnings.filterwarnings('ignore', message="The indices of the two GeoSeries are different.")


model = CatBoostRegressor()
model.load_model('./main/ai/data/mediawisemodel.cbm')


def split_on_intervals(min_val, max_val, n):
    step = (max_val - min_val) / n
    intervals = [min_val + (step * x) for x in range(n + 1)]
    return intervals

def create_groups(x_intervals, y_intervals):
    groups = {}
    x_intervals = np.concatenate([[-np.inf], x_intervals, [np.inf]])
    y_intervals = np.concatenate([[-np.inf], y_intervals, [np.inf]])

    for x_i in range(len(x_intervals) - 1):
        for y_i in range(len(y_intervals) - 1):
            groups[f'x:{x_intervals[x_i]:.2f}-{x_intervals[x_i+1]:.2f}|y:{y_intervals[y_i]:.2f}-{y_intervals[y_i+1]:.2f}'] = 0

    return groups


def sort_on_groups(x_vals, y_vals, x_intervals, y_intervals, groups, only_vals=False):
    for x, y in zip(x_vals, y_vals):
        for x_i in range(len(x_intervals) - 1):
            for y_i in range(len(y_intervals) - 1):
                if (x_intervals[x_i] <= x < x_intervals[x_i + 1]) and (y_intervals[y_i] <= y < y_intervals[y_i + 1]):
                    groups[f'x:{x_intervals[x_i]:.2f}-{x_intervals[x_i+1]:.2f}|y:{y_intervals[y_i]:.2f}-{y_intervals[y_i+1]:.2f}'] += 1

    return list(groups.values()) if only_vals else groups


def create_dataset(config, gdf):
    x_intervals = split_on_intervals(config['min_xval'], config['max_xval'], config['x_ngroups'])
    y_intervals = split_on_intervals(config['min_yval'], config['max_yval'], config['y_ngroups'])

    groups = create_groups(x_intervals, y_intervals)

    groups_values = []
    for _, row in gdf.iterrows():
        points = np.array([[float(x['lat']), float(x['lon'])] for x in row['points']])
        group_values = sort_on_groups(points[:, 0], points[:, 1], x_intervals, y_intervals, groups.copy(), only_vals=True)
        groups_values.append(group_values)

    groups_values = np.array(groups_values)

    result = pd.DataFrame(groups_values, columns=list(groups.keys()))

    # Add additional features
    result['num_points'] = gdf['points'].apply(len)
    result['avg_lat'] = gdf['points'].apply(lambda x: np.mean([float(p['lat']) for p in x]))
    result['avg_lon'] = gdf['points'].apply(lambda x: np.mean([float(p['lon']) for p in x]))
    result['avg_azimuth'] = gdf['points'].apply(lambda x: np.mean([p['azimuth'] for p in x]))

    # # Add target audience features
    result['gender'] = gdf['gender'].map({'all': 0, 'male': 1, 'female': 2})
    result['ageFrom'] = gdf['ageFrom']
    result['ageTo'] = gdf['ageTo']
    result['age_range'] = gdf['ageTo'] - gdf['ageFrom']
    result['income'] = gdf['income'].map({'a': 1, 'b': 2, 'c': 3, 'ab': 4, 'bc': 5, 'ac': 6, 'abc': 7})

    #Add new features
    result['distance_to_center'] = gdf['distance_to_center']
    result['distance_to_metro'] = gdf['distance_to_metro']
    result['population_density'] = gdf['population_density']
    result['distance_to_shopping_center'] = gdf['distance_to_shopping_center']

    return result



def get_point_coordinates(gdf):
    points = []
    for geom in gdf.geometry:
        if isinstance(geom, Point):
            points.append((geom.x, geom.y))
        elif isinstance(geom, MultiPoint):
            # Для MultiPoint берем первую точку
            points.append((geom.geoms[0].x, geom.geoms[0].y))
    return np.array(points)

population_density = { # wiki
    'Центральный': 11702.67,
    'Северный': 10709.15,
    'Северо-Восточный': 14289.05,
    'Восточный': 9743.75,
    'Юго-Восточный': 12893.76,
    'Южный': 13422.73,
    'Юго-Западный': 12890.82,
    'Западный': 9312.38,
    'Северо-Западный': 11144.78,
    'Зеленоградский': 7272.25,
    'Новомосковский': 1497.79,
    'Троицкий': 181.13
}

# Load and prepare data
metro_stations = ox.features_from_place('Moscow, Russia', tags={'railway': 'station', 'station': 'subway'})
shopping_centers = ox.features_from_place('Moscow, Russia', tags={'shop': 'mall'})
moscow = ox.geocode_to_gdf('Moscow, Russia')


# Function to get centroid coordinates
def get_centroid_coords(geom):
    if geom.geom_type == 'Point':
        return (geom.y, geom.x)
    else:
        centroid = geom.centroid
        return (centroid.y, centroid.x)


# Prepare KD-trees
metro_points = np.array([get_centroid_coords(geom) for geom in metro_stations.geometry])
shopping_points = np.array([get_centroid_coords(geom) for geom in shopping_centers.geometry])
metro_tree = cKDTree(metro_points)
shopping_tree = cKDTree(shopping_points)

# Prepare spatial index
moscow_sindex = moscow.sindex


def enrich_data_vectorized(points, target_audience):
    df = pd.DataFrame(points)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat))
    gdf.crs = 'EPSG:4326'

    red_square = (55.753930, 37.620393)

    # Vectorized distance calculation
    coords = np.column_stack((gdf.geometry.y, gdf.geometry.x))
    gdf['distance_to_center'] = geodesic(red_square, coords).kilometers

    # Use KD-tree for faster nearest neighbor search
    gdf['distance_to_metro'] = metro_tree.query(coords)[0]
    gdf['distance_to_shopping_center'] = shopping_tree.query(coords)[0]

    # Vectorized district assignment
    possible_matches_index = list(moscow_sindex.intersection(gdf.total_bounds))
    possible_matches = moscow.iloc[possible_matches_index]
    points_in_districts = gpd.sjoin(gdf, possible_matches, how='left', predicate='within')
    gdf['district'] = points_in_districts['name']

    gdf['population_density'] = gdf['district'].map(population_density)

    # Add target audience data
    for key, value in target_audience.items():
        gdf[key] = value

    return create_dataset(config, gdf)


def predict_reach_batch(points_batch, target_audience):
    X = enrich_data_vectorized(points_batch, target_audience)
    return model.predict(X)


def optimize_campaign_fixed_points(all_points, target_audience, num_points, batch_size=100):
    selected_points = []
    available_points = all_points.copy()
    current_reach = 0

    pbar = tqdm(total=num_points, desc="Selecting points")

    while len(selected_points) < num_points and available_points:
        batch = available_points[:batch_size]
        reach_increases = []
        for point in batch:
            new_reach = predict_reach(selected_points + [point], target_audience)
            reach_increase = new_reach - current_reach
            reach_increases.append(reach_increase)

        best_idx = np.argmax(reach_increases)
        best_increase = reach_increases[best_idx]

        if best_increase > 0:
            best_point = batch[best_idx]
            selected_points.append(best_point)
            available_points.remove(best_point)
            current_reach += best_increase
            pbar.update(1)
        else:
            available_points = available_points[batch_size:]

    pbar.close()
    return selected_points


def chunk_data(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


prediction_cache = {}


def predict_reach(points, target_audience):
    # Convert points to a hashable type for caching
    points_key = tuple(sorted((p['lon'], p['lat']) for p in points))
    # Check if we have a cached result
    if points_key in prediction_cache:
        return prediction_cache[points_key]

    # If not in cache, compute the prediction
    df = pd.DataFrame({'points': [points], 'income': [target_audience['income']], 'gender': [target_audience['gender']],
                       'ageTo': [target_audience['ageTo']], 'ageFrom': [target_audience['ageFrom']]})

    df['geometry'] = df['points'].apply(lambda x: Point(float(x[0]['lon']), float(x[0]['lat'])))
    gdf = gpd.GeoDataFrame(df, geometry='geometry')
    gdf.crs = 'EPSG:4326'

    # Compute features
    red_square = (55.753930, 37.620393)
    gdf['distance_to_center'] = gdf.apply(lambda row: geodesic((row.geometry.y, row.geometry.x), red_square).kilometers,
                                          axis=1)

    coords = np.array([(point.y, point.x) for point in gdf.geometry])
    gdf['distance_to_metro'] = metro_tree.query(coords)[0]
    gdf['distance_to_shopping_center'] = shopping_tree.query(coords)[0]

    possible_matches_index = list(moscow_sindex.intersection(gdf.total_bounds))
    possible_matches = moscow.iloc[possible_matches_index]
    points_in_districts = gpd.sjoin(gdf, possible_matches, how='left', predicate='within')
    gdf['district'] = points_in_districts['name']
    gdf['population_density'] = gdf['district'].map(population_density)

    # Add target audience data
    for key, value in target_audience.items():
        gdf[key] = value

    # Create dataset for prediction
    X = create_dataset(config, gdf)

    # Make prediction
    prediction = model.predict(X)[0]

    # Cache the result
    prediction_cache[points_key] = prediction

    return prediction


def run_optimization(all_points, target_audience, num_points, batch_size=100):
    optimal_points = optimize_campaign_fixed_points(all_points, target_audience, num_points, batch_size)
    final_reach = predict_reach(optimal_points, target_audience)
    print(f"Optimal points: {len(optimal_points)}")
    print(f"Predicted reach: {final_reach}")
    return optimal_points, final_reach

class AI:
    """
        Класс для методотов ИИ
        """

    def ping(self, keys_type) -> dict:
        unique_points = pd.read_json('./main/ai/data/unique_points.json')
        target_audience = {
            "income": keys_type["income"],
            "gender": keys_type["gender"],
            "ageTo": keys_type["ageTo"],
            "ageFrom": keys_type["ageFrom"],
        }
        all_points = unique_points.to_dict('records')
        points, value = run_optimization(unique_points, target_audience, keys_type["adSides"])

        return {"points": points, "value": value}

    def get(self, keys_type) -> Tuple[List[List[Any]], Optional[Any]]:
        ai_data = self.ping(keys_type)
        return [[point['lat'], point['lon']] for point in ai_data.get('points')], ai_data.get('value')


class AI_Interface:
    """
    Переходник для ИИ и веб-сервера
    """

    def get_all_point() -> List[dict]:
        return [{
            "coord": ALL_POINT,
            "value": 1
        }]

    def get_coord(keys_type) -> List[dict]:
        ai = AI()
        coord, value = ai.get(keys_type)
        # return позже будет заменён
        return coord, value
