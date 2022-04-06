import random
from typing import List

from .random import Random
from .recommender import Recommender


class TopPop(Recommender):
    def __init__(self, top_tracks: List[int], fallback):
        self.top_tracks = top_tracks
        self.fallback = fallback

    def recommend_next(self, user: int, prev_track: int, prev_track_time: float) -> int:
        if self.top_tracks:
            shuffled = list(self.top_tracks)
            random.shuffle(shuffled)
            return shuffled[0]

        return self.fallback.recommend_next(user, prev_track, prev_track_time)
