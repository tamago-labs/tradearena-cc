import React from 'react';
import Link from 'next/link';

export default function Footer() {
    return (
        <footer className="border-t border-gray-800  ">
            <div className="max-w-7xl mx-auto px-6 py-6">
                <div className="flex items-center justify-between">
                    {/* Logo and Brand */}
                    <p className="text-center text-sm text-gray-400">
                        © 2026 Tamago Labs. All rights reserved.
                    </p>
                    {/* Links and Info */}
                    <div className="flex items-center space-x-6">
                        <Link 
                            href="https://github.com/tamago-labs/tradearena-cc"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-sm text-gray-400 hover:text-white transition-colors"
                        >
                            GitHub
                        </Link>
                        <Link 
                            href="https://docs.tamagolabs.com"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-sm text-gray-400 hover:text-white transition-colors"
                        >
                            Docs
                        </Link>
                    </div>
                </div> 
            </div>
        </footer>
    );
}
