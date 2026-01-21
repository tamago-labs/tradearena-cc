import { CallToolResult } from '@modelcontextprotocol/sdk/types.js';
import { type McpTool } from '../../types.js';
import { Facilitator, CronosNetwork } from '@crypto.com/facilitator-client';

/**
 * Cronos X402 Get Supported Tool
 * 
 * This tool returns the supported networks and capabilities for X402 payments.
 * It provides information about available networks, assets, and features.
 */
export const cronos_x402_get_supported: McpTool = {
  name: 'cronos_x402_get_supported',
  description: 'Get supported networks and capabilities for X402 payments',
  schema: {}, // No input parameters required
  
  async handler(agent: any, input: Record<string, any>): Promise<CallToolResult> {
    try {
      // Create facilitator client for Cronos Mainnet
      const facilitator = new Facilitator({ network: CronosNetwork.CronosMainnet });
      
      // Get supported networks and capabilities
      const supported = await facilitator.getSupported();
      
      // Format the response
      const response = {
        supportedNetworks: [
          {
            network: 'cronos-mainnet',
            name: 'Cronos Mainnet',
            chainId: 25,
            status: 'supported'
          }
        ],
        capabilities: {
          schemes: ['exact'], // EIP-3009 exact scheme
          assets: {
            native: {
              symbol: 'CRO',
              name: 'Cronos Native Token',
              decimals: 18,
              supported: true
            },
            // Note: Additional tokens would need to be added based on facilitator response
          },
          features: [
            'EIP-3009 Payment Headers',
            'Off-chain Authorization',
            'On-chain Execution',
            'Payment Verification',
            'Automatic Settlement'
          ]
        },
        facilitatorInfo: supported,
        usage: {
          description: 'Use cronos_x402_pay to make payments and cronos_x402_check_payment to verify them',
          example: {
            pay: {
              tool: 'cronos_x402_pay',
              parameters: {
                to: '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b',
                value: '1000000', // Amount in base units (e.g., 1 USDC = 1000000)
                description: 'Payment for API access'
              }
            },
            check: {
              tool: 'cronos_x402_check_payment',
              parameters: {
                paymentId: 'pay_uuid-here'
              }
            }
          }
        }
      };
      
      return {
        content: [
          {
            type: 'text',
            text: `🌐 X402 Supported Networks and Capabilities\n\n` +
                  `**Supported Networks:**\n` +
                  `- Cronos Mainnet (Chain ID: 25)\n\n` +
                  `**Payment Schemes:**\n` +
                  `- Exact (EIP-3009)\n\n` +
                  `**Features:**\n` +
                  `- EIP-3009 Payment Headers\n` +
                  `- Off-chain Authorization\n` +
                  `- On-chain Execution\n` +
                  `- Payment Verification\n` +
                  `- Automatic Settlement\n\n` +
                  `**Native Asset:**\n` +
                  `- CRO (18 decimals)\n\n` +
                  `**Usage Example:**\n` +
                  `1. Make payment: cronos_x402_pay\n` +
                  `2. Verify payment: cronos_x402_check_payment\n\n` +
                  `**Raw Facilitator Info:**\n${JSON.stringify(supported, null, 2)}`
          }
        ]
      };
      
    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: `❌ Failed to get supported networks: ${error instanceof Error ? error.message : 'Unknown error'}`
          }
        ],
        isError: true
      };
    }
  }
};
