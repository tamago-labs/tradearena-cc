"use client"

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, ChevronUp, ArrowRight, ExternalLink } from 'lucide-react';
import Link from 'next/link';

const FinalQA = () => {
    const [activeQuestion, setActiveQuestion] = useState<number | null>(null);

    const faqs = [
        {
            question: "How do I get started with my first AI agent?",
            answer: "Download TradeArena terminal from our github. Install dependencies as per instruction then you can setup AI model and trading chain.",
            category: "getting-started"
        },
        {
            question: "Is my capital safe with AI agents trading?",
            answer: "Everything is run locally. You need to provide private key for local MCP server to sign transaction which acts like a buffer the AI never this sensitive info.",
            category: "security"
        },
        {
            question: "How does AI decision verification work?",
            answer: "Optionally, you can enable or disable on the settings menu but once enabled this will store AI decision into Walrus (Testnet for now) that later we will use this to construct performance ranking that benefits to all vibe traders.",
            category: "verification"
        },
        {
            question: "Which AI model performs best in DeFi trading?",
            answer: "You can check this on the Arena page and make possible by everyone sharing trading decision on each AI model to improve collective intelligence.",
            category: "performance"
        },

        {
            question: "Can I customize my AI agent's trading strategy?",
            answer: "You can keep chatting with AI before decide what you going to do and this conversation will keep locally and resume at anytime.",
            category: "customization"
        },
        {
            question: "What DeFi protocols are supported?",
            answer: "Support 20+ across 3 different blockchain. More will be added.",
            category: "protocols"
        }
    ];

    const toggleQuestion = (index: number) => {
        setActiveQuestion(activeQuestion === index ? null : index);
    };

    return (
        <section className="py-20 px-6 bg-gradient-to-b from-black/70 to-black">
            <div className="max-w-6xl mx-auto">
                {/* Section Header */}
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
                        <span className="bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
                            Frequently Asked
                        </span>
                        <span className="text-green-400">
                            {' '}Questions
                        </span>
                    </motion.h2>
                    <motion.p
                        className="text-xl text-gray-400 max-w-3xl mx-auto"
                        initial={{ opacity: 0 }}
                        whileInView={{ opacity: 1 }}
                        transition={{ delay: 0.3 }}
                    >
                        Everything you need to know about transparent AI trading on TradeArena.
                    </motion.p>
                </motion.div>

                {/* FAQ Accordion */}
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                    className="max-w-4xl mx-auto"
                >
                    {faqs.map((faq, index) => {
                        const isActive = activeQuestion === index;

                        return (
                            <motion.div
                                key={index}
                                className="bg-gray-900/30 border border-gray-800 rounded-lg mb-4 overflow-hidden"
                                initial={{ opacity: 0, y: 20 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.1 * index }}
                            >
                                <button
                                    onClick={() => toggleQuestion(index)}
                                    className="w-full px-6 py-4 flex items-center justify-between text-left hover:bg-gray-800/30 transition-colors"
                                >
                                    <span className="text-white font-semibold">{faq.question}</span>

                                    <motion.div
                                        animate={{ rotate: isActive ? 180 : 0 }}
                                        transition={{ duration: 0.3 }}
                                    >
                                        <ChevronDown className="w-5 h-5 text-gray-400" />
                                    </motion.div>
                                </button>

                                <AnimatePresence>
                                    {isActive && (
                                        <motion.div
                                            initial={{ height: 0, opacity: 0 }}
                                            animate={{ height: 'auto', opacity: 1 }}
                                            exit={{ height: 0, opacity: 0 }}
                                            transition={{ duration: 0.3 }}
                                            className="border-t border-gray-800"
                                        >
                                            <div className="p-6">
                                                <p className="text-gray-300 leading-relaxed">{faq.answer}</p>
                                            </div>
                                        </motion.div>
                                    )}
                                </AnimatePresence>
                            </motion.div>
                        );
                    })}
                </motion.div>

                {/* CTA Section */}
                {/* <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.8 }}
                    className="mt-20"
                >
                    <div className="bg-gradient-to-r from-green-500/10 to-blue-500/10 border border-green-500/20 rounded-2xl p-8 lg:p-12 text-center">
                        <motion.h3
                            className="text-2xl lg:text-3xl font-bold mb-4"
                            initial={{ opacity: 0 }}
                            whileInView={{ opacity: 1 }}
                            transition={{ delay: 0.9 }}
                        >
                            <span className="bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
                                Join Collective
                            </span>
                            <span className="text-green-400">
                                {' '}Intelligence
                            </span>
                        </motion.h3>
                        
                        <motion.p
                            className="text-lg text-gray-300 mb-8 max-w-2xl mx-auto"
                            initial={{ opacity: 0 }}
                            whileInView={{ opacity: 1 }}
                            transition={{ delay: 1.0 }}
                        >
                            Connect with traders, share strategies, and build better AI together. 
                            Be part of the transparent trading revolution.
                        </motion.p>

                        <motion.div
                            className="flex flex-col sm:flex-row gap-4 justify-center items-center"
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            transition={{ delay: 1.1 }}
                        >
                            <Link
                                href="https://discord.gg/tradearena"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="px-8 py-4 bg-gradient-to-r from-[#00ff88] to-[#00d4ff] text-black font-bold rounded-lg hover:shadow-lg hover:shadow-[#00ff88]/50 transition-all flex items-center justify-center group"
                            >
                                Join Community
                                <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
                            </Link>
                            
                            <Link
                                href="/docs"
                                className="px-8 py-4 bg-black/60 border border-gray-700 text-white font-semibold rounded-lg hover:border-gray-600 transition-all flex items-center justify-center group"
                            >
                                Learn More
                                <ExternalLink className="w-5 h-5 ml-2 group-hover:translate-y-[-2px] transition-transform" />
                            </Link>
                        </motion.div>
 

                        <motion.div
                            className="grid grid-cols-1 sm:grid-cols-3 gap-6 mt-12"
                            initial={{ opacity: 0 }}
                            whileInView={{ opacity: 1 }}
                            transition={{ delay: 1.2 }}
                        >
                            <div className="text-center">
                                <div className="text-2xl font-bold text-green-400 mb-1">5,000+</div>
                                <div className="text-sm text-gray-400">Active Traders</div>
                            </div>
                            <div className="text-center">
                                <div className="text-2xl font-bold text-green-400 mb-1">50K+</div>
                                <div className="text-sm text-gray-400">Trades Verified</div>
                            </div>
                            <div className="text-center">
                                <div className="text-2xl font-bold text-green-400 mb-1">$2M+</div>
                                <div className="text-sm text-gray-400">TVL Protected</div>
                            </div>
                        </motion.div>
                    </div>
                </motion.div> */}
            </div>
        </section>
    );
};

export default FinalQA;
