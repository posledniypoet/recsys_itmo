from .recommender import Recommender
from .contextual import Contextual
from .indexed import Indexed
from .random import Random
from .sticky_artist import StickyArtist
from .toppop import TopPop


class MyRecommender(Recommender):
    def __init__(self, tracks_redis, artists_redis, recommendations_redis, catalog, last_best_track: int,
                 last_best_track_time: float,
                 count_medium_tracks: int):
        self.tracks_redis = tracks_redis
        self.artists_redis = artists_redis
        self.catalog = catalog
        self.random = Random(tracks_redis)
        self.fallback_toppop = TopPop(catalog.top_tracks, self.random)
        self.fallback_contextual = Contextual(tracks_redis, catalog, self.fallback_toppop)
        self.fallback_indexed = Indexed(recommendations_redis, catalog, self.fallback_contextual)
        self.fallback_sticky_artist = StickyArtist(tracks_redis.connection, artists_redis.connection, catalog)
        if last_best_track is not None:
            self.last_best_track = last_best_track
            self.last_best_track_time = last_best_track_time
        else:
            self.last_best_track_time = float(0)
            self.last_best_track = 0
        if count_medium_tracks is not None:
            self.count_medium_tracks = count_medium_tracks
        else:
            self.count_medium_tracks = 0

    def recommend_next(self, user: int, prev_track: int, prev_track_time: float) -> int:
        track_data = self.tracks_redis.get(prev_track)

        if track_data is not None:
            track = self.catalog.from_bytes(track_data)
        else:
            raise ValueError(f"Track not found: {prev_track}")

        artist_data = self.artists_redis.get(track.artist)
        if artist_data is not None:
            artist_tracks = self.catalog.from_bytes(artist_data)
        else:
            raise ValueError(f"Artist not found: {prev_track}")
        if len(artist_tracks) <= 1 and prev_track_time >= 0.5:
            try:
                return self.fallback_contextual.recommend_next(user, prev_track, prev_track_time)
            except ValueError:
                return self.fallback_indexed.recommend_next(user, prev_track, prev_track_time)
        elif len(artist_tracks) <= 1 and prev_track_time < 0.5:
            try:
                return self.fallback_indexed.recommend_next(user, prev_track, prev_track_time)
            except ValueError:
                return self.fallback_toppop.recommend_next(user, prev_track, prev_track_time)
        if prev_track_time >= 0.7:
            self.last_best_track = prev_track
            self.last_best_track_time = prev_track_time
            self.count_medium_tracks = 0
            try:
                return self.fallback_sticky_artist.recommend_next(user, prev_track, prev_track_time)
            except ValueError:
                return self.fallback_contextual.recommend_next(user, prev_track, prev_track_time)
        elif 0.7 > prev_track_time >= 0.5:
            self.count_medium_tracks += 1
            if self.count_medium_tracks >= 10:
                try:
                    return self.fallback_contextual.recommend_next(user, self.last_best_track,
                                                                   self.last_best_track_time)
                except ValueError:
                    return self.fallback_indexed.recommend_next(user, prev_track, prev_track_time)
            else:
                try:
                    return self.fallback_sticky_artist.recommend_next(user, prev_track, prev_track_time)
                except ValueError:
                    return self.fallback_indexed.recommend_next(user, prev_track, prev_track_time)
        elif 0.5 > prev_track_time:
            try:
                return self.fallback_contextual.recommend_next(user, self.last_best_track, self.last_best_track_time)
            except ValueError:
                return self.fallback_indexed.recommend_next(user, prev_track, prev_track_time)
