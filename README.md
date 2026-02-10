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
   - **Option A (Recommended for MCP Clients)**: Pass the token via your client's `env` configuration (e.g., in VS Code `mcp.json`). This is more secure and flexible.
   - **Option B (.env file)**: Create a `.env` file in the project root and add `LICHESS_API_TOKEN=your_token_here`.
   - Create a token at [lichess.org/account/oauth/token](https://lichess.org/account/oauth/token).
   - **Recommended Scopes**: `preference:read`, `challenge:write`, `board:play`, `study:read`.
4. Run the server:
   - **Stdio (Local)**: `.\scripts\start-mcp-stdio.ps1`
   - **HTTP (SSE)**: `.\scripts\start-mcp-http.ps1`

## Transport Options
- **Stdio**: Standard for local IDE integration (Claude Desktop, VS Code).
- **SSE (HTTP)**: Use this if you want to host the server centrally.
  1. Start the server: `.\scripts\start-mcp-http.ps1`
  2. Use the `url` config in your client (see `mcp-config-example.json`).

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
        "{PathToProject}/scripts/start-mcp-stdio.ps1"
      ],
      "env": {
        "LICHESS_API_TOKEN": "your_token_here"
      }
    }
  }
}
```
> [!IMPORTANT]
> Make sure to replace `{PathToProject}` with the absolute path to your cloned repository.

## Key Features
- **Rate Limiting**: Automatic 1s delay between requests and 60s pause on 429 errors.
- **HTTP/2 Support**: Uses `httpx` with HTTP/2 for optimal performance.
- **Error Handling**: Graceful error reporting via MCP text content.
