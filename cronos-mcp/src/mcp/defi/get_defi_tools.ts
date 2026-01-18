import { z } from "zod";
import { CronosAnalytics } from "../../utils/cronos_analytics";
import { type McpTool } from "../../types";

export const CronosGetAllFarmsTool: McpTool = {
    name: "cronos_get_all_farms",
    description: "Get all yield farms for DeFi protocols with APR/APY data from H2Finance and VVS Finance",
    schema: {
        protocol: z.enum(['h2finance', 'vvsfinance'])
            .describe("DeFi protocol to query for yield farming data"),
    },
    handler: async (input: Record<string, any>) => {
        try {
            const result = await CronosAnalytics.getAllFarms(input.protocol);
            
            if (result.status === 'error') {
                throw new Error(result.message);
            }
            
            const farms = Array.isArray(result.data) ? result.data : [];
            const activeFarms = farms.filter((farm: any) => !farm.isFinished);
            
            return {
                status: "success",
                message: `✅ Retrieved ${farms.length} farms from ${input.protocol} (${activeFarms.length} active)`,
                data: {
                    ...result.data,
                    protocol: input.protocol,
                    farms: farms,
                    summary: {
                        totalFarms: farms.length,
                        activeFarms: activeFarms.length,
                        finishedFarms: farms.length - activeFarms.length,
                        averageAPR: activeFarms.length > 0 
                            ? activeFarms.reduce((sum: number, farm: any) => sum + (farm.baseApr || 0), 0) / activeFarms.length
                            : 0
                    }
                }
            };
        } catch (error: any) {
            throw new Error(`Failed to get farms from ${input.protocol}: ${error.message}`);
        }
    }
};

export const CronosGetFarmBySymbolTool: McpTool = {
    name: "cronos_get_farm_by_symbol",
    description: "Get specific yield farm details by LP symbol from H2Finance or VVS Finance",
    schema: {
        protocol: z.enum(['h2finance', 'vvsfinance'])
            .describe("DeFi protocol to query"),
        symbol: z.string()
            .describe("LP symbol to query (e.g., 'zkCRO-MOON', 'CRO-USDC', 'CRO-ETH')")
    },
    handler: async (input: Record<string, any>) => {
        try {
            const result = await CronosAnalytics.getFarmBySymbol(input.protocol, input.symbol);
            
            if (result.status === 'error') {
                throw new Error(result.message);
            }
            
            return {
                status: "success",
                message: `✅ Farm details retrieved for ${input.symbol} from ${input.protocol}`,
                data: {
                    ...result.data,
                    protocol: input.protocol,
                    symbol: input.symbol,
                    yieldInfo: {
                        baseAPR: result.data?.baseApr || 0,
                        baseAPY: result.data?.baseApy || 0,
                        lpAPR: result.data?.lpApr || 0,
                        lpAPY: result.data?.lpApy || 0,
                        isActive: !result.data?.isFinished,
                        rewardEndDate: result.data?.rewardEndAt
                    }
                }
            };
        } catch (error: any) {
            throw new Error(`Failed to get farm data for ${input.symbol}: ${error.message}`);
        }
    }
};

export const CronosGetWhitelistedTokensTool: McpTool = {
    name: "cronos_get_whitelisted_tokens",
    description: "Get whitelisted tokens for DeFi protocols from H2Finance and VVS Finance",
    schema: {
        protocol: z.enum(['h2finance', 'vvsfinance'])
            .describe("DeFi protocol to query for whitelisted tokens")
    },
    handler: async (input: Record<string, any>) => {
        try {
            const result = await CronosAnalytics.getWhitelistedTokens(input.protocol);
            
            if (result.status === 'error') {
                throw new Error(result.message);
            }
            
            const tokens = Array.isArray(result.data) ? result.data : [];
            
            return {
                status: "success",
                message: `✅ Retrieved ${tokens.length} whitelisted tokens from ${input.protocol}`,
                data: {
                    ...result.data,
                    protocol: input.protocol,
                    tokens: tokens,
                    summary: {
                        totalTokens: tokens.length,
                        protocol: input.protocol
                    }
                }
            };
        } catch (error: any) {
            throw new Error(`Failed to get whitelisted tokens from ${input.protocol}: ${error.message}`);
        }
    }
};
