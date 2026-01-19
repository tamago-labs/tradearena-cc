import { setSuiClient, getQuote, buildTx } from "@7kprotocol/sdk-ts";
import { Agent } from "../../agent";
import { TransactionResponse } from "../../types";
import { COIN_MAPPING } from "./util";

interface SwapParams {
  fromToken: string;
  toToken: string;
  amount: number;
  slippage?: number;
}

export async function swapWith7k(
  agent: Agent,
  fromToken: string,
  toToken: string,
  amount: number,
  slippage: number = 0.01 // 1% default slippage
): Promise<TransactionResponse> {
  try {
    const client = agent.client;

    // Convert token symbols to coin types
    const fromCoinType = COIN_MAPPING.get(fromToken) || fromToken;
    const toCoinType = COIN_MAPPING.get(toToken) || toToken;

    // Check balance
    const [balance, metadata] = await Promise.all([
      client.getBalance({
        owner: agent.walletAddress,
        coinType: fromCoinType,
      }),
      client.getCoinMetadata({
        coinType: fromCoinType,
      }),
    ]);

    if (!metadata) {
      throw new Error(`Token ${fromToken} not found`);
    }

    const adjustInputAmount = amount * 10 ** (metadata?.decimals || 9);

    if (Number(balance.totalBalance) < adjustInputAmount) {
      throw new Error("Insufficient balance");
    }

    // Set up 7k SDK
    setSuiClient(client as any);

    // Get quote from 7k
    const quoteResponse = await getQuote({
      tokenIn: fromCoinType,
      tokenOut: toCoinType,
      amountIn: BigInt(adjustInputAmount).toString(),
    });

    // Build transaction
    const txBuild = await buildTx({
      quoteResponse,
      accountAddress: agent.walletAddress,
      slippage: slippage,
      commission: {
        partner: "0xfcd7df57ede898715bc7c5aba3dd31e23b715d2dd16668383ce123666a5e24c3",
        commissionBps: 0,
      },
    });

    // Execute transaction
    const txExec = await client.signAndExecuteTransaction({
      signer: agent.wallet,
      transaction: txBuild as any,
    });

    const tx = await client.waitForTransaction({
      digest: txExec.digest,
      options: {
        showEffects: true,
      },
    });

    return {
      digest: txExec.digest,
      status: tx.effects?.status.status || "unknown",
    };
  } catch (error: any) {
    throw new Error(`Failed to swap tokens: ${error.message}`);
  }
}

export async function get7kSwapQuote(
  agent: Agent,
  fromToken: string,
  toToken: string,
  amount: number
): Promise<any> {
  try {
    const client = agent.client;

    // Convert token symbols to coin types
    const fromCoinType = COIN_MAPPING.get(fromToken) || fromToken;
    const toCoinType = COIN_MAPPING.get(toToken) || toToken;

    // Get metadata for decimals
    const metadata = await client.getCoinMetadata({
      coinType: fromCoinType,
    });

    if (!metadata) {
      throw new Error(`Token ${fromToken} not found`);
    }

    const adjustInputAmount = amount * 10 ** (metadata?.decimals || 9);

    // Set up 7k SDK
    setSuiClient(client as any);

    // Get quote from 7k
    const quoteResponse = await getQuote({
      tokenIn: fromCoinType,
      tokenOut: toCoinType,
      amountIn: BigInt(adjustInputAmount).toString(),
    });

    // Handle different response formats
    const outputAmount = (quoteResponse as any).outputAmount || (quoteResponse as any).expectedOutputAmount || "0";
    const priceImpact = (quoteResponse as any).priceImpactPercent || (quoteResponse as any).priceImpact || 0;

    return {
      fromToken,
      toToken,
      inputAmount: amount,
      expectedOutput: Number(outputAmount) / Math.pow(10, metadata.decimals || 9),
      priceImpact: Number(priceImpact),
      routes: (quoteResponse as any).routes || [],
    };
  } catch (error: any) {
    throw new Error(`Failed to get quote: ${error.message}`);
  }
}

export async function get7kTradingPairs(
  agent: Agent
): Promise<any> {
  try {
    // Return available trading pairs from COIN_MAPPING
    const availableTokens = Array.from(COIN_MAPPING.keys());
    
    // Create all possible pairs
    const pairs = [];
    for (let i = 0; i < availableTokens.length; i++) {
      for (let j = i + 1; j < availableTokens.length; j++) {
        pairs.push({
          from: availableTokens[i],
          to: availableTokens[j],
          pair: `${availableTokens[i]}/${availableTokens[j]}`,
        });
        pairs.push({
          from: availableTokens[j],
          to: availableTokens[i],
          pair: `${availableTokens[j]}/${availableTokens[i]}`,
        });
      }
    }

    return {
      supportedTokens: availableTokens,
      tradingPairs: pairs,
      totalPairs: pairs.length,
    };
  } catch (error: any) {
    throw new Error(`Failed to get trading pairs: ${error.message}`);
  }
}
