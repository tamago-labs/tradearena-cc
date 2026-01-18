import { GetSwapQuoteTool } from "./get_swap_quote_tool";
import { ExecuteSwapTool } from "./execute_swap_tool";
import { GetPoolInfoTool } from "./get_pool_info_tool";
import { GetRouteTool } from "./get_route_tool";
import { type McpTool } from "../../types";

// DragonSwap Tools - All DragonSwap DEX operations
export const DragonSwapTools: Record<string, McpTool> = {
    // Quote and routing operations
    "dragonswap_get_quote": GetSwapQuoteTool,        // Get swap quotes without executing
    "dragonswap_get_pool_info": GetPoolInfoTool,      // Get pool information and liquidity data
    "dragonswap_get_route": GetRouteTool,             // Get best routing path (supports multi-hop)
    "dragonswap_execute_swap": ExecuteSwapTool,       // Execute token swaps
};

// Export individual tools for direct access
export {
    GetSwapQuoteTool,
    ExecuteSwapTool,
    GetPoolInfoTool,
    GetRouteTool
};

// Tool categories for better organization
export const DragonSwapToolCategories = {
    QUOTE: ["dragonswap_get_quote", "dragonswap_get_route"],
    POOL_INFO: ["dragonswap_get_pool_info"],
    TRADING: ["dragonswap_execute_swap"]
} as const;

// Helper function to get tools by category
export function getDragonSwapToolsByCategory(category: keyof typeof DragonSwapToolCategories): McpTool[] {
    const toolNames = DragonSwapToolCategories[category];
    return toolNames.map(name => DragonSwapTools[name]).filter(Boolean);
}

// Helper function to get tool descriptions
export function getDragonSwapToolDescriptions(): Record<string, string> {
    return Object.entries(DragonSwapTools).reduce((acc, [name, tool]) => {
        acc[name] = tool.description;
        return acc;
    }, {} as Record<string, string>);
}

// Default export for convenience
export default DragonSwapTools;
