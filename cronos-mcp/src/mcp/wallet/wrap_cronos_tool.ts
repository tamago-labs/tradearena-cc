import { z } from "zod";
import { CronosWalletAgent } from "../../agent/wallet";
import { type McpTool } from "../../types";
import { networkInfo, TOKENS } from "../../config";

export const WrapCROTool: McpTool = {
    name: "cronos_wrap_cro",
    description: "Wrap native CRO tokens into WCRO (Wrapped CRO)",
    schema: {
        amount: z.string()
            .describe("Amount of CRO to wrap in human-readable format (e.g., '1.5', '100')")
    },
    handler: async (agent: CronosWalletAgent, input: Record<string, any>) => {
        try {
            const { amount } = input;

            // Get balance before wrapping
            const walletInfo = await agent.getWalletInfo();
            const balanceBefore = walletInfo.nativeBalance;

            // Check if user has enough CRO
            if (parseFloat(balanceBefore) < parseFloat(amount)) {
                throw new Error(`Insufficient CRO balance. Available: ${balanceBefore}, Required: ${amount}`);
            }

            // Wrap CRO using the wallet agent
            const result = await agent.wrapCRO(amount);

            return {
                status: "success",
                message: "✅ CRO tokens wrapped successfully",
                transaction_hash: result.hash,
                details: {
                    amount,
                    amountWei: (parseFloat(amount) * 1e18).toString(),
                    token: 'CRO',
                    wrappedToken: 'WCRO',
                    wrappedTokenAddress: TOKENS.WCRO,
                    balanceBefore,
                    network: "cronos",
                    explorer_url: `${networkInfo.blockExplorer}/tx/${result.hash}`
                }
            };
        } catch (error: any) {
            throw new Error(`Failed to wrap CRO: ${error.message}`);
        }
    }
};
