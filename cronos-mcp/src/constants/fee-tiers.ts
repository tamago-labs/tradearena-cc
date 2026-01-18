/**
 * VVS Finance fee tiers for different pool types
 */
export const VVS_FEE_TIERS = {
  '0.05%': 500,    // 0.05% fee tier for stable pools
  '0.3%': 3000,    // 0.3% fee tier for standard pools
  '1%': 10000,     // 1% fee tier for exotic pools
} as const;

/**
 * Pool type descriptions for each fee tier
 */
export const POOL_TYPE_DESCRIPTIONS = {
  '0.05%': 'Stable pools (similar assets like USDC/USDT)',
  '0.3%': 'Standard pools (most common pairs)',
  '1%': 'Exotic pools (volatile or less common pairs)',
} as const;

/**
 * Default slippage tolerances for different token types
 */
export const DEFAULT_SLIPPAGE = {
  stable: 0.1,      // 0.1% for stablecoin swaps
  standard: 0.5,    // 0.5% for standard swaps
  exotic: 1.0,      // 1.0% for exotic swaps
} as const;

/**
 * Minimum and maximum slippage tolerances
 */
export const SLIPPAGE_LIMITS = {
  minimum: 0.01,    // 0.01% minimum
  maximum: 50.0,    // 50% maximum
} as const;
