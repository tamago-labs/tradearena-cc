import { z } from "zod";
import { Agent } from "../../agent";
import { type McpTool } from "../../types";
import { swapWith7k, get7kSwapQuote, get7kTradingPairs } from "../../tools/7k/swap";

export const SevenKSwapTool: McpTool = {
    name: "sui_7k_swap",
    description: "Swap tokens using 7k DEX aggregator for best rates across Sui DEXs.",
    schema: {
        fromToken: z.string().describe("Token symbol to swap from (e.g., 'SUI', 'USDC', 'WETH')"),
        toToken: z.string().describe("Token symbol to swap to (e.g., 'SUI', 'USDC', 'WETH')"),
        amount: z.number().positive().describe("Amount to swap")
    },
    handler: async (agent: Agent, input: Record<string, any>) => {
        try {
            const result = await swapWith7k(agent, input.fromToken, input.toToken, input.amount);
            return {
                status: "success",
                message: "Successfully swapped tokens using 7k DEX aggregator",
                transactionDigest: result.digest
            };
        } catch (error: any) {
            return {
                status: "error",
                message: error.message
            };
        }
    }
};

export const SevenKQuoteTool: McpTool = {
    name: "sui_7k_get_quote",
    description: "Get swap quote from 7k DEX aggregator with price impact and routing information.",
    schema: {
        fromToken: z.string().describe("Token symbol to swap from (e.g., 'SUI', 'USDC', 'WETH')"),
        toToken: z.string().describe("Token symbol to swap to (e.g., 'SUI', 'USDC', 'WETH')"),
        amount: z.number().positive().describe("Amount to swap")
    },
    handler: async (agent: Agent, input: Record<string, any>) => {
        try {
            const quote = await get7kSwapQuote(agent, input.fromToken, input.toToken, input.amount);
            return {
                status: "success",
                quote: quote
            };
        } catch (error: any) {
            return {
                status: "error",
                message: error.message
            };
        }
    }
};

export const SevenKTradingPairsTool: McpTool = {
    name: "sui_7k_get_trading_pairs",
    description: "Get available trading pairs from 7k DEX aggregator with liquidity information.",
    schema: {},
    handler: async (agent: Agent, input: Record<string, any>) => {
        try {
            const pairs = await get7kTradingPairs(agent);
            return {
                status: "success",
                tradingPairs: pairs
            };
        } catch (error: any) {
            return {
                status: "error",
                message: error.message
            };
        }
    }
};
