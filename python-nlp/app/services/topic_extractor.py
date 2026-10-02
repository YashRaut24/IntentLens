import re
from typing import Dict, List, Tuple

# Domain taxonomy of software engineering, CS fundamentals, tools & frameworks
TECH_TAXONOMY = {
    # Languages
    "python": "Python",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "java": "Java",
    "c++": "C++",
    "cpp": "C++",
    "c#": "C#",
    "csharp": "C#",
    "c": "C",
    "rust": "Rust",
    "golang": "Go",
    "go": "Go",
    "kotlin": "Kotlin",
    "swift": "Swift",
    "php": "PHP",
    "ruby": "Ruby",
    "sql": "SQL",
    "html": "HTML",
    "css": "CSS",
    "bash": "Bash",
    "r": "R",

    # Frameworks & Libraries
    "react": "React",
    "react.js": "React",
    "angular": "Angular",
    "vue": "Vue",
    "vue.js": "Vue",
    "next.js": "Next.js",
    "nextjs": "Next.js",
    "express": "Express",
    "express.js": "Express",
    "node": "Node.js",
    "node.js": "Node.js",
    "nodejs": "Node.js",
    "fastapi": "FastAPI",
    "django": "Django",
    "flask": "Flask",
    "spring": "Spring Boot",
    "spring boot": "Spring Boot",
    "pytorch": "PyTorch",
    "tensorflow": "TensorFlow",
    "keras": "Keras",
    "opencv": "OpenCV",
    "scikit-learn": "Scikit-Learn",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "tailwind": "Tailwind CSS",
    "tailwind css": "Tailwind CSS",
    "flutter": "Flutter",
    "react native": "React Native",

    # Databases & Caching
    "mongodb": "MongoDB",
    "postgresql": "PostgreSQL",
    "postgres": "PostgreSQL",
    "mysql": "MySQL",
    "redis": "Redis",
    "cassandra": "Cassandra",
    "sqlite": "SQLite",
    "dynamodb": "DynamoDB",
    "memcached": "Memcached",

    # DevOps, Cloud & Tools
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "k8s": "Kubernetes",
    "git": "Git",
    "github": "GitHub",
    "aws": "AWS",
    "azure": "Azure",
    "gcp": "Google Cloud",
    "linux": "Linux",
    "nginx": "Nginx",
    "terraform": "Terraform",
    "kafka": "Apache Kafka",
    "apache kafka": "Apache Kafka",
    "rabbitmq": "RabbitMQ",

    # CS Concepts & Algorithms
    "recursion": "Recursion",
    "loops": "Loops",
    "binary tree": "Binary Tree",
    "binary trees": "Binary Trees",
    "binary search tree": "Binary Search Tree",
    "binary search": "Binary Search",
    "linked list": "Linked List",
    "linked lists": "Linked Lists",
    "dynamic programming": "Dynamic Programming",
    "graphs": "Graph Algorithms",
    "graph traversal": "Graph Traversal",
    "bfs": "BFS",
    "dfs": "DFS",
    "dijkstra": "Dijkstra Algorithm",
    "heap": "Heap / Priority Queue",
    "trie": "Trie",
    "sorting": "Sorting Algorithms",
    "quicksort": "QuickSort",
    "mergesort": "MergeSort",
    "two pointer": "Two Pointer Technique",
    "sliding window": "Sliding Window",
    "normalization": "Database Normalization",
    "acid": "ACID Properties",
    "deadlocks": "Deadlocks",
    "virtual memory": "Virtual Memory",
    "paging": "Paging",
    "operating systems": "Operating Systems",
    "computer networks": "Computer Networks",
    "tcp": "TCP",
    "udp": "UDP",
    "osi model": "OSI Model",
    "rest": "REST API",
    "graphql": "GraphQL",
    "neural networks": "Neural Networks",
    "deep learning": "Deep Learning",
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "ai": "Artificial Intelligence",
    "dl": "Deep Learning",
    "transformers": "Transformers",
    "attention mechanism": "Attention Mechanism",
    "backpropagation": "Backpropagation",
    "microservices": "Microservices",
    "system design": "System Design",
    "mern": "MERN Stack",
    "mern stack": "MERN Stack",
}

_nlp = None

def get_spacy_nlp():
    global _nlp
    if _nlp is None:
        try:
            import spacy
            _nlp = spacy.load("en_core_web_sm")
        except Exception:
            try:
                import spacy
                _nlp = spacy.blank("en")
            except Exception:
                _nlp = False
    return _nlp

def extract_topics_and_skills(text: str) -> Dict[str, List[str]]:
    """
    Extracts core topics and related/secondary concepts using:
    - Prepositional/syntactic pattern parsing (e.g. 'learn X after Y', 'difference between X and Y')
    - Domain taxonomy identification
    - spaCy noun chunk & entity extraction
    """
    if not text:
        return {"topics": [], "related_concepts": []}

    lower_text = text.lower()
    topics: List[str] = []
    related_concepts: List[str] = []

    # 1. Structural Comparison: "difference between X and Y"
    comp_match = re.search(r"(?:difference between|compare|versus|vs\.?)\s+([A-Za-z0-9#\+\.\-]+)\s+(?:and|&|vs\.?|to)\s+([A-Za-z0-9#\+\.\-]+)", text, re.IGNORECASE)
    if comp_match:
        t1, t2 = comp_match.group(1).strip(), comp_match.group(2).strip()
        t1_norm = TECH_TAXONOMY.get(t1.lower(), t1.capitalize())
        t2_norm = TECH_TAXONOMY.get(t2.lower(), t2.capitalize())
        return {
            "topics": [t1_norm, t2_norm],
            "related_concepts": []
        }

    # 2. Sequential / Prerequisite: "learn X after Y" or "learn X from scratch but know Y"
    seq_match = re.search(r"learn\s+([A-Za-z0-9#\+\.\-]+)\s+(?:after|knowing|from|with)\s+([A-Za-z0-9#\+\.\-]+)", text, re.IGNORECASE)
    if seq_match:
        t_main, t_rel = seq_match.group(1).strip(), seq_match.group(2).strip()
        topics.append(TECH_TAXONOMY.get(t_main.lower(), t_main.capitalize()))
        related_concepts.append(TECH_TAXONOMY.get(t_rel.lower(), t_rel.capitalize()))

    # 3. Known vs Unknown: "understand X but ... Y"
    known_match = re.search(r"understand\s+([A-Za-z0-9#\+\.\-]+)\s+(?:but|however|yet).*?(?:don\'?t understand|confused about|struggle with)\s+([A-Za-z0-9#\+\.\-]+)", text, re.IGNORECASE)
    if known_match:
        known, unknown = known_match.group(1).strip(), known_match.group(2).strip()
        topics.append(TECH_TAXONOMY.get(unknown.lower(), unknown.capitalize()))
        related_concepts.append(TECH_TAXONOMY.get(known.lower(), known.capitalize()))

    # 4. Taxonomy matching (sort by length descending to match multi-word phrases first)
    sorted_tax = sorted(TECH_TAXONOMY.items(), key=lambda x: len(x[0]), reverse=True)
    found_tax_canonical = []
    for phrase, canonical in sorted_tax:
        pattern = r"\b" + re.escape(phrase) + r"\b"
        if re.search(pattern, lower_text):
            if canonical not in found_tax_canonical and canonical not in topics and canonical not in related_concepts:
                found_tax_canonical.append(canonical)

    if found_tax_canonical:
        if not topics:
            topics.append(found_tax_canonical[0])
            if len(found_tax_canonical) > 1:
                for rem in found_tax_canonical[1:]:
                    if rem not in related_concepts:
                        related_concepts.append(rem)
        else:
            for extra in found_tax_canonical:
                if extra not in topics and extra not in related_concepts:
                    related_concepts.append(extra)

    # 5. spaCy noun chunk & entity extraction fallback/augmentation
    nlp = get_spacy_nlp()
    if nlp and not isinstance(nlp, bool):
        try:
            doc = nlp(text)
            for ent in doc.ents:
                ent_clean = ent.text.strip()
                if len(ent_clean) > 2 and ent_clean.lower() not in ["can", "you", "what", "how", "give"]:
                    if ent_clean not in topics and ent_clean not in related_concepts:
                        if not topics:
                            topics.append(ent_clean)
                        elif ent_clean not in related_concepts:
                            related_concepts.append(ent_clean)
        except Exception:
            pass

    # Clean duplicates preserving order and strip punctuation
    clean_topics = [t.strip().strip(".,;:?!'\"()[]{}") for t in dict.fromkeys(topics) if t.strip().strip(".,;:?!'\"()[]{}")]
    clean_related = [r.strip().strip(".,;:?!'\"()[]{}") for r in dict.fromkeys(related_concepts) if r.strip().strip(".,;:?!'\"()[]{}") and r.strip().strip(".,;:?!'\"()[]{}") not in clean_topics]

    return {
        "topics": clean_topics[:3] if clean_topics else ["General Computer Science"],
        "related_concepts": clean_related[:3]
    }
