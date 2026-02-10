import os
import logging
import asyncio
from typing import Optional
from fastmcp import FastMCP
from dotenv import load_dotenv
from src.client import LichessClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

LICHESS_TOKEN = os.getenv("LICHESS_API_TOKEN")
if not LICHESS_TOKEN or LICHESS_TOKEN == "your_token_here":
    logger.warning("LICHESS_API_TOKEN is not set or still has the placeholder value.")

# Create FastMCP instance
mcp = FastMCP("Lichess")

# Shared client instance (lazy initialized to ensure it uses the right event loop if needed)
_client: Optional[LichessClient] = None

def get_client() -> LichessClient:
    global _client
    if _client is None:
        _client = LichessClient(LICHESS_TOKEN)
    return _client

@mcp.tool()
async def get_my_profile():
    """Retrieve the authenticated user's profile information."""
    return await get_client().get_my_profile()

@mcp.tool()
async def get_user_public_data(username: str):
    """Get public information about a Lichess user."""
    return await get_client().get_user_public_data(username)

@mcp.tool()
async def get_user_activity(username: str):
    """Get the recent activity of a Lichess user."""
    return await get_client().get_user_activity(username)

@mcp.tool()
async def get_ongoing_games():
    """Get the games currently being played by the authenticated user."""
    return await get_client().get_ongoing_games()

@mcp.tool()
async def get_user_games(username: str, limit: int = 10, as_pgn: bool = False):
    """Retrieve the most recent games of a user. Default limit is 10."""
    return await get_client().get_user_games(username, limit=limit, pgn=as_pgn)

@mcp.tool()
async def get_game_details(game_id: str, as_pgn: bool = False):
    """Retrieve details of a specific game by ID."""
    return await get_client().get_game_by_id(game_id, pgn=as_pgn)

@mcp.tool()
async def get_users_status(usernames: list[str]):
    """Check the online status of multiple users."""
    return await get_client().get_users_status(usernames)

@mcp.tool()
async def list_tournaments():
    """List current and upcoming Arena tournaments."""
    return await get_client().list_tournaments()

@mcp.tool()
async def get_team_info(team_id: str):
    """Get information about a Lichess team."""
    return await get_client().get_team_info(team_id)

@mcp.tool()
async def get_team_members(team_id: str):
    """Get the list of members in a team."""
    return await get_client().get_team_members(team_id)

@mcp.tool()
async def list_user_studies(username: str):
    """Get the list of studies created by a user."""
    return await get_client().list_user_studies(username)

@mcp.tool()
async def get_daily_puzzle():
    """Get the daily chess puzzle."""
    return await get_client().get_daily_puzzle()

@mcp.tool()
async def explore_opening(fen: str, source: str = "lichess", variant: str = "standard"):
    """
    Explore opening statistics from Masters or Lichess databases.
    source: 'masters' or 'lichess'
    """
    client = get_client()
    if source == "masters":
        return await client.explore_masters(fen)
    return await client.explore_lichess(fen, variant)

@mcp.tool()
async def lookup_tablebase(fen: str):
    """Lookup Syzygy tablebase for endgame positions."""
    return await get_client().lookup_tablebase(fen)

@mcp.tool()
async def create_challenge(username: str, rated: bool = False, clock_limit: int = 300, clock_increment: int = 3, color: str = "random"):
    """Challenge a user to a game."""
    return await get_client().create_challenge(
        username, 
        rated=rated, 
        clock_limit=clock_limit, 
        clock_increment=clock_increment, 
        color=color
    )

@mcp.tool()
async def make_move(game_id: str, move: str):
    """Make a move in an ongoing game (Board API). move in UCI format (e.g., 'e2e4')."""
    return await get_client().make_move(game_id, move)

if __name__ == "__main__":
    import sys
    # Handle simple transport selection if passed
    transport = "stdio"
    if "--transport" in sys.argv:
        idx = sys.argv.index("--transport")
        if idx + 1 < len(sys.argv):
            transport = sys.argv[idx + 1]
    
    mcp.run(transport=transport)
