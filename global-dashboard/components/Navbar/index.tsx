"use client"

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Github, Menu, X } from 'lucide-react';
import { useState, useEffect } from 'react';

const navItems = [
    { href: '/', label: 'Home' },
    { href: '/arena', label: 'Arena' },
    { href: '/benchmark', label: 'Benchmark' },
];

export default function Navbar() {
    const pathname = usePathname();
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    // Close menu when clicking outside
    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            const target = event.target as Element;
            if (isMenuOpen && !target.closest('.nav-menu') && !target.closest('.menu-button')) {
                setIsMenuOpen(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, [isMenuOpen]);

    // Close menu when route changes
    useEffect(() => {
        setIsMenuOpen(false);
    }, [pathname]);

    return (
        <>
            <nav className="border-b border-gray-800 relative z-50">
                <div className="max-w-7xl mx-auto px-6 py-4">
                    <div className="flex items-center justify-between">
                        <Link href="/" className="flex items-center space-x-3">
                            <div className="px-6 py-3 rounded-lg">
                                <span className="font-mono font-bold text-xl bg-gradient-to-r from-[#00ff88] to-[#00d4ff] bg-clip-text text-transparent tracking-wider">TradeArena</span>
                            </div>
                        </Link>

                        {/* Desktop Navigation */}
                        <div className="hidden md:flex items-center space-x-8">
                            {navItems.map((item) => (
                                <Link
                                    key={item.href}
                                    href={item.href}
                                    className={`text-sm font-medium transition-colors ${
                                        pathname === item.href
                                            ? 'text-[#00ff88]'
                                            : 'text-gray-300 hover:text-white'
                                    }`}
                                >
                                    {item.label}
                                </Link>
                            ))}

                            <a
                                href="https://github.com/tamago-labs/tradearena-cc"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="flex items-center gap-2 text-sm font-medium text-gray-300 hover:text-white transition-colors"
                            >
                                Docs
                            </a>
                        </div>

                        {/* Mobile Menu Button */}
                        <button
                            className="menu-button md:hidden flex items-center justify-center w-10 h-10 rounded-lg hover:bg-gray-800 transition-colors"
                            onClick={() => setIsMenuOpen(!isMenuOpen)}
                            aria-label="Toggle menu"
                        >
                            {isMenuOpen ? (
                                <X className="w-5 h-5 text-gray-300" />
                            ) : (
                                <Menu className="w-5 h-5 text-gray-300" />
                            )}
                        </button>
                    </div>
                </div>
            </nav>

            {/* Mobile Menu Overlay */}
            {isMenuOpen && (
                <>
                    {/* Backdrop */}
                    <div 
                        className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 md:hidden"
                        onClick={() => setIsMenuOpen(false)}
                    />

                    {/* Mobile Menu Panel */}
                    <div className="nav-menu fixed top-0 right-0 w-64 h-full bg-gray-900 border-l border-gray-800 z-50 md:hidden">
                        <div className="p-6">
                            {/* Mobile Header */}
                            <div className="flex items-center justify-between mb-8">
                                <Link 
                                    href="/" 
                                    className="flex items-center space-x-3"
                                    onClick={() => setIsMenuOpen(false)}
                                >
                                    <span className="font-mono font-bold text-xl bg-gradient-to-r from-[#00ff88] to-[#00d4ff] bg-clip-text text-transparent tracking-wider">TradeArena</span>
                                </Link>
                                <button
                                    className="flex items-center justify-center w-8 h-8 rounded-lg hover:bg-gray-800 transition-colors"
                                    onClick={() => setIsMenuOpen(false)}
                                    aria-label="Close menu"
                                >
                                    <X className="w-4 h-4 text-gray-300" />
                                </button>
                            </div>

                            {/* Mobile Navigation Items */}
                            <div className="space-y-2">
                                {navItems.map((item) => (
                                    <Link
                                        key={item.href}
                                        href={item.href}
                                        className={`block px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
                                            pathname === item.href
                                                ? 'bg-gray-800 text-[#00ff88]'
                                                : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                                        }`}
                                        onClick={() => setIsMenuOpen(false)}
                                    >
                                        {item.label}
                                    </Link>
                                ))}

                                <a
                                    href="https://github.com/tamago-labs/tradearena-cc"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="block px-4 py-3 rounded-lg text-sm font-medium text-gray-300 hover:bg-gray-800 hover:text-white transition-colors"
                                    onClick={() => setIsMenuOpen(false)}
                                >
                                    Docs
                                </a>
                            </div>
                        </div>
                    </div>
                </>
            )}
        </>
    );
}
