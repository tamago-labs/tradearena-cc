import { Transaction } from "@mysten/sui/transactions";
import { Agent } from "../../agent";
import { TransactionResponse } from "../../types";

// Scallop Protocol constants
const SCALLOP_CORE_PACKAGE = "0xefe8b36d5b2e43728cc323298626b83177803521d195cfb11e15b910e892fddf";
const SCALLOP_MARKET_OBJECT = "0xa757975255146dc9686aa823b7838b507f315d704f428cbadad2f4ea061939d9";

export interface BorrowPosition {
    coinType: string;
    borrowed: string;
    collateral: string;
    healthRatio: string;
}

/**
 * Borrow tokens from Scallop protocol using collateral
 * @param agent Sui agent instance
 * @param borrowCoinType Type of coin to borrow
 * @param collateralCoinType Type of coin used as collateral
 * @param borrowAmount Amount to borrow
 * @param collateralAmount Amount of collateral to deposit
 * @returns Transaction response
 */
export async function borrowFromScallop(
    agent: Agent,
    borrowCoinType: string,
    collateralCoinType: string,
    borrowAmount: number,
    collateralAmount: number
): Promise<TransactionResponse> {
    try {
        const tx = new Transaction();

        // Split collateral coin
        const [collateralCoin] = tx.splitCoins(tx.gas, [collateralAmount]);

        // Deposit collateral
        tx.moveCall({
            target: `${SCALLOP_CORE_PACKAGE}::lending::deposit_collateral`,
            arguments: [
                tx.object(SCALLOP_MARKET_OBJECT),
                collateralCoin,
            ],
            typeArguments: [collateralCoinType],
        });

        // Borrow tokens
        tx.moveCall({
            target: `${SCALLOP_CORE_PACKAGE}::lending::borrow`,
            arguments: [
                tx.object(SCALLOP_MARKET_OBJECT),
                tx.pure.u64(borrowAmount),
            ],
            typeArguments: [borrowCoinType],
        });

        tx.setGasBudget(15000000);

        const result = await agent.client.signAndExecuteTransaction({
            signer: agent.wallet,
            transaction: tx,
            options: {
                showEffects: true,
                showEvents: true,
            },
        });

        if (result.effects?.status?.status === "success") {
            return {
                digest: result.digest,
                status: "success",
            };
        } else {
            throw new Error("Transaction failed");
        }
    } catch (error: any) {
        console.error("Borrow from Scallop failed:", error);
        throw new Error(`Borrow failed: ${error.message}`);
    }
}

/**
 * Repay borrowed tokens to Scallop protocol
 * @param agent Sui agent instance
 * @param coinType Type of coin to repay
 * @param amount Amount to repay
 * @returns Transaction response
 */
export async function repayToScallop(
    agent: Agent,
    coinType: string,
    amount: number
): Promise<TransactionResponse> {
    try {
        const tx = new Transaction();

        // Split coin for repayment
        const [coin] = tx.splitCoins(tx.gas, [amount]);

        // Repay borrowed tokens
        tx.moveCall({
            target: `${SCALLOP_CORE_PACKAGE}::lending::repay`,
            arguments: [
                tx.object(SCALLOP_MARKET_OBJECT),
                coin,
            ],
            typeArguments: [coinType],
        });

        tx.setGasBudget(10000000);

        const result = await agent.client.signAndExecuteTransaction({
            signer: agent.wallet,
            transaction: tx,
            options: {
                showEffects: true,
                showEvents: true,
            },
        });

        if (result.effects?.status?.status === "success") {
            return {
                digest: result.digest,
                status: "success",
            };
        } else {
            throw new Error("Transaction failed");
        }
    } catch (error: any) {
        console.error("Repay to Scallop failed:", error);
        throw new Error(`Repay failed: ${error.message}`);
    }
}

/**
 * Get borrowing positions from Scallop
 * @param agent Sui agent instance
 * @param walletAddress User's wallet address
 * @returns Array of borrow positions
 */
export async function getScallopBorrowPositions(
    agent: Agent,
    walletAddress: string
): Promise<BorrowPosition[]> {
    try {
        const objects = await agent.client.getOwnedObjects({
            owner: walletAddress,
            filter: {
                StructType: `${SCALLOP_CORE_PACKAGE}::lending::BorrowPosition`
            },
            options: {
                showContent: true,
                showType: true,
            },
        });

        const positions: BorrowPosition[] = [];

        for (const obj of objects.data) {
            if (obj.data?.content && 'fields' in obj.data.content) {
                const fields = obj.data.content.fields as any;
                positions.push({
                    coinType: fields.coin_type || "Unknown",
                    borrowed: fields.borrowed_amount || "0",
                    collateral: fields.collateral_amount || "0",
                    healthRatio: fields.health_ratio || "0",
                });
            }
        }

        return positions;
    } catch (error: any) {
        console.error("Get Scallop borrow positions failed:", error);
        return [];
    }
}
