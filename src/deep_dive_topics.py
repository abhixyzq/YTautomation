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
