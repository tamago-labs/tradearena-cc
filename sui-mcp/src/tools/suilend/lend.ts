import { Agent } from "../../agent";
import { TransactionResponse } from "../../types";
import {  getWalletHolding, listSUITokenSupportStakeSDKSuilend, getSuilendSdkData } from "./util";
import { Transaction } from "@mysten/sui/transactions";

interface LendingParams {
  symbol: string;
  amount: number;
}

interface WithdrawParams {
  symbol: string;
  amount: number;
}

export async function lendToSuilend(
  agent: Agent,
  params: LendingParams,
): Promise<TransactionResponse> {
  try {
    const { symbol, amount } = params;

    if (amount <= 0) {
      throw new Error("Amount must be greater than 0");
    }

    // Check balance
    const balancesMetadata = await getWalletHolding(agent);

    const tokenData = balancesMetadata.find(
      (r) => r.symbol.toLowerCase() === symbol.toLowerCase(),
    );

    if (!tokenData) {
      throw new Error("Token not found in your wallet");
    }

    if (Number(tokenData.balance) < amount) {
      throw new Error("Insufficient balance");
    }

    // Create transaction
    const transaction = new Transaction();
    transaction.setSender(agent.walletAddress);

    // Get Suilend SDK data
    const appData = await getSuilendSdkData(agent);

    const adjustedAmount = amount * Math.pow(10, tokenData.decimals);
    const coinType = tokenData.address;

    // Check if token is a liquid staking token or regular token
    const isNotEcosystemLTS = listSUITokenSupportStakeSDKSuilend.includes(symbol);

    if (isNotEcosystemLTS) {
      // Regular token lending
      await appData?.suilendClient.depositIntoObligation(
        agent.walletAddress,
        coinType,
        adjustedAmount,
        transaction,
      );
    } else {
      // Liquid staking token lending - simplified for now
      const lstClient = (appData?.lstClientMap as any)?.[symbol];
      if (!lstClient) {
        throw new Error("This token is not supported for lending");
      }

      const lstData = (appData?.lstDataMap as any)?.[symbol];
      if (!lstData) {
        throw new Error("Liquid staking data not found for this token");
      }

      await appData?.suilendClient.depositCoin(
        agent.walletAddress,
        { mintAndRebalance: (tx: any, amt: number) => ({}) }, // Simplified mock
        coinType,
        transaction,
      );
    }

    const txExec = await agent.client.signAndExecuteTransaction({
      signer: agent.wallet,
      transaction: transaction,
    });

    const res = await agent.client.waitForTransaction({
      digest: txExec.digest,
      options: {
        showEffects: true,
      },
    });

    return {
      digest: txExec.digest,
      status: res.effects?.status.status || "unknown",
    };
  } catch (error: any) {
    throw new Error(`Failed to lend token to Suilend: ${error.message}`);
  }
}

export async function withdrawFromSuilend(
  agent: Agent,
  params: WithdrawParams,
): Promise<TransactionResponse> {
  try {
    const { symbol, amount } = params;

    if (amount <= 0) {
      throw new Error("Amount must be greater than 0");
    }

    // Get token metadata
    const balancesMetadata = await getWalletHolding(agent);

    const tokenData = balancesMetadata.find(
      (r) => r.symbol.toLowerCase() === symbol.toLowerCase(),
    );

    if (!tokenData) {
      throw new Error("Token not found in your wallet");
    }

    // Create transaction
    const transaction = new Transaction();
    transaction.setSender(agent.walletAddress);

    // Get Suilend SDK data
    const appData = await getSuilendSdkData(agent);

    const adjustedAmount = amount * Math.pow(10, tokenData.decimals);

    const obligation = appData?.obligations?.[0];
    const obligationOwnerCap = appData?.obligationOwnerCaps?.find(
      (o: any) => o?.obligationId === obligation?.id,
    );

    if (!obligation) {
      throw new Error("No obligation found. You need to have a lending position first.");
    }

    if (!obligationOwnerCap) {
      throw new Error("No obligation owner cap found.");
    }

    const lstDataUnstacking = (appData?.lstDataMap as any)?.[tokenData.symbol];
    if (!lstDataUnstacking) {
      throw new Error("This token is not supported for withdrawal");
    }

    const coinTypeUnstaking =
      appData?.lendingMarket?.reserves?.find(
        (r: any) => r.symbol === tokenData.symbol,
      )?.coinType || lstDataUnstacking?.token?.coinType;

    // Real Suilend SDK call for withdrawal
    await appData?.suilendClient.withdrawAndSendToUser(
      agent.walletAddress,
      obligationOwnerCap.id,
      obligation.id,
      coinTypeUnstaking,
      adjustedAmount,
      transaction,
    );

    const txExec = await agent.client.signAndExecuteTransaction({
      signer: agent.wallet,
      transaction: transaction,
    });

    const res = await agent.client.waitForTransaction({
      digest: txExec.digest,
      options: {
        showEffects: true,
      },
    });

    return {
      digest: txExec.digest,
      status: res.effects?.status.status || "unknown",
    };
  } catch (error: any) {
    throw new Error(`Failed to withdraw token from Suilend: ${error.message}`);
  }
}

export async function getSuilendPositions(
  agent: Agent,
  walletAddress?: string,
): Promise<any> {
  try {
    const address = walletAddress || agent.walletAddress;
    
    // Get Suilend SDK data to fetch real positions
    const appData = await getSuilendSdkData(agent);
    
    const obligations = appData?.obligations || [];
    const reserveMap = appData?.reserveMap || {};
    
    if (obligations.length === 0) {
      return {
        status: "success",
        positions: [],
        totalDepositedUSD: "$0",
        totalAccruedInterestUSD: "$0",
        totalBorrowedUSD: "$0"
      };
    }

    const positions: any[] = [];
    let totalDepositedUSD = 0;
    let totalAccruedInterestUSD = 0;

    // Process each obligation to extract position data
    for (const obligation of obligations) {
      if (obligation.deposits && Array.isArray(obligation.deposits)) {
        for (const deposit of obligation.deposits) {
          const reserveInfo = reserveMap[deposit.coinType];
          if (reserveInfo) {
            const depositedAmount = Number(deposit.value) / Math.pow(10, reserveInfo.decimals || 9);
            const accruedInterest = Number(deposit.indexValue || 0) / Math.pow(10, reserveInfo.decimals || 9);
            const valueUSD = depositedAmount * (reserveInfo.price || 0);
            const interestUSD = accruedInterest * (reserveInfo.price || 0);
            
            totalDepositedUSD += valueUSD;
            totalAccruedInterestUSD += interestUSD;

            positions.push({
              symbol: reserveInfo.symbol || deposit.coinType.split('::').pop()?.toUpperCase() || 'UNKNOWN',
              depositedAmount: depositedAmount.toFixed(6),
              accruedInterest: accruedInterest.toFixed(6),
              apy: `${(reserveInfo.depositAprPercent || 0).toFixed(2)}%`,
              valueUSD: `$${valueUSD.toFixed(2)}`,
              interestUSD: `$${interestUSD.toFixed(2)}`,
              coinType: deposit.coinType
            });
          }
        }
      }
    }

    return {
      status: "success",
      positions,
      totalDepositedUSD: `$${totalDepositedUSD.toFixed(2)}`,
      totalAccruedInterestUSD: `$${totalAccruedInterestUSD.toFixed(2)}`,
      totalBorrowedUSD: "$0", // Would need to process borrows similarly
      obligationsCount: obligations.length
    };
  } catch (error: any) {
    throw new Error(`Failed to get Suilend positions: ${error.message}`);
  }
}
