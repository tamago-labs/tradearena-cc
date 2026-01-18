import { type McpTool } from "../../types";
import { GetWalletInfoTool } from './get_wallet_info_tool';
import { SendERC20TokenTool } from './send_erc20_token_tool';
import { SendNativeTokenTool } from './send_native_token_tool';
import { WrapCROTool } from './wrap_cronos_tool';
import { UnwrapCROTool } from './unwrap_cronos_tool';
import { CheckAllowanceTool } from './check_allowance_tool';
import { ApproveTokenTool } from './approve_token_tool';

// Export all wallet tools using the new zod-based format
export const WalletTools: Record<string, McpTool> = {
  "cronos_get_wallet_info": GetWalletInfoTool,
  "cronos_send_erc20_token": SendERC20TokenTool,
  "cronos_send_native_token": SendNativeTokenTool,
  "cronos_wrap_cro": WrapCROTool,
  "cronos_unwrap_cro": UnwrapCROTool,
  "cronos_check_allowance": CheckAllowanceTool,
  "cronos_approve_token": ApproveTokenTool,
};

// Re-export individual tools for direct access
export {
  GetWalletInfoTool,
  SendERC20TokenTool,
  SendNativeTokenTool,
  WrapCROTool,
  UnwrapCROTool,
  CheckAllowanceTool,
  ApproveTokenTool,
};
