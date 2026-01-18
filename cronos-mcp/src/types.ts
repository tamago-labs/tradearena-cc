import { z } from 'zod';

export interface McpTool {
    name: string;
    description: string;
    schema: Record<string, any>;
    handler: (agent: any, input: Record<string, any>) => Promise<any>;
}

// Common schemas
export const AddressSchema = z.string()
    .regex(/^0x[a-fA-F0-9]{40}$/, "Invalid Ethereum address format")
    .describe("Ethereum address (0x...)");

export const NetworkSchema = z.enum(['cronos', 'cronos-testnet'])
    .describe("Network name");

// Token information for wallet operations
export interface TokenInfo {
    address: string;
    symbol: string;
    name: string;
    decimals: number;
    balance: string;
}

 

// Price API response types
export const PriceDataSchema = z.object({
  symbol: z.string(),
  price: z.number(),
  percent_change_24h: z.number(),
  market_cap: z.number(),
  volume_24h: z.number(),
  last_updated: z.string(),
  timestamp: z.string()
});

export const PriceApiResponseSchema = z.object({
  success: z.boolean(),
  data: z.array(PriceDataSchema),
  count: z.number()
});

export type PriceData = z.infer<typeof PriceDataSchema>;
export type PriceApiResponse = z.infer<typeof PriceApiResponseSchema>;

// VVS Finance Pool Information
export interface VVSPoolInfo {
  address: string;
  token0: {
    address: string;
    symbol: string;
    decimals: number;
  };
  token1: {
    address: string;
    symbol: string;
    decimals: number;
  };
  fee: number;
  liquidity: string;
  sqrtPriceX96: string;
  tick: number;
  tickSpacing: number;
}

// VVS Swap Quote
export interface VVSSwapQuote {
  tokenIn: string;
  tokenOut: string;
  amountIn: string;
  amountOut: string;
  priceImpact: number;
  route: {
    pools: string[];
    tokens: string[];
    fees: number[];
  };
  gasEstimate: string;
}

// VVS Route Information
export interface VVSRoute {
  tokenIn: string;
  tokenOut: string;
  amountIn: string;
  routes: Array<{
    pools: string[];
    tokens: string[];
    fees: number[];
    amountOut: string;
    priceImpact: number;
  }>;
  bestRoute: {
    pools: string[];
    tokens: string[];
    fees: number[];
    amountOut: string;
    priceImpact: number;
  };
}

// Token balance types
export interface TokenBalance {
  symbol: string;
  address: string;
  balance: string;
  decimals: number;
}

export interface WalletInfo {
  address: string;
  nativeBalance: string;
  tokens: TokenBalance[];
  network: {
    chainId: number;
    name: string;
  };
}

// Transaction types
export interface TransactionResult {
  hash: string;
  status: 'success' | 'failed';
  blockNumber?: number;
  gasUsed?: string;
  error?: string;
}

// Send token parameters
export interface SendTokenParams {
  token: string;
  amount: string;
  to: string;
}

// Approve token parameters
export interface ApproveTokenParams {
  token: string;
  spender: string;
  amount: string;
}

// Wrap/Unwrap parameters
export interface WrapParams {
  amount: string;
}

// Swap parameters
export interface SwapParams {
  tokenIn: string;
  tokenOut: string;
  amountIn: string;
  slippage?: number;
  recipient?: string;
  deadline?: number;
}

// Check allowance parameters
export interface CheckAllowanceParams {
  token: string;
  spender: string;
}

// Error types
export class VVSFinanceError extends Error {
  constructor(
    message: string,
    public code?: string,
    public details?: any
  ) {
    super(message);
    this.name = 'VVSFinanceError';
  }
}

export class NetworkError extends VVSFinanceError {
  constructor(message: string, details?: any) {
    super(message, 'NETWORK_ERROR', details);
    this.name = 'NetworkError';
  }
}

export class TransactionError extends VVSFinanceError {
  constructor(message: string, details?: any) {
    super(message, 'TRANSACTION_ERROR', details);
    this.name = 'TransactionError';
  }
}

export class InsufficientLiquidityError extends VVSFinanceError {
  constructor(message: string) {
    super(message, 'INSUFFICIENT_LIQUIDITY');
    this.name = 'InsufficientLiquidityError';
  }
}

export class InsufficientBalanceError extends VVSFinanceError {
  constructor(message: string) {
    super(message, 'INSUFFICIENT_BALANCE');
    this.name = 'InsufficientBalanceError';
  }
}

export class SlippageExceededError extends VVSFinanceError {
  constructor(message: string) {
    super(message, 'SLIPPAGE_EXCEEDED');
    this.name = 'SlippageExceededError';
  }
}
