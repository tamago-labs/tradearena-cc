 
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

export const CronosTools = {
  // Basic wallet information and account management
  ...WalletTools,
  
  // VVS Finance tools
  ...VVSTools,
}

// Export individual modules for direct access
export * from './wallet';
