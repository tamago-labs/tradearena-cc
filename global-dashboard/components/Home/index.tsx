"use client"


import AgentCapabilities from "./AgentCapabilities"
import CriticalQuestion from "./CriticalQuestion"
import Hero from "./Hero"
import HowItWorks from "./HowItWorks"
import CustomViews from "./CustomViews"
import WhyDecentralizedStorage from "./WhyDecentralizedStorage"
import StrandsFramework from "./StrandsFramework"
import WhatIsArena from "./WhatIsArena"
import FinalQA from "./FinalQA"

const HomeContainer = () => {
    return (
        <div className="min-h-screen bg-[#0a0a0f] text-white">
            <Hero />
            <CriticalQuestion />
            <HowItWorks />
            <CustomViews />
            <StrandsFramework />
            <AgentCapabilities /> 
            <WhyDecentralizedStorage />
            <WhatIsArena />
            <FinalQA />
        </div>
    )
}

export default HomeContainer
