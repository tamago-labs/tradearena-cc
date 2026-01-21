import { CallToolResult } from '@modelcontextprotocol/sdk/types.js';
import { Facilitator, CronosNetwork, Contract } from '@crypto.com/facilitator-client';
import { ethers } from 'ethers';
import { type McpTool } from '../../types.js';
import { z } from 'zod';
import * as crypto from 'node:crypto';

// Schema for payment request
export const PaymentRequestSchema = z.object({
  to: z.string().describe('Recipient address to pay'),
  value: z.string().describe('Amount to pay in base units (e.g., 1000000 for 1 USDC)'),
  description: z.string().optional().describe('Payment description'),
  asset: z.string().optional().describe('Token contract address (optional, uses native CRO if not provided)'),
  validBefore: z.number().optional().describe('Unix timestamp when payment expires (optional)'),
  validAfter: z.number().optional().describe('Unix timestamp when payment becomes valid (optional)'),
});

export type PaymentRequest = z.infer<typeof PaymentRequestSchema>;

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

// Helper function to create signer from private key
const createSigner = (): ethers.Wallet => {
  const privateKey = process.env.CRONOS_PRIVATE_KEY;
  if (!privateKey) {
    throw new Error('CRONOS_PRIVATE_KEY environment variable is required for making payments');
  }
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
  description: 'Generate an X402 payment (client side) - creates EIP-3009 header and requirements',
  schema: PaymentRequestSchema,
  
  async handler(agent: any, input: Record<string, any>): Promise<CallToolResult> {
    try {
      const { to, value, description, asset, validBefore, validAfter } = input as PaymentRequest;
      
      // Validate inputs
      if (!ethers.isAddress(to)) {
        throw new Error('Invalid recipient address');
      }
      
      if (!value || isNaN(Number(value)) || Number(value) <= 0) {
        throw new Error('Invalid payment amount');
      }
      
      // Create facilitator and signer
      const facilitator = createFacilitator();
      const signer = createSigner();
      
      // Generate unique payment ID
      const paymentId = generatePaymentId();
      
      // Set expiration time (default 10 minutes from now)
      const expiresAt = validBefore || Math.floor(Date.now() / 1000) + 600;
      
      // Convert asset string to Contract enum if provided
      let assetContract: Contract | undefined;
      if (asset) {
        // Map to supported contracts, default to USDCe on mainnet
        if (asset.toLowerCase() === Contract.USDCe.toLowerCase()) {
          assetContract = Contract.USDCe;
        } else {
          // For now, only support USDCe on mainnet
          throw new Error(`Unsupported asset: ${asset}. Only USDCe (${Contract.USDCe}) is supported on Cronos Mainnet`);
        }
      }
      
      // Generate payment header (EIP-3009) - using the correct SDK interface
      const paymentHeader = await facilitator.generatePaymentHeader({
        to,
        value,
        signer,
        validBefore: expiresAt,
        validAfter: validAfter || 0,
        asset: assetContract,
      });
      
      // Generate payment requirements for the merchant
      const paymentRequirements = facilitator.generatePaymentRequirements({
        payTo: to,
        description: description || 'X402 payment via TradeArena',
        maxAmountRequired: value,
        asset: assetContract,
        maxTimeoutSeconds: 600, // 10 minutes
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
      
      return {
        content: [
          {
            type: 'text',
            text: `✅ X402 payment generated successfully!\n\n` +
                  `Payment ID: ${paymentId}\n` +
                  `From: ${signer.address}\n` +
                  `To: ${to}\n` +
                  `Amount: ${value} ${asset ? 'tokens' : 'native CRO'}\n` +
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
                `💡 Make sure CRONOS_PRIVATE_KEY environment variable is set with a valid private key.`
        }
        ],
        isError: true
      };
    }
  }
};
