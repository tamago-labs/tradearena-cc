import 'dotenv/config';
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CronosWalletAgent } from './agent/wallet';
import { CronosAnalytics } from './utils/cronos_analytics';
import { validateEnvironment, account, getEnvironmentConfig } from './config';
import { CronosTools } from './mcp';


// Create MCP server

function createCronosMcpServer(agent: CronosWalletAgent) {

  // Create MCP server instance
  const server = new McpServer({
    name: "cronos-mcp",
    version: "1.0.0"
  });

  // Combine all tools
  const allTools = CronosTools;

  // Register all tools
  for (const [toolKey, tool] of Object.entries(allTools)) {
    server.tool(tool.name, tool.description, tool.schema, async (params: any): Promise<any> => {
      try {
        // Execute the handler with the agent and params
        const result = await tool.handler(agent, params);

        // Format the result as MCP tool response
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      } catch (error) {
        console.error(`Tool execution error [${tool.name}]:`, error);
        // Handle errors in MCP format
        return {
          isError: true,
          content: [
            {
              type: "text",
              text: error instanceof Error
                ? error.message
                : "Unknown error occurred",
            },
          ],
        };
      }
    });
  }

  const toolCount = Object.keys(allTools).length;
  console.error(`✅ Registered ${toolCount} Cronos tools`);
  return server;
}

async function main() {
  try {
    console.error("🔍 Starting Cronos MCP Server...");

    // Validate environment before proceeding
    validateEnvironment();
    const environment = getEnvironmentConfig();

    // Initialize CronosAnalytics for SDK functionality
    CronosAnalytics.initialize();

    // Create wallet agent instance with private key if available
    const privateKey = environment.privateKey;
    const walletAgent = new CronosWalletAgent(privateKey);

    // Create and start MCP server
    const server = createCronosMcpServer(walletAgent);
    const transport = new StdioServerTransport();
    await server.connect(transport);

    const totalTools = Object.keys(CronosTools).length
    console.error(`✅ Cronos MCP Server running with ${totalTools} tools`);

  } catch (error) {
    console.error('❌ Error starting Cronos MCP server:', error);
    process.exit(1);
  }
}

// Handle shutdown gracefully
process.on('SIGINT', async () => {
  console.error('\n🛑 Shutting down Cronos MCP Server...');
  process.exit(0);
});

process.on('SIGTERM', async () => {
  console.error('\n🛑 Shutting down Cronos MCP Server...');
  process.exit(0);
});

// Start the server
main();
