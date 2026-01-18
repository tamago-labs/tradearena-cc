import { z } from "zod";
import { CronosWalletAgent } from "../../agent/wallet";
import { type McpTool } from "../../types";
import { networkInfo } from "../../config";

export const ApproveTokenTool: McpTool = {
    name: "cronos_approve_token",
    description: "Approve a spender to use a specific amount of your tokens",
    schema: {
        token_address: z.string()
            .describe("Token address or symbol (e.g., 'USDC', '0x1234...')"),
        spender: z.string()
            .describe("Spender address (e.g., '0x1234...')"),
        amount: z.string()
            .describe("Amount to approve in human-readable format (e.g., '1.5', '100'), or 'max' for unlimited approval")
    },
    handler: async (agent: CronosWalletAgent, input: Record<string, any>) => {
        try {
            const { token_address, spender, amount } = input;

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

            // Handle "max" approval
            let approvalAmount = amount;
            if (amount.toLowerCase() === 'max') {
                approvalAmount = '115792089237316195423570985008687907853269984665640564039457584007913129639935'; // max uint256
            }

            // Get current allowance before approval
            const currentAllowance = await agent.getTokenAllowance(tokenAddr as any, spender as any);

            // Approve token
            const result = await agent.approveToken(tokenAddr as any, spender as any, approvalAmount);

            // Get new allowance after approval
            const newAllowance = await agent.getTokenAllowance(tokenAddr as any, spender as any);

            // Convert allowances to human-readable format
            const currentAllowanceFormatted = (parseFloat(currentAllowance) / Math.pow(10, tokenInfo.decimals)).toString();
            const newAllowanceFormatted = (parseFloat(newAllowance) / Math.pow(10, tokenInfo.decimals)).toString();

            return {
                status: "success",
                message: "✅ Token approved successfully",
                transaction_hash: result.hash,
                details: {
                    tokenAddress: tokenAddr,
                    tokenSymbol: tokenInfo.symbol,
                    tokenDecimals: tokenInfo.decimals,
                    owner: agent.getAddress(),
                    spender,
                    amount: amount === 'max' ? 'unlimited' : amount,
                    amountRaw: approvalAmount,
                    allowanceBefore: currentAllowance,
                    allowanceAfter: newAllowance,
                    allowanceBeforeFormatted: currentAllowanceFormatted,
                    allowanceAfterFormatted: newAllowanceFormatted,
                    isUnlimited: newAllowance === '115792089237316195423570985008687907853269984665640564039457584007913129639935',
                    network: "cronos",
                    explorer_url: `${networkInfo.blockExplorer}/tx/${result.hash}`
                }
            };
        } catch (error: any) {
            throw new Error(`Failed to approve token: ${error.message}`);
        }
    }
};
