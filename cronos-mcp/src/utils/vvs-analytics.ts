import axios from 'axios';
import { networkInfo } from '../config';
import BigNumber from 'bignumber.js';

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
    base_volume_usd: number;
    quote_volume_usd: number;
    price: number;
    hasWCRO: boolean;
    isStablePair: boolean;
    // dataQuality: {
    //     hasValidLiquidity: boolean;
    //     hasValidPrice: boolean;
    //     hasVolume: boolean;
    // };
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
    private readonly PAIRS_NO_WEI_CONVERSION = [
        '0x66e428c3f67a68878562e79A0234c1F83c208770_0xc21223249CA28397B4B6541dfFaEcC539BfF0c59',
        '0x5C7F8A570d578ED84E63fdFA7b1eE72dEae1AE23_0xc21223249CA28397B4B6541dfFaEcC539BfF0c59',
        '0x7a7c9db510aB29A2FC362a4c34260BEcB5cE3446_0xe44Fd7fCb2b1581822D0c862B68222998a0c299a',
        '0x2D03bECE6747ADC00E1a131BBA1469C15fD11e03_0x5C7F8A570d578ED84E63fdFA7b1eE72dEae1AE23'
    ];

    constructor() {
        this.network = 'cronos'; // Fixed since networkInfo doesn't have a 'name' property
    }

    private shouldSkipWeiConversion(pairId: string): boolean {
        return this.PAIRS_NO_WEI_CONVERSION.includes(pairId);
    }

    private sanitizeValue(pairId: string, value: any): number {
        if (this.shouldSkipWeiConversion(pairId)) {
            return this.sanitizeNumber(value);
        }
        return this.sanitizeAndConvert(value);
    }
 

    // Data validation and sanitization
    private sanitizeNumber(value: any): number {
        if (typeof value === 'string') {
            const num = parseFloat(value);
            // Check for absurd values that indicate data corruption
            if (isNaN(num) || !isFinite(num) || num > 1e30) {
                return 0; // Return 0 for corrupted data
            }
            return num;
        }
        if (typeof value === 'number') {
            if (isNaN(value) || !isFinite(value) || value > 1e30) {
                return 0;
            }
            return value;
        }
        return 0;
    }

    // BigNumber utility functions for precise wei/ether conversions
    private weiToEther(weiValue: string | number): number {
        try {
            const wei = new BigNumber(weiValue.toString().split(".")[0]);
            return wei.dividedBy(1e18).toNumber();
        } catch (error) {
            return 0;
        }
    }

    private sanitizeAndConvert(value: any): number {
        try {
            const sanitized = this.sanitizeNumber(value.toString().split(".")[0]);
            return new BigNumber(sanitized).dividedBy(1e18).toNumber();
        } catch (error) {
            return 0;
        }
    }

    private isValidLiquidityValue(value: number): boolean {
        // Reasonable liquidity should be between $0.000001 and $1B for most pairs
        return value >= 0.000001 && value <= 1e9;
    }

    private isValidPrice(value: number): boolean {
        // Reasonable token prices should be between $0.000001 and $100,000
        return value >= 0.000001 && value <= 100000;
    }

    private async getTokenPriceMap(): Promise<Map<string, number>> {
        try {
            const tokensResult = await this.getTokens(1000);
            const priceMap = new Map<string, number>();
            
            if (tokensResult.status === 'success' && tokensResult.data?.tokens) {
                tokensResult.data.tokens.forEach(token => {
                    priceMap.set(token.address.toLowerCase(), token.price);
                });
            }
            
            return priceMap;
        } catch (error) {
            return new Map<string, number>();
        }
    }

    private isStableToken(symbol: string): boolean {
        const stableTokens = ['USDT', 'USDC', 'DAI', 'BUSD', 'TUSD', 'FRAX'];
        return stableTokens.includes(symbol?.toUpperCase() || '');
    }

    async getPairs(limit: number = 1000): Promise<VVSData> {
        try { 
            // Get token prices first for USD conversion
            const tokenPriceMap = await this.getTokenPriceMap();

            const response = await axios.get(`${VVS_API_BASE}/pairs`, {
                timeout: 30000 // 30 seconds for slow VVS API
            });
            const data = response.data;

            let pairs = Object.entries(data.data || {});

            if (limit && pairs.length > limit) {
                pairs = pairs.slice(0, limit);
            }

            const pairAnalysis = pairs.map(([pairId, pairData]: [string, any]) => {
                // Sanitize all numerical values using conditional conversion based on pair ID
                let liquidity = this.sanitizeValue(pairId, pairData.liquidity);
                let liquidityCRO = this.sanitizeValue(pairId, pairData.liquidity_CRO);
                let baseVolume = this.sanitizeValue(pairId, pairData.base_volume); // Convert from wei if needed
                let quoteVolume = this.sanitizeValue(pairId, pairData.quote_volume); // Convert from wei if needed
                let price = this.sanitizeValue(pairId, pairData.price);

                // Get USD prices for base and quote tokens
                const baseTokenUSDPrice = tokenPriceMap.get(pairData.base_address?.toLowerCase() || '') || 0;
                const quoteTokenUSDPrice = tokenPriceMap.get(pairData.quote_address?.toLowerCase() || '') || 0;

                // Convert volumes to USD
                let baseVolumeUSD = 0;
                let quoteVolumeUSD = 0;

                // Handle base volume USD conversion
                if (baseTokenUSDPrice > 0) {
                    baseVolumeUSD = baseVolume * baseTokenUSDPrice;
                } else if (price > 0 && quoteTokenUSDPrice > 0) {
                    // If base token has no USD price, use: base_volume * price * quote_token_usd_price
                    baseVolumeUSD = baseVolume * price * quoteTokenUSDPrice;
                }

                // Handle quote volume USD conversion
                if (quoteTokenUSDPrice > 0) {
                    quoteVolumeUSD = quoteVolume * quoteTokenUSDPrice;
                } else if (price > 0 && baseTokenUSDPrice > 0) {
                    // If quote token has no USD price, use: quote_volume * (1/price) * base_token_usd_price
                    quoteVolumeUSD = quoteVolume * (1 / price) * baseTokenUSDPrice;
                }

                // Special handling for stable pairs where one token is already USD
                if (this.isStableToken(pairData.quote_symbol)) {
                    quoteVolumeUSD = quoteVolume; // Quote volume is already in USD
                    if (price > 0 && baseTokenUSDPrice === 0) {
                        baseVolumeUSD = baseVolume * price; // Use price to convert base to USD
                    }
                } else if (this.isStableToken(pairData.base_symbol)) {
                    baseVolumeUSD = baseVolume; // Base volume is already in USD
                    if (price > 0 && quoteTokenUSDPrice === 0) {
                        quoteVolumeUSD = quoteVolume / price; // Use price to convert quote to USD
                    }
                }

                const totalVolumeUSD = baseVolumeUSD + quoteVolumeUSD;

                return {
                    pairId,
                    base_symbol: pairData.base_symbol,
                    quote_symbol: pairData.quote_symbol,
                    base_address: pairData.base_address,
                    quote_address: pairData.quote_address,
                    liquidity: liquidity,
                    liquidity_CRO: liquidityCRO,
                    base_volume: baseVolume,
                    quote_volume: quoteVolume,
                    base_volume_usd: baseVolumeUSD,
                    quote_volume_usd: quoteVolumeUSD,
                    price,
                    hasWCRO: pairId.includes('0x5C7F8A570d578ED84E63fdFA7b1eE72dEae1AE23'),
                    isStablePair: this.isStablePair(pairData), 
                    formatted: {
                        liquidityUSD: this.formatCurrency(liquidity),
                        liquidityCRO: this.formatTokenAmount(liquidityCRO),
                        baseVolume: this.formatCurrency(baseVolumeUSD),
                        quoteVolume: this.formatCurrency(quoteVolumeUSD),
                        totalVolume: this.formatCurrency(totalVolumeUSD),
                        price: this.formatPrice(price, pairData.quote_symbol)
                    }
                };
            });
 

            // Sort by valid liquidity
            const sortedPairs = pairAnalysis.sort((a, b) =>
                (b.liquidity || 0) - (a.liquidity || 0)
            );

            return {
                status: 'success',
                data: {
                    pairs: sortedPairs,
                    updated_at: data.updated_at,
                    summary: {
                        totalPairs: sortedPairs.length,
                        totalLiquidityUSD: sortedPairs.reduce((sum, pair) => sum + (pair.liquidity || 0), 0),
                        totalVolumeUSD: sortedPairs.reduce((sum, pair) => sum + (pair.base_volume_usd || 0) + (pair.quote_volume_usd || 0), 0),
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

    async getTokens(limit: number = 500): Promise<VVSData> {
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
                        priceUSD: this.formatCurrency(priceUSD), // Token USD prices should be formatted as currency
                        priceCRO: this.formatPrice(priceCRO, 'CRO'), // CRO prices should show quote token
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
                    return (b.base_volume_usd + b.quote_volume_usd) - (a.base_volume_usd + a.quote_volume_usd);
                }
                return (b.liquidity || 0) - (a.liquidity || 0);
            }).slice(0, limit);

            const analytics = {
                totalLiquidityInTopPairs: sortedPairs.reduce((sum, pair) => sum + (pair.liquidity || 0), 0),
                totalVolumeInTopPairs: sortedPairs.reduce((sum, pair) => sum + (pair.base_volume_usd || 0) + (pair.quote_volume_usd || 0), 0),
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

        // Use the number directly - it's already in correct units after wei conversion
        const value = num;

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

    private formatPrice(price: number, quoteSymbol: string = ''): string {
        if (!isFinite(price) || isNaN(price) || price <= 0) return `0${quoteSymbol ? ' ' + quoteSymbol : ''}`;

        let formattedPrice: string;
        if (price >= 1000) {
            formattedPrice = price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        } else if (price >= 1) {
            formattedPrice = price.toFixed(4);
        } else if (price >= 0.0001) {
            formattedPrice = price.toFixed(6);
        } else if (price > 0) {
            formattedPrice = price.toFixed(8);
        } else {
            return `0${quoteSymbol ? ' ' + quoteSymbol : ''}`;
        }

        return `${formattedPrice}${quoteSymbol ? ' ' + quoteSymbol : ''}`;
    }

    private isStablePair(pairData: any): boolean {
        const stableTokens = ['USDT', 'USDC', 'DAI', 'BUSD', 'TUSD', 'FRAX'];
        const baseSymbol = pairData.base_symbol?.toUpperCase() || '';
        const quoteSymbol = pairData.quote_symbol?.toUpperCase() || '';

        return stableTokens.includes(baseSymbol) || stableTokens.includes(quoteSymbol);
    }
}
