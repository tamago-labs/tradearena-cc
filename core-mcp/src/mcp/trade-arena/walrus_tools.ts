import { z } from "zod";
import { Agent } from '../../agent'; 
import { type McpTool } from '../../types';

// Store Trade Data on Walrus Tool
export const tradeArenaWalrusStoreTool: McpTool = {
  name: 'trade_arena_walrus_store',
  description: 'Store AI trading decisions and execution context on Walrus for benchmarking and collective intelligence',
  schema: {
    agent_id: z.string().describe("Unique agent identifier"),
    ai_model: z.string().describe("AI model name (e.g., GPT-5, Claude, DeepSeek)"),

    chain: z.string().describe("Target chain (e.g., Sui, Cronos, Kaia)"),
    protocol: z.string().describe("Target protocol (e.g., Navi, KiloLend, VVS Finance)"),

    action: z.string().describe("Decision action (LONG, SHORT, SWAP, STAKE, BORROW, etc.)"),
    pair: z.string().optional().describe("Trading pair or asset focus"),
    notional_usd: z.number().optional().describe("USD notional size of the decision"),

    tx_hash: z.string().optional().describe("Transaction hash if executed"),
    entry_price: z.number().optional().describe("Entry price for the decision"),

    strategy_name: z.string().describe("Strategy name or label"),
    strategy_intent: z.string().describe("What the agent is trying to achieve"),
    risk_level: z.enum(["low", "medium", "high"]).describe("Risk level of the strategy"),

    reasoning_summary: z.string().describe("Concise reasoning"),
    signals: z.string().optional().describe("Signals or indicators used"),
    assumptions: z.string().optional().describe("Assumptions made"),

    confidence: z.number().min(0).max(100),

    epochs: z.number().min(1).default(3)
  },

  handler: async (agent: Agent, input: Record<string, any>) => {
    const tradeData = {
      timestamp: Math.floor(Date.now() / 1000),
      ...input
    };

    const blobId = await agent.storeTradeData(tradeData, input.epochs);

    return {
      success: true,
      data: { blob_id: blobId, trade_data: tradeData },
      message: `Decision stored on Walrus: ${blobId}`
    };
  }
};

// Get Trade Data from Walrus Tool
export const tradeArenaWalrusRetrieveTool: McpTool = {
  name: 'trade_arena_walrus_retrieve',
  description: 'Retrieve trade data from Walrus using blob ID',
  schema: {
    blob_id: z.string().describe("Walrus blob ID to retrieve trade data from")
  },
  handler: async (agent: Agent, input: Record<string, any>) => {
    try {
      const tradeData = await agent.getTradeData(input.blob_id);

      return {
        success: true,
        data: {
          blob_id: input.blob_id,
          trade_data: tradeData
        },
        message: `Trade data retrieved successfully from Walrus blob: ${input.blob_id}`
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
        message: `Failed to retrieve trade data from Walrus blob: ${input.blob_id}`
      };
    }
  }
};
