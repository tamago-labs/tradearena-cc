import { z } from "zod";
import { CronosAnalytics } from "../../utils/cronos_analytics";
import { type McpTool } from "../../types";

export const CronosGetAllTickersTool: McpTool = {
    name: "cronos_get_all_tickers",
    description: "Get all available trading pairs and market data from Crypto.com Exchange",
    schema: {
        limit: z.number()
            .optional()
            .describe("Limit number of results (default: 50, max: 200)")
            .default(50)
    },
    handler: async (input: Record<string, any>) => {
        try {
            const result = await CronosAnalytics.getAllTickers();
            
            if (result.status === 'error') {
                throw new Error(result.message);
            }
            
            // Apply limit if specified
            let tickers = (result.data as any) || [];
            if (input.limit && tickers.length > input.limit) {
                tickers = tickers.slice(0, input.limit);
            }
            
            return {
                status: "success",
                message: `✅ Retrieved ${tickers.length} trading pairs from Crypto.com Exchange`,
                data: {
                    tickers: tickers,
                    count: tickers.length,
                    exchange: "Crypto.com Exchange",
                    network: "cronos-mainnet",
                    timestamp: Date.now(),
                    summary: {
                        totalPairs: result.data?.length || 0,
                        croBasePairs: tickers.filter((t: any) => t.i && t.i.endsWith('_CRO')).length,
                        usdBasePairs: tickers.filter((t: any) => t.i && (t.i.endsWith('_USD') || t.i.endsWith('_USDT') || t.i.endsWith('_USDC'))).length
                    }
                }
            };
        } catch (error: any) {
            throw new Error(`Failed to get all tickers: ${error.message}`);
        }
    }
};

export const CronosGetTickerTool: McpTool = {
    name: "cronos_get_ticker",
    description: "Get specific trading pair data and market information from Crypto.com Exchange",
    schema: {
        instrument: z.string()
            .describe("Trading pair instrument name (e.g., 'CRO_USD', 'BTC_CRO', 'ETH_USDT')")
            .min(1)
    },
    handler: async (input: Record<string, any>) => {
        try {
            const result = await CronosAnalytics.getTickerByInstrument(input.instrument);
            
            if (result.status === 'error') {
                throw new Error(result.message);
            }
            
            return {
                status: "success",
                message: `✅ Ticker data retrieved for ${input.instrument}`,
                data: {
                    instrument: input.instrument,
                    ...result.data,
                    exchange: "Crypto.com Exchange",
                    network: "cronos-mainnet",
                    timestamp: Date.now(),
                    analysis: {
                        isCROPair: input.instrument.includes('CRO'),
                        isStablePair: input.instrument.includes('USD') || input.instrument.includes('USDT') || input.instrument.includes('USDC'),
                        priceAvailable: !!(result.data as any)?.a,
                        volumeAvailable: !!(result.data as any)?.v
                    }
                }
            };
        } catch (error: any) {
            throw new Error(`Failed to get ticker for ${input.instrument}: ${error.message}`);
        }
    }
};

export const CronosGetMarketSummaryTool: McpTool = {
    name: "cronos_get_market_summary",
    description: "Get market summary and CRO-related trading data from Crypto.com Exchange",
    schema: {
        includeCROPairs: z.boolean()
            .optional()
            .describe("Include CRO trading pairs analysis (default: true)")
            .default(true)
    },
    handler: async (input: Record<string, any>) => {
        try {
            const result = await CronosAnalytics.getMarketSummary(input.includeCROPairs);
            
            if (result.status === 'error') {
                throw new Error(result.message);
            }
            
            return {
                status: "success",
                message: `✅ Market summary retrieved from Crypto.com Exchange`,
                data: {
                    exchange: "Crypto.com Exchange",
                    network: "cronos-mainnet",
                    timestamp: Date.now(),
                    ...result.data
                }
            };
        } catch (error: any) {
            throw new Error(`Failed to get market summary: ${error.message}`);
        }
    }
};
