#!/usr/bin/env node

import { SuiConfig } from './types';
import { z } from 'zod';

// Validation schemas using zod
export const SuiMCPEnvironmentSchema = z.object({
    privateKey: z.string().optional().describe("Wallet private key"),
    network: z.string().describe("Network")
});

export interface SuiMCPEnvironment {
    privateKey?: string;
    network: string;
}


export function getEnvironmentConfig(): SuiMCPEnvironment {

    const config = {
        privateKey: process.env.SUI_PRIVATE_KEY || "",
        network: "mainnet"
    };

    // Validate with zod schema
    const validatedConfig = SuiMCPEnvironmentSchema.parse(config);

    return validatedConfig;
}

export function validateEnvironment(): void {
    try {
        const config = getEnvironmentConfig();
        const keyStatus = config.privateKey ? 'with private key' : 'without private key';
        console.error(`✅ SUI-MCP configured: transaction mode on sui network (${keyStatus})`);
    } catch (error) {
        console.error('❌ Invalid environment configuration:', error);
        throw error;
    }
}

export function getSuiConfig(): SuiConfig {
    validateEnvironment();

    return getEnvironmentConfig()
}
