import { z } from "zod";
import { VVSAnalytics } from "../../utils/vvs-analytics";
import { type McpTool, AddressSchema } from "../../types";

const vvsAnalytics = new VVSAnalytics();

export const GetVVSSummaryTool: McpTool = {
    name: "cronos_get_vvs_summary",
    description: "Get VVS DEX summary with top trading pairs and liquidity data",
    schema: {
        limit: z.number()
            .optional()
            .describe("Limit number of pairs returned (default: 50, max: 1000)")
            .default(50),
    },
    handler: async (input: Record<string, any>) => {
        try {
            const limit = input.limit || 50;
            const result = await vvsAnalytics.getSummary(limit);
            
            if (result.status !== 'success' || !result.data) {
                throw new Error(result.message || 'Failed to get VVS summary');
            }
            
            return {
                status: "success",
                message: `✅ VVS DEX summary retrieved`,
                data: {
                    ...result.data,
                    protocol: "VVS Finance",
                    description: "Top DEX on Cronos network",
                    wcroInfo: {
                        address: "0x5C7F8A570d578ED84E63fdFA7b1eE72dEae1AE23",
                        note: "CRO is represented as WCRO in pairs"
                    }
                }
            };
        } catch (error: any) {
            throw new Error(`Failed to get VVS summary: ${error.message}`);
        }
    }
};

export const GetVVSTokensTool: McpTool = {
    name: "cronos_get_vvs_tokens",
    description: "Get all tokens available on VVS with price information",
    schema: {
        limit: z.number()
            .optional()
            .describe("Limit number of tokens returned (default: 100, max: 1000)")
            .default(100),
    },
    handler: async (input: Record<string, any>) => {
        try {
            const limit = input.limit || 100;
            const result = await vvsAnalytics.getTokens(limit);
            
            if (result.status !== 'success' || !result.data) {
                throw new Error(result.message || 'Failed to get VVS tokens');
            }
            
            return {
                status: "success",
                message: `✅ VVS tokens retrieved`,
                data: {
                    ...result.data,
                    protocol: "VVS Finance",
                    wcroInfo: {
                        address: "0x5C7F8A570d578ED84E63fdFA7b1eE72dEae1AE23",
                        note: "Canonical WCRO address used by VVS"
                    }
                }
            };
        } catch (error: any) {
            throw new Error(`Failed to get VVS tokens: ${error.message}`);
        }
    }
};

export const GetVVSTokenInfoTool: McpTool = {
    name: "cronos_get_vvs_token_info",
    description: "Get specific token information from VVS including USD and CRO prices",
    schema: {
        tokenAddress: AddressSchema
            .describe("Token contract address (0x...)"),
    },
    handler: async (input: Record<string, any>) => {
        try {
            const result = await vvsAnalytics.getTokenInfo(input.tokenAddress);
            
            if (result.status !== 'success' || !result.data) {
                throw new Error(result.message || 'Failed to get VVS token info');
            }
            
            return {
                status: "success",
                message: `✅ VVS token info retrieved for ${input.tokenAddress}`,
                data: {
                    ...result.data,
                    protocol: "VVS Finance",
                    tokenAddress: input.tokenAddress
                }
            };
        } catch (error: any) {
            throw new Error(`Failed to get VVS token info: ${error.message}`);
        }
    }
};

export const GetVVSPairsTool: McpTool = {
    name: "cronos_get_vvs_pairs",
    description: "Get all trading pairs on VVS with detailed liquidity and volume data",
    schema: {
        limit: z.number()
            .optional()
            .describe("Limit number of pairs returned (default: 100, max: 1000)")
            .default(100),
    },
    handler: async (input: Record<string, any>) => {
        try {
            const limit = input.limit || 100;
            const result = await vvsAnalytics.getPairs(limit);
            
            if (result.status !== 'success' || !result.data) {
                throw new Error(result.message || 'Failed to get VVS pairs');
            }
            
            return {
                status: "success",
                message: `✅ VVS trading pairs retrieved`,
                data: {
                    ...result.data,
                    protocol: "VVS Finance",
                    dexInfo: {
                        type: "Automated Market Maker (AMM)",
                        chainName: "Cronos",
                        wcroAddress: "0x5C7F8A570d578ED84E63fdFA7b1eE72dEae1AE23"
                    }
                }
            };
        } catch (error: any) {
            throw new Error(`Failed to get VVS pairs: ${error.message}`);
        }
    }
};

export const GetVVSTopPairsTool: McpTool = {
    name: "cronos_get_vvs_top_pairs",
    description: "Get top VVS trading pairs by liquidity with analytics",
    schema: {
        limit: z.number()
            .optional()
            .describe("Number of top pairs to return (default: 10, max: 50)")
            .default(10),
        sortBy: z.enum(['liquidity', 'volume'])
            .optional()
            .describe("Sort criteria (default: liquidity)"),
    },
    handler: async (input: Record<string, any>) => {
        try {
            const limit = input.limit || 10;
            const sortBy = input.sortBy || 'liquidity';
            const result = await vvsAnalytics.getTopPairs(limit, sortBy);
            
            if (result.status !== 'success' || !result.data) {
                throw new Error(result.message || 'Failed to get top VVS pairs');
            }
            
            return {
                status: "success",
                message: `✅ Top ${limit} VVS pairs retrieved (sorted by ${sortBy})`,
                data: {
                    ...result.data,
                    protocol: "VVS Finance",
                    sortBy,
                    limit,
                    network: "cronos"
                }
            };
        } catch (error: any) {
            throw new Error(`Failed to get top VVS pairs: ${error.message}`);
        }
    }
};
