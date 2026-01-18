

export interface SuiConfig {
    privateKey: string;
    walletAddress: string;
    network: 'testnet' | 'mainnet'; 
    walrusUploadRelayHost?: string;
    walrusMaxTip?: number;
}

export interface McpTool {
    name: string;
    description: string;
    schema: any;
    handler: any;
}

export interface TokenBalance {
    address: string;
    name: string;
    symbol: string;
    decimals: number;
    balance: string;
}

export interface TransactionResponse {
    digest?: string;
    status: string;
    error?: string;
}

export interface SwapQuote {
    fromToken: string;
    toToken: string;
    inputAmount: number;
    estimatedOutput: number;
}

export interface FaucetParams {
    usdcGlobalId?: string;
    btcGlobalId?: string;
    packageId: string;
    amount: number;
    recipient: string;
}

export interface TransactionResult {
    status: 'success' | 'error';
    digest?: string;
    error?: string;
    message: string;
}
