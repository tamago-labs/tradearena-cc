import { z } from "zod";
import { Agent } from "../../agent"
import { type McpTool } from "../../types";

export const StakeSuiTool: McpTool = {
    name: "sui_stake",
    description: "Stake SUI tokens with a validator",
    schema: {
        amount: z.number().positive().describe("Amount of SUI to stake"),
        poolId: z.string().describe("Validator pool ID to stake with")
    },
    handler: async (agent: Agent, input: Record<string, any>) => {
        try {
            const result = await agent.stake(input.amount, input.poolId)
            return {
                message: `Successfully staked ${input.amount} SUI`,
                ...result
            };
        } catch (error: any) {
            throw new Error(`Failed to stake: ${error.message}`)
        }
    }
};
