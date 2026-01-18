import { createPublicClient, createWalletClient, http, WalletClient, Address, parseUnits, formatUnits, maxUint256 } from 'viem';
import { privateKeyToAccount, type Account, generatePrivateKey } from 'viem/accounts';
import { 
  publicClient, 
  walletClient, 
  account, 
  networkInfo,
  TOKENS,
  getEnvironmentConfig
} from '../config'; 
import { WalletInfo, TokenInfo } from '../types';
import { cronos } from "viem/chains"

/**
 * Cronos Wallet Agent - handles all wallet operations on Cronos network
 */
export class CronosWalletAgent  {
  
  private account: Account | null = null;
  private walletClient: WalletClient | null = null;

  constructor(privateKey?: string) {
    if (privateKey) {
      // Initialize wallet for transaction capabilities
      // Ensure private key is properly formatted as hex string
      const formattedPrivateKey = privateKey.startsWith('0x') ? privateKey : `0x${privateKey}`;

      // Validate private key format
      if (!/^0x[0-9a-fA-F]{64}$/.test(formattedPrivateKey)) {
        throw new Error(`Invalid private key format. Expected 64 hex characters (32 bytes), got: ${formattedPrivateKey.length - 2} characters`);
      }

      this.account = privateKeyToAccount(formattedPrivateKey as `0x${string}`);
      this.walletClient = createWalletClient({
        account: this.account,
        chain: cronos,
        transport: http(networkInfo.rpcProviderUrl)
      });
    } else {
      // Generate a random account for read-only operations
      const randomPrivateKey = generatePrivateKey();
      this.account = privateKeyToAccount(randomPrivateKey);
    }
  }

  /**
   * Get wallet address
   */
  getAddress(): Address {
    return account.address;
  }

  /**
   * Get comprehensive wallet information including token balances
   */
  async getWalletInfo(): Promise<WalletInfo> {
    const address = this.getAddress();
    
    // Get native CRO balance
    const nativeBalance = await publicClient.getBalance({
      address: address
    });

    // Get token balances for major tokens
    const tokenAddresses = Object.values(TOKENS).filter(
      addr => addr !== TOKENS.CRO // Exclude native token
    );

    const tokenInfos: TokenInfo[] = [];

    for (const tokenAddress of tokenAddresses) {
      try {
        const tokenInfo = await this.getTokenInfo(tokenAddress, address);
        if (tokenInfo) {
          tokenInfos.push(tokenInfo);
        }
      } catch (error) {
        // Skip tokens that fail to load
        console.warn(`Failed to load token ${tokenAddress}:`, error);
      }
    }

    return {
      address: address,
      nativeBalance: (Number(nativeBalance) / 1e18).toString(),
      tokens: tokenInfos,
      network: {
        chainId: 25,
        name: "cronos"
      }
    };
  }

  /**
   * Get token information including balance for a specific token
   */
  async getTokenInfo(tokenAddress: Address, walletAddress?: Address): Promise<TokenInfo | null> {
    try {
      const targetAddress = walletAddress || this.getAddress();
      
      // Get token metadata (name, symbol, decimals)
      const [name, symbol, decimals] = await Promise.all([
        publicClient.readContract({
          address: tokenAddress,
          abi: [
            {
              inputs: [],
              name: 'name',
              outputs: [{ type: 'string' }],
              stateMutability: 'view',
              type: 'function'
            }
          ] as const,
          functionName: 'name'
        }),
        publicClient.readContract({
          address: tokenAddress,
          abi: [
            {
              inputs: [],
              name: 'symbol',
              outputs: [{ type: 'string' }],
              stateMutability: 'view',
              type: 'function'
            }
          ] as const,
          functionName: 'symbol'
        }),
        publicClient.readContract({
          address: tokenAddress,
          abi: [
            {
              inputs: [],
              name: 'decimals',
              outputs: [{ type: 'uint8' }],
              stateMutability: 'view',
              type: 'function'
            }
          ] as const,
          functionName: 'decimals'
        })
      ]);

      // Get token balance
      const balance = await publicClient.readContract({
        address: tokenAddress,
        abi: [
          {
            inputs: [{ name: 'account', type: 'address' }],
            name: 'balanceOf',
            outputs: [{ type: 'uint256' }],
            stateMutability: 'view',
            type: 'function'
          }
        ] as const,
        functionName: 'balanceOf',
        args: [targetAddress]
      });

      const balanceNumber = Number(balance) / Math.pow(10, decimals);

      return {
        address: tokenAddress,
        symbol,
        name,
        decimals,
        balance: balanceNumber.toString()
      };
    } catch (error) {
      return null;
    }
  }

  /**
   * Send native CRO tokens
   */
  async sendNativeToken(to: Address, amount: string): Promise<{ hash: string }> {
    const amountInWei = BigInt(Math.floor(parseFloat(amount) * 1e18).toString());
    
    const hash = await walletClient.sendTransaction({
      account,
      to,
      value: amountInWei,
      chain: networkInfo.chain
    });

    return { hash };
  }

  /**
   * Send ERC20 tokens
   */
  async sendERC20Token(
    tokenAddress: Address, 
    to: Address, 
    amount: string
  ): Promise<{ hash: string }> {
    // Get token decimals first
    const decimals = await publicClient.readContract({
      address: tokenAddress,
      abi: [
        {
          inputs: [],
          name: 'decimals',
          outputs: [{ type: 'uint8' }],
          stateMutability: 'view',
          type: 'function'
        }
      ] as const,
      functionName: 'decimals'
    });

    const amountInWei = BigInt(Math.floor(parseFloat(amount) * Math.pow(10, decimals)).toString());

    const hash = await walletClient.writeContract({
      address: tokenAddress,
      abi: [
        {
          inputs: [
            { name: 'to', type: 'address' },
            { name: 'amount', type: 'uint256' }
          ],
          name: 'transfer',
          outputs: [{ type: 'bool' }],
          stateMutability: 'nonpayable',
          type: 'function'
        }
      ] as const,
      functionName: 'transfer',
      args: [to, amountInWei],
      account,
      chain: networkInfo.chain
    });

    return { hash };
  }

  /**
   * Check token allowance
   */
  async getTokenAllowance(
    tokenAddress: Address,
    spender: Address,
    owner?: Address
  ): Promise<string> {
    const ownerAddress = owner || this.getAddress();
    
    const allowance = await publicClient.readContract({
      address: tokenAddress,
      abi: [
        {
          inputs: [
            { name: 'owner', type: 'address' },
            { name: 'spender', type: 'address' }
          ],
          name: 'allowance',
          outputs: [{ type: 'uint256' }],
          stateMutability: 'view',
          type: 'function'
        }
      ] as const,
      functionName: 'allowance',
      args: [ownerAddress, spender]
    });

    return allowance.toString();
  }

  /**
   * Approve token spending
   */
  async approveToken(
    tokenAddress: Address,
    spender: Address,
    amount: string
  ): Promise<{ hash: string }> {
    // Get token decimals
    const decimals = await publicClient.readContract({
      address: tokenAddress,
      abi: [
        {
          inputs: [],
          name: 'decimals',
          outputs: [{ type: 'uint8' }],
          stateMutability: 'view',
          type: 'function'
        }
      ] as const,
      functionName: 'decimals'
    });

    const amountInWei = BigInt(Math.floor(parseFloat(amount) * Math.pow(10, decimals)).toString());

    const hash = await walletClient.writeContract({
      address: tokenAddress,
      abi: [
        {
          inputs: [
            { name: 'spender', type: 'address' },
            { name: 'amount', type: 'uint256' }
          ],
          name: 'approve',
          outputs: [{ type: 'bool' }],
          stateMutability: 'nonpayable',
          type: 'function'
        }
      ] as const,
      functionName: 'approve',
      args: [spender, amountInWei],
      account,
      chain: networkInfo.chain
    });

    return { hash };
  }

  /**
   * Wrap CRO to WCRO
   */
  async wrapCRO(amount: string): Promise<{ hash: string }> {
    const amountInWei = BigInt(Math.floor(parseFloat(amount) * 1e18).toString());

    const hash = await walletClient.writeContract({
      address: TOKENS.WCRO,
      abi: [
        {
          inputs: [],
          name: 'deposit',
          outputs: [],
          stateMutability: 'payable',
          type: 'function'
        }
      ] as const,
      functionName: 'deposit',
      value: amountInWei,
      account,
      chain: networkInfo.chain
    });

    return { hash };
  }

  /**
   * Unwrap WCRO to CRO
   */
  async unwrapWCRO(amount: string): Promise<{ hash: string }> {
    const amountInWei = BigInt(Math.floor(parseFloat(amount) * 1e18).toString());

    const hash = await walletClient.writeContract({
      address: TOKENS.WCRO,
      abi: [
        {
          inputs: [{ name: 'amount', type: 'uint256' }],
          name: 'withdraw',
          outputs: [],
          stateMutability: 'nonpayable',
          type: 'function'
        }
      ] as const,
      functionName: 'withdraw',
      args: [amountInWei],
      account,
      chain: networkInfo.chain
    });

    return { hash };
  }

  /**
   * Wait for transaction confirmation
   */
  async waitForTransaction(hash: string, maxWaitTime?: number): Promise<any> {
    return await publicClient.waitForTransactionReceipt({
      hash: hash as Address,
      timeout: maxWaitTime || 60000 // 60 seconds default
    });
  }

  /**
   * Get transaction status
   */
  async getTransactionStatus(hash: string): Promise<{
    status: 'success' | 'pending' | 'failed';
    blockNumber?: string;
    gasUsed?: string;
    gasPrice?: string;
  }> {
    try {
      const receipt = await publicClient.getTransactionReceipt({
        hash: hash as Address
      });

      if (receipt) {
        return {
          status: receipt.status === 'success' ? 'success' : 'failed',
          blockNumber: receipt.blockNumber?.toString(),
          gasUsed: receipt.gasUsed?.toString(),
          gasPrice: receipt.effectiveGasPrice?.toString()
        };
      } else {
        // Transaction not yet mined
        return { status: 'pending' };
      }
    } catch (error) {
      return { status: 'failed' };
    }
  }

  /**
   * Get current block number
   */
  async getCurrentBlockNumber(): Promise<string> {
    const blockNumber = await publicClient.getBlockNumber();
    return blockNumber.toString();
  }

  /**
   * Get gas price
   */
  async getGasPrice(): Promise<string> {
    const gasPrice = await publicClient.getGasPrice();
    return gasPrice.toString();
  }
}

// Export singleton instance
export const cronosWalletAgent = new CronosWalletAgent();
