import requests
from typing import List, Optional, Dict
from ._config import BASE_URL
from ._exception import EmochiApiError, EmochiNetworkError, EmochiCharacterNotFound
from ._state import State
from .models.character import Character

class CharacterMixin:
    state: State

    def get_character(self, prompt_id: str) -> Character:
        url = f"{BASE_URL}/prompt/{prompt_id}"
        params = {"enableDisplayWelcomeMessage": "true"}
        headers = self.state.get_headers()
        try:
            r = requests.get(url, params=params, headers=headers, timeout=15)
            if r.status_code == 200:
                data = r.json()
                prompt_data = data.get("prompt", data)
                return Character.from_dict(prompt_data)
            elif r.status_code == 404:
                raise EmochiCharacterNotFound(f"Không tìm thấy nhân vật với ID '{prompt_id}'.", 404)
            else:
                raise EmochiApiError(f"Lỗi lấy chi tiết nhân vật (HTTP {r.status_code}): {r.text}", r.status_code)
        except requests.RequestException as e:
            raise EmochiNetworkError(f"Lỗi mạng khi tải nhân vật: {e}")

    def get_ranking(self, take: int = 20, period: str = "daily", ranking_type: str = "all") -> List[Character]:
        url = f"{BASE_URL}/community/ranking"
        params = {
            "rankingType": ranking_type,
            "period": period,
            "take": min(take, 30)
        }
        headers = self.state.get_headers()
        try:
            r = requests.get(url, params=params, headers=headers, timeout=15)
            if r.status_code == 200:
                data = r.json()
                characters = []
                data_list = data.get("data", [])
                if isinstance(data_list, list):
                    for group in data_list:
                        if isinstance(group, dict) and "characters" in group:
                            tag_name = group.get("tag") or ""
                            for item in group["characters"]:
                                char = Character.from_dict(item)
                                if tag_name and tag_name not in char.tags:
                                    char.tags.append(tag_name)
                                    char.category = tag_name.capitalize()
                                characters.append(char)
                return characters
            else:
                raise EmochiApiError(f"Lỗi lấy bảng xếp hạng (HTTP {r.status_code}): {r.text}", r.status_code)
        except requests.RequestException as e:
            raise EmochiNetworkError(f"Lỗi mạng khi tải bảng xếp hạng: {e}")

    def get_characters_by_tags(self, take: int = 20, period: str = "daily") -> Dict[str, List[Character]]:
        url = f"{BASE_URL}/community/ranking"
        params = {
            "rankingType": "tags",
            "period": period,
            "take": min(take, 20)
        }
        headers = self.state.get_headers()
        try:
            r = requests.get(url, params=params, headers=headers, timeout=15)
            if r.status_code == 200:
                data = r.json()
                result = {}
                data_list = data.get("data", [])
                if isinstance(data_list, list):
                    for group in data_list:
                        if isinstance(group, dict) and "characters" in group:
                            tag = group.get("tag") or "other"
                            tag_chars = []
                            for item in group["characters"]:
                                c = Character.from_dict(item)
                                c.category = tag.capitalize()
                                tag_chars.append(c)
                            result[tag] = tag_chars
                return result
            else:
                raise EmochiApiError(f"Lỗi lấy nhân vật theo tag (HTTP {r.status_code}): {r.text}", r.status_code)
        except requests.RequestException as e:
            raise EmochiNetworkError(f"Lỗi mạng khi tải nhân vật theo tag: {e}")

    def get_all_characters(self, max_total: int = 250) -> List[Character]:
        seen_ids = set()
        all_chars: List[Character] = []

        def add_chars(chars: List[Character]):
            for c in chars:
                if c.id and c.id not in seen_ids:
                    seen_ids.add(c.id)
                    all_chars.append(c)

        for period in ["daily", "weekly", "monthly"]:
            try:
                rank_chars = self.get_ranking(take=30, period=period, ranking_type="all")
                add_chars(rank_chars)
            except Exception:
                pass

        try:
            by_tags = self.get_characters_by_tags(take=20, period="daily")
            for tag, chars in by_tags.items():
                add_chars(chars)
        except Exception:
            pass

        return all_chars[:max_total]

    def search_characters(self, query: str, take: int = 20, skip: int = 0) -> List[Character]:
        url = f"{BASE_URL}/prompt/search/v2"
        params = {
            "query": query.strip(),
            "take": take,
            "skip": skip,
            "threshold": "0.8",
            "language": "en",
            "nsfw": "false",
            "deviceType": "mobile",
            "userAB": "new_search_experiment"
        }
        headers = self.state.get_headers()
        try:
            r = requests.get(url, params=params, headers=headers, timeout=15)
            if r.status_code == 200:
                data = r.json()
                results = []
                items = data.get("prompts") or data.get("data") or []
                for item in items:
                    results.append(Character.from_dict(item))
                return results
            else:
                raise EmochiApiError(f"Lỗi tìm kiếm nhân vật (HTTP {r.status_code}): {r.text}", r.status_code)
        except requests.RequestException as e:
            raise EmochiNetworkError(f"Lỗi mạng khi tìm kiếm nhân vật: {e}")
