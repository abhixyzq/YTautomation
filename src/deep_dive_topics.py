"""
Deep Dive Epic Topics & Engineering Paradoxes Engine
Curates high-IQ, mind-bending technology mysteries, mathematical paradoxes,
and engineering marvels in the style of Veritasium, Lemmino, and Think School.
"""

import random
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

CURATED_MYSTERIES: List[Dict[str, Any]] = [
    {
        "id": "quantum_encryption_apocalypse",
        "category": "Quantum & Cryptography",
        "title": "What Happens When Quantum Computers Break All Bank Encryption?",
        "core_paradox": "Every modern secret on Earth—banking, nuclear codes, and passwords—relies on prime factorization being hard. Shor's Algorithm mathematically proves it's trivial on quantum hardware.",
        "inciting_incident": "The race to post-quantum cryptography (Kyber) and Harvest Now, Decrypt Later espionage campaigns.",
        "real_world_analogy": "Locking your front door with a combination lock that has 10 billion dials, but the intruder has a key that turns every dial simultaneously.",
        "catastrophe_case_study": "The sudden collapse of RSA-2048 and the chaos of legacy satellite and medical hardware that can never be patched.",
        "paradigm_shift": "Mathematics is no longer a permanent shield—physics determines what is secret, and what is exposed."
    },
    {
        "id": "agi_mathematical_impossibility",
        "category": "AI Limits & Mathematics",
        "title": "Why AGI is Mathematically Impossible (The Limits of Computation)",
        "core_paradox": "Alan Turing and Kurt Gödel proved that infinite truths exist that can never be computed by any algorithm, no matter how many GPUs you add.",
        "inciting_incident": "The trillion-dollar hallucination: Tech giants promise reasoning machines, but LLMs are mathematically bounded probabilistic token interpolators.",
        "real_world_analogy": "Giving a parrot a library of a billion books—it sounds like a philosopher, but if the room catches fire, it repeats Shakespeare.",
        "catastrophe_case_study": "Model Collapse: When AI starts training on AI-generated data, mathematical entropy forces the model to degenerate into gibberish in 5 generations.",
        "paradigm_shift": "Intelligence is not next-token prediction. We haven't built the foundation of thought; we've built the world's most sophisticated mirror."
    },
    {
        "id": "asml_extreme_ultraviolet_miracle",
        "category": "Silicon & Nanoscale Physics",
        "title": "The $200M Machine That Shoots Molten Tin at 200,000 MPH",
        "core_paradox": "To print microchips at 2 nanometers, visible light is too fat. Humanity had to harvest Extreme Ultraviolet radiation that gets absorbed by ordinary air.",
        "inciting_incident": "Only ONE company on Earth (ASML in Veldhoven, Netherlands) knows how to build EUV lithography machines. Without them, human computing freezes.",
        "real_world_analogy": "Shooting a bullet out of a sniper rifle, hitting a falling coin from 10 miles away, and doing it 50,000 times per second in a vacuum.",
        "catastrophe_case_study": "The geopolitical choke point: A single earthquake or military embargo on ASML halts the entire global smartphone and data center supply chain.",
        "paradigm_shift": "We have reached the atomic edge. Beyond 2 nanometers, quantum tunneling means electrons teleport through silicon walls like ghosts."
    },
    {
        "id": "ariane5_integer_overflow_catastrophe",
        "category": "Engineering Catastrophes & Glitches",
        "title": "How a 64-bit Number Destroyed a $500 Million Rocket in 37 Seconds",
        "core_paradox": "Ariane 5 was the most advanced rocket of its era, engineered by thousands of rocket scientists, yet it self-destructed because of a 10-line software reuse shortcut.",
        "inciting_incident": "June 4, 1996: Flight 501 launches from French Guiana. 36.7 seconds later, it veers 90 degrees and explodes in the sky.",
        "real_world_analogy": "Pouring a gallon of water into a pint glass—the software tried to stuff a 64-bit floating point number into a 16-bit integer slot with no overflow protection.",
        "catastrophe_case_study": "The Inertial Reference System crashed, causing the rocket guidance computers to interpret debug error codes as physical angle changes.",
        "paradigm_shift": "Complexity is the enemy of reliability. When software controls physics, there is zero tolerance for architectural assumptions."
    },
    {
        "id": "undersea_internet_chokepoint",
        "category": "Invisible Digital Infrastructure",
        "title": "The 500 Glass Threads Holding Up the Entire Global Economy",
        "core_paradox": "Everyone thinks the 'Cloud' is in the sky via satellites. In reality, 99% of all international internet traffic travels through fragile glass tubes lying on the ocean floor.",
        "inciting_incident": "Shark bites, anchor drops, and underwater landslides that cut off entire nations like Tonga, Vietnam, and West Africa in minutes.",
        "real_world_analogy": "Connecting two global financial centers with a garden hose of light laid across mountain ranges 20,000 feet underwater.",
        "catastrophe_case_study": "The Red Sea cable severing: How 4 cables cut by a dragging ship anchor knocked out 25% of all Asia-to-Europe data bandwidth overnight.",
        "paradigm_shift": "The internet is not abstract software. It is a fragile physical wire vulnerable to deep-sea predators and geopolitics."
    },
    {
        "id": "crowdstrike_kernel_crash_autopsy",
        "category": "Operating Systems & Digital Warfare",
        "title": "The Null Pointer That Brought Down 8.5 Million Windows Machines",
        "core_paradox": "Modern operating systems are built with ring-zero hyper-protected security architectures, yet a single bad configuration file paralyzed world aviation, hospitals, and banks.",
        "inciting_incident": "July 19, 2024: 8.5 million enterprise Windows machines reboot into an endless Blue Screen of Death loop (PAGE_FAULT_IN_NONPAGED_AREA).",
        "real_world_analogy": "Inviting a security guard with an automatic weapon directly into the operating room, and the guard slips on a banana peel.",
        "catastrophe_case_study": "Channel 291 file: Memory address 0x9c read out of bounds because kernel-level drivers bypass user-space crash containment.",
        "paradigm_shift": "Monoculture in software infrastructure creates global systemic fragility. When everyone runs the same antivirus, a single bug is a global outage."
    },
    {
        "id": "stuxnet_physics_of_cyberwar",
        "category": "Cybersecurity & Geopolitics",
        "title": "The World's First Digital Weapon That Destroyed Physical Steel",
        "core_paradox": "Code is supposed to be mathematical logic inside memory chips. Stuxnet crossed the boundary between bits and atoms to physically rip uranium centrifuges apart.",
        "inciting_incident": "Natanz nuclear facility in Iran: Centrifuges spinning at 1,000 Hertz mysteriously shatter into pieces while diagnostic screens show normal operations.",
        "real_world_analogy": "Rewiring a car's speedometer so it says you're going 40 MPH while secretly flooring the accelerator to 180 MPH until the engine melts.",
        "catastrophe_case_study": "Zero-day weaponization: Stuxnet used 4 separate Windows zero-day exploits, PLC programmable logic overrides, and frequency manipulation.",
        "paradigm_shift": "Cyber warfare is kinetic warfare. Anything controlled by software can be weaponized as a bomb."
    },
    {
        "id": "boeing_737_mcas_software_flaw",
        "category": "Aerospace & Systems Safety",
        "title": "Boeing 737 MAX: The Software Loop That Overrode The Pilots",
        "core_paradox": "A commercial airliner with dual human pilots and redundant mechanical controls was repeatedly pitched into catastrophic nose-dives by an invisible background software routine relying on a single angle-of-attack sensor.",
        "inciting_incident": "Lion Air 610 and Ethiopian 302: Pilots desperately fought the trim wheel against automated software commands they were never trained existed.",
        "real_world_analogy": "Installing a powerful autopilot that grabs the steering wheel and pushes your car into the ditch every 10 seconds because a single windshield sensor has dust on it.",
        "catastrophe_case_study": "MCAS (Maneuvering Characteristics Augmentation System) lacked sensor cross-check logic, creating a fatal single-point-of-failure in life-critical flight control.",
        "paradigm_shift": "Automation without human observability is lethal. When software hides physical control from operators, failure is inevitable."
    },
    {
        "id": "voyager_1_15_billion_miles_patch",
        "category": "Interstellar Engineering & Computing",
        "title": "NASA's Impossible Hack: Fixing Code 15 Billion Miles Away",
        "core_paradox": "Voyager 1 was launched in 1977 with 68 kilobytes of memory on an 8-track tape drive. In 2024, NASA engineers debugged and patched corrupted memory registers across a 45-hour radio round-trip in interstellar space.",
        "inciting_incident": "November 2023: Voyager 1's telemetry system begins transmitting an unbroken loop of repeating binary zeroes instead of interstellar scientific data.",
        "real_world_analogy": "Performing open-heart surgery with chopsticks on a patient who is on Mars, where every movement of your hand takes two full days to execute.",
        "catastrophe_case_study": "Flight Data System (FDS) memory chip failure: 3% of memory corrupted, requiring NASA to split the corrupted routine into fragments and relocate them across disparate free memory blocks.",
        "paradigm_shift": "Simplicity and documentation endure. 50-year-old assembly code with handwritten memos outlasted modern disposable software architectures."
    },
    {
        "id": "y2k_bug_myth_vs_reality",
        "category": "Software History & Infrastructure",
        "title": "The Y2K Bug: How a $500 Billion Fix Saved the Modern World",
        "core_paradox": "People remember Y2K as an overhyped media hoax because 'nothing happened'. In reality, nothing happened because humanity executed the largest coordinated software remediation in history.",
        "inciting_incident": "Early programmers stored years as two digits ('99' instead of '1999') to save precious punch-card bytes, creating a global clock overflow at midnight 2000.",
        "real_world_analogy": "An odometer that rolls from 99 to 00, causing life support, oil refineries, and nuclear reactors to believe it is 1900 and shut down.",
        "catastrophe_case_study": "COBOL retrofitting: Hundreds of thousands of retired mainframe engineers mobilized to inspect billions of lines of financial and military code before midnight.",
        "paradigm_shift": "The greatest engineering successes are invisible. When engineers do their job flawlessly, the public assumes there was never any danger."
    },
    {
        "id": "bitcoin_genesis_block_mystery",
        "category": "Cryptographic Protocols & Game Theory",
        "title": "The Cryptographic Enigma of Satoshi Nakamoto's Genesis Block",
        "core_paradox": "Block 0 of the Bitcoin blockchain contains 50 unspendable coins and a permanent newspaper headline about bank bailouts. Its creator vanished, leaving behind an unstoppable economic protocol.",
        "inciting_incident": "January 3, 2009: Hash 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f is mined into existence.",
        "real_world_analogy": "Carving a mathematical clock into stone that ticks every 10 minutes, owned by nobody, powered by proof-of-work thermodynamic physics.",
        "catastrophe_case_study": "The Byzantine Generals Problem solved without central authority using cryptographic SHA-256 difficulty adjustments.",
        "paradigm_shift": "Money is an information protocol. Scarcity can be enforced through pure computational energy."
    },
    {
        "id": "morris_worm_1988_internet_crash",
        "category": "Cybersecurity & Internet Archeology",
        "title": "The 99-Line Program That Took Down the Entire Internet in 1988",
        "core_paradox": "A 23-year-old Cornell student wanted to measure the size of the internet. A single arithmetic replication bug caused his worm to infect and freeze 10% of all connected computers on Earth.",
        "inciting_incident": "November 2, 1988: Systems at MIT, NASA, and DARPA slow to a crawl as hundreds of copies of the same program overwhelm Unix processes.",
        "real_world_analogy": "Sending a census survey letter with instructions to photocopy itself 10 times and mail it to every neighbor—until post offices choke to death.",
        "catastrophe_case_study": "Buffer overflow in fingerd and sendmail debug trap: The first conviction under the Computer Fraud and Abuse Act.",
        "paradigm_shift": "The internet was built on implicit trust among academics. The Morris Worm proved that digital infrastructure requires zero-trust architecture."
    },
    {
        "id": "therac_25_deadliest_race_condition",
        "category": "Medical Engineering & Systems Safety",
        "title": "The Deadliest Race Condition: When Code Turned Radiation Lethal",
        "core_paradox": "A state-of-the-art cancer radiation therapy machine removed physical hardware interlocks in favor of software safety checks. A typing-speed race condition administered lethal 25,000-rad radiation doses.",
        "inciting_incident": "1985-1987: Patients at clinics in Texas and Washington reported feeling intense electrical shocks, while machine operators saw cryptic 'Malfunction 54' error codes.",
        "real_world_analogy": "A physical gate switch replaced with a software flag, but if the operator types too fast, the flag updates half a millisecond before the tungsten shield moves into place.",
        "catastrophe_case_study": "One-byte counter overflow in shared memory between the keyboard entry routine and beam alignment task.",
        "paradigm_shift": "Software must never replace physical fail-safes. In life-critical systems, software safety is an illusion without hardware interlocks."
    },
    {
        "id": "flash_crash_2010_trillion_dollar_drop",
        "category": "Algorithmic Finance & Chaos Theory",
        "title": "The 2010 Flash Crash: How Bots Erased $1 Trillion in 36 Minutes",
        "core_paradox": "At 2:42 PM on May 6, 2010, the Dow Jones plunged 1,000 points in minutes. Shares of Procter & Gamble dropped to a single penny before rebounding—driven by automated high-frequency trading algorithms feeding each other bad data.",
        "inciting_incident": "A single $4.1 billion automated sell order dumped into the E-mini S&P futures market triggered an algorithmic liquidity vacuum across all electronic exchanges.",
        "real_world_analogy": "Two automated microphone speakers facing each other, generating a deafening feedback loop that blows out the amplifiers in seconds.",
        "catastrophe_case_study": "Hot-potato volume trading: Market-maker algorithms shut down simultaneously to avoid risk, causing liquidity to evaporate to zero.",
        "paradigm_shift": "Markets are no longer human auctions. They are decentralized algorithmic networks susceptible to instantaneous cascading collapse."
    },
    {
        "id": "deepseek_v3_moe_architecture_breakthrough",
        "category": "AI Architecture & Silicon Economics",
        "title": "How DeepSeek Broke the Trillion-Dollar AI Hardware Monopoly",
        "core_paradox": "Silicon Valley spent $100 billion buying tens of thousands of Nvidia H100 GPUs to train frontier LLMs. A small Chinese lab trained an open model of equivalent capability for under $6 million using Multi-Head Latent Attention.",
        "inciting_incident": "January 2025: DeepSeek-V3 and R1 launch open-source weights, causing a historic single-day $600 billion wipeout in US semiconductor market cap.",
        "real_world_analogy": "While everyone was buying bigger fuel tanks for a rocket, someone invented a hybrid engine that uses 95% less fuel by firing only 8 of its 256 thrusters per millisecond.",
        "catastrophe_case_study": "FP8 mixed precision, dual-pipe overlapping communication, and Multi-token Prediction circumventing memory bandwidth bottlenecks.",
        "paradigm_shift": "Brute-force compute scaling has diminishing returns. Algorithmic architectural efficiency will always triumph over raw capital expenditure."
    }
]


def get_deep_dive_topic(previously_published: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Selects a fresh, high-stakes mind-bending tech mystery.
    Ensures previously published titles are avoided.
    """
    published_titles = [p.lower() for p in (previously_published or [])]
    available = [
        m for m in CURATED_MYSTERIES
        if not any(m["title"].lower() in p or p in m["title"].lower() for p in published_titles)
    ]
    if not available:
        logger.info("All curated topics published at least once. Cycling through full mystery pool.")
        available = CURATED_MYSTERIES

    chosen = random.choice(available)
    logger.info(f"Selected High-IQ Mystery: [{chosen['category']}] {chosen['title']}")
    return chosen


def enrich_custom_topic_for_deep_dive(topic_prompt: str) -> Dict[str, Any]:
    """
    Transforms any raw user topic into a high-stakes Mind-Bending Explainer premise.
    """
    return {
        "id": "custom_inquiry",
        "category": "High-IQ Technical Inquiry",
        "title": topic_prompt if topic_prompt.endswith("?") else f"{topic_prompt}: The Untold Engineering Mystery",
        "core_paradox": f"The hidden technical truth and counter-intuitive mechanics behind {topic_prompt}.",
        "inciting_incident": f"Why the conventional understanding of {topic_prompt} is fundamentally flawed.",
        "real_world_analogy": f"A vivid physical metaphor breaking down the invisible mechanics of {topic_prompt}.",
        "catastrophe_case_study": f"The decisive turning point or failure that revealed the true nature of {topic_prompt}.",
        "paradigm_shift": f"What {topic_prompt} reveals about the future of human engineering and intelligence."
    }
