"use client"

import { motion, AnimatePresence } from 'framer-motion';
import { X, ExternalLink } from 'lucide-react';

interface DemoModalProps {
    isOpen: boolean;
    onClose: () => void;
}

const DemoModal: React.FC<DemoModalProps> = ({ isOpen, onClose }) => {
    const handleContinueToDemo = () => {
        window.open('https://demo.tradearena.cc', '_blank', 'noopener,noreferrer');
        onClose();
    };

    return (
        <AnimatePresence>
            {isOpen && (
                <>
                    {/* Backdrop */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        transition={{ duration: 0.3 }}
                        className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50"
                        onClick={onClose}
                    />
                    
                    {/* Modal */}
                    <motion.div
                        initial={{ opacity: 0, scale: 0.95, y: 20 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.95, y: 20 }}
                        transition={{ duration: 0.3 }}
                        className="fixed inset-0 z-50 flex items-center justify-center p-6"
                        onClick={(e) => e.stopPropagation()}
                    >
                        <div className="bg-gray-900 border border-gray-800 rounded-2xl max-w-lg w-full p-8 relative">
                            {/* Close Button */}
                            <button
                                onClick={onClose}
                                className="absolute top-4 right-4 text-gray-400 hover:text-white transition-colors"
                            >
                                <X className="w-5 h-5" />
                            </button>

                            {/* Content */}
                            <div className="space-y-6">
                                {/* Header */}
                                <div>
                                    <h3 className="text-2xl font-bold text-white mb-2">
                                        Demo Environment Notice
                                    </h3>
                                </div>

                                {/* Message */}
                                <div className="space-y-4 text-gray-300">
                                    <p>
                                        Welcome to our live demonstration terminal showcasing TradeArena's AI trading capabilities. This operates on mainnet with a small amount of real money provided by us for testing purposes only.
                                    </p>
                                    <p>
                                        Please use this terminal responsibly to explore our platform's features and functionality.
                                    </p>
                                </div>

                                {/* Buttons */}
                                <div className="flex gap-3 pt-4">
                                    <button
                                        onClick={handleContinueToDemo}
                                        className="flex-1 px-6 py-3 bg-gradient-to-r from-[#00ff88] to-[#00d4ff] text-black font-bold rounded-lg hover:shadow-lg hover:shadow-[#00ff88]/50 transition-all flex items-center justify-center group"
                                    >
                                        Continue to Demo Terminal
                                        <ExternalLink className="w-4 h-4 ml-2 group-hover:translate-x-0.5 transition-transform" />
                                    </button>
                                    <button
                                        onClick={onClose}
                                        className="px-6 py-3 bg-black/60 border border-gray-700 text-white font-semibold rounded-lg hover:border-gray-600 transition-all"
                                    >
                                        Close
                                    </button>
                                </div>
                            </div>
                        </div>
                    </motion.div>
                </>
            )}
        </AnimatePresence>
    );
};

export default DemoModal;
