import asyncio
import httpx
import json
import logging
from typing import Any, Dict, Optional, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class LichessClient:
    BASE_URL = "https://lichess.org/api"
    
    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.headers = {
            "User-Agent": "Lichess-MCP-Server/1.0 (+github.com/google-deepmind/antigravity)",
        }
        if token:
            self.headers["Authorization"] = f"Bearer {token}"
        
        self.client = httpx.AsyncClient(
            http2=True,
            headers=self.headers,
            timeout=30.0
        )
        self.last_request_time = datetime.min
        self.rate_limit_lock = asyncio.Lock()

    async def _handle_rate_limiting(self):
        async with self.rate_limit_lock:
            now = datetime.now()
            elapsed = (now - self.last_request_time).total_seconds()
            if elapsed < 1.0:
                await asyncio.sleep(1.0 - elapsed)
            self.last_request_time = datetime.now()

    async def _request(self, method: str, path: str, **kwargs) -> Any:
        await self._handle_rate_limiting()
        
        url = f"{self.BASE_URL}/{path}" if not path.startswith("http") else path
        
        try:
            response = await self.client.request(method, url, **kwargs)
            
            if response.status_code == 429:
                logger.warning("Rate limit hit (429). Sleeping for 60 seconds.")
                await asyncio.sleep(60)
                return await self._request(method, path, **kwargs)
            
            response.raise_for_status()
            
            if "application/x-ndjson" in response.headers.get("Content-Type", ""):
                return [json.loads(line) for line in response.text.strip().split("\n") if line]
            
            if "application/json" in response.headers.get("Content-Type", ""):
                return response.json()
            
            return response.text
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Lichess API error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            raise

    async def get_my_profile(self):
        return await self._request("GET", "account")

    async def get_user_public_data(self, username: str):
        return await self._request("GET", f"user/{username}")

    async def get_user_activity(self, username: str):
        return await self._request("GET", f"user/{username}/activity")

    async def get_users_status(self, ids: List[str]):
        return await self._request("GET", "users/status", params={"ids": ",".join(ids)})

    async def get_ongoing_games(self):
        return await self._request("GET", "account/playing")

    async def get_user_games(self, username: str, limit: int = 10, pgn: bool = False):
        headers = {"Accept": "application/x-chess-pgn"} if pgn else {"Accept": "application/x-ndjson"}
        params = {"max": limit}
        return await self._request("GET", f"games/user/{username}", params=params, headers=headers)

    async def get_game_by_id(self, game_id: str, pgn: bool = False):
        headers = {"Accept": "application/x-chess-pgn"} if pgn else {"Accept": "application/json"}
        return await self._request("GET", f"game/export/{game_id}", headers=headers)

    # Tournaments
    async def list_tournaments(self):
        return await self._request("GET", "tournament")

    async def get_tournament_info(self, tournament_id: str):
        return await self._request("GET", f"tournament/{tournament_id}")

    # Teams
    async def get_team_info(self, team_id: str):
        return await self._request("GET", f"team/{team_id}")

    async def get_team_members(self, team_id: str):
        return await self._request("GET", f"team/{team_id}/users")

    # Studies
    async def list_user_studies(self, username: str):
        return await self._request("GET", f"study/by/{username}")

    # Puzzles
    async def get_daily_puzzle(self):
        return await self._request("GET", "puzzle/daily")

    async def get_puzzle_dashboard(self, days: int = 30):
        return await self._request("GET", f"puzzle/dashboard/{days}")

    # Opening Explorer
    async def explore_masters(self, fen: str):
        return await self._request("GET", "openings/masters", params={"fen": fen})

    async def explore_lichess(self, fen: str, variant: str = "standard"):
        return await self._request("GET", f"openings/lichess", params={"fen": fen, "variant": variant})

    # Tablebase
    async def lookup_tablebase(self, fen: str):
        return await self._request("GET", "https://tablebase.lichess.ovh/standard", params={"fen": fen})

    # Bot/Board API
    async def create_challenge(self, username: str, **kwargs):
        # kwargs can include clock_limit, clock_increment, days, variant, rated, color
        return await self._request("POST", f"challenge/{username}", data=kwargs)

    async def accept_challenge(self, challenge_id: str):
        return await self._request("POST", f"challenge/{challenge_id}/accept")

    async def decline_challenge(self, challenge_id: str, reason: str = "generic"):
        return await self._request("POST", f"challenge/{challenge_id}/decline", data={"reason": reason})

    async def make_move(self, game_id: str, move: str):
        # move can be UCI or SAN (if supported by endpoint, usually UCI for board API)
        return await self._request("POST", f"board/game/{game_id}/move/{move}")

    async def write_chat(self, game_id: str, room: str, text: str):
        return await self._request("POST", f"board/game/{game_id}/chat", data={"room": room, "text": text})

    async def close(self):
        await self.client.aclose()
