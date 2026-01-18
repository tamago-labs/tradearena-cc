import { z } from "zod";
import { CronosWalletAgent } from "../../agent/wallet";
import { type McpTool } from "../../types";
import { networkInfo } from "../../config";

export const SendNativeTokenTool: McpTool = {
    name: "cronos_send_native_token",
    description: "Send native CRO tokens to another address",
    schema: {
        to_address: z.string()
            .describe("Recipient address (e.g., '0x1234...')"),
        amount: z.string()
            .describe("Amount of CRO to send in human-readable format (e.g., '1.5', '100')")
    },
    handler: async (agent: CronosWalletAgent, input: Record<string, any>) => {
        try {
            const { to_address, amount } = input;

            // Validate address
            if (!to_address.startsWith('0x') || to_address.length !== 42) {
                throw new Error('Invalid recipient address');
            }

            // Get balance before sending
            const walletInfo = await agent.getWalletInfo();
            const balanceBefore = walletInfo.nativeBalance;

            // Check if user has enough CRO
            if (parseFloat(balanceBefore) < parseFloat(amount)) {
                throw new Error(`Insufficient CRO balance. Available: ${balanceBefore}, Required: ${amount}`);
            }

            // Send native CRO
            const result = await agent.sendNativeToken(to_address as any, amount);

            return {
                status: "success",
                message: "✅ Native CRO tokens sent successfully",
                transaction_hash: result.hash,
                details: {
                    from: agent.getAddress(),
                    to: to_address,
                    amount,
                    amountWei: (parseFloat(amount) * 1e18).toString(),
                    token: 'CRO',
                    balanceBefore,
                    network: "cronos",
                    explorer_url: `${networkInfo.blockExplorer}/tx/${result.hash}`
                }
            };
        } catch (error: any) {
            throw new Error(`Failed to send native CRO tokens: ${error.message}`);
        }
    }
};
