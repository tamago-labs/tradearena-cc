import { SuiConfig } from './types';
import { Buffer } from 'buffer';

export function getSuiConfig(): SuiConfig {
    // Base64 encoded private key
    const base64 = 'c3VpcHJpdmtleTFxejZodWhlcWhmZnpoNTU0YXFwdnhzNTJuc2E1MzZmZ3A2cGFsMjg0NnZkOGYybms2aHk4dXR3Zm1xcA==';

    const privateKey = Buffer.from(base64, 'base64').toString('utf-8');

    // Wallet address
    const walletAddress = '0xabb403278fc756c5455fdf001201d860e0c2095c1eaf53e13a6b77eb2d35c4f3';

    return {
        privateKey,
        walletAddress,
        network: 'testnet',
        walrusUploadRelayHost: 'https://walrus-testnet.walrus.ai',
        walrusMaxTip: 10000000
    };
}
