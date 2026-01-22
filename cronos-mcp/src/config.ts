import { Chain, createPublicClient, createWalletClient, http, WalletClient } from 'viem';
import { privateKeyToAccount, Address, Account, generatePrivateKey } from 'viem/accounts';
import { cronos } from 'viem/chains';
import { z } from 'zod';

type NetworkType = 'cronos'

interface NetworkConfig {
    rpcProviderUrl: string;
    blockExplorer: string;
    chain: Chain;
    chainId: number;
    nativeCurrency: string;
}

// Cronos MCP Environment Configuration
export interface CronosMCPEnvironment {
    cronosRpcUrl: string;
    privateKey?: string;
}
 

// Validation schemas using zod
export const CronosMCPEnvironmentSchema = z.object({
    privateKey: z.string().optional().describe("Wallet private key"),
    cronosRpcUrl: z.string().url().describe("CRONOS RPC URL")
});


export function getEnvironmentConfig(): CronosMCPEnvironment {

    const config = {
        privateKey: process.env.CRONOS_PRIVATE_KEY || "",
        cronosRpcUrl: "https://evm.cronos.org"
    };

    // Validate with zod schema
    const validatedConfig = CronosMCPEnvironmentSchema.parse(config);

    return validatedConfig;
}

// Validate environment variables and log configuration
export function validateEnvironment(): void {
    try {
        const config = getEnvironmentConfig();
        const keyStatus = config.privateKey ? 'with private key' : 'without private key';
        console.error(`✅ CRONOS-MCP configured: transaction mode on cronos network (${keyStatus})`);
    } catch (error) {
        console.error('❌ Invalid environment configuration:', error);
        throw error;
    }
}

// Network configurations - Cronos Mainnet only
const networkConfigs: Record<NetworkType, NetworkConfig> = {
    cronos: {
        rpcProviderUrl: 'https://evm.cronos.org',
        blockExplorer: 'https://cronoscan.com',
        chain: cronos,
        chainId: 25,
        nativeCurrency: 'CRO'
    }
} as const;

const getNetwork = (): NetworkType => {
    return 'cronos';
};

const getAccount = (): Account => {
    const config = getEnvironmentConfig();
    const hasPrivateKey = !!(config?.privateKey);

    if (!hasPrivateKey) {
        const privateKey = generatePrivateKey();
        return privateKeyToAccount(privateKey);
    } else {
        const privateKey = config.privateKey!;
        const formattedPrivateKey = privateKey.startsWith('0x') ? privateKey : `0x${privateKey}`;

        // Validate that the private key is a valid hex string
        if (!/^0x[0-9a-fA-F]{64}$/.test(formattedPrivateKey)) {
            throw new Error(`Invalid private key format. Expected 64 hex characters (32 bytes), got: ${formattedPrivateKey.length - 2} characters`);
        }

        return privateKeyToAccount(formattedPrivateKey as `0x${string}`);
    }
}

// Initialize client configuration
export const network = getNetwork();

export const networkInfo = {
    ...networkConfigs[network],
};

export const account: Account = getAccount()

const baseConfig = {
    chain: networkInfo.chain,
    transport: http(networkInfo.rpcProviderUrl),
} as const;

export const publicClient = createPublicClient(baseConfig);

export const walletClient = createWalletClient({
    ...baseConfig,
    account,
}) as WalletClient;

// Multi-chain client factory
export function createClientForNetwork(networkType: NetworkType) {
    const config = networkConfigs[networkType];
    const baseConfig = {
        chain: config.chain,
        transport: http(config.rpcProviderUrl),
    };

    return {
        publicClient: createPublicClient(baseConfig),
        walletClient: createWalletClient({
            ...baseConfig,
            account,
        }) as WalletClient,
        networkInfo: config
    };
}

// VVS Finance Contracts on Cronos
export const VVS_CONTRACTS = {
    // Core contracts
    FACTORY: '0x54Ff509102D51Bf4e0d06184A051c1e917333254' as Address,
    ROUTER: '0x2e5dbaa86FcA7cb73F060300C55B51C72f1B8554' as Address,
    V3_FACTORY: '0x5e12F3bdEb62c6296Fa457b1A69438d7Fe8C6E2e' as Address,
    V3_SWAP_ROUTER: '0xE3Df4f9b1454EC806a712932d62810ddC641B8cC' as Address,
    SMART_ROUTER: '0xF15133D086a2Cf2a8a6FFA730Fb02C8421Eecc92' as Address,
} as const;

// Core tokens on Cronos
export const TOKENS = {
    // Native
    CRO: "0x0000000000000000000000000000000000000000" as Address,
    WCRO: '0x5C7F8A570d578ED84E63fdFA7b1eE72dEae1AE23' as Address,

    // Major Tokens
    WBTC: '0x062E66477Faf219F25D27dCED647BF57C3107d52' as Address,
    WETH: '0xe44Fd7fCb2b1581822D0c862B68222998a0c299a' as Address,
    USDC: '0xc21223249CA28397B4B6541dfFaEcC539BfF0c59' as Address,
    USDCe: '0xf951eC28187D9E5Ca673Da8FE6757E6f0Be5F77C' as Address,
    VVS: '0x2D03bECE6747ADC00E1a131BBA1469C15fD11e03' as Address,
    USDT: '0x66e428c3f67a68878562e79A0234c1F83c208770' as Address,
    SHIB: '0xbed48612bc69fa1cab67052b42a95fb30c1bcfee' as Address,
    // BIFI: '0xe6801928061CDbE32AC5AD0634427E140EFd05F9' as Address,
    // ATOM: '0xb888d8dd1733d72681b30c00ee76bde93ae7aa93' as Address,
    // DOGE: '0x1a8e39ae59e5556b56b76fcba98d22c9ae557396' as Address,
    // TONIC: '0xdd73dea10abc2bff99c60882ec5b2b81bb1dc5b2' as Address,
    // LINK: '0xbc6f24649ccd67ec42342accdceccb2efa27c9d9' as Address,
    // ENJ: '0x0a92ea8a197919acb9bc26660ed0d43d01ed26b7' as Address,
    // SINGLE: '0x0804702a4e749d39a35fde73d1df0b1f1d6b8347' as Address,
    // LUNA: '0x9278C8693e7328bef49804BacbFb63253565dffD' as Address,
    // ELON: '0x02DCcaf514C98451320a9365C5b46C61d3246ff3' as Address,
    // TUSD: '0x87EFB3ec1576Dec8ED47e58B832bEdCd86eE186e' as Address,
    // DOT: '0x994047FE66406CbD646cd85B990E11D7F5dB8fC7' as Address,
    // PENDLE: '0x49c3bBB239f4FB44327073510f4bA72D207a81D6' as Address,
    // EOS: '0xA37caA841072a305a0799718aFA16cd504C52118' as Address,
    // XLM: '0x747d6C858168B8cD6e537160320b5dE58FD3367C' as Address,
    // ADA: '0x0e517979C2c1c1522ddB0c73905e0D39b3F990c0' as Address,
    // DERC: '0x98616a1427a1734DaEbA1E1894db48051244A065' as Address,
    // RADAR: '0xa58e3AeAeA3292c3E260378e55E9684C59E7A27a' as Address,
} as const;

// V3 Fee tiers for Uniswap V3 style pools
export const FEE_TIERS = {
    LOWEST: 100,    // 0.01%
    LOW: 500,       // 0.05%
    MEDIUM: 3000,   // 0.3%
    HIGH: 10000,    // 1%
} as const;

// Default Slippage Tolerance (in basis points)
export const DEFAULT_SLIPPAGE = 50; // 0.5%

// Default Transaction Deadline (in minutes)
export const DEFAULT_DEADLINE = 20;

// Pool Creation Constants
export const POOL_CONSTANTS = {
    MIN_TICK: -887272,
    MAX_TICK: 887272,
    TICK_SPACING: {
        100: 1,
        500: 10,
        3000: 60,
        10000: 200,
    },
} as const;
