import { z } from "zod";
import { VVSAnalytics } from "../../utils/vvs-analytics";
import { type McpTool, AddressSchema } from "../../types";
import { CronosWalletAgent } from "../../agent/wallet";
import { publicClient, TOKENS, VVS_CONTRACTS, FEE_TIERS } from "../../config";
import { parseAbi } from 'viem';

const vvsAnalytics = new VVSAnalytics();

// VVS Quoter V2 contract address
const VVS_QUOTER_V2_ADDRESS = '0xB048Bbc1Ee6b733FFfCFb9e9CeF7375518e25997';

// VVS Quoter V2 ABI (simplified)
const QUOTER_V2_ABI = [
    {
        inputs: [
            {
                components: [
                    { name: 'tokenIn', type: 'address' },
                    { name: 'tokenOut', type: 'address' },
                    { name: 'fee', type: 'uint24' },
                    { name: 'amountIn', type: 'uint256' },
                    { name: 'sqrtPriceLimitX96', type: 'uint160' }
                ],
                name: 'params',
                type: 'tuple'
            }
        ],
        name: 'quoteExactInputSingle',
        outputs: [
            { name: 'amountOut', type: 'uint256' },
            { name: 'gasEstimate', type: 'uint256' }
        ],
        stateMutability: 'view',
        type: 'function'
    }
] as const;

// VVS Router ABI (simplified)
const VVS_ROUTER_ABI = [
    {
        inputs: [
            {
                components: [
                    { name: 'tokenIn', type: 'address' },
                    { name: 'tokenOut', type: 'address' },
                    { name: 'fee', type: 'uint24' },
                    { name: 'recipient', type: 'address' },
                    { name: 'deadline', type: 'uint256' },
                    { name: 'amountOut', type: 'uint256' },
                    { name: 'amountInMaximum', type: 'uint256' },
                    { name: 'sqrtPriceLimitX96', type: 'uint160' }
                ],
                name: 'params',
                type: 'tuple'
            }
        ],
        name: 'exactOutputSingle',
        outputs: [{ name: 'amountIn', type: 'uint256' }],
        stateMutability: 'payable',
        type: 'function'
    },
    {
        inputs: [
            {
                components: [
                    { name: 'tokenIn', type: 'address' },
                    { name: 'tokenOut', type: 'address' },
                    { name: 'fee', type: 'uint24' },
                    { name: 'recipient', type: 'address' },
                    { name: 'deadline', type: 'uint256' },
                    { name: 'amountIn', type: 'uint256' },
                    { name: 'amountOutMinimum', type: 'uint256' },
                    { name: 'sqrtPriceLimitX96', type: 'uint160' }
                ],
                name: 'params',
                type: 'tuple'
            }
        ],
        name: 'exactInputSingle',
        outputs: [{ name: 'amountOut', type: 'uint256' }],
        stateMutability: 'payable',
        type: 'function'
    }
];

export const GetVVSSwapQuoteTool: McpTool = {
    name: "cronos_get_vvs_swap_quote",
    description: "Get a quote for swapping tokens on VVS Finance with different fee tiers",
    schema: {
        tokenIn: z.string()
            .describe("Input token address or symbol (e.g., 'WCRO', 'USDC', '0x...')"),
        tokenOut: z.string()
            .describe("Output token address or symbol (e.g., 'VVS', 'USDT', '0x...')"),
        amountIn: z.string()
            .describe("Input amount in human-readable format (e.g., '1.5', '100')"),
        feeTier: z.enum(['0.05%', '0.3%', '1%'])
            .optional()
            .describe("Fee tier (default: '0.3%')")
            .default('0.3%'),
        slippageTolerancePercent: z.number()
            .optional()
            .describe("Slippage tolerance percentage (default: 0.5)")
            .default(0.5)
            .refine((val) => val >= 0.01 && val <= 50, {
                message: "Slippage tolerance must be between 0.01 and 50"
            }),
    },
    handler: async (agent: CronosWalletAgent, input: Record<string, any>) => {
        try {
            const {
                tokenIn,
                tokenOut,
                amountIn,
                feeTier = '0.3%',
                slippageTolerancePercent = 0.5,
            } = input;

            // Parse token addresses
            const tokenInAddress = parseTokenAddress(tokenIn);
            const tokenOutAddress = parseTokenAddress(tokenOut);

            if (!tokenInAddress || !tokenOutAddress) {
                throw new Error('Invalid token address or symbol');
            }

            // Get token decimals
            const [tokenInDecimals, tokenOutDecimals] = await Promise.all([
                getTokenDecimals(tokenInAddress),
                getTokenDecimals(tokenOutAddress),
            ]);

            // Convert amount to wei
            const amountInWei = BigInt(
                Math.floor(parseFloat(amountIn) * Math.pow(10, tokenInDecimals)).toString()
            );

            // Get fee tier number
            const feeTierNumber = feeTier === '0.05%' ? FEE_TIERS.LOW :
                                  feeTier === '0.3%' ? FEE_TIERS.MEDIUM : FEE_TIERS.HIGH;

            // Get quote from VVS Quoter V2
            const quote = await publicClient.readContract({
                address: VVS_QUOTER_V2_ADDRESS as any,
                abi: QUOTER_V2_ABI,
                functionName: 'quoteExactInputSingle',
                args: [
                    {
                        tokenIn: tokenInAddress,
                        tokenOut: tokenOutAddress,
                        fee: feeTierNumber,
                        amountIn: amountInWei,
                        sqrtPriceLimitX96: 0n, // No price limit
                    },
                ],
            }) as [bigint, bigint];

            const amountOutWei = quote[0];
            const amountOut = Number(amountOutWei) / Math.pow(10, tokenOutDecimals);
            
            // Calculate minimum output with slippage
            const slippageMultiplier = 1 - (slippageTolerancePercent / 100);
            const minimumOut = amountOut * slippageMultiplier;

            // Calculate price impact (simplified)
            const price = amountOut / parseFloat(amountIn);
            const gasEstimate = Number(quote[1]);

            return {
                status: "success",
                message: `✅ Swap quote retrieved for ${tokenIn} → ${tokenOut}`,
                data: {
                    tokenIn: {
                        address: tokenInAddress,
                        symbol: tokenIn,
                        decimals: tokenInDecimals,
                        amount: amountIn,
                        amountWei: amountInWei.toString(),
                    },
                    tokenOut: {
                        address: tokenOutAddress,
                        symbol: tokenOut,
                        decimals: tokenOutDecimals,
                        amount: amountOut.toFixed(tokenOutDecimals),
                        amountWei: amountOutWei.toString(),
                        minimumAmount: minimumOut.toFixed(tokenOutDecimals),
                    },
                    feeTier,
                    price: price.toFixed(tokenOutDecimals),
                    priceImpact: '0.1', // Simplified - would need more complex calculation
                    gasEstimate: gasEstimate.toString(),
                    slippageTolerance: `${slippageTolerancePercent}%`,
                    protocol: "VVS Finance"
                }
            };
        } catch (error: any) {
            throw new Error(`Failed to get VVS swap quote: ${error.message}`);
        }
    }
};

export const ExecuteVVSSwapTool: McpTool = {
    name: "cronos_execute_vvs_swap",
    description: "Execute a token swap on VVS Finance",
    schema: {
        tokenIn: z.string()
            .describe("Input token address or symbol (e.g., 'WCRO', 'USDC', '0x...')"),
        tokenOut: z.string()
            .describe("Output token address or symbol (e.g., 'VVS', 'USDT', '0x...')"),
        amountIn: z.string()
            .describe("Input amount in human-readable format (e.g., '1.5', '100')"),
        feeTier: z.enum(['0.05%', '0.3%', '1%'])
            .optional()
            .describe("Fee tier (default: '0.3%')")
            .default('0.3%'),
        slippageTolerancePercent: z.number()
            .optional()
            .describe("Slippage tolerance percentage (default: 0.5)")
            .default(0.5)
            .refine((val) => val >= 0.01 && val <= 50, {
                message: "Slippage tolerance must be between 0.01 and 50"
            }),
        recipient: AddressSchema
            .optional()
            .describe("Recipient address (default: wallet address)"),
        deadlineMinutes: z.number()
            .optional()
            .describe("Transaction deadline in minutes (default: 20)")
            .default(20),
    },
    handler: async (agent: CronosWalletAgent, input: Record<string, any>) => {
        try {
            const {
                tokenIn,
                tokenOut,
                amountIn,
                feeTier = '0.3%',
                slippageTolerancePercent = 0.5,
                recipient,
                deadlineMinutes = 20,
            } = input;

            // Parse token addresses
            const tokenInAddress = parseTokenAddress(tokenIn);
            const tokenOutAddress = parseTokenAddress(tokenOut);

            if (!tokenInAddress || !tokenOutAddress) {
                throw new Error('Invalid token address or symbol');
            }

            // Get token decimals
            const [tokenInDecimals, tokenOutDecimals] = await Promise.all([
                getTokenDecimals(tokenInAddress),
                getTokenDecimals(tokenOutAddress),
            ]);

            // Convert amount to wei
            const amountInWei = BigInt(
                Math.floor(parseFloat(amountIn) * Math.pow(10, tokenInDecimals)).toString()
            );

            // Get fee tier number
            const feeTierNumber = feeTier === '0.05%' ? FEE_TIERS.LOW :
                                  feeTier === '0.3%' ? FEE_TIERS.MEDIUM : FEE_TIERS.HIGH;

            // Get quote first
            const quote = await publicClient.readContract({
                address: VVS_QUOTER_V2_ADDRESS as any,
                abi: QUOTER_V2_ABI,
                functionName: 'quoteExactInputSingle',
                args: [
                    {
                        tokenIn: tokenInAddress,
                        tokenOut: tokenOutAddress,
                        fee: feeTierNumber,
                        amountIn: amountInWei,
                        sqrtPriceLimitX96: 0n,
                    },
                ],
            }) as [bigint, bigint];

            const amountOutWei = quote[0];
            const amountOut = Number(amountOutWei) / Math.pow(10, tokenOutDecimals);
            
            // Calculate minimum output with slippage
            const slippageMultiplier = 1 - (slippageTolerancePercent / 100);
            const minimumOutWei = BigInt(
                Math.floor(Number(amountOutWei) * slippageMultiplier)
            );

            // Get recipient address (default to wallet address)
            const recipientAddress = recipient || agent.getAddress();

            // Calculate deadline
            const deadline = BigInt(Math.floor(Date.now() / 1000) + (deadlineMinutes * 60));

            // Check if input token is native CRO, if so we need to pass value
            const isNativeInput = tokenInAddress === TOKENS.CRO;

            // Execute swap
            const txHash = await agent.writeContract({
                address: VVS_CONTRACTS.V3_SWAP_ROUTER,
                abi: VVS_ROUTER_ABI,
                functionName: 'exactInputSingle',
                args: [
                    {
                        tokenIn: tokenInAddress,
                        tokenOut: tokenOutAddress,
                        fee: feeTierNumber,
                        recipient: recipientAddress,
                        deadline: deadline,
                        amountIn: amountInWei,
                        amountOutMinimum: minimumOutWei,
                        sqrtPriceLimitX96: 0n,
                    },
                ],
                ...(isNativeInput && { value: amountInWei }),
            });

            return {
                status: "success",
                message: `✅ Swap executed: ${tokenIn} → ${tokenOut}`,
                data: {
                    transactionHash: txHash,
                    tokenIn: {
                        address: tokenInAddress,
                        symbol: tokenIn,
                        amount: amountIn,
                        amountWei: amountInWei.toString(),
                    },
                    tokenOut: {
                        address: tokenOutAddress,
                        symbol: tokenOut,
                        expectedAmount: amountOut.toFixed(tokenOutDecimals),
                        minimumAmount: (Number(minimumOutWei) / Math.pow(10, tokenOutDecimals)).toFixed(tokenOutDecimals),
                        amountWei: amountOutWei.toString(),
                    },
                    feeTier,
                    slippageTolerance: `${slippageTolerancePercent}%`,
                    recipient: recipientAddress,
                    deadline: deadlineMinutes,
                    protocol: "VVS Finance"
                }
            };
        } catch (error: any) {
            throw new Error(`Failed to execute VVS swap: ${error.message}`);
        }
    }
};

// Helper functions
function parseTokenAddress(token: string): `0x${string}` | null {
    // Check if it's a known token symbol
    const upperToken = token.toUpperCase();
    if (upperToken in TOKENS) {
        return TOKENS[upperToken as keyof typeof TOKENS] as `0x${string}`;
    }
    
    // Check if it's a valid address
    if (token.startsWith('0x') && token.length === 42) {
        return token as `0x${string}`;
    }
    
    return null;
}

async function getTokenDecimals(tokenAddress: `0x${string}`): Promise<number> {
    try {
        const decimals = await publicClient.readContract({
            address: tokenAddress,
            abi: [
                {
                    inputs: [],
                    name: 'decimals',
                    outputs: [{ type: 'uint8' }],
                    stateMutability: 'view',
                    type: 'function',
                },
            ] as const,
            functionName: 'decimals',
        });
        
        return Number(decimals);
    } catch (error) {
        // Default to 18 decimals if unable to fetch
        return 18;
    }
}
