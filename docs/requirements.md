# Requirements: Lichess MCP Server

## 1. Project Overview
The goal is to build a comprehensive Model Context Protocol (MCP) server that interfaces with the entire Lichess.org API. This server will allow LLMs (like Claude or ChatGPT) to interact with Lichess data, manage accounts, play games (via Bot/Board APIs), and perform chess analysis.

## 2. Core Features
The MCP server must implement tools for all major Lichess API domains:

### 2.1 Account & Relations
- `get_my_profile`: Retrieve the authenticated user's profile.
- `get_my_preferences`: Get user settings.
- `get_my_email`: Get account email (requires scope).
- `follow_user` / `unfollow_user`: Manage social relations.
- `block_user` / `unblock_user`: Manage blocks.

### 2.2 Users
- `get_user_public_data`: Get public info for any user.
- `get_users_status`: Check who is online/playing.
- `get_user_activity`: Recent activity of a user.
- `get_user_performance_stats`: Detailed stats for a specific variant (e.g., Blitz, Bullet).
- `search_users`: Search for users by prefix.

### 2.3 Games
- `export_game_by_id`: Retrieve a game in PGN or JSON format.
- `export_user_games`: List/stream games played by a specific user.
- `get_ongoing_games`: Get games currently being played by a user.
- `import_game`: Import a game from PGN into Lichess.

### 2.4 Tournaments & Swiss
- `list_tournaments`: Get upcoming/current Arena tournaments.
- `get_tournament_info`: Details and standings of an Arena.
- `list_swiss_tournaments`: Get Swiss tournament lists.
- `get_swiss_info`: Details and standings of a Swiss tournament.

### 2.5 Teams
- `get_team_info`: Detailed info about a team.
- `get_team_members`: List users in a team.
- `join_team` / `leave_team`: Manage team membership.
- `get_team_tournaments`: List tournaments organized by a team.

### 2.6 Studies
- `list_user_studies`: Get studies created by a user.
- `export_study_chapter`: Get PGN of a specific chapter.
- `export_study`: Export entire study as PGN.

### 2.7 Simuls, TV & Broadcasts
- `get_current_simuls`: List active simultaneous exhibitions.
- `get_tv_channels`: Get list of current TV channels and games.
- `stream_tv_game`: (Resource) Stream moves of a game on Lichess TV.
- `list_broadcasts`: Get list of official Lichess broadcasts.
- `get_broadcast_info`: Details and standings of a broadcast tournament.
- `get_broadcast_round_pgn`: Export PGN of a broadcast round.

### 2.8 Opening Explorer & Tablebase
- `explore_opening_masters`: Opening stats from the Masters database.
- `explore_opening_lichess`: Opening stats from the Lichess player database.
- `get_tablebase_lookup`: Syzygy tablebase lookup for endgame positions.

### 2.9 Puzzles
- `get_daily_puzzle`: Fetch the current puzzle of the day.
- `get_puzzle_dashboard`: Retrieve user's puzzle performance stats.
- `get_puzzle_next`: Get the next puzzle for the authenticated user.

### 2.10 Messages (Inbox)
- `send_message`: Send a private message to a user.

### 2.11 Bot & Board API (Critical)
- `stream_incoming_events`: Listen for challenges and game starts.
- `create_challenge`: Challenge another user.
- `accept_challenge` / `decline_challenge`: Handle incoming challenges.
- `make_move`: Send a move (UCI or SAN) in an ongoing game.
- `write_chat`: Send messages in the game chat.
- `resign_game` / `offer_draw`: Game conclusion controls.

## 3. MCP Specifics

### 3.1 Tools
The tools listed in Section 2 will be the primary entry points for the LLM to take actions.

### 3.2 Resources
- `lichess://game/{gameId}`: The current state and moves of a game.
- `lichess://user/{username}/games`: A list of recent games by a user.
- `lichess://tv/{channel}`: Live stream of moves from a specific TV channel.
- `lichess://study/{studyId}`: The full PGN content of a study.

### 3.3 Prompts
- `analyze-game`: A prompt template that guides the LLM through analyzing a specific game.
- `suggest-move`: A prompt that provides context (opening explorer, clock, board state) to suggest the next move.
- `team-outreach`: A template for drafting messages to team members or organizers.

## 4. Technical Implementation Details

### 4.1 Data Handling
- **NDJSON Scaling**: For streaming endpoints (like game exports), the server must parse line-delimited JSON efficiently without loading everything into memory.
- **Pagination**: Many Lichess endpoints use cursor-based or offset pagination. Tools should handle this transparently or provide `next_page` parameters to the LLM.
- **Content Types**: Prefer `application/json` where possible, but handle `application/x-chess-pgn` for game exports to provide the LLM with the most useful format for analysis.

### 4.2 Rate Limiting (Detailed)
- **Standard**: 1 request per second.
- **Burst**: Small bursts allowed but must settle back.
- **1-Minute Block**: If a 429 is received, the server must automatically pause all outgoing requests for 60 seconds.
- **User-Agent**: Must include a descriptive User-Agent as per Lichess guidelines (e.g., `Lichess-MCP-Server/1.0 (+github.com/user/repo)`).

## 5. Technology Stack
- **Language**: Python 3.10+
- **Libraries**:
    - `mcp`: The official MCP Python SDK.
    - `httpx[http2]`: For high-performance async requests (HTTP/2 is recommended by Lichess).
    - `chess`: The `python-chess` library for move validation and PGN parsing.
    - `python-dotenv`: For managing API tokens.

## 6. Authentication
- **Mechanism**: OAuth2 or Personal Access Token (PAT).
- **Scope Management**: The server should warn if a tool is called but the provided token lacks the necessary scope (e.g., `write:games`).

## 7. Technical Requirements
- **Standard Input/Output**: The server must communicate via JSON-RPC over `stdio`.
- **Tool Definitions**: Every tool must have clear descriptions and strictly typed arguments for the LLM to understand.
- **Error Handling**: Graceful handling of invalid game IDs, non-existent users, and network timeouts.

## 8. Security Considerations
- **No Hardcoded Keys**: Ensure no API keys are stored in the codebase.
- **Input Validation**: Sanitize all inputs (usernames, game IDs, PGNs) before sending to Lichess.
- **Trust**: As per user request, this server is built from scratch to ensure full control over data handling and security.

## 9. Deployment
- The server should be packaged as a standard Python package.
- Must be compatible with `mcp-cli` or integrated directly into clients like Claude Desktop.
- Provide a `docker-compose.yml` for containerized deployment if needed.
