import axios from 'axios';
import { networkInfo } from '../config';

const VVS_API_BASE = 'https://api.vvs.finance/info/api';

export interface VVSPair {
    pairId: string;
    base_symbol: string;
    quote_symbol: string;
    base_address: string;
    quote_address: string;
    liquidity: number;
    liquidity_CRO: number;
    base_volume: number;
    quote_volume: number;
    price: number;
    hasWCRO: boolean;
    isStablePair: boolean;
    dataQuality: {
        hasValidLiquidity: boolean;
        hasValidPrice: boolean;
        hasVolume: boolean;
    };
    formatted: {
        liquidityUSD: string;
        liquidityCRO: string;
        baseVolume: string;
        quoteVolume: string;
        totalVolume: string;
        price: string;
    };
}

export interface VVSToken {
    address: string;
    symbol: string;
    price: number;
    price_CRO: number;
    volume24h?: number;
    marketCap?: number;
    isWCRO: boolean;
    dataQuality: {
        hasValidUSDPrice: boolean;
        hasValidCROPrice: boolean;
    };
    formatted: {
        priceUSD: string;
        priceCRO: string;
        volume24h?: string;
        marketCap?: string;
    };
}

export interface VVSData {
    status: 'success' | 'error';
    data?: {
        pairs?: VVSPair[];
        tokens?: VVSToken[];
        summary?: any;
        analytics?: any; // Added analytics property
        updated_at?: string;
    };
    message?: string;
    network: string;
    timestamp: number;
}

export class VVSAnalytics {
    private network: string;

    constructor() {
        this.network = 'cronos'; // Fixed since networkInfo doesn't have a 'name' property
    }

    // Data validation and sanitization
    private sanitizeNumber(value: any): number {
        if (typeof value === 'string') {
            const num = parseFloat(value);
            // Check for absurd values that indicate data corruption
            if (isNaN(num) || !isFinite(num) || num > 1e15) {
                return 0; // Return 0 for corrupted data
            }
            return num;
        }
        if (typeof value === 'number') {
            if (isNaN(value) || !isFinite(value) || value > 1e15) {
                return 0;
            }
            return value;
        }
        return 0;
    }

    private isValidLiquidityValue(value: number): boolean {
        // Reasonable liquidity should be between $1 and $1B for most pairs
        return value >= 1 && value <= 1e9;
    }

    private isValidPrice(value: number): boolean {
        // Reasonable token prices should be between $0.000001 and $100,000
        return value >= 0.000001 && value <= 100000;
    }

    async getPairs(limit: number = 100): Promise<VVSData> {
        try {
            const response = await axios.get(`${VVS_API_BASE}/pairs`);
            const data = response.data;

            let pairs = Object.entries(data.data || {});
            if (limit && pairs.length > limit) {
                pairs = pairs.slice(0, limit);
            }

            const pairAnalysis = pairs.map(([pairId, pairData]: [string, any]) => {
                // Sanitize all numerical values
                let liquidityUSD = this.sanitizeNumber(pairData.liquidity);
                let liquidityCRO = this.sanitizeNumber(pairData.liquidity_CRO);
                let baseVolume = this.sanitizeNumber(pairData.base_volume);
                let quoteVolume = this.sanitizeNumber(pairData.quote_volume);
                let price = this.sanitizeNumber(pairData.price);

                // Additional validation for VVS-specific issues
                if (!this.isValidLiquidityValue(liquidityUSD)) {
                    console.warn(`Invalid liquidity for pair ${pairId}: ${liquidityUSD}, setting to 0`);
                    liquidityUSD = 0;
                }

                if (!this.isValidPrice(price)) {
                    console.warn(`Invalid price for pair ${pairId}: ${price}, setting to 0`);
                    price = 0;
                }

                // Convert from wei if values are too large (common VVS issue)
                if (liquidityUSD > 1e12) {
                    liquidityUSD = liquidityUSD / 1e18; // Convert from wei
                }
                if (liquidityCRO > 1e12) {
                    liquidityCRO = liquidityCRO / 1e18;
                }

                return {
                    pairId,
                    base_symbol: pairData.base_symbol,
                    quote_symbol: pairData.quote_symbol,
                    base_address: pairData.base_address,
                    quote_address: pairData.quote_address,
                    liquidity: liquidityUSD,
                    liquidity_CRO: liquidityCRO,
                    base_volume: baseVolume,
                    quote_volume: quoteVolume,
                    price,
                    hasWCRO: pairId.includes('0x5C7F8A570d578ED84E63fdFA7b1eE72dEae1AE23'),
                    isStablePair: this.isStablePair(pairData),
                    dataQuality: {
                        hasValidLiquidity: liquidityUSD > 0 && this.isValidLiquidityValue(liquidityUSD),
                        hasValidPrice: price > 0 && this.isValidPrice(price),
                        hasVolume: baseVolume > 0 || quoteVolume > 0
                    },
                    formatted: {
                        liquidityUSD: this.formatCurrency(liquidityUSD),
                        liquidityCRO: this.formatTokenAmount(liquidityCRO),
                        baseVolume: this.formatCurrency(baseVolume),
                        quoteVolume: this.formatCurrency(quoteVolume),
                        totalVolume: this.formatCurrency(baseVolume + quoteVolume),
                        price: this.formatPrice(price)
                    }
                };
            });

            // Filter out pairs with invalid data
            const validPairs = pairAnalysis.filter(pair => 
                pair.dataQuality.hasValidLiquidity || pair.dataQuality.hasVolume
            );

            // Sort by valid liquidity
            const sortedPairs = validPairs.sort((a, b) => 
                (b.liquidity || 0) - (a.liquidity || 0)
            );

            return {
                status: 'success',
                data: {
                    pairs: sortedPairs,
                    updated_at: data.updated_at,
                    summary: {
                        totalPairs: validPairs.length,
                        totalLiquidityUSD: sortedPairs.reduce((sum, pair) => sum + (pair.liquidity || 0), 0),
                        totalVolumeUSD: sortedPairs.reduce((sum, pair) => sum + (pair.base_volume || 0) + (pair.quote_volume || 0), 0),
                        wcroPairs: sortedPairs.filter(pair => pair.hasWCRO).length,
                        stablePairs: sortedPairs.filter(p => p.isStablePair).length
                    }
                },
                network: this.network,
                timestamp: Date.now()
            };
        } catch (error: any) {
            return {
                status: 'error',
                message: error.message || 'Failed to get VVS pairs',
                network: this.network,
                timestamp: Date.now()
            };
        }
    }

    async getTokens(limit: number = 100): Promise<VVSData> {
        try {
            const response = await axios.get(`${VVS_API_BASE}/tokens`);
            const data = response.data;

            let tokens = Object.entries(data.data || {});
            if (limit && tokens.length > limit) {
                tokens = tokens.slice(0, limit);
            }

            const tokenAnalysis = tokens.map(([address, tokenData]: [string, any]) => {
                let priceUSD = this.sanitizeNumber(tokenData.price);
                let priceCRO = this.sanitizeNumber(tokenData.price_CRO);
                
                // Validate prices
                if (!this.isValidPrice(priceUSD)) {
                    priceUSD = 0;
                }
                if (!this.isValidPrice(priceCRO)) {
                    priceCRO = 0;
                }

                const isWCRO = address.toLowerCase() === '0x5c7f8a570d578ed84e63fdfa7b1ee72deae1ae23';

                return {
                    address,
                    symbol: tokenData.symbol,
                    price: priceUSD, // Fixed: Added missing 'price' property
                    priceUSD,
                    price_CRO: priceCRO,
                    volume24h: this.sanitizeNumber(tokenData.volume24h),
                    marketCap: this.sanitizeNumber(tokenData.marketCap),
                    isWCRO,
                    dataQuality: {
                        hasValidUSDPrice: priceUSD > 0 && this.isValidPrice(priceUSD),
                        hasValidCROPrice: priceCRO > 0 && this.isValidPrice(priceCRO)
                    },
                    formatted: {
                        priceUSD: this.formatPrice(priceUSD),
                        priceCRO: this.formatPrice(priceCRO),
                        volume24h: tokenData.volume24h ? this.formatCurrency(this.sanitizeNumber(tokenData.volume24h)) : undefined,
                        marketCap: tokenData.marketCap ? this.formatCurrency(this.sanitizeNumber(tokenData.marketCap)) : undefined
                    }
                };
            });

            // Filter valid tokens
            const validTokens = tokenAnalysis.filter(token => 
                token.dataQuality.hasValidUSDPrice || token.dataQuality.hasValidCROPrice
            );

            return {
                status: 'success',
                data: {
                    tokens: validTokens,
                    updated_at: data.updated_at,
                    summary: {
                        totalTokens: validTokens.length,
                        wcroPrice: validTokens.find(t => t.isWCRO)?.priceUSD || 0,
                        wcroAddress: '0x5C7F8A570d578ED84E63fdFA7b1eE72dEae1AE23'
                    }
                },
                network: this.network,
                timestamp: Date.now()
            };
        } catch (error: any) {
            return {
                status: 'error',
                message: error.message || 'Failed to get VVS tokens',
                network: this.network,
                timestamp: Date.now()
            };
        }
    }

    async getSummary(limit: number = 50): Promise<VVSData> {
        try {
            const pairsResult = await this.getPairs(1000); // Get all pairs first
            const tokensResult = await this.getTokens(100); // Get tokens for additional info

            if (pairsResult.status !== 'success' || !pairsResult.data?.pairs) {
                throw new Error('Failed to fetch pairs data');
            }

            const sortedPairs = pairsResult.data.pairs
                .sort((a, b) => (b.liquidity || 0) - (a.liquidity || 0))
                .slice(0, limit);

            return {
                status: 'success',
                data: {
                    pairs: sortedPairs,
                    tokens: tokensResult.data?.tokens || [],
                    summary: {
                        ...pairsResult.data.summary,
                        ...tokensResult.data?.summary
                    },
                    updated_at: pairsResult.data.updated_at
                },
                network: this.network,
                timestamp: Date.now()
            };
        } catch (error: any) {
            return {
                status: 'error',
                message: error.message || 'Failed to get VVS summary',
                network: this.network,
                timestamp: Date.now()
            };
        }
    }

    async getTokenInfo(tokenAddress: string): Promise<VVSData> {
        try {
            const tokensResult = await this.getTokens(1000);
            
            if (tokensResult.status !== 'success' || !tokensResult.data?.tokens) {
                throw new Error('Failed to fetch tokens data');
            }

            const token = tokensResult.data.tokens.find(t => 
                t.address.toLowerCase() === tokenAddress.toLowerCase()
            );

            if (!token) {
                throw new Error(`Token not found: ${tokenAddress}`);
            }

            return {
                status: 'success',
                data: {
                    tokens: [token], // Fixed: Changed 'token' to 'tokens' array
                    updated_at: tokensResult.data.updated_at
                },
                network: this.network,
                timestamp: Date.now()
            };
        } catch (error: any) {
            return {
                status: 'error',
                message: error.message || 'Failed to get VVS token info',
                network: this.network,
                timestamp: Date.now()
            };
        }
    }

    async getTopPairs(limit: number = 10, sortBy: 'liquidity' | 'volume' = 'liquidity'): Promise<VVSData> {
        try {
            const pairsResult = await this.getPairs(1000);
            
            if (pairsResult.status !== 'success' || !pairsResult.data?.pairs) {
                throw new Error('Failed to fetch pairs data');
            }

            const sortedPairs = pairsResult.data.pairs.sort((a, b) => {
                if (sortBy === 'volume') {
                    return (b.base_volume + b.quote_volume) - (a.base_volume + a.quote_volume);
                }
                return (b.liquidity || 0) - (a.liquidity || 0);
            }).slice(0, limit);

            const analytics = {
                totalLiquidityInTopPairs: sortedPairs.reduce((sum, pair) => sum + (pair.liquidity || 0), 0),
                totalVolumeInTopPairs: sortedPairs.reduce((sum, pair) => sum + (pair.base_volume || 0) + (pair.quote_volume || 0), 0),
                wcroPairs: sortedPairs.filter(pair => pair.hasWCRO).length,
                stablePairs: sortedPairs.filter(p => p.isStablePair).length,
                averageLiquidity: sortedPairs.reduce((sum, pair) => sum + (pair.liquidity || 0), 0) / sortedPairs.length
            };
            
            return {
                status: 'success',
                data: {
                    pairs: sortedPairs,
                    analytics,
                    summary: pairsResult.data.summary,
                    updated_at: pairsResult.data.updated_at
                },
                network: this.network,
                timestamp: Date.now()
            };
        } catch (error: any) {
            return {
                status: 'error',
                message: error.message || 'Failed to get top VVS pairs',
                network: this.network,
                timestamp: Date.now()
            };
        }
    }

    // Enhanced formatting methods with better validation
    private formatTokenAmount(amount: number | string): string {
        const num = typeof amount === 'string' ? parseFloat(amount) : amount;
        
        if (!isFinite(num) || isNaN(num) || num <= 0) return '0';
        
        // Don't divide by 1e18 if already a reasonable number
        const value = num > 1e15 ? num / 1e18 : num;
        
        if (value >= 1e12) return `${(value / 1e12).toFixed(2)}T`;
        if (value >= 1e9) return `${(value / 1e9).toFixed(2)}B`;
        if (value >= 1e6) return `${(value / 1e6).toFixed(2)}M`;
        if (value >= 1e3) return `${(value / 1e3).toFixed(2)}K`;
        return value.toFixed(2);
    }

    private formatCurrency(amount: number): string {
        if (!isFinite(amount) || isNaN(amount) || amount <= 0) return '$0.00';
        
        if (amount >= 1e12) return `$${(amount / 1e12).toFixed(2)}T`;
        if (amount >= 1e9) return `$${(amount / 1e9).toFixed(2)}B`;
        if (amount >= 1e6) return `$${(amount / 1e6).toFixed(2)}M`;
        if (amount >= 1e3) return `$${(amount / 1e3).toFixed(2)}K`;
        if (amount >= 1) return `$${amount.toFixed(2)}`;
        if (amount >= 0.01) return `$${amount.toFixed(4)}`;
        return `$${amount.toFixed(8)}`;
    }

    private formatPrice(price: number): string {
        if (!isFinite(price) || isNaN(price) || price <= 0) return '$0.00';
        
        if (price >= 1000) return `$${price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        if (price >= 1) return `$${price.toFixed(4)}`;
        if (price >= 0.0001) return `$${price.toFixed(6)}`;
        if (price > 0) return `$${price.toFixed(8)}`;
        return '$0.00';
    }

    private isStablePair(pairData: any): boolean {
        const stableTokens = ['USDT', 'USDC', 'DAI', 'BUSD', 'TUSD', 'FRAX'];
        const baseSymbol = pairData.base_symbol?.toUpperCase() || '';
        const quoteSymbol = pairData.quote_symbol?.toUpperCase() || '';
        
        return stableTokens.includes(baseSymbol) || stableTokens.includes(quoteSymbol);
    }
}
