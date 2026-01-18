import { z } from "zod";
import { CronosWalletAgent } from "../../agent/wallet";
import { type McpTool } from "../../types";
import { networkInfo } from "../../config";

export const SendERC20TokenTool: McpTool = {
    name: "cronos_send_erc20_token",
    description: "Send ERC20 tokens to another address",
    schema: {
        token_address: z.string()
            .describe("Token address or symbol (e.g., 'USDC', '0x1234...')"),
        to_address: z.string()
            .describe("Recipient address (e.g., '0x1234...')"),
        amount: z.string()
            .describe("Amount of tokens to send in human-readable format (e.g., '1.5', '100')")
    },
    handler: async (agent: CronosWalletAgent, input: Record<string, any>) => {
        try {
            const { token_address, to_address, amount } = input;

            // Validate addresses
            if (!to_address.startsWith('0x') || to_address.length !== 42) {
                throw new Error('Invalid recipient address');
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

            // Get token info and balance before sending
            const tokenInfo = await agent.getTokenInfo(tokenAddr as any);
            if (!tokenInfo) {
                throw new Error('Token not found or invalid token contract');
            }

            // Check if user has enough tokens
            if (parseFloat(tokenInfo.balance) < parseFloat(amount)) {
                throw new Error(`Insufficient token balance. Available: ${tokenInfo.balance}, Required: ${amount}`);
            }

            // Send ERC20 tokens
            const result = await agent.sendERC20Token(tokenAddr as any, to_address as any, amount);

            return {
                status: "success",
                message: "✅ ERC20 tokens sent successfully",
                transaction_hash: result.hash,
                details: {
                    from: agent.getAddress(),
                    to: to_address,
                    tokenAddress: tokenAddr,
                    tokenSymbol: tokenInfo.symbol,
                    amount,
                    amountWei: (parseFloat(amount) * Math.pow(10, tokenInfo.decimals)).toString(),
                    balanceBefore: tokenInfo.balance,
                    network: "cronos",
                    explorer_url: `${networkInfo.blockExplorer}/tx/${result.hash}`
                }
            };
        } catch (error: any) {
            throw new Error(`Failed to send ERC20 tokens: ${error.message}`);
        }
    }
};
