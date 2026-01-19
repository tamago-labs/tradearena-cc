import { z } from "zod";
import { Agent } from "../../agent";
import { type McpTool } from "../../types";
import { lendToSuilend, withdrawFromSuilend, getSuilendPositions } from "../../tools/suilend/lend";

export const SuilendLendTool: McpTool = {
    name: "sui_suilend_lend",
    description: "Lend tokens to Suilend protocol to earn interest. Supports SUI, USDC, USDT and other major tokens.",
    schema: {
        symbol: z.string().describe("Token symbol to lend (e.g., 'SUI', 'USDC', 'USDT')"),
        amount: z.number().positive().describe("Amount to lend in the token's base unit")
    },
    handler: async (agent: Agent, input: Record<string, any>) => {
        try {
            const result = await lendToSuilend(agent, { symbol: input.symbol, amount: input.amount });
            return {
                status: "success",
                message: "Successfully lent tokens to Suilend protocol",
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

export const SuilendWithdrawTool: McpTool = {
    name: "sui_suilend_withdraw",
    description: "Withdraw lent tokens from Suilend protocol.",
    schema: {
        symbol: z.string().describe("Token symbol to withdraw (e.g., 'SUI', 'USDC', 'USDT')"),
        amount: z.number().positive().describe("Amount to withdraw")
    },
    handler: async (agent: Agent, input: Record<string, any>) => {
        try {
            const result = await withdrawFromSuilend(agent, { symbol: input.symbol, amount: input.amount });
            return {
                status: "success",
                message: "Successfully withdrew tokens from Suilend protocol",
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

export const SuilendPositionsTool: McpTool = {
    name: "sui_suilend_get_positions",
    description: "Get all lending positions on Suilend protocol.",
    schema: {
        walletAddress: z.string().optional().describe("Wallet address to check positions for. If omitted, uses connected wallet.")
    },
    handler: async (agent: Agent, input: Record<string, any>) => {
        try {
            const walletAddress = input?.walletAddress || agent.walletAddress;
            const positions = await getSuilendPositions(agent, walletAddress);
            return {
                status: "success",
                positions: positions
            };
        } catch (error: any) {
            return {
                status: "error",
                message: error.message
            };
        }
    }
};
