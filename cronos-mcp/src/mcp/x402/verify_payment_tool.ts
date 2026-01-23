import { CallToolResult } from '@modelcontextprotocol/sdk/types.js';
import { Facilitator, CronosNetwork, VerifyRequest } from '@crypto.com/facilitator-client';
import { type McpTool } from '../../types.js';
import { z } from 'zod';
import * as crypto from 'node:crypto';

// In-memory store for payment records
const paymentRecords = new Map<string, any>();

// Helper function to create facilitator client
const createFacilitator = (): Facilitator => {
  return new Facilitator({ network: CronosNetwork.CronosMainnet });
};

// Helper function to generate unique payment ID if not provided
const generatePaymentId = (): string => {
  return `pay_${crypto.randomUUID()}`;
};

/**
 * Cronos X402 Verify Payment Tool
 * 
 * This tool handles the merchant side of X402:
 * 1. Verifies EIP-3009 payment headers from clients
 * 2. Settles verified payments on-chain
 * 3. Records successful payments for entitlement tracking
 */
export const cronos_x402_verify_payment: McpTool = {
  name: 'cronos_x402_verify_payment',
  description: 'Verify and settle an X402 payment from a client (merchant side)',
  schema: {
    paymentHeader: z.string().describe('Base64-encoded EIP-3009 payment header from client'),
    paymentRequirements: z.object({
      scheme: z.string(),
      network: z.string(),
      payTo: z.string(),
      asset: z.string().optional(),
      maxAmountRequired: z.string(),
      maxTimeoutSeconds: z.number().optional(),
      description: z.string(),
      mimeType: z.string().optional(),
    }).describe('Payment requirements from the 402 challenge'),
    paymentId: z.string().optional().describe('Optional payment ID to track the payment'),
  },

  async handler(agent: any, input: Record<string, any>): Promise<CallToolResult> {
    try {
      const { paymentHeader, paymentRequirements, paymentId: providedPaymentId } = input;

      // Create facilitator client
      const facilitator = createFacilitator();

      // Generate payment ID if not provided
      const paymentId = providedPaymentId || generatePaymentId();

      // Build verification request - cast to any to handle type compatibility
      const verifyRequest = {
        x402Version: 1,
        paymentHeader,
        paymentRequirements,
      } as VerifyRequest;

      // Verify the payment
      const verifyResponse = await facilitator.verifyPayment(verifyRequest);

      if (!verifyResponse.isValid) {
        return {
          content: [
            {
              type: 'text',
              text: `❌ Payment verification failed\n\n` +
                `Payment ID: ${paymentId}\n` +
                `Reason: ${JSON.stringify(verifyResponse, null, 2)}`
            }
          ],
          isError: true
        };
      }

      // Settle the payment
      const settleResponse = await facilitator.settlePayment(verifyRequest);

      if (settleResponse.event !== 'payment.settled') {
        return {
          content: [
            {
              type: 'text',
              text: `❌ Payment settlement failed\n\n` +
                `Payment ID: ${paymentId}\n` +
                `Reason: ${JSON.stringify(settleResponse, null, 2)}`
            }
          ],
          isError: true
        };
      }

      // Record successful payment
      const paymentRecord = {
        paymentId,
        txHash: settleResponse.txHash,
        settled: true,
        at: Date.now(),
        payTo: paymentRequirements.payTo,
        amount: paymentRequirements.maxAmountRequired,
        asset: paymentRequirements.asset || 'USDC.e',
        network: paymentRequirements.network,
      };

      paymentRecords.set(paymentId, paymentRecord);

      return {
        content: [
          {
            type: 'text',
            text: `✅ X402 payment verified and settled successfully!\n\n` +
              `Payment ID: ${paymentId}\n` +
              `Transaction Hash: ${settleResponse.txHash}\n` +
              `Recipient: ${paymentRequirements.payTo}\n` +
              `Amount: ${paymentRequirements.maxAmountRequired} ${paymentRequirements.asset || 'CRO'}\n` +
              `Network: ${paymentRequirements.network}\n` +
              `Settled at: ${new Date(paymentRecord.at).toISOString()}\n\n` +
              `Use this Payment ID for entitlement checks: ${paymentId}`
          }
        ]
      };

    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: `❌ X402 payment verification failed: ${error instanceof Error ? error.message : 'Unknown error'}`
          }
        ],
        isError: true
      };
    }
  }
};

// Export the payment records for use by other tools
export const getPaymentRecords = () => paymentRecords;
