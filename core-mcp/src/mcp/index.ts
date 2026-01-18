 
import {
    tradeArenaWalrusStoreTool,
    tradeArenaWalrusRetrieveTool
} from "./trade-arena/walrus_tools";
import { PythTools } from "./pyth";
 

export const SuiMcpTools = { 
    // Trade Arena Walrus Tools
    "tradeArenaWalrusStoreTool": tradeArenaWalrusStoreTool,
    "tradeArenaWalrusRetrieveTool": tradeArenaWalrusRetrieveTool,
    ...PythTools
}
