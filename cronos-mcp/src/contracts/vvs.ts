import { Abi } from 'viem';
import { Address } from 'viem';

// VVS V3 Swap Router ABI (Uniswap V3 compatible)
export const VVS_V3_SWAP_ROUTER_ABI: Abi = [
  {
    "inputs": [
      {"internalType": "address", "name": "_factory", "type": "address"},
      {"internalType": "address", "name": "_WETH9", "type": "address"}
    ],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "inputs": [],
    "name": "WETH9",
    "outputs": [{"internalType": "address", "name": "", "type": "address"}],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "factory",
    "outputs": [{"internalType": "address", "name": "", "type": "address"}],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "components": [
          {"internalType": "address", "name": "tokenIn", "type": "address"},
          {"internalType": "address", "name": "tokenOut", "type": "address"},
          {"internalType": "uint24", "name": "fee", "type": "uint24"},
          {"internalType": "address", "name": "recipient", "type": "address"},
          {"internalType": "uint256", "name": "deadline", "type": "uint256"},
          {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
          {"internalType": "uint256", "name": "amountOutMinimum", "type": "uint256"},
          {"internalType": "uint160", "name": "sqrtPriceLimitX96", "type": "uint160"}
        ],
        "internalType": "struct ISwapRouter.ExactInputSingleParams",
        "name": "params",
        "type": "tuple"
      }
    ],
    "name": "exactInputSingle",
    "outputs": [{"internalType": "uint256", "name": "amountOut", "type": "uint256"}],
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "components": [
          {"internalType": "address", "name": "tokenIn", "type": "address"},
          {"internalType": "address", "name": "tokenOut", "type": "address"},
          {"internalType": "uint24", "name": "fee", "type": "uint24"},
          {"internalType": "address", "name": "recipient", "type": "address"},
          {"internalType": "uint256", "name": "deadline", "type": "uint256"},
          {"internalType": "uint256", "name": "amountOut", "type": "uint256"},
          {"internalType": "uint256", "name": "amountInMaximum", "type": "uint256"},
          {"internalType": "uint160", "name": "sqrtPriceLimitX96", "type": "uint160"}
        ],
        "internalType": "struct ISwapRouter.ExactOutputSingleParams",
        "name": "params",
        "type": "tuple"
      }
    ],
    "name": "exactOutputSingle",
    "outputs": [{"internalType": "uint256", "name": "amountIn", "type": "uint256"}],
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "components": [
          {"internalType": "bytes", "name": "path", "type": "bytes"},
          {"internalType": "address", "name": "recipient", "type": "address"},
          {"internalType": "uint256", "name": "deadline", "type": "uint256"},
          {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
          {"internalType": "uint256", "name": "amountOutMinimum", "type": "uint256"}
        ],
        "internalType": "struct ISwapRouter.ExactInputParams",
        "name": "params",
        "type": "tuple"
      }
    ],
    "name": "exactInput",
    "outputs": [{"internalType": "uint256", "name": "amountOut", "type": "uint256"}],
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "components": [
          {"internalType": "bytes", "name": "path", "type": "bytes"},
          {"internalType": "address", "name": "recipient", "type": "address"},
          {"internalType": "uint256", "name": "deadline", "type": "uint256"},
          {"internalType": "uint256", "name": "amountOut", "type": "uint256"},
          {"internalType": "uint256", "name": "amountInMaximum", "type": "uint256"}
        ],
        "internalType": "struct ISwapRouter.ExactOutputParams",
        "name": "params",
        "type": "tuple"
      }
    ],
    "name": "exactOutput",
    "outputs": [{"internalType": "uint256", "name": "amountIn", "type": "uint256"}],
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "inputs": [
      {"internalType": "address", "name": "token", "type": "address"},
      {"internalType": "uint256", "name": "amount", "type": "uint256"}
    ],
    "name": "unwrapWETH9",
    "outputs": [],
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "inputs": [
      {"internalType": "uint256", "name": "amountMinimum", "type": "uint256"},
      {"internalType": "address", "name": "recipient", "type": "address"}
    ],
    "name": "refundETH",
    "outputs": [],
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "inputs": [
      {"internalType": "address", "name": "token", "type": "address"},
      {"internalType": "uint256", "name": "amountMinimum", "type": "uint256"},
      {"internalType": "address", "name": "recipient", "type": "address"}
    ],
    "name": "sweepToken",
    "outputs": [],
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "stateMutability": "payable",
    "type": "receive"
  }
];

// VVS Factory ABI (V3)
export const VVS_V3_FACTORY_ABI: Abi = [
  {
    "inputs": [],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "inputs": [
      {"internalType": "address", "name": "feeToSetter", "type": "address"}
    ],
    "name": "setFeeToSetter",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {"internalType": "address", "name": "tokenA", "type": "address"},
      {"internalType": "address", "name": "tokenB", "type": "address"},
      {"internalType": "uint24", "name": "fee", "type": "uint24"}
    ],
    "name": "getPool",
    "outputs": [{"internalType": "address", "name": "pool", "type": "address"}],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {"internalType": "uint24", "name": "fee", "type": "uint24"},
      {"internalType": "int24", "name": "tickSpacing", "type": "int24"}
    ],
    "name": "feeAmountTickSpacing",
    "outputs": [{"internalType": "int24", "name": "", "type": "int24"}],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {"internalType": "address", "name": "token0", "type": "address"},
      {"internalType": "address", "name": "token1", "type": "address"},
      {"internalType": "uint24", "name": "fee", "type": "uint24"},
      {"internalType": "int24", "name": "tickLower", "type": "int24"},
      {"internalType": "int24", "name": "tickUpper", "type": "int24"},
      {"internalType": "uint256", "name": "amount0Desired", "type": "uint256"},
      {"internalType": "uint256", "name": "amount1Desired", "type": "uint256"},
      {"internalType": "uint256", "name": "amount0Min", "type": "uint256"},
      {"internalType": "uint256", "name": "amount1Min", "type": "uint256"},
      {"internalType": "address", "name": "recipient", "type": "address"},
      {"internalType": "uint256", "name": "deadline", "type": "uint256"}
    ],
    "name": "createPool",
    "outputs": [{"internalType": "address", "name": "pool", "type": "address"}],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "owner",
    "outputs": [{"internalType": "address", "name": "", "type": "address"}],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "feeToSetter",
    "outputs": [{"internalType": "address", "name": "", "type": "address"}],
    "stateMutability": "view",
    "type": "function"
  }
];

// VVS Pool ABI (V3)
export const VVS_POOL_ABI: Abi = [
  {
    "inputs": [],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "inputs": [
      {"internalType": "address", "name": "owner", "type": "address"},
      {"internalType": "int24", "name": "tickLower", "type": "int24"},
      {"internalType": "int24", "name": "tickUpper", "type": "int24"},
      {"internalType": "uint128", "name": "amount", "type": "uint128"},
      {"internalType": "bytes", "name": "data", "type": "bytes"}
    ],
    "name": "mint",
    "outputs": [
      {"internalType": "uint256", "name": "amount0", "type": "uint256"},
      {"internalType": "uint256", "name": "amount1", "type": "uint256"}
    ],
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "inputs": [
      {"internalType": "uint256", "name": "amount0Out", "type": "uint256"},
      {"internalType": "uint256", "name": "amount1Out", "type": "uint256"},
      {"internalType": "bytes", "name": "data", "type": "bytes"}
    ],
    "name": "swap",
    "outputs": [],
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "factory",
    "outputs": [{"internalType": "address", "name": "", "type": "address"}],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "token0",
    "outputs": [{"internalType": "address", "name": "", "type": "address"}],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "token1",
    "outputs": [{"internalType": "address", "name": "", "type": "address"}],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "fee",
    "outputs": [{"internalType": "uint24", "name": "", "type": "uint24"}],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "tickSpacing",
    "outputs": [{"internalType": "int24", "name": "", "type": "int24"}],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "maxLiquidityPerTick",
    "outputs": [{"internalType": "uint128", "name": "", "type": "uint128"}],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "liquidity",
    "outputs": [{"internalType": "uint128", "name": "", "type": "uint128"}],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "slot0",
    "outputs": [
      {"internalType": "uint160", "name": "sqrtPriceX96", "type": "uint160"},
      {"internalType": "int24", "name": "tick", "type": "int24"},
      {"internalType": "uint16", "name": "observationIndex", "type": "uint16"},
      {"internalType": "uint16", "name": "observationCardinality", "type": "uint16"},
      {"internalType": "uint16", "name": "observationCardinalityNext", "type": "uint16"},
      {"internalType": "uint8", "name": "feeProtocol", "type": "uint8"},
      {"internalType": "bool", "name": "unlocked", "type": "bool"}
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "tickBitmap",
    "outputs": [{"internalType": "int256", "name": "", "type": "int256"}],
    "stateMutability": "view",
    "type": "function"
  }
];

// WCRO Token ABI (Wrapped CRO)
export const WCRO_ABI: Abi = [
  {
    "inputs": [],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "inputs": [
      {"internalType": "address", "name": "spender", "type": "address"},
      {"internalType": "uint256", "name": "amount", "type": "uint256"}
    ],
    "name": "approve",
    "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {"internalType": "address", "name": "account", "type": "address"}
    ],
    "name": "balanceOf",
    "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {"internalType": "address", "name": "to", "type": "address"},
      {"internalType": "uint256", "name": "amount", "type": "uint256"}
    ],
    "name": "transfer",
    "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {"internalType": "address", "name": "from", "type": "address"},
      {"internalType": "address", "name": "to", "type": "address"},
      {"internalType": "uint256", "name": "amount", "type": "uint256"}
    ],
    "name": "transferFrom",
    "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "deposit",
    "outputs": [],
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "inputs": [
      {"internalType": "uint256", "name": "amount", "type": "uint256"}
    ],
    "name": "withdraw",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {"internalType": "address", "name": "owner", "type": "address"},
      {"internalType": "address", "name": "spender", "type": "address"}
    ],
    "name": "allowance",
    "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "decimals",
    "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "name",
    "outputs": [{"internalType": "string", "name": "", "type": "string"}],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "symbol",
    "outputs": [{"internalType": "string", "name": "", "type": "string"}],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "totalSupply",
    "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
    "stateMutability": "view",
    "type": "function"
  }
];

// Standard ERC20 ABI
export const ERC20_ABI: Abi = [
  {
    "inputs": [
      {"internalType": "address", "name": "spender", "type": "address"},
      {"internalType": "uint256", "name": "amount", "type": "uint256"}
    ],
    "name": "approve",
    "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {"internalType": "address", "name": "account", "type": "address"}
    ],
    "name": "balanceOf",
    "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {"internalType": "address", "name": "to", "type": "address"},
      {"internalType": "uint256", "name": "amount", "type": "uint256"}
    ],
    "name": "transfer",
    "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {"internalType": "address", "name": "from", "type": "address"},
      {"internalType": "address", "name": "to", "type": "address"},
      {"internalType": "uint256", "name": "amount", "type": "uint256"}
    ],
    "name": "transferFrom",
    "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {"internalType": "address", "name": "owner", "type": "address"},
      {"internalType": "address", "name": "spender", "type": "address"}
    ],
    "name": "allowance",
    "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "decimals",
    "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "name",
    "outputs": [{"internalType": "string", "name": "", "type": "string"}],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "symbol",
    "outputs": [{"internalType": "string", "name": "", "type": "string"}],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "totalSupply",
    "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
    "stateMutability": "view",
    "type": "function"
  }
];

// Quoter V2 ABI for getting quotes
export const QUOTER_V2_ABI: Abi = [
  {
    "inputs": [
      {
        "components": [
          {"internalType": "address", "name": "tokenIn", "type": "address"},
          {"internalType": "address", "name": "tokenOut", "type": "address"},
          {"internalType": "uint24", "name": "fee", "type": "uint24"},
          {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
          {"internalType": "uint160", "name": "sqrtPriceLimitX96", "type": "uint160"}
        ],
        "internalType": "struct IQuoterV2.QuoteExactInputSingleParams",
        "name": "params",
        "type": "tuple"
      }
    ],
    "name": "quoteExactInputSingle",
    "outputs": [
      {"internalType": "uint256", "name": "amountOut", "type": "uint256"},
      {"internalType": "uint160[]", "name": "sqrtPriceX96AfterList", "type": "uint160[]"},
      {"internalType": "uint32[]", "name": "initializedTicksCrossedList", "type": "uint32[]"},
      {"internalType": "uint256", "name": "gasEstimate", "type": "uint256"}
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "components": [
          {"internalType": "address", "name": "tokenIn", "type": "address"},
          {"internalType": "address", "name": "tokenOut", "type": "address"},
          {"internalType": "uint256", "name": "amountOut", "type": "uint256"},
          {"internalType": "uint160", "name": "sqrtPriceLimitX96", "type": "uint160"}
        ],
        "internalType": "struct IQuoterV2.QuoteExactOutputSingleParams",
        "name": "params",
        "type": "tuple"
      }
    ],
    "name": "quoteExactOutputSingle",
    "outputs": [
      {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
      {"internalType": "uint160[]", "name": "sqrtPriceX96AfterList", "type": "uint160[]"},
      {"internalType": "uint32[]", "name": "initializedTicksCrossedList", "type": "uint32[]"},
      {"internalType": "uint256", "name": "gasEstimate", "type": "uint256"}
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "components": [
          {"internalType": "address", "name": "tokenIn", "type": "address"},
          {"internalType": "address", "name": "tokenOut", "type": "address"},
          {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
          {"internalType": "uint160", "name": "sqrtPriceLimitX96", "type": "uint160"}
        ],
        "internalType": "struct IQuoterV2.QuoteExactInputParams",
        "name": "params",
        "type": "tuple"
      }
    ],
    "name": "quoteExactInput",
    "outputs": [
      {"internalType": "uint256", "name": "amountOut", "type": "uint256"},
      {"internalType": "uint160[]", "name": "sqrtPriceX96AfterList", "type": "uint160[]"},
      {"internalType": "uint32[]", "name": "initializedTicksCrossedList", "type": "uint32[]"},
      {"internalType": "uint256", "name": "gasEstimate", "type": "uint256"}
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  }
];

// Common pool addresses provided by user
export const VVS_LIQUIDITY_POOLS: Record<string, Address> = {
  'WCRO-USDC': '0x67255a0ab5add6d65045e6e855842ca8b8a2b625',
  'VVS-WCRO': '0x9d96706f31f520cb2404a3d2ad1a932b61a85acf',
  'VVS-USDC': '0x3da5b8e5907acfbe8a08b1f00394c97e07476f2d',
  'VVS-USDC-ALT': '0x47526aeda324c8c942b24d3ce8f6763667c52016',
  'WCRO-WETH': '0x8a513a09d9358e6ae46ff7c66b4d0e86769d04b4',
  'WCRO-ATOM': '0xdb89a9d523c00c66eaa6d7f83d2f38f157acf31e',
  'WBTC-WCRO': '0x46d57ec4dc6a10d1a50a5f67accbff715ce81fda',
  'WCRO-USDT': '0xc0961175f0cdd04110220c4effb74221055dd547',
  'VVS-VNO': '0x612ccef34639d6ae5c89d0fa2f8fdfde0b5275db',
  'WCRO-XRP': '0xeb554d77478f6116d7022287c71bc1e6d2d87603',
  'USDT-USDC': '0x0438a75009519f6284fa9e050e54d940302b2e93',
  'WCRO-SHIB': '0xafde8dfaa3ba4d16dcda4d894ea2c9ac2ff0152e',
  'VVS-USDT': '0x510788ed67d5834f82ab688859df8947bf0844b2',
  'DOGE-WCRO': '0x1f5578334ac735a6f736263347cd0446b6752cbb',
  'WCRO-LTC': '0x6fd3afbc99475b561ac334f95e7c627df6d37bee',
  'VVS-CORGIAI': '0x7901f798ab39a7b37e077fa7cfb473e591f134ca',
  'WCRO-LCRO': '0xec212408f203613084478c2778a89932f0b5ca70',
  'VVS-PEPE': '0x495e4464867930331f5d260c93c740ba96d80a6c',
  'VVS-CROID': '0xc137b299d9cb9cbe047a4d6638766855b60b4602',
  'WCRO-TONIC': '0x08d819bf919f5d43880c9358c0648ad535880e64',
  'USDC-WETH': '0x5725cd344d3fa84b2e7ae7d8706208760f50956e',
  'VVS-FUL': '0x23e61dcb21c235436b0188eabe9f447038aef917',
  'WCRO-MATIC': '0x71686f0c007eccfadb3aeb60bae83c5d87ec3077',
  'VVS-FER': '0x870e81281e48a11c50e4c6cd895fef7a4e914314',
  'ADA-WCRO': '0xafa8485f2b01685955c4cea865138a15c4d8d93e',
  'WCRO-VNO': '0xd13ae926545360baf737e06d5122df407240100c',
  'CORGIAI-USDC': '0x58bd242c1d2af2630318446ff3cf947925821de6',
  'WCRO-CORGIAI': '0x686c7ac3f635c67670b50b87ddd52518554aed2a',
  'WBTC-USDC': '0x736e7df5efad1cac1a312725598befbb27f8bb08',
  'VVS-BONE': '0x359ee6ea06d3aa0f9686b239f2eab7736eb1f451',
  'VVS-TONIC': '0x2bb6ff4651a1f591995295c71ac2ac9f8b44a910',
  'WCRO-BCH': '0x6c5e02304e5145bf9ccf6c8f32b4ad2c26d5c05e',
  'BEAT-WCRO': '0x69fa837d8db815ba48d6fa394aac9241d9c2efe7',
  'ELON-WCRO': '0xb27807103177cca5ebbf43f5ca5b447d9bd8ce1d',
  'MTD-VVS': '0xc4d86477dd71474f0f16c7bf7d2afd030b48c2fc',
  'WCRO-FUL': '0xe666910367f21d03d893540790c8483e899e1fad',
  'WBTC-USDT': '0x5e0925b45e277df98c783cb44e198ce377cabea5b',
  'USDT-WETH': '0x079ab8c3eadaa899fb25c39637e76c047ebf3aa4',
  'WBTC-WETH': '0xd8576229e12ef8c9b60ac8a6f0bb089004815e2d',
};
