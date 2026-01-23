import { CallToolResult } from '@modelcontextprotocol/sdk/types.js';
import { Facilitator, CronosNetwork, Contract } from '@crypto.com/facilitator-client';
import { ethers } from 'ethers';
import { type McpTool } from '../../types.js';
import { CronosWalletAgent } from '../../agent/wallet.js';
import { z } from 'zod';
import * as crypto from 'node:crypto';
import axios from 'axios';

// Schema for payment result
export const PaymentResultSchema = z.object({
  paymentId: z.string(),
  paymentHeader: z.string(),
  paymentRequirements: z.object({
    scheme: z.string(),
    network: z.string(),
    payTo: z.string(),
    asset: z.string().optional(),
    maxAmountRequired: z.string(),
    maxTimeoutSeconds: z.number(),
    description: z.string(),
    mimeType: z.string().optional(),
  }),
  signerAddress: z.string(),
  expiresAt: z.number(),
});

export type PaymentResult = z.infer<typeof PaymentResultSchema>;

// Helper function to create facilitator client
const createFacilitator = (): Facilitator => {
  return new Facilitator({ network: CronosNetwork.CronosMainnet });
};

// Helper function to create signer from CronosWalletAgent
const createSigner = (agent: CronosWalletAgent): ethers.Wallet => {
  const privateKey = agent.getPrivateKey();
  return new ethers.Wallet(privateKey);
};

// Helper function to generate unique payment ID
const generatePaymentId = (): string => {
  return `pay_${crypto.randomUUID()}`;
};

/**
 * Cronos X402 Payment Tool (Client Side)
 * 
 * This tool handles the client side of X402:
 * 1. Generates EIP-3009 payment headers using the configured wallet
 * 2. Creates payment requirements for the merchant
 * 3. Returns everything needed for the client to submit to a merchant
 */
export const cronos_x402_payment: McpTool = {
  name: 'cronos_x402_payment',
  description: 'Generate an X402 payment - creates EIP-3009 header and requirements',
  schema: {
    to: z.string().describe('Recipient address to pay'),
    value: z.string().describe('Amount to pay in base units (e.g., 1000000 for 1 USDC.e)'),
    description: z.string().optional().describe('Payment description'),
    apiEndpoint: z.string().optional().describe('Optional API endpoint to submit payment to for immediate settlement'),
  },

  async handler(agent: CronosWalletAgent, input: Record<string, any>): Promise<CallToolResult> {
    try {
      const { to, description, apiEndpoint, value } = input;

      // Validate inputs
      if (!ethers.isAddress(to)) {
        throw new Error('Invalid recipient address');
      }

      if (!value || isNaN(Number(value)) || Number(value) <= 0) {
        throw new Error('Invalid payment amount');
      }
 
      // Create facilitator and signer
      const facilitator = createFacilitator();
      const signer = createSigner(agent);

      // Generate unique payment ID
      const paymentId = generatePaymentId();

      // Set expiration time (default 10 minutes from now)
      const expiresAt = Math.floor(Date.now() / 1000) + 600

      // Generate payment header (EIP-3009)
      const paymentHeader = await facilitator.generatePaymentHeader({
        to,
        value,
        signer,
        validBefore: expiresAt
      });

      // Generate payment requirements for the merchant
      const paymentRequirements = facilitator.generatePaymentRequirements({
        payTo: to,
        description: description || 'X402 payment via TradeArena',
        maxAmountRequired: value
      });

      // Create payment result
      const paymentResult: PaymentResult = {
        paymentId,
        paymentHeader,
        paymentRequirements: {
          scheme: paymentRequirements.scheme,
          network: paymentRequirements.network,
          payTo: paymentRequirements.payTo,
          asset: paymentRequirements.asset,
          maxAmountRequired: paymentRequirements.maxAmountRequired,
          maxTimeoutSeconds: paymentRequirements.maxTimeoutSeconds,
          description: paymentRequirements.description,
          mimeType: paymentRequirements.mimeType,
        },
        signerAddress: signer.address,
        expiresAt,
      };

      // If apiEndpoint is provided, submit the payment immediately
      if (apiEndpoint) {
        try {
          const submitResponse = await axios.post(apiEndpoint, {
            paymentId,
            paymentHeader,
            paymentRequirements: paymentResult.paymentRequirements,
          }, {
            headers: {
              'Content-Type': 'application/json',
            },
            timeout: 30000, // 30 second timeout
          });

          return {
            content: [
              {
                type: 'text',
                text: `✅ X402 payment generated and submitted successfully!\n\n` +
                  `Payment ID: ${paymentId}\n` +
                  `From: ${signer.address}\n` +
                  `To: ${to}\n` +
                  `Amount: ${value} USDC.e\n` +
                  `Description: ${description || 'No description'}\n` +
                  `Expires at: ${new Date(expiresAt * 1000).toISOString()}\n` +
                  `Submitted to: ${apiEndpoint}\n\n` +
                  `🎯 Merchant Response:\n${JSON.stringify(submitResponse.data, null, 2)}\n\n` +
                  `📋 Payment Header (Base64):\n${paymentHeader}\n\n` +
                  `💡 Payment was submitted and processed by the merchant.`
              }
            ]
          };
        } catch (submitError) {
          return {
            content: [
              {
                type: 'text',
                text: `⚠️ X402 payment generated but submission failed\n\n` +
                  `Payment ID: ${paymentId}\n` +
                  `From: ${signer.address}\n` +
                  `To: ${to}\n` +
                  `Amount: ${value} USDC.e\n` +
                  `Description: ${description || 'No description'}\n` +
                  `Expires at: ${new Date(expiresAt * 1000).toISOString()}\n` +
                  `Submission Error: ${submitError instanceof Error ? submitError.message : 'Unknown error'}\n\n` +
                  `📋 Payment Header (Base64):\n${paymentHeader}\n\n` +
                  `📋 Payment Requirements:\n${JSON.stringify(paymentResult.paymentRequirements, null, 2)}\n\n` +
                  `💡 Payment was generated but failed to submit to ${apiEndpoint}. You can manually submit the payment data above.`
              }
            ],
            isError: true
          };
        }
      }

      // Default behavior: return payment data for manual submission
      return {
        content: [
          {
            type: 'text',
            text: `✅ X402 payment generated successfully!\n\n` +
              `Payment ID: ${paymentId}\n` +
              `From: ${signer.address}\n` +
              `To: ${to}\n` +
              `Amount: ${value} USDC.e\n` +
              `Description: ${description || 'No description'}\n` +
              `Expires at: ${new Date(expiresAt * 1000).toISOString()}\n\n` +
              `📋 Payment Header (Base64):\n${paymentHeader}\n\n` +
              `📋 Payment Requirements:\n${JSON.stringify(paymentResult.paymentRequirements, null, 2)}\n\n` +
              `💡 Submit these to a merchant's payment endpoint to complete the payment.`
          }
        ]
      };

    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: `❌ X402 payment generation failed: ${error instanceof Error ? error.message : 'Unknown error'}\n\n` +
              `💡 Make sure the CronosWalletAgent is properly initialized with a valid private key.`
          }
        ],
        isError: true
      };
    }
  }
};