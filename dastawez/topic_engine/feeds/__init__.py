"""
iDastawez Topic Engine Feeds Package
Exposes all 6 primary and secondary feeds.
"""

from .sarkari_result import fetch_sarkari_result_feed
from .online_update_stm import fetch_online_update_stm_feed
from .govt_ministries import fetch_govt_ministries_feed
from .recruitment_boards import fetch_recruitment_boards_feed
from .google_trends import fetch_google_trends_feed, get_trends_similarity_score
from .youtube_search import fetch_youtube_search_trends, get_youtube_intent_score
