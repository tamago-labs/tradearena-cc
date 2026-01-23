import { CallToolResult } from '@modelcontextprotocol/sdk/types.js';
import { type McpTool } from '../../types.js';
import { z } from 'zod';
import { getPaymentRecords } from './verify_payment_tool.js';
 
/**
 * Cronos X402 Check Entitlement Tool
 * 
 * This tool checks if a user has paid for access by verifying the payment ID.
 * It returns the payment details if found and settled.
 */
export const cronos_x402_check_entitlement: McpTool = {
  name: 'cronos_x402_check_entitlement',
  description: 'Check if a payment ID corresponds to a settled payment (entitlement verification)',
  schema: {
    paymentId: z.string().describe('Payment ID to check entitlement for'),
  },

  async handler(agent: any, input: Record<string, any>): Promise<CallToolResult> {
    try {
      const { paymentId } = input;

      // Get payment records from the verify payment tool
      const paymentRecords = getPaymentRecords();

      // Check if payment exists and is settled
      const paymentRecord = paymentRecords.get(paymentId);

      if (!paymentRecord) {
        return {
          content: [
            {
              type: 'text',
              text: `❌ No payment found for Payment ID: ${paymentId}\n\n` +
                `This payment ID either doesn't exist or hasn't been verified yet.\n` +
                `Use cronos_x402_verify_payment to verify and settle payments first.`
            }
          ],
          isError: true
        };
      }

      if (!paymentRecord.settled) {
        return {
          content: [
            {
              type: 'text',
              text: `⏳ Payment found but not yet settled\n\n` +
                `Payment ID: ${paymentId}\n` +
                `Status: Pending settlement\n` +
                `Created at: ${new Date(paymentRecord.at).toISOString()}\n\n` +
                `The payment has been verified but settlement is still in progress.`
            }
          ]
        };
      }

      // Payment exists and is settled - return entitlement details
      return {
        content: [
          {
            type: 'text',
            text: `✅ Valid entitlement found!\n\n` +
              `Payment ID: ${paymentId}\n` +
              `Status: Settled ✅\n` +
              `Transaction Hash: ${paymentRecord.txHash}\n` +
              `Recipient: ${paymentRecord.payTo}\n` +
              `Amount: ${paymentRecord.amount} ${paymentRecord.asset}\n` +
              `Network: ${paymentRecord.network}\n` +
              `Settled at: ${new Date(paymentRecord.at).toISOString()}\n\n` +
              `This payment ID grants access to protected resources.`
          }
        ]
      };

    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: `❌ Failed to check entitlement: ${error instanceof Error ? error.message : 'Unknown error'}`
          }
        ],
        isError: true
      };
    }
  }
};

/**
 * Cronos X402 List Payments Tool
 * 
 * This tool lists all recorded payments for debugging and management.
 */
export const cronos_x402_list_payments: McpTool = {
  name: 'cronos_x402_list_payments',
  description: 'List all recorded payments (for debugging and management)',
  schema: {},

  async handler(agent: any, input: Record<string, any>): Promise<CallToolResult> {
    try {
      const paymentRecords = getPaymentRecords();

      if (paymentRecords.size === 0) {
        return {
          content: [
            {
              type: 'text',
              text: `📄 No payments recorded yet.\n\n` +
                `Use cronos_x402_verify_payment to verify and settle payments.`
            }
          ]
        };
      }

      let paymentList = `📄 All Recorded Payments (${paymentRecords.size} total):\n\n`;

      for (const [paymentId, record] of paymentRecords.entries()) {
        const status = record.settled ? '✅ Settled' : '⏳ Pending';
        const settledDate = new Date(record.at).toISOString();

        paymentList += `Payment ID: ${paymentId}\n`;
        paymentList += `Status: ${status}\n`;
        paymentList += `Amount: ${record.amount} ${record.asset}\n`;
        paymentList += `Recipient: ${record.payTo}\n`;
        paymentList += `Network: ${record.network}\n`;
        paymentList += `Date: ${settledDate}\n`;
        if (record.txHash) {
          paymentList += `Tx Hash: ${record.txHash}\n`;
        }
        paymentList += '\n';
      }

      return {
        content: [
          {
            type: 'text',
            text: paymentList
          }
        ]
      };

    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: `❌ Failed to list payments: ${error instanceof Error ? error.message : 'Unknown error'}`
          }
        ],
        isError: true
      };
    }
  }
};
