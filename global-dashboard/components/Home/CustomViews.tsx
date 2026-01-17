"use client"

import { motion } from 'framer-motion';
import { useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

const CustomViews = () => {
    const [activeTab, setActiveTab] = useState(0);

    const dashboardTypes = [
        {
            title: "Portfolio Overview",
            description: "Multi-chain wallet balances and asset allocation charts with real-time tracking across all your trading accounts.",
            badge: "Balance Tracking",
            icon: "💼"
        },
        {
            title: "Strategy Performance",
            description: "Win rates, P&L charts, and detailed strategy comparisons with AI-powered performance insights.",
            badge: "Performance Metrics",
            icon: "📈"
        },
        {
            title: "Market Intelligence",
            description: "Real-time market data feeds with AI-generated insights, trend analysis, and opportunity detection.",
            badge: "Market Analysis",
            icon: "🧠"
        },
        {
            title: "Risk Analysis",
            description: "Exposure metrics, volatility indicators, and stress testing to keep your trading strategy within risk limits.",
            badge: "Risk Management",
            icon: "🛡️"
        },
        {
            title: "Custom Analytics",
            description: "Any visualization you can describe - let your AI agent create personalized charts and analytics unique to your needs.",
            badge: "Unlimited Views",
            icon: "🎨"
        }
    ];


    return (
        <section
            className="py-20 px-6 bg-black/40"
        >
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
                            Agent-Built
                        </span>
                        <span className="text-green-400">
                            {' '}Views
                        </span>
                    </motion.h2>
                    <motion.p
                        className="text-xl text-gray-400 max-w-3xl mx-auto"
                        initial={{ opacity: 0 }}
                        whileInView={{ opacity: 1 }}
                        transition={{ delay: 0.3 }}
                    >
                        After configuration, your AI agent can generate custom dashboards to visualize trades, reasoning, and performance in real time.
                    </motion.p>
                </motion.div>

                {/* Main Content - Slider Layout */}
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, delay: 0.4 }}
                    className="max-w-4xl mx-auto"
                >
                    {/* Slider Container */}
                    <div className="relative">
                        {/* Navigation Buttons */}
                        <button
                            onClick={() => setActiveTab((prev) => (prev === 0 ? dashboardTypes.length - 1 : prev - 1))}
                            className="absolute left-2 top-1/2 -translate-y-1/2 z-50 bg-black/90 backdrop-blur-sm border border-gray-700 rounded-full p-4 hover:bg-gray-900 transition-all shadow-lg"
                            aria-label="Previous view"
                        >
                            <ChevronLeft className="w-5 h-5 text-gray-300" />
                        </button>
                        <button
                            onClick={() => setActiveTab((prev) => (prev + 1) % dashboardTypes.length)}
                            className="absolute right-2 top-1/2 -translate-y-1/2 z-50 bg-black/90 backdrop-blur-sm border border-gray-700 rounded-full p-4 hover:bg-gray-900 transition-all shadow-lg"
                            aria-label="Next view"
                        >
                            <ChevronRight className="w-5 h-5 text-gray-300" />
                        </button>

                        <motion.div
                            key={activeTab}
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.5 }}
                            className="bg-gray-900/30 border border-gray-800 rounded-2xl p-8"
                        >
                            {/* Screenshot */}
                            <div className="mb-6 rounded-xl overflow-hidden bg-gradient-to-br from-gray-800 to-gray-900" style={{ minHeight: '300px' }}>
                                <div className="relative w-full h-[300px]">
                                    <img
                                        src="/screenshot-1.png"
                                        alt={dashboardTypes[activeTab].title}
                                        className="absolute inset-0 w-full h-full object-cover"
                                        style={{ display: 'block' }}
                                    />
                                    {/* Dashboard Type Overlay */}
                                    <div className="absolute inset-0 bg-black/30 flex items-center justify-center">
                                        <div className="text-center text-white">
                                            <div className="text-5xl mb-3">{dashboardTypes[activeTab].icon}</div>
                                            <div className="font-semibold text-lg">{dashboardTypes[activeTab].title}</div>
                                            <div className="text-sm opacity-70 mt-1">{dashboardTypes[activeTab].badge}</div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Content */}
                            <div className="space-y-4">
                                <div className="flex items-center gap-3 mb-2">
                                    <span className="text-3xl">{dashboardTypes[activeTab].icon}</span>
                                    <h3 className="text-2xl font-bold text-white">
                                        {dashboardTypes[activeTab].title}
                                    </h3>
                                </div>

                                <p className="text-gray-300 leading-relaxed text-lg">
                                    {dashboardTypes[activeTab].description}
                                </p>

                                {/* Badge */}
                                <div className="inline-block px-4 py-2 bg-gradient-to-r from-green-600 to-emerald-600 text-white font-semibold rounded-full">
                                    {dashboardTypes[activeTab].badge}
                                </div>
                            </div>
                        </motion.div>
                    </div>

                    {/* Pagination Dots */}
                    <div className="flex justify-center gap-2 mt-6">
                        {dashboardTypes.map((_, index) => (
                            <button
                                key={index}
                                onClick={() => setActiveTab(index)}
                                className={`w-2 h-2 rounded-full transition-all duration-300 ${index === activeTab
                                    ? 'bg-green-400 w-8'
                                    : 'bg-gray-600 hover:bg-gray-500'
                                    }`}
                                aria-label={`Go to view ${index + 1}`}
                            />
                        ))}
                    </div>
                </motion.div>
            </div>
        </section>
    );
};

export default CustomViews;
