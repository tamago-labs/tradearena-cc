import { DelegatedStake, getFullnodeUrl, SuiClient } from "@mysten/sui/client";
import { Ed25519Keypair } from "@mysten/sui/keypairs/ed25519";
import { Transaction } from "@mysten/sui/transactions";
import { SwapQuote, TokenBalance, TransactionResponse } from "../types"; 
import { getSuiConfig } from "../config"; 
import { WalrusClient, WalrusConfig } from "../tools/walrus/client";

export class Agent {

    public client: SuiClient
    public wallet: Ed25519Keypair
    public walletAddress: string;
    public network: 'testnet' | 'mainnet'
    public walrusClient: WalrusClient

    constructor() {

        const config = getSuiConfig()

        this.client = new SuiClient({
            url: getFullnodeUrl(config.network)
        });

        this.network = config.network;

        // Initialize wallet using private key only
        this.wallet = Ed25519Keypair.fromSecretKey(config.privateKey);
        this.walletAddress = this.wallet.getPublicKey().toSuiAddress();

        // Initialize Walrus client
        const walrusConfig: WalrusConfig = {
            network: config.network,
            uploadRelayHost: config.walrusUploadRelayHost,
            maxTip: config.walrusMaxTip
        };
        this.walrusClient = new WalrusClient(this.wallet, walrusConfig);
    }

    async getWalletAddress(): Promise<string> {
        return this.walletAddress;
    }
  
    // Walrus Methods
    async storeTradeData(tradeData: any, epochs?: number): Promise<string> {
        return this.walrusClient.storeTradeData(tradeData, epochs);
    }

    async getTradeData(blobId: string): Promise<any> {
        return this.walrusClient.getTradeData(blobId);
    }
 
    async signAndExecuteTransaction(tx: Transaction) {
        const result = await this.client.signAndExecuteTransaction({
            signer: this.wallet,
            transaction: tx,
            options: {
                showEffects: true,
                showEvents: true,
                showObjectChanges: true
            }
        });
        return result;
    }

}
