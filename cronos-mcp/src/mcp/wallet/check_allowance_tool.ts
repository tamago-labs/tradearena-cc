import { z } from "zod";
import { CronosWalletAgent } from "../../agent/wallet";
import { type McpTool } from "../../types";
import { networkInfo } from "../../config";

export const CheckAllowanceTool: McpTool = {
    name: "cronos_check_allowance",
    description: "Check the allowance amount that a spender can use from your token balance",
    schema: {
        token_address: z.string()
            .describe("Token address or symbol (e.g., 'USDC', '0x1234...')"),
        spender: z.string()
            .describe("Spender address (e.g., '0x1234...')")
    },
    handler: async (agent: CronosWalletAgent, input: Record<string, any>) => {
        try {
            const { token_address, spender } = input;

            // Validate spender address
            if (!spender.startsWith('0x') || spender.length !== 42) {
                throw new Error('Invalid spender address');
            }

            let tokenAddr = token_address;
            // Check if it's a known token symbol
            if (!token_address.startsWith('0x')) {
                const { TOKENS } = await import('../../config');
                const upperToken = token_address.toUpperCase();
                if (upperToken in TOKENS) {
                    tokenAddr = TOKENS[upperToken as keyof typeof TOKENS] as string;
                } else {
                    throw new Error(`Unknown token symbol: ${token_address}`);
                }
            }

            // Validate token address
            if (!tokenAddr.startsWith('0x') || tokenAddr.length !== 42) {
                throw new Error('Invalid token address');
            }

            // Get token info
            const tokenInfo = await agent.getTokenInfo(tokenAddr as any);
            if (!tokenInfo) {
                throw new Error('Token not found or invalid token contract');
            }

            // Check allowance
            const allowance = await agent.getTokenAllowance(tokenAddr as any, spender as any);

            // Convert allowance to human-readable format
            const allowanceFormatted = (parseFloat(allowance) / Math.pow(10, tokenInfo.decimals)).toString();

            return {
                status: "success",
                message: "✅ Allowance checked successfully",
                details: {
                    tokenAddress: tokenAddr,
                    tokenSymbol: tokenInfo.symbol,
                    tokenDecimals: tokenInfo.decimals,
                    owner: agent.getAddress(),
                    spender,
                    allowanceRaw: allowance,
                    allowanceFormatted,
                    isUnlimited: allowance === '115792089237316195423570985008687907853269984665640564039457584007913129639935',
                    network: "cronos"
                }
            };
        } catch (error: any) {
            throw new Error(`Failed to check allowance: ${error.message}`);
        }
    }
};
