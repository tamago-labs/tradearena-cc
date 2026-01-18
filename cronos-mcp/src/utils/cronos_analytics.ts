import { Token, Wallet, Block, Transaction, Exchange, Defi, CronosId, CronosEvm, Client } from "@crypto.com/developer-platform-client";
import { DefiProtocol } from "@crypto.com/developer-platform-client";

export interface AnalyticsResponse {
    status: 'success' | 'error';
    data?: any;
    message?: string;
    network: string;
    timestamp: number;
}

export class CronosAnalytics {
    private static readonly API_KEY = 'I1bUrnNJcDkpUMoYpdCfC5mCqncUDoie';
    private static readonly NETWORK = 'cronos-mainnet';
    private static initialized = false;

    // Initialize the SDK with hardcoded API key
    static initialize(): void {
        if (!this.initialized) {
            Client.init({
                apiKey: this.API_KEY
            });
            this.initialized = true;
            console.error('🔑 CronosAnalytics initialized with Crypto.com SDK');
        }
    }

    // Ensure initialization before any API call
    private static ensureInitialized(): void {
        if (!this.initialized) {
            this.initialize();
        }
    }

    // === DEFI ANALYTICS METHODS ===

    static async getAllFarms(protocol: 'h2finance' | 'vvsfinance'): Promise<AnalyticsResponse> {
        this.ensureInitialized();
        
        try {
            const defiProtocol = protocol === 'h2finance' ? DefiProtocol.H2 : DefiProtocol.VVS;
            const result = await Defi.getAllFarms(defiProtocol);
            
            const farms = Array.isArray(result.data) ? result.data : [];
            const activeFarms = farms.filter((farm: any) => !farm.isFinished);
            
            return {
                status: 'success',
                data: {
                    ...result.data,
                    protocol: protocol,
                    summary: {
                        totalFarms: farms.length,
                        activeFarms: activeFarms.length,
                        finishedFarms: farms.length - activeFarms.length,
                        averageAPR: activeFarms.length > 0 
                            ? activeFarms.reduce((sum: number, farm: any) => sum + (farm.baseApr || 0), 0) / activeFarms.length
                            : 0
                    }
                },
                network: this.NETWORK,
                timestamp: Date.now()
            };
        } catch (error: any) {
            return {
                status: 'error',
                message: error.message || 'Failed to get farms',
                network: this.NETWORK,
                timestamp: Date.now()
            };
        }
    }

    static async getFarmBySymbol(protocol: 'h2finance' | 'vvsfinance', symbol: string): Promise<AnalyticsResponse> {
        this.ensureInitialized();
        
        try {
            const defiProtocol = protocol === 'h2finance' ? DefiProtocol.H2 : DefiProtocol.VVS;
            const result = await Defi.getFarmBySymbol(defiProtocol, symbol);
            
            return {
                status: 'success',
                data: {
                    ...result.data,
                    protocol: protocol,
                    symbol: symbol,
                    yieldInfo: {
                        baseAPR: result.data?.baseApr || 0,
                        baseAPY: result.data?.baseApy || 0,
                        lpAPR: result.data?.lpApr || 0,
                        lpAPY: result.data?.lpApy || 0,
                        isActive: !result.data?.isFinished,
                        rewardEndDate: result.data?.rewardEndAt
                    }
                },
                network: this.NETWORK,
                timestamp: Date.now()
            };
        } catch (error: any) {
            return {
                status: 'error',
                message: error.message || 'Failed to get farm data',
                network: this.NETWORK,
                timestamp: Date.now()
            };
        }
    }

    static async getWhitelistedTokens(protocol: 'h2finance' | 'vvsfinance'): Promise<AnalyticsResponse> {
        this.ensureInitialized();
        
        try {
            const defiProtocol = protocol === 'h2finance' ? DefiProtocol.H2 : DefiProtocol.VVS;
            const result = await Defi.getWhitelistedTokens(defiProtocol);
            
            return {
                status: 'success',
                data: {
                    ...result.data,
                    protocol: protocol
                },
                network: this.NETWORK,
                timestamp: Date.now()
            };
        } catch (error: any) {
            return {
                status: 'error',
                message: error.message || 'Failed to get whitelisted tokens',
                network: this.NETWORK,
                timestamp: Date.now()
            };
        }
    }

    // === EXCHANGE & MARKET METHODS ===

    static async getAllTickers(): Promise<AnalyticsResponse> {
        this.ensureInitialized();
        
        try {
            const result = await Exchange.getAllTickers();
            
            return {
                status: 'success',
                data: {
                    ...result.data,
                    exchangeInfo: 'Crypto.com Exchange data'
                },
                network: this.NETWORK,
                timestamp: Date.now()
            };
        } catch (error: any) {
            return {
                status: 'error',
                message: error.message || 'Failed to get exchange tickers',
                network: this.NETWORK,
                timestamp: Date.now()
            };
        }
    }

    static async getTickerByInstrument(instrument: string): Promise<AnalyticsResponse> {
        this.ensureInitialized();
        
        try {
            const result = await Exchange.getTickerByInstrument(instrument);
            const tickerData = result.data as any;
            
            return {
                status: 'success',
                data: {
                    ...result.data,
                    instrument: instrument,
                    analysis: {
                        isCROPair: instrument.includes('CRO'),
                        isStablePair: instrument.includes('USD') || instrument.includes('USDT') || instrument.includes('USDC'),
                        priceAvailable: !!tickerData?.a,
                        volumeAvailable: !!tickerData?.v
                    }
                },
                network: this.NETWORK,
                timestamp: Date.now()
            };
        } catch (error: any) {
            return {
                status: 'error',
                message: error.message || 'Failed to get ticker data',
                network: this.NETWORK,
                timestamp: Date.now()
            };
        }
    }

    static async getMarketSummary(includeCROPairs: boolean = true): Promise<AnalyticsResponse> {
        this.ensureInitialized();
        
        try {
            // Get all tickers for analysis
            const allTickersResult = await Exchange.getAllTickers();
            const tickers = (allTickersResult.data as any) || [];
            
            // Get specific CRO price if available
            let croPrice = null;
            if (includeCROPairs) {
                try {
                    const croResult = await Exchange.getTickerByInstrument('CRO_USD');
                    croPrice = croResult.data;
                } catch {
                    // Try alternative CRO pairs
                    try {
                        const croResult = await Exchange.getTickerByInstrument('CRO_USDT');
                        croPrice = croResult.data;
                    } catch {
                        // CRO price not available
                    }
                }
            }
            
            return {
                status: 'success',
                data: {
                    exchange: "Crypto.com Exchange",
                    summary: {
                        totalTradingPairs: tickers.length,
                        croPrice: croPrice,
                        croBasePairs: tickers.filter((t: any) => t.i && t.i.endsWith('_CRO')).length,
                        usdBasePairs: tickers.filter((t: any) => t.i && (t.i.endsWith('_USD') || t.i.endsWith('_USDT') || t.i.endsWith('_USDC'))).length
                    },
                    croPairs: includeCROPairs ? tickers.filter((t: any) => t.i && (t.i.includes('CRO_') || t.i.includes('_CRO'))) : []
                },
                network: this.NETWORK,
                timestamp: Date.now()
            };
        } catch (error: any) {
            return {
                status: 'error',
                message: error.message || 'Failed to get market summary',
                network: this.NETWORK,
                timestamp: Date.now()
            };
        }
    }

    // === UTILITY METHODS ===

    static getNetworkInfo(): AnalyticsResponse {
        return {
            status: 'success',
            data: {
                network: this.NETWORK,
                name: 'Cronos Mainnet',
                chain: 'CronosEVM',
                hasApiKey: true,
                apiKey: `****${this.API_KEY.slice(-4)}`
            },
            network: this.NETWORK,
            timestamp: Date.now()
        };
    }

    // Format large numbers for better readability
    static formatBalance(balance: string, decimals: number = 18): string {
        const balanceNum = parseFloat(balance) / Math.pow(10, decimals);
        if (balanceNum >= 1e9) return `${(balanceNum / 1e9).toFixed(2)}B`;
        if (balanceNum >= 1e6) return `${(balanceNum / 1e6).toFixed(2)}M`;
        if (balanceNum >= 1e3) return `${(balanceNum / 1e3).toFixed(2)}K`;
        return balanceNum.toFixed(4);
    }

    // Validate Ethereum address format
    static isValidAddress(address: string): boolean {
        return /^0x[a-fA-F0-9]{40}$/.test(address);
    }

    // Validate CronosId format
    static isValidCronosId(name: string): boolean {
        return CronosId.isCronosId(name);
    }
}
