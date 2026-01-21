 
import { WalletTools } from './wallet';

// Import all VVS tools
import { 
  GetVVSSummaryTool,
  GetVVSTokensTool, 
  GetVVSTokenInfoTool,
  GetVVSPairsTool,
  GetVVSTopPairsTool 
} from './vvs/vvs_tools';

import { 
  GetVVSSwapQuoteTool,
  ExecuteVVSSwapTool 
} from './vvs/swap_tools';

// Import DeFi tools
import {
  CronosGetAllFarmsTool,
  CronosGetFarmBySymbolTool,
  CronosGetWhitelistedTokensTool
} from './defi/get_defi_tools';

// Import Exchange tools
import {
  CronosGetAllTickersTool,
  CronosGetTickerTool,
  CronosGetMarketSummaryTool
} from './crypto-com-exchange/get_exchange_tools';

// Import X402 tools
import {
  cronos_x402_payment,
  cronos_x402_verify_payment,
  cronos_x402_check_entitlement,
  cronos_x402_list_payments,
  cronos_x402_get_supported
} from './x402';

// Combine all VVS tools
const VVSTools = {
  // VVS Analytics tools
  cronos_get_vvs_summary: GetVVSSummaryTool,
  cronos_get_vvs_tokens: GetVVSTokensTool,
  cronos_get_vvs_token_info: GetVVSTokenInfoTool,
  cronos_get_vvs_pairs: GetVVSPairsTool,
  cronos_get_vvs_top_pairs: GetVVSTopPairsTool,
  
  // VVS Swap tools
  cronos_get_vvs_swap_quote: GetVVSSwapQuoteTool,
  cronos_execute_vvs_swap: ExecuteVVSSwapTool,
};

// Combine all DeFi tools
const DeFiTools = {
  cronos_get_all_farms: CronosGetAllFarmsTool,
  cronos_get_farm_by_symbol: CronosGetFarmBySymbolTool,
  cronos_get_whitelisted_tokens: CronosGetWhitelistedTokensTool,
};

// Combine all Exchange tools
const ExchangeTools = {
  cronos_get_all_tickers: CronosGetAllTickersTool,
  cronos_get_ticker: CronosGetTickerTool,
  cronos_get_market_summary: CronosGetMarketSummaryTool,
};

// Combine all X402 tools
const X402Tools = {
  cronos_x402_payment,
  cronos_x402_verify_payment,
  cronos_x402_check_entitlement,
  cronos_x402_list_payments,
  cronos_x402_get_supported
};

export const CronosTools = {
  // Basic wallet information and account management
  ...WalletTools,
  
  // VVS Finance tools
  ...VVSTools,
  
  // DeFi analytics tools
  ...DeFiTools,
  
  // Crypto.com Exchange tools
  ...ExchangeTools,
  
  // X402 Payment tools
  ...X402Tools,
}

// Export individual modules for direct access
export * from './wallet';
export * from './defi/get_defi_tools';
export * from './crypto-com-exchange/get_exchange_tools';
export * from './x402';
