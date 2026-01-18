import { z } from "zod";
import { CronosWalletAgent } from "../../agent/wallet";
import { type McpTool } from "../../types";
import { networkInfo, TOKENS } from "../../config";

export const UnwrapCROTool: McpTool = {
    name: "cronos_unwrap_cro",
    description: "Unwrap WCRO (Wrapped CRO) tokens back to native CRO",
    schema: {
        amount: z.string()
            .describe("Amount of WCRO to unwrap in human-readable format (e.g., '1.5', '100')")
    },
    handler: async (agent: CronosWalletAgent, input: Record<string, any>) => {
        try {
            const { amount } = input;

            // Get WCRO balance before unwrapping
            const wcroTokenInfo = await agent.getTokenInfo(TOKENS.WCRO as any);
            const balanceBefore = wcroTokenInfo?.balance || '0';

            // Check if user has enough WCRO
            if (parseFloat(balanceBefore) < parseFloat(amount)) {
                throw new Error(`Insufficient WCRO balance. Available: ${balanceBefore}, Required: ${amount}`);
            }

            // Unwrap WCRO using the wallet agent
            const result = await agent.unwrapWCRO(amount);

            return {
                status: "success",
                message: "✅ WCRO tokens unwrapped successfully",
                transaction_hash: result.hash,
                details: {
                    amount,
                    amountWei: (parseFloat(amount) * 1e18).toString(),
                    token: 'WCRO',
                    unwrappedToken: 'CRO',
                    wrappedTokenAddress: TOKENS.WCRO,
                    wcroBalanceBefore: balanceBefore,
                    network: "cronos",
                    explorer_url: `${networkInfo.blockExplorer}/tx/${result.hash}`
                }
            };
        } catch (error: any) {
            throw new Error(`Failed to unwrap WCRO: ${error.message}`);
        }
    }
};
