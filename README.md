# Lichess MCP Server

A comprehensive Model Context Protocol (MCP) server for the Lichess.org API.

## Status
**Completed Phase 1**: Core MCP server build with Tools for:
- Account & Users
- Game Retrieval
- Tournaments & Teams
- Puzzles & Opening Explorer
- Bot/Board API (Challenges & Moves)

## Quick Start
1. Clone this repository.
2. Initialize and Install:
   ```powershell
   .\scripts\build.ps1
   ```
3. Setup Authentication:
   - This project uses a `.env` file for security.
   - Open `.env` and replace `your_token_here` with your Lichess Personal Access Token.
   - Create a token at [lichess.org/account/oauth/token](https://lichess.org/account/oauth/token).
   - **Recommended Scopes**: `preference:read`, `challenge:write`, `board:play`, `study:read`.
4. Run the server:
   - **Default (Stdio)**: `.\scripts\start.ps1`
   - **Advanced (Stdio/SSE)**: `.\scripts\start-mcp-server.ps1 -Transport sse -Port 8000`

## Transport Options
- **Stdio**: Standard way for local integration with Claude Desktop.
- **SSE (HTTP)**: Exposes the server over HTTP (SSE) at `/sse` and `/messages`.

### Claude Desktop Configuration
To use this server with Claude Desktop, you can refer to the [mcp-config-example.json](./mcp-config-example.json) file or add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "lichess-stdio-mcp-server": {
      "command": "powershell",
      "args": [
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        "{PathToClonedRepo}/scripts/start-mcp-stdio.ps1"
      ]
    }
  }
}
```
> [!IMPORTANT]
> Make sure to use the absolute path to `start-mcp-stdio.ps1`.

## Key Features
- **Rate Limiting**: Automatic 1s delay between requests and 60s pause on 429 errors.
- **HTTP/2 Support**: Uses `httpx` with HTTP/2 for optimal performance.
- **Error Handling**: Graceful error reporting via MCP text content.
