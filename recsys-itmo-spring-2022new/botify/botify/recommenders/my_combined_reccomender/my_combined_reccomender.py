import random

from ..random import Random
from ..recommender import Recommender
from ..sticky_artist import StickyArtist
from ..toppop import TopPop


class SATPR(Recommender):
    def __init__(self, tracks_redis, artists_redis, catalog,
                 alpha: float, beta: int, epsilon: float, previous_track_time):
        self.tracks_redis = tracks_redis
        self.artists_redis = artists_redis
        self.catalog = catalog
        self.jump_count = 0
        if alpha is not None and 1 > alpha > 0:
            self.alpha = alpha
        else:
            self.alpha = 0.5
        if epsilon is not None and 1 - alpha > epsilon > 0:
            self.epsilon = epsilon
        else:
            self.epsilon = self.alpha / 2
        if beta is not None and beta > 0:
            self.beta = beta
        else:
            self.beta = 5
        self.top_pop = TopPop(tracks_redis, artists_redis)
        self.random = Random(tracks_redis)
        self.sticky_artist = StickyArtist(tracks_redis, artists_redis, catalog)
        self.previous_track_time = None
        self.set_previous_track_time(previous_track_time)

    def recommend_next(self, user: int, prev_track: int, prev_track_time: float) -> int:
        artist_data, artist_tracks = StickyArtist.get_artist_data_sticky_artist(self.sticky_artist, prev_track)

        if self.jump_count >= self.beta:
            self.jump_count = 0
            self.set_previous_track_time(prev_track_time)
            return self.random.recommend_next(user, prev_track, prev_track_time)

        if len(artist_data) == 1:
            self.jump_count += 1
            self.set_previous_track_time(prev_track_time)
            return self.top_pop.recommend_next(user, prev_track, prev_track_time)

        if prev_track_time <= self.alpha:
            self.jump_count += 1
            self.set_previous_track_time(prev_track_time)
            return self.top_pop.recommend_next(user, prev_track, prev_track_time)

        if self.previous_track_time is not None and self.previous_track_time - prev_track_time > self.epsilon:
            self.set_previous_track_time(prev_track_time)
            return self.top_pop.recommend_next(user, prev_track, prev_track_time)

        index = random.randint(0, len(artist_tracks) - 1)
        self.set_previous_track_time(prev_track_time)
        return artist_tracks[index]

    def set_previous_track_time(self, prev_track_time):
        self.previous_track_time = prev_track_time
