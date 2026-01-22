"use client"

import { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { Terminal } from 'lucide-react';

const InteractiveTerminal = ({ autoStart = false, embedded = false }: { autoStart?: boolean; embedded?: boolean }) => {
    const [isPlaying, setIsPlaying] = useState(false);
    const [isPaused, setIsPaused] = useState(false);
    // const [currentStep, setCurrentStep] = useState(0);
    const [terminalState, setTerminalState] = useState({
        screen: 'main',
        selectedItem: 0,
        messages: [] as string[],
        userInput: '',
        processing: false
    });
    
    const terminalRef = useRef<HTMLDivElement>(null);
    const demoControllerRef = useRef<{
        shouldStop: boolean;
        shouldPause: boolean;
        resume: () => void;
    }>({
        shouldStop: false,
        shouldPause: false,
        resume: () => {}
    });


    const mainMenuItems = [
        'Interactive Mode',
        'Manage Views', 
        'Configure Agent',
        'Settings'
    ];

    const interactiveMenuItems = [
        'Start New Session',
        'Resume Last Session', 
        'Back to Main Menu'
    ];

    const demoSteps = [
        {
            type: 'show_main_menu',
            delay: 2000
        },
        {
            type: 'navigate_to_interactive',
            delay: 1000
        },
        {
            type: 'select_interactive',
            delay: 500
        },
        {
            type: 'show_interactive_menu',
            delay: 1000
        },
        {
            type: 'start_new_session',
            delay: 500
        },
        {
            type: 'show_ai_chat',
            delay: 1000
        },
        {
            type: 'user_input',
            input: 'help maximise my 50 USDT',
            delay: 2000
        },
        {
            type: 'ai_response',
            delay: 3000
        },
        {
            type: 'user_input',
            input: 'go for option 2',
            delay: 2000
        },
        {
            type: 'ai_response',
            input: 'go for option 2',
            delay: 6000
        },
        {
            type: 'execution_result',
            delay: 2000
        },
        {
            type: 'demo_complete',
            delay: 4000
        }
    ];

    useEffect(() => {
        if (autoStart && !isPlaying) {
            runDemo();
        }
        
        return () => {
            // Cleanup on unmount
            demoControllerRef.current.shouldStop = true;
        };
    }, [autoStart]);

    // Auto-scroll to bottom when terminal state changes
    useEffect(() => {
        if (terminalRef.current) {
            setTimeout(() => {
                terminalRef.current?.scrollTo({
                    top: terminalRef.current.scrollHeight,
                    behavior: 'smooth'
                });
            }, 100);
        }
    }, [terminalState]);

    const sleep = (ms: number) => {
        return new Promise(resolve => setTimeout(resolve, ms));
    };

    const waitForResume = () => {
        return new Promise<void>((resolve) => {
            const checkResume = () => {
                if (!demoControllerRef.current.shouldPause) {
                    resolve();
                } else {
                    setTimeout(checkResume, 100);
                }
            };
            checkResume();
        });
    };

    const runDemo = async () => {
        const startDemo = async () => {
            setIsPlaying(true);
            setIsPaused(false);
            // setCurrentStep(0);
            demoControllerRef.current.shouldStop = false;
            demoControllerRef.current.shouldPause = false;

            try {
                for (let i = 0; i < demoSteps.length; i++) {
                    if (demoControllerRef.current.shouldStop) break;
                    
                    if (demoControllerRef.current.shouldPause) {
                        await waitForResume();
                    }
                    
                    if (demoControllerRef.current.shouldStop) break;

                    // setCurrentStep(i);
                    const step = demoSteps[i];
                    
                    // Execute step based on type
                    switch (step.type) {
                        case 'show_main_menu':
                            setTerminalState({
                                screen: 'main',
                                selectedItem: 0,
                                messages: [],
                                userInput: '',
                                processing: false
                            });
                            break;
                            
                        case 'navigate_to_interactive':
                            // Simulate arrow key navigation
                            for (let j = 0; j <= 0; j++) {
                                setTerminalState(prev => ({ ...prev, selectedItem: j }));
                                await sleep(300);
                            }
                            break;
                            
                        case 'select_interactive':
                            await sleep(500);
                            break;
                            
                        case 'show_interactive_menu':
                            setTerminalState({
                                screen: 'interactive',
                                selectedItem: 0,
                                messages: [],
                                userInput: '',
                                processing: false
                            });
                            break;
                            
                        case 'start_new_session':
                            setTerminalState(prev => ({ ...prev, selectedItem: 0 }));
                            await sleep(500);
                            break;
                            
                        case 'show_ai_chat':
                            setTerminalState({
                                screen: 'chat',
                                selectedItem: 0,
                                messages: ['AI Agent Initialized', 'Portfolio: 50 USDT', 'Network: KAIA', '', 'Agent: Ready for commands'],
                                userInput: '',
                                processing: false
                            });
                            break;
                            
                        case 'user_input':
                            setTerminalState(prev => ({ ...prev, userInput: '', processing: true }));
                            // Simulate typing
                            for (let char of step.input!) {
                                setTerminalState(prev => ({ ...prev, userInput: prev.userInput + char }));
                                await sleep(50);
                            }
                            setTerminalState(prev => ({ 
                                ...prev, 
                                messages: [...prev.messages, `> ${prev.userInput}`],
                                userInput: '',
                                processing: false
                            }));
                            break;
                            
                        case 'ai_response':
                            const response = step.input === 'go for option 2' ? [
                                'Agent: Executing Leverage Strategy...',
                                '',
                                '⚡ Initiating transactions...',
                                '',
                                '✅ Supply Transaction: 0x7f9a2b3c4d5e6f8a1b2c3d4e5f6a7b8c9',
                                '   • 50 USDT supplied to KiloLend',
                                '   • Collateral value: 50 USDT',
                                '',
                                '✅ Borrow Transaction: 0x9b8c3d2e1f5a6b7c8d9e0f1a2b3c4d5e6',
                                '   • Borrowed: 25 KAIA (current price: $0.85)',
                                '   • Current Health Factor: 1.5',
                                '',
                                '📈 Position Summary:',
                                '• Total Supply: 50 USDT',
                                '• Total Borrow: 21.25 USDT (25 KAIA)',
                                '• Health Factor: 1.5 (Safe range: >1.2)',
                                '• Estimated APY: 9.8%',
                                '',
                                '🔄 Strategy Active - Monitoring market conditions...'
                            ] : [
                                '🤖 Analyzing opportunities on KAIA network...',
                                '📊 Current KiloLend APY: 3.14%',
                                '🔍 Market conditions: Optimal for leverage',
                                '',
                                'I recommend 2 strategies:',
                                '',
                                '1️⃣  **Safe Play** - Supply to KiloLend',
                                '   • APY: 3.14%',
                                '   • Risk: Minimal',
                                '   • Expected return: 51.57 USDT/year',
                                '',
                                '2️⃣  **Leverage Play** - Supply + Borrow',
                                '   • Supply: 50 USDT → KiloLend',
                                '   • Borrow: 25 KAIA (50% LTV)',
                                '   • Stake borrowed KAIA for yield',
                                '   • Risk: Moderate (HF: 1.5)',
                                '   • Expected return: ~8-12% APY',
                                '',
                                'Choose your strategy (1 or 2):'
                            ];
                            
                            setTerminalState(prev => ({ ...prev, messages: [...prev.messages, ...response] }));
                            break;
                            
                        case 'execution_result':
                            // Execution already handled in ai_response
                            break;
                            
                        case 'demo_complete':
                            setTerminalState(prev => ({ 
                                ...prev, 
                                messages: [...prev.messages, '', '✨ Demo Complete! Try the live terminal above to execute real strategies.']
                            }));
                            break;
                    }
                    
                    if (demoControllerRef.current.shouldStop) break;
                    
                    // Wait before next step
                    await sleep(step.delay);
                }
            } catch (error) {
                console.error('Demo execution error:', error);
            } finally {
                setIsPlaying(false);
                setIsPaused(false);
                
                // Auto-restart after 4 seconds if not stopped
                if (!demoControllerRef.current.shouldStop) {
                    await sleep(4000);
                    if (!demoControllerRef.current.shouldStop) {
                        startDemo();
                    }
                }
            }
        };

        startDemo();
    };
 
 
 

    // Render terminal content based on current state
    const renderTerminalContent = () => {
        const { screen, selectedItem, messages, userInput, processing } = terminalState;

        if (screen === 'main') {
            return (
                <div className="text-green-400">
                    <div className="text-center mb-4">TRADEARENA TERMINAL</div>
                    <div className="text-center mb-6 text-green-300">v1.0.0</div>
                    <div className="space-y-1">
                        {mainMenuItems.map((item, index) => (
                            <div key={index} className={index === selectedItem ? 'bg-green-400 text-black px-2' : ''}>
                                {index === selectedItem ? '●' : '  '} {item}
                            </div>
                        ))}
                    </div>
                    <div className="mt-4 text-green-300 text-xs">
                        Use ↑↓ arrows to navigate • Enter to select • Escape to go back • <span className="animate-pulse">_</span>
                    </div>
                </div>
            );
        }

        if (screen === 'interactive') {
            return (
                <div className="text-green-400">
                    <div className="text-center mb-2">INTERACTIVE MODE</div>
                    <div className="text-center mb-6 text-green-300">SELECT SESSION TYPE</div>
                    <div className="space-y-1">
                        {interactiveMenuItems.map((item, index) => (
                            <div key={index} className={index === selectedItem ? 'bg-green-400 text-black px-2' : ''}>
                                {index === selectedItem ? '●' : '  '} {item}
                            </div>
                        ))}
                    </div>
                    <div className="mt-4 text-green-300 text-xs">
                        Use ↑↓ arrows to navigate • Enter to select • Escape to go back • <span className="animate-pulse">_</span>
                    </div>
                </div>
            );
        }

        if (screen === 'chat') {
            return (
                <div className="text-green-400">
                    <div className="space-y-1">
                        {messages.map((message, index) => (
                            <div key={index} className={
                                message.includes('✅') || message.includes('⚡') ? 'text-green-400' :
                                message.includes('🤖') || message.includes('📊') || message.includes('🔍') ? 'text-blue-400' :
                                message.includes('📈') || message.includes('💰') || message.includes('🔄') ? 'text-yellow-400' :
                                message.includes('Agent:') || message.includes('Portfolio:') || message.includes('Network:') ? 'text-green-300' :
                                message.startsWith('>') ? 'text-green-400' :
                                'text-gray-300'
                            }>
                                {message}
                            </div>
                        ))}
                    </div>
                    {processing && (
                        <div className="flex items-center gap-2 mt-2">
                            <div className="text-green-400"> {userInput}</div>
                            <span className="animate-pulse">_</span>
                        </div>
                    )}
                </div>
            );
        }

        return (
            <div className="text-gray-500">
                <p>Welcome to TradeArena Terminal!</p>
                <p>Click "Run Demo" to see how our AI agents execute DeFi strategies.</p>
                <p className="mt-2">Features:</p>
                <ul className="ml-4 mt-1 space-y-1">
                    <li>• AI-powered DeFi strategy execution</li>
                    <li>• Real-time portfolio management</li>
                    <li>• Multi-chain support (KAIA, Cronos, Sui, Aptos)</li>
                    <li>• Leveraged yield farming strategies</li>
                    <li>• On-chain transaction verification</li>
                </ul>
            </div>
        );
    };

    return (
        <section className={`${embedded ? '' : 'py-20 px-6 bg-black/50'}`}>
            <div className={`${embedded ? '' : 'max-w-6xl mx-auto'}`}>
                {/* Section Header - Only show when not embedded */}
                {!embedded && (
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8 }}
                        className="text-center mb-16"
                    >
                        <motion.h2
                            className="text-3xl lg:text-4xl font-bold mb-6"
                            initial={{ opacity: 0 }}
                            whileInView={{ opacity: 1 }}
                            transition={{ delay: 0.2 }}
                        >
                            <span className="bg-gradient-to-r from-[#00ff88] via-[#00d4ff] to-[#ff00ff] bg-clip-text text-transparent">
                                Deploy Your AI Agent in Minutes
                            </span>
                        </motion.h2>
                        <motion.p
                            className="text-xl text-gray-400 max-w-3xl mx-auto"
                            initial={{ opacity: 0 }}
                            whileInView={{ opacity: 1 }}
                            transition={{ delay: 0.3 }}
                        >
                            Watch how different AI models perform when deployed with real capital in actual DeFi markets.
                        </motion.p>
                    </motion.div>
                )}

                {/* Terminal Interface */}
                <motion.div
                    initial={{ opacity: 0, y: 50 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, delay: 0.4 }}
                    className="max-w-4xl mx-auto"
                >
                    <div className="bg-black border border-gray-800 rounded-lg overflow-hidden shadow-2xl">
                        {/* Terminal Header */}
                        <div className="bg-gray-900 px-4 py-3 flex items-center justify-between border-b border-gray-800">
                            <div className="flex items-center gap-3">
                                <Terminal className="w-4 h-4 text-gray-400" />
                                <span className="text-gray-300 font-mono text-sm">TradeArena Terminal</span>
                            </div>
                            {isPlaying && (
                                <motion.div
                                    className="flex items-center gap-2"
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                >
                                    <motion.div
                                        className="w-2 h-2 rounded-full bg-[#00ff88]"
                                        animate={{ scale: [1, 1.5, 1] }}
                                        transition={{ duration: 1, repeat: Infinity }}
                                    />
                                    <span className="text-gray-400 text-xs">AI Demo</span>
                                </motion.div>
                            )}
                        </div>

                        {/* Terminal Content */}
                        <div
                            ref={terminalRef}
                            className="p-4 h-[28rem] overflow-y-auto font-mono text-sm"
                            style={{ backgroundColor: '#0a0a0f' }}
                            role="log"
                            aria-live="polite"
                            aria-label="Terminal output"
                        >
                            {renderTerminalContent()}

                            {/* Progress Indicator */}
                            {isPlaying && (
                                <motion.div
                                    className="flex items-center gap-2 mt-2"
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                >
                                    <motion.div
                                        className={`w-2 h-2 rounded-full ${isPaused ? 'bg-yellow-400' : 'bg-[#00ff88]'}`}
                                        animate={!isPaused ? { scale: [1, 1.5, 1] } : {}}
                                        transition={{ duration: 1, repeat: !isPaused ? Infinity : 0 }}
                                    />
                                    <span className="text-gray-400">
                                        {isPaused ? 'Paused' : 'Processing...'}
                                    </span>
                                </motion.div>
                            )}
                        </div>
                    </div>
                </motion.div>
            </div>
        </section>
    );
};

export default InteractiveTerminal;
