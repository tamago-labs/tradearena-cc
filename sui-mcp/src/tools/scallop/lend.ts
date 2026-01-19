import { Transaction } from "@mysten/sui/transactions";
import { Agent } from "../../agent";
import { TransactionResponse } from "../../types";

// Scallop Protocol constants
const SCALLOP_CORE_PACKAGE = "0xefe8b36d5b2e43728cc323298626b83177803521d195cfb11e15b910e892fddf";
const SCALLOP_MARKET_OBJECT = "0xa757975255146dc9686aa823b7838b507f315d704f428cbadad2f4ea061939d9";

export interface LendPosition {
    coinType: string;
    amount: string;
    interestRate: string;
}

/**
 * Lend tokens to Scallop protocol to earn interest
 * @param agent Sui agent instance
 * @param coinType Type of coin to lend (e.g., "0x2::sui::SUI")
 * @param amount Amount to lend in the smallest unit
 * @returns Transaction response
 */
export async function lendToScallop(
    agent: Agent,
    coinType: string,
    amount: number
): Promise<TransactionResponse> {
    try {
        const tx = new Transaction();

        // Split coin for the exact amount
        const [coin] = tx.splitCoins(tx.gas, [amount]);

        // Call Scallop lending function
        tx.moveCall({
            target: `${SCALLOP_CORE_PACKAGE}::lending::lend`,
            arguments: [
                tx.object(SCALLOP_MARKET_OBJECT),
                coin,
            ],
            typeArguments: [coinType],
        });

        // Set gas budget
        tx.setGasBudget(10000000);

        // Sign and execute transaction
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
        console.error("Lend to Scallop failed:", error);
        throw new Error(`Lend failed: ${error.message}`);
    }
}

/**
 * Withdraw lent tokens from Scallop protocol
 * @param agent Sui agent instance
 * @param coinType Type of coin to withdraw
 * @param amount Amount to withdraw
 * @returns Transaction response
 */
export async function withdrawFromScallop(
    agent: Agent,
    coinType: string,
    amount: number
): Promise<TransactionResponse> {
    try {
        const tx = new Transaction();

        // Call Scallop withdraw function
        tx.moveCall({
            target: `${SCALLOP_CORE_PACKAGE}::lending::withdraw`,
            arguments: [
                tx.object(SCALLOP_MARKET_OBJECT),
                tx.pure.u64(amount),
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
        console.error("Withdraw from Scallop failed:", error);
        throw new Error(`Withdraw failed: ${error.message}`);
    }
}

/**
 * Get lending position details from Scallop
 * @param agent Sui agent instance
 * @param walletAddress User's wallet address
 * @returns Array of lending positions
 */
export async function getScallopPositions(
    agent: Agent,
    walletAddress: string
): Promise<LendPosition[]> {
    try {
        // Get all objects owned by the user
        const objects = await agent.client.getOwnedObjects({
            owner: walletAddress,
            filter: {
                StructType: `${SCALLOP_CORE_PACKAGE}::lending::LendingPosition`
            },
            options: {
                showContent: true,
                showType: true,
            },
        });

        const positions: LendPosition[] = [];

        for (const obj of objects.data) {
            if (obj.data?.content && 'fields' in obj.data.content) {
                const fields = obj.data.content.fields as any;
                positions.push({
                    coinType: fields.coin_type || "Unknown",
                    amount: fields.amount || "0",
                    interestRate: fields.interest_rate || "0",
                });
            }
        }

        return positions;
    } catch (error: any) {
        console.error("Get Scallop positions failed:", error);
        return [];
    }
}
