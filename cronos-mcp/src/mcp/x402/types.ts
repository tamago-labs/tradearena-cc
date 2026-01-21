import { z } from 'zod';

// X402 Payment Request schema
export const PaymentRequestSchema = z.object({
  to: z.string().describe('Recipient address'),
  value: z.string().describe('Payment amount in base units'),
  description: z.string().optional().describe('Payment description'),
  asset: z.string().optional().describe('Asset address (leave empty for native)'),
  validBefore: z.number().optional().describe('Expiry timestamp (optional)'),
  validAfter: z.number().optional().describe('Valid after timestamp (optional)')
});

export type PaymentRequest = z.infer<typeof PaymentRequestSchema>;

// X402 Payment Result schema
export const PaymentResultSchema = z.object({
  paymentId: z.string().describe('Unique payment identifier'),
  txHash: z.string().describe('Transaction hash'),
  settled: z.boolean().describe('Whether payment was settled'),
  at: z.number().describe('Timestamp of settlement'),
  to: z.string().describe('Recipient address'),
  value: z.string().describe('Payment amount'),
  description: z.string().optional().describe('Payment description')
});

export type PaymentResult = z.infer<typeof PaymentResultSchema>;

// Check Payment Request schema
export const CheckPaymentRequestSchema = z.object({
  paymentId: z.string().describe('Payment ID to check')
});

export type CheckPaymentRequest = z.infer<typeof CheckPaymentRequestSchema>;

// Check Payment Result schema
export const CheckPaymentResultSchema = z.object({
  found: z.boolean().describe('Whether payment was found in conversation history'),
  payment: PaymentResultSchema.optional().describe('Payment details if found')
});

export type CheckPaymentResult = z.infer<typeof CheckPaymentResultSchema>;
