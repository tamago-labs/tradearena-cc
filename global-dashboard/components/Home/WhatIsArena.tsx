"use client"

import { motion } from 'framer-motion';

const WhatIsArena = () => {
    const features = [
        {
            title: "Data Categorization",
            description: "Automatically organizes raw trading data by strategy type - DEX trades, staking positions, yield farming, and more.",
            badge: "Smart Sorting",
            icon: "📊"
        },
        {
            title: "AI Model Rankings", 
            description: "Performance scores for every AI model based on real trading results, not backtests or simulations.",
            badge: "Live Rankings",
            icon: "🤖"
        },
        {
            title: "Strategy Intelligence",
            description: "Identifies which strategies work best in different market conditions and with specific AI models.", 
            badge: "Pattern Recognition",
            icon: "🧠"
        },
        {
            title: "Performance Leaders",
            description: "Discovers top-performing combinations of users, AI models, and strategies for maximum results.",
            badge: "Leaderboard", 
            icon: "🏆"
        }
    ];

    return (
        <section className="py-20 px-6 bg-black/30">
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
                            Turns Chaos into
                        </span>
                        <span className="text-green-400">
                            {' '}Clarity
                        </span>
                    </motion.h2>
                    <motion.p
                        className="text-xl text-gray-400 max-w-3xl mx-auto"
                        initial={{ opacity: 0 }}
                        whileInView={{ opacity: 1 }}
                        transition={{ delay: 0.3 }}
                    >
                        With TradeArena, you can see how decentralized trading data gets organized, ranked, and optimized for maximum clarity.
                    </motion.p>
                </motion.div>

                {/* Cards Grid */}
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, delay: 0.4 }}
                    className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl mx-auto"
                >
                    {features.map((feature, index) => (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.1 * index }}
                            whileHover={{ 
                                scale: 1.02,
                                borderColor: 'rgba(34, 197, 94, 0.5)'
                            }}
                            className="bg-gray-900/30 border border-gray-800 rounded-2xl p-8 transition-all duration-300 hover:border-green-500/50"
                        >
                            {/* Icon */}
                            <motion.div 
                                className="text-6xl mb-6"
                                initial={{ scale: 0 }}
                                whileInView={{ scale: 1 }}
                                transition={{ delay: 0.2 + index * 0.1 }}
                            >
                                {feature.icon}
                            </motion.div>

                            {/* Content */}
                            <div className="space-y-4">
                                {/* Title */}
                                <h3 className="text-2xl font-bold text-white">
                                    {feature.title}
                                </h3>
                                
                                {/* Description */}
                                <p className="text-gray-300 leading-relaxed">
                                    {feature.description}
                                </p>

                                {/* Badge */}
                                {/* <div className="inline-block px-4 py-2 bg-gradient-to-r from-green-600/20 to-emerald-600/20 text-green-400 font-semibold rounded-full border border-green-600/30">
                                    {feature.badge}
                                </div> */}
                            </div>
                        </motion.div>
                    ))}
                </motion.div>
            </div>
        </section>
    );
};

export default WhatIsArena;
