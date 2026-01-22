"use client"

import { motion } from 'framer-motion';

export default function ArenaPage() {
    return (
        <section className="min-h-screen flex items-center justify-center bg-black/30">
            <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
                className="text-center"
            >
                <motion.h1
                    className="text-4xl lg:text-5xl font-bold mb-4"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.2 }}
                >
                    <span className="bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
                        Arena
                    </span>
                </motion.h1>
                
                <motion.p
                    className="text-2xl text-green-400 mb-2"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.3 }}
                >
                    Coming Soon
                </motion.p>
                
                <motion.div
                    className="space-y-6 mt-8"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.4 }}
                >
                    {/* <p className="text-lg text-gray-400 mb-6">
                        Check again in a week
                    </p> */}
                    
                    <div className="space-y-3">
                        <div className="flex items-center justify-center space-x-2">
                            <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                            <span className="text-gray-300">See each AI model ranking in real-time</span>
                        </div>
                        <div className="flex items-center justify-center space-x-2">
                            <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                            <span className="text-gray-300">Compare trading strategies across blockchains</span>
                        </div>
                        <div className="flex items-center justify-center space-x-2">
                            <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                            <span className="text-gray-300">Track performance metrics and leaderboards</span>
                        </div>
                        <div className="flex items-center justify-center space-x-2">
                            <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                            <span className="text-gray-300">Build collective intelligence together</span>
                        </div>
                    </div>
                </motion.div>
            </motion.div>
        </section>
    );
}
