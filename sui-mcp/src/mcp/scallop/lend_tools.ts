import { z } from "zod";
import { Agent } from "../../agent";
import { type McpTool } from "../../types";
import { lendToScallop, withdrawFromScallop, getScallopPositions } from "../../tools/scallop/lend";

export const ScallopLendTool: McpTool = {
    name: "sui_scallop_lend",
    description: "Lend tokens to Scallop protocol to earn interest. Supports SUI and other major tokens.",
    schema: {
        coinType: z.string().describe("Type of coin to lend (e.g., '0x2::sui::SUI' for SUI)"),
        amount: z.number().positive().describe("Amount to lend in the token's base unit")
    },
    handler: async (agent: Agent, input: Record<string, any>) => {
        try {
            const result = await lendToScallop(agent, input.coinType, input.amount);
            return {
                status: "success",
                message: "Successfully lent tokens to Scallop protocol",
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

export const ScallopWithdrawTool: McpTool = {
    name: "sui_scallop_withdraw",
    description: "Withdraw lent tokens from Scallop protocol.",
    schema: {
        coinType: z.string().describe("Type of coin to withdraw"),
        amount: z.number().positive().describe("Amount to withdraw")
    },
    handler: async (agent: Agent, input: Record<string, any>) => {
        try {
            const result = await withdrawFromScallop(agent, input.coinType, input.amount);
            return {
                status: "success",
                message: "Successfully withdrew tokens from Scallop protocol",
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

export const ScallopGetPositionsTool: McpTool = {
    name: "sui_scallop_get_positions",
    description: "Get all lending positions on Scallop protocol.",
    schema: {
        walletAddress: z.string().optional().describe("Wallet address to check positions for. If omitted, uses connected wallet.")
    },
    handler: async (agent: Agent, input: Record<string, any>) => {
        try {
            const walletAddress = input?.walletAddress || agent.walletAddress;
            const positions = await getScallopPositions(agent, walletAddress);
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
