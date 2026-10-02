import React from 'react';
import './About.css';

export default function About() {
  const pipelineSteps = [
    { num: '01', title: 'Student Query Intake', desc: 'You describe your learning goal naturally, mentioning what you want to learn, what you already know, or where you are struggling.' },
    { num: '02', title: 'Learning Goal Extraction', desc: 'Linguistic patterns and noun phrase structures isolate your target technology, framework, or career objective.' },
    { num: '03', title: 'Known Skill Extraction', desc: 'Identifies existing skills explicitly stated as known ("I know Python", "familiar with JavaScript") so they are never flagged as gaps.' },
    { num: '04', title: 'Explicit Gap Detection', desc: 'Pinpoints stated weaknesses ("weak at statistics", "struggle with recursion", "never worked with NLP").' },
    { num: '05', title: 'Prerequisite Cross-Referencing', desc: 'Compares target goals against domain prerequisites, classifying foundational concepts into Covered, Stated Gap, or Potential Gap.' },
    { num: '06', title: 'Context & Level Detection', desc: 'Identifies your learning context (Career Prep, Project Building, Exam Prep, etc.) and proficiency level (Beginner, Intermediate, Advanced).' },
    { num: '07', title: 'Starting Point & Reasoning', desc: 'Synthesizes your profile to recommend the exact initial concept to study, with clear pedagogical reasoning explaining WHY.' },
    { num: '08', title: 'Internal Intent Validation', desc: 'Supervised classification and dense sentence embeddings (all-MiniLM-L6-v2) run internally to validate semantic confidence.' },
  ];

  return (
    <div className="about-page-container">
      {/* Intro section */}
      <section className="about-hero">
        <span className="about-badge">NLP LEARNING INTELLIGENCE</span>
        <h1 className="about-title">
          Natural Language Learning Goal & <br />
          <span className="serif-accent">Skill Gap Analyzer</span>
        </h1>
        <p className="about-lead">
          When students describe what they want to study, they express multiple dimensions at once:
          their dream goal, their current foundation, their struggles, and their preparation timeline.
          IntentLens uses Natural Language Processing to extract these dimensions and determine
          where the student should start.
        </p>
      </section>

      {/* The Problem & Solution */}
      <section className="about-card-section">
        <h2 className="section-heading">Why Intent Alone is Not Enough</h2>
        <div className="why-grid">
          <div className="why-box">
            <h3 className="why-title">The Limitation of Intent Classification</h3>
            <p className="why-text">
              A student gaining the label "Your intent is LEARNING_REQUEST" receives zero academic value.
              Traditional chatbots and classifiers stop at surface categorization instead of extracting
              actionable pedagogical signals.
            </p>
          </div>
          <div className="why-box">
            <h3 className="why-title">Structured Knowledge States</h3>
            <p className="why-text">
              IntentLens separates what you want to learn from what you already know, identifying
              explicit weaknesses and potential prerequisite gaps without making false assumptions.
            </p>
          </div>
          <div className="why-box">
            <h3 className="why-title">Pedagogical Starting Points</h3>
            <p className="why-text">
              By understanding that you already know Python and machine learning, IntentLens recommends
              Deep Learning as your bridge toward LLMs rather than sending you back to coding basics.
            </p>
          </div>
        </div>
      </section>

      {/* Step by Step Process */}
      <section className="about-card-section">
        <h2 className="section-heading">The 8-Stage NLP Extraction Pipeline</h2>
        <div className="pipeline-steps-grid">
          {pipelineSteps.map((step) => (
            <div key={step.num} className="step-card">
              <span className="step-num">{step.num}</span>
              <h4 className="step-title">{step.title}</h4>
              <p className="step-desc">{step.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Technology in Simple Terms */}
      <section className="about-card-section">
        <h2 className="section-heading">NLP Components & Architecture</h2>
        <div className="tech-stack-table-wrapper">
          <table className="tech-stack-table">
            <thead>
              <tr>
                <th>Component</th>
                <th>Technology</th>
                <th>Role in the Pipeline</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Goal & Skill Extractor</td>
                <td>spaCy + Regex + CS Taxonomy</td>
                <td>Extracts target technologies and validates claimed competencies versus stated gaps.</td>
              </tr>
              <tr>
                <td>Gap Extractor</td>
                <td>Linguistic Pattern Analysis</td>
                <td>Detects explicit struggle statements, unfamiliarity, and weakness claims.</td>
              </tr>
              <tr>
                <td>Prerequisite Matcher</td>
                <td>Domain Knowledge Base</td>
                <td>Maps foundational prerequisites into Known, Stated Gap, and Potential Gap states.</td>
              </tr>
              <tr>
                <td>Semantic Similarity Engine</td>
                <td>Sentence-Transformers (all-MiniLM-L6-v2)</td>
                <td>Calculates dense 384-dimensional cosine similarity for semantic validation.</td>
              </tr>
              <tr>
                <td>Intent Classifier</td>
                <td>TF-IDF + Logistic Regression</td>
                <td>Acts as an internal supporting NLP signal to guide query interpretation.</td>
              </tr>
              <tr>
                <td>Application Layer</td>
                <td>MERN + FastAPI Microservice</td>
                <td>High-performance asynchronous Python backend with Express and React.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      {/* Cognivue Future Integration */}
      <section className="about-card-section">
        <h2 className="section-heading">Future Platform Integration</h2>
        <p className="cognivue-note">
          While IntentLens operates as a completely independent, standalone academic NLP mini project,
          its structured output schema is engineered to serve as an upstream natural language understanding
          module for larger learning systems (such as Cognivue's cognitive frontier and mastery engines).
        </p>
      </section>
    </div>
  );
}
