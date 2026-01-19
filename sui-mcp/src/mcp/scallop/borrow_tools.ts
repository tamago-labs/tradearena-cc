import { z } from "zod";
import { Agent } from "../../agent";
import { type McpTool } from "../../types";
import { borrowFromScallop, repayToScallop, getScallopBorrowPositions } from "../../tools/scallop/borrow";

export const ScallopBorrowTool: McpTool = {
    name: "sui_scallop_borrow",
    description: "Borrow tokens from Scallop protocol using collateral. Deposit collateral and borrow in one transaction.",
    schema: {
        borrowCoinType: z.string().describe("Type of coin to borrow"),
        collateralCoinType: z.string().describe("Type of coin to use as collateral"),
        borrowAmount: z.number().positive().describe("Amount to borrow"),
        collateralAmount: z.number().positive().describe("Amount of collateral to deposit")
    },
    handler: async (agent: Agent, input: Record<string, any>) => {
        try {
            const result = await borrowFromScallop(
                agent, 
                input.borrowCoinType, 
                input.collateralCoinType, 
                input.borrowAmount, 
                input.collateralAmount
            );
            return {
                status: "success",
                message: "Successfully borrowed tokens from Scallop protocol",
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

export const ScallopRepayTool: McpTool = {
    name: "sui_scallop_repay",
    description: "Repay borrowed tokens to Scallop protocol.",
    schema: {
        coinType: z.string().describe("Type of coin to repay"),
        amount: z.number().positive().describe("Amount to repay")
    },
    handler: async (agent: Agent, input: Record<string, any>) => {
        try {
            const result = await repayToScallop(agent, input.coinType, input.amount);
            return {
                status: "success",
                message: "Successfully repaid tokens to Scallop protocol",
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

export const ScallopGetBorrowPositionsTool: McpTool = {
    name: "sui_scallop_get_borrow_positions",
    description: "Get all borrowing positions on Scallop protocol with health ratios.",
    schema: {
        walletAddress: z.string().optional().describe("Wallet address to check positions for. If omitted, uses connected wallet.")
    },
    handler: async (agent: Agent, input: Record<string, any>) => {
        try {
            const walletAddress = input?.walletAddress || agent.walletAddress;
            const positions = await getScallopBorrowPositions(agent, walletAddress);
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
