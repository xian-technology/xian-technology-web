def _slugify(value: str) -> str:
    return (
        value.lower()
        .replace(" ", "-")
        .replace("/", "-")
        .replace("_", "-")
        .replace("—", "-")
    )


SITE_URL = "https://xian.technology"
SOCIAL_PREVIEW_TITLE = "Python-Native Contracting on a CometBFT Backbone"
SOCIAL_PREVIEW_DESCRIPTION = (
    "Xian is a CometBFT-backed blockchain with a pure Python contracting engine. "
    "Write native Python contracts without transpilers."
)
SOCIAL_PREVIEW_IMAGE_PATH = "/social-preview.png"
SOCIAL_PREVIEW_IMAGE_URL = f"{SITE_URL}{SOCIAL_PREVIEW_IMAGE_PATH}"
HOME_SOCIAL_META = [
    {"property": "og:type", "content": "website"},
    {"property": "og:site_name", "content": "Xian Technology"},
    {"property": "og:url", "content": SITE_URL},
    {"property": "og:title", "content": SOCIAL_PREVIEW_TITLE},
    {"property": "og:description", "content": SOCIAL_PREVIEW_DESCRIPTION},
    {"property": "og:image:secure_url", "content": SOCIAL_PREVIEW_IMAGE_URL},
    {"property": "og:image:type", "content": "image/png"},
    {"property": "og:image:width", "content": "1200"},
    {"property": "og:image:height", "content": "630"},
    {"property": "og:image:alt", "content": SOCIAL_PREVIEW_TITLE},
    {"name": "twitter:card", "content": "summary_large_image"},
    {"name": "twitter:title", "content": SOCIAL_PREVIEW_TITLE},
    {"name": "twitter:description", "content": SOCIAL_PREVIEW_DESCRIPTION},
    {"name": "twitter:image", "content": SOCIAL_PREVIEW_IMAGE_URL},
    {"name": "twitter:image:alt", "content": SOCIAL_PREVIEW_TITLE},
    {"name": "twitter:site", "content": "@xian_technology"},
]


NAV_LINKS = [
    {"label": "Home", "href": "/"},
    {
        "label": "Technology",
        "href": "/consensus",
        "children": [
            {"label": "Consensus", "href": "/consensus", "description": "CometBFT backbone securing the network."},
            {"label": "Contracting", "href": "/contracting", "description": "Python-native smart contracts and patterns."},
            {"label": "Node & Network", "href": "/node-network", "description": "Running nodes and bootstrapping networks."},
            {"label": "ABCI", "href": "/abci", "description": "Python ABCI app bridging consensus and execution."},
            {"label": "Data Service & Tooling", "href": "/tooling", "description": "SDKs, integrations, and developer utilities."},
            {"label": "Roadmap", "href": "/roadmap", "description": "Milestones and upcoming work across the stack."},
        ],
    },
    {
        "label": "Developers",
        "href": "/developers",
        "children": [
            {"label": "Contracting Playground", "href": "https://playground.xian.technology", "description": "Interactive browser IDE for contracts.", "highlighted": True},
            {"label": "Documentation", "href": "https://docs.xian.technology", "description": "Specs, contracts, and BDS queries."},
            {"label": "Tutorials & First Steps", "href": "/tutorials", "description": "Guides to go from zero to deployed."},
            {"label": "Contracting Hub", "href": "https://hub.xian.technology", "description": "Curated, deploy-ready contracts with metadata.", "highlighted": True},
            {"label": "Samples/SDKs", "href": "/samples", "description": "Code samples and SDK usage for Xian tooling."},
            {"label": "API References", "href": "/api", "description": "Endpoints for BDS, transactions, and contracts."},
        ],
    },
    {
        "label": "About",
        "href": "/about",
        "children": [
            {"label": "About", "href": "/about", "description": "Mission, approach, and what we are building."},
            {"label": "FAQ", "href": "/faq", "description": "Common questions about Xian."},
            {"label": "Contact", "href": "/contact", "description": "Reach out for support, partnerships, or questions."},
        ],
    },
]

CORE_COMPONENTS = [
    {
        "title": "CometBFT Consensus Engine",
        "description": "Byzantine fault-tolerant, deterministic state machine replication securing every block.",
        "href": "/consensus",
        "icon": "satellite",
    },
    {
        "title": "Python ABCI for CometBFT",
        "description": "ABCI application in Python bridging consensus with the contracting runtime and state patches.",
        "href": "/abci",
        "icon": "link",
    },
    {
        "title": "Python Smart Contract Engine",
        "description": "Pure Python contracts with deterministic execution—no transpilers or alternate languages.",
        "href": "/contracting",
        "icon": "code",
    },
    {
        "title": "Tooling & Interfaces",
        "description": "xian-py SDK plus BDS GraphQL for querying chain data and building integrations.",
        "href": "/tooling",
        "icon": "wrench",
    },
]

NOTEWORTHY_QUOTES = [
    {
        "quote": (
            "Mastery of technology must infuse everything we do. Not just in our labs, but in the field, in our tradecraft, "
            "and even more importantly, in the mindset of every officer. We must be as comfortable with lines of code as we are "
            "with human sources, as fluent in Python as we are in multiple languages."
        ),
        "author": "Blaise Metreweli — Head of MI6",
        "source": "https://www.theguardian.com/uk-news/2025/dec/15/new-mi6-head-blaise-metreweli-speech-russia-threat",
    },
    {
        "quote": (
            "Python is now the most used language on GitHub as global open source activity continues to extend beyond traditional "
            "software development. We saw Python emerge for the first time as the most used language on GitHub. "
            "Python is used heavily across machine learning, data science, scientific computing, hobbyist, and home automation."
        ),
        "author": "GitHub Staff — Octoverse 2024",
        "source": "https://github.blog/news-insights/octoverse/octoverse-2024/",
    },
    {
        "quote": (
            "Python is approachable because it's designed for developers who are learning, tinkering, and exploring. Python's future remains bright "
            "because its values align with how developers actually learn and build: readability, approachability, stability, and a touch of irreverence."
        ),
        "author": "Guido van Rossum — Python Creator",
        "source": "https://github.blog/developer-skills/programming-languages-and-frameworks/why-developers-still-flock-to-python-guido-van-rossum-on-readability-ai-and-the-future-of-programming",
    },
]

BDS_COMPONENTS = [
    {
        "title": "Opt-in at install",
        "description": "Enable BDS when provisioning the node. It runs inside the ABCI app—no extra daemon to manage.",
        "icon": "plug",
    },
    {
        "title": "Complete transaction history",
        "description": "Capture every transaction—successes and failures—with status, stamps, contract/function, and block metadata for auditing.",
        "icon": "history",
    },
    {
        "title": "PostgreSQL + GraphQL",
        "description": "Data lands in PostgreSQL and is served through PostGraphile, so you can query with GraphQL or tap Postgres directly.",
        "icon": "database",
    },
]

TECHNOLOGY_TRACKS = [
    {
        "title": "Pure Python Contracts",
        "icon": "code",
        "description": (
            "Advance libraries that let developers express complex financial and governance "
            "logic in idiomatic Python, with deterministic execution and precise tooling."
        ),
        "points": [
            "Comprehensive standard library with battle-tested primitives",
            "Robust audit harnesses and differential testing utilities",
            "Accelerated developer onboarding with curated blueprints",
        ],
        "code_sample": (
            "# Deploy a contract\n"
            "@export\n"
            "def transfer(to: str, amount: int):\n"
            "    assert amount > 0\n"
            "    balances[to] += amount"
        ),
    },
    {
        "title": "High-Assurance Node",
        "icon": "zap",
        "description": (
            "Refine the Xian node with next generation instrumentation, blazing sync times, "
            "and transparent performance dashboards for operators."
        ),
        "points": [
            "Deterministic Python runtime tuned for blockchain workloads",
            "Observability-first metrics, structured logs, and tracing adapters",
            "Optimized networking stack ready for institutional deployments",
        ],
        "code_sample": (
            "# Node configuration\n"
            "xian_node = Node(\n"
            "    network='mainnet',\n"
            "    sync_mode='fast',\n"
            "    metrics=True\n"
            ")"
        ),
    },
    {
        "title": "Secure Upgrades",
        "icon": "shield",
        "description": (
            "Provide governance tooling that keeps production contracts evolving without "
            "downtime, leveraging migration kits and formal verification hooks."
        ),
        "points": [
            "Versioned contract archetypes with automated changelog diffing",
            "On-chain governance frameworks aligned with community mandates",
            "Gradual rollout pipelines with rigorous rollback strategies",
        ],
        "code_sample": (
            "# Upgrade contract\n"
            "upgrade_contract(\n"
            "    name='token',\n"
            "    version='2.0.0',\n"
            "    migration=migrate_v2\n"
            ")"
        ),
    },
]

ECOSYSTEM_INITIATIVES = [
    {
        "title": "Research Guild",
        "icon": "microscope",
        "description": (
            "Collaborative working group dedicated to provable correctness, type-safe "
            "smart contract patterns, and cryptographic resilience."
        ),
        "links": ["Research papers", "Technical specifications", "Formal verification"],
    },
    {
        "title": "Builder Studio",
        "icon": "construction",
        "description": (
            "Hands-on support for teams shipping production dApps on Xian Network, "
            "from architecture reviews to on-call debugging."
        ),
        "links": ["Architecture review", "Code audits", "Performance optimization"],
    },
    {
        "title": "Education Program",
        "icon": "book_open",
        "description": (
            "Curriculum, workshops, and tooling walkthroughs that help Python engineers "
            "become confident blockchain developers in weeks, not months."
        ),
        "links": ["Getting started guide", "Video tutorials", "Live workshops"],
    },
]

COMMUNITY_STREAMS = [
    {
        "title": "Contract Uplift Missions",
        "description": (
            "Audit, refactor, and extend flagship contracts already live on Xian Network "
            "to keep pace with new standards and evolving market requirements."
        ),
    },
    {
        "title": "Open Grants",
        "description": (
            "Targeted funding rounds for ecosystem teams building ADA-compliant wallets, "
            "analytics dashboards, or protocol integrations."
        ),
    },
    {
        "title": "Validator Collective",
        "description": (
            "Operator consortium focused on resilience, upgrade rehearsal, and coordinated "
            "responses across mainnet and testnet environments."
        ),
    },
]

__all__ = [
    "HOME_SOCIAL_META",
    "CORE_COMPONENTS",
    "BDS_COMPONENTS",
    "COMMUNITY_STREAMS",
    "ECOSYSTEM_INITIATIVES",
    "NAV_LINKS",
    "NOTEWORTHY_QUOTES",
    "SITE_URL",
    "SOCIAL_PREVIEW_DESCRIPTION",
    "SOCIAL_PREVIEW_IMAGE_PATH",
    "SOCIAL_PREVIEW_IMAGE_URL",
    "SOCIAL_PREVIEW_TITLE",
    "TECHNOLOGY_TRACKS",
]
