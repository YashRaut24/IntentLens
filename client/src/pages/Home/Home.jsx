import React from 'react';
import Hero from '../../components/Hero/Hero';
import './Home.css';

const TRANSFORMATION_EXAMPLES = [
  {
    title: 'Modern Web Development',
    query: '"I want to learn React. I already know HTML, CSS and basic JavaScript."',
    goal: 'React',
    known: ['HTML', 'CSS', 'JavaScript'],
    gaps: 'No explicit gaps stated',
    start: 'React Fundamentals',
    reason: 'JavaScript foundations are already solid, so the student can skip web basics and dive straight into components, props, and JSX.',
  },
  {
    title: 'AI Chatbot Engineering',
    query: '"I want to build an AI chatbot using Python, but I\'ve never worked with NLP."',
    goal: 'AI Chatbot',
    known: ['Python'],
    gaps: 'NLP (Explicitly mentioned weakness)',
    start: 'NLP Fundamentals',
    reason: 'Python is already known, but NLP was explicitly mentioned as unfamiliar. Tokenization and vector embeddings are the critical unlock.',
  },
  {
    title: 'Machine Learning Internship Prep',
    query: '"I\'m preparing for an ML internship. I know Python and sklearn but I\'m weak at statistics."',
    goal: 'Machine Learning Internship Preparation',
    known: ['Python', 'scikit-learn'],
    gaps: 'Statistics (Stated high-priority gap)',
    start: 'Statistics and Probability for Machine Learning',
    reason: 'Code tools are familiar, but mathematical and statistical modeling is the explicitly stated barrier.',
  },
  {
    title: 'Competitive Programming',
    query: '"I know Java and basic DSA. I want to start competitive programming but I\'m not good at dynamic programming."',
    goal: 'Competitive Programming',
    known: ['Java', 'Data Structures and Algorithms'],
    gaps: 'Dynamic Programming (Stated difficulty)',
    start: 'Dynamic Programming Fundamentals',
    reason: 'With Java and basic DSA already in place, recursion, memoization, and tabular transitions are the primary roadblock.',
  },
];

export default function Home({ onNavigatePage }) {
  return (
    <div className="home-page">
      <Hero
        onAnalyzeClick={() => onNavigatePage('analyze')}
        onExplorePipeline={() => onNavigatePage('about')}
      />

      {/* Core Intelligence Pillars */}
      <section className="home-features-section">
        <div className="section-header-centered">
          <span className="section-badge">NLP LEARNING INTELLIGENCE</span>
          <h2 className="section-title">
            From Natural Language to <span className="serif-accent">Actionable Starting Points</span>
          </h2>
          <p className="section-desc">
            A student doesn't benefit from being told "Your intent is LEARNING_REQUEST".
            IntentLens extracts what you want to learn, what you already know, what foundations
            you may be missing, and exactly where you should start.
          </p>
        </div>

        <div className="features-grid">
          <div className="feature-card">
            <span className="feature-number">01</span>
            <h3 className="feature-title">Extracts Learning Goals</h3>
            <p className="feature-text">
              Uses linguistic patterns and dependency structures to identify target technologies,
              frameworks, or career goals.
            </p>
          </div>

          <div className="feature-card">
            <span className="feature-number">02</span>
            <h3 className="feature-title">Extracts Known Skills</h3>
            <p className="feature-text">
              Distinguishes concepts you already know ("I know Python") so you never waste time
              revisiting solved fundamentals.
            </p>
          </div>

          <div className="feature-card">
            <span className="feature-number">03</span>
            <h3 className="feature-title">Identifies Skill Gaps</h3>
            <p className="feature-text">
              Pinpoints explicit struggles ("weak at statistics") and cross-references prerequisite
              concepts not yet covered.
            </p>
          </div>

          <div className="feature-card">
            <span className="feature-number">04</span>
            <h3 className="feature-title">Generates Clear Reasons</h3>
            <p className="feature-text">
              Recommends a specific starting point with pedagogical justification explaining WHY
              this foundation comes next.
            </p>
          </div>
        </div>
      </section>

      {/* Real Transformation Examples */}
      <section className="taxonomy-section">
        <div className="taxonomy-header">
          <div>
            <span className="section-badge">REAL TRANSFORMATION EXAMPLES</span>
            <h2 className="section-title">See How IntentLens Understands Learners</h2>
          </div>
          <p className="taxonomy-intro">
            Here is how natural language inputs are transformed into structured knowledge states
            and logical starting points.
          </p>
        </div>

        <div className="taxonomy-grid">
          {TRANSFORMATION_EXAMPLES.map((item, idx) => (
            <div key={idx} className="taxonomy-card">
              <div className="tax-top">
                <span className="tax-name">{item.title}</span>
                <span className="tax-code">NLP MAPPING</span>
              </div>
              <div className="tax-example-box">
                <span className="example-tag">STUDENT QUERY:</span>
                <p className="example-text">{item.query}</p>
              </div>
              <div className="transform-details">
                <div className="t-row">
                  <span className="t-label">Goal:</span>
                  <span className="t-val accent-val">{item.goal}</span>
                </div>
                <div className="t-row">
                  <span className="t-label">You Know:</span>
                  <span className="t-val">{item.known.join(', ')}</span>
                </div>
                <div className="t-row">
                  <span className="t-label">Gaps:</span>
                  <span className="t-val gap-val">{item.gaps}</span>
                </div>
                <div className="t-row">
                  <span className="t-label">Starting Point:</span>
                  <span className="t-val start-val">{item.start}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Technology Section */}
      <section className="tech-stack-section">
        <div className="section-header-centered">
          <span className="section-badge">PURE NLP ARCHITECTURE</span>
          <h2 className="section-title">Academic NLP & Semantic Stack</h2>
          <p className="section-desc">
            Built using principled Natural Language Processing techniques with local sentence embeddings and supervised learning.
          </p>
        </div>

        <div className="tech-pills-grid">
          <div className="tech-pill-box">
            <span className="tech-title">spaCy NLP</span>
            <span className="tech-desc">POS tagging, dependency parsing & noun chunks</span>
          </div>
          <div className="tech-pill-box">
            <span className="tech-title">Sentence Transformers</span>
            <span className="tech-desc">all-MiniLM-L6-v2 dense 384-d semantic embeddings</span>
          </div>
          <div className="tech-pill-box">
            <span className="tech-title">TF-IDF Vectorization</span>
            <span className="tech-desc">N-gram vocabulary with supervised intent classification</span>
          </div>
          <div className="tech-pill-box">
            <span className="tech-title">Knowledge State Logic</span>
            <span className="tech-desc">Lightweight prerequisite mapping (Known, Gap, Target)</span>
          </div>
        </div>
      </section>

      {/* Call to Action Banner */}
      <section className="cta-banner">
        <div className="cta-content">
          <h2 className="cta-title">
            Describe Your Goal. <span className="serif-accent">Find Where to Start.</span>
          </h2>
          <p className="cta-text">
            Type your learning goal in natural language. IntentLens will analyze your foundation and point you in the right direction.
          </p>
          <button
            className="btn-primary cta-btn"
            onClick={() => onNavigatePage('analyze')}
          >
            Find My Starting Point →
          </button>
        </div>
      </section>
    </div>
  );
}
