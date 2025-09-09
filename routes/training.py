from flask import Blueprint, request, jsonify
from src.models.training import db, User, ModuleProgress, CertificationAttempt, LearningActivity
from datetime import datetime
import json

training_bp = Blueprint('training', __name__)

# Sample training data
TRAINING_DATA = {
    "tracks": [
        {
            "id": 1,
            "title": "AI Foundations",
            "description": "Build foundational knowledge of AI concepts, terminology, and business applications within the IT channel context.",
            "duration": "Months 1-3",
            "color": "from-blue-500 to-cyan-500",
            "certification": "AI Foundation Certified",
            "modules": [
                {
                    "id": 1,
                    "title": "AI Business Fundamentals",
                    "description": "Define AI, ML, Deep Learning and articulate business value",
                    "duration": "2 weeks",
                    "topics": [
                        "The AI Revolution: History, terminology, hype vs reality",
                        "The Business of AI: Value creation frameworks, identifying opportunities"
                    ],
                    "interactiveElements": [
                        {
                            "type": "exercise",
                            "title": "AI Opportunity Matrix",
                            "description": "Analyze three current clients and map potential AI opportunities"
                        },
                        {
                            "type": "presentation",
                            "title": "Business Case Presentation",
                            "description": "Develop and present a high-level business case for one AI opportunity"
                        }
                    ]
                },
                {
                    "id": 2,
                    "title": "The IT Channel AI Landscape",
                    "description": "Understand AI applications specific to MSPs, VARs, and IT service providers",
                    "duration": "2 weeks",
                    "topics": [
                        "MSP AI Use Cases: Service delivery automation, predictive maintenance",
                        "VAR AI Opportunities: Solution enhancement, customer experience"
                    ],
                    "interactiveElements": [
                        {
                            "type": "workshop",
                            "title": "Channel Partner Workshop",
                            "description": "Role-play AI solution discussions with different channel partner types"
                        }
                    ]
                },
                {
                    "id": 3,
                    "title": "AI Tools and Platforms Overview",
                    "description": "Survey of major AI platforms and tools relevant to IT channel",
                    "duration": "2 weeks",
                    "topics": [
                        "Microsoft AI Stack: Azure AI, Copilot ecosystem",
                        "Google AI Platform: Workspace AI, Cloud AI services"
                    ],
                    "interactiveElements": [
                        {
                            "type": "simulation",
                            "title": "Platform Comparison",
                            "description": "Compare AI platforms for specific client scenarios"
                        }
                    ]
                },
                {
                    "id": 4,
                    "title": "AI Project Methodology",
                    "description": "Learn structured approach to AI project planning and execution",
                    "duration": "2 weeks",
                    "topics": [
                        "AI Project Lifecycle: Discovery, planning, implementation, optimization",
                        "Success Metrics: KPIs, ROI measurement, value realization"
                    ],
                    "interactiveElements": [
                        {
                            "type": "roadmap",
                            "title": "Project Roadmap Creation",
                            "description": "Create a detailed project roadmap for a sample AI implementation"
                        }
                    ]
                },
                {
                    "id": 5,
                    "title": "AI Ethics and Governance (Presh.ai Context)",
                    "description": "Understand ethical AI principles and Presh.ai's governance framework",
                    "duration": "2 weeks",
                    "topics": [
                        "Presh.ai AI Policy: AI as an Aid, Not an Agent philosophy",
                        "Ethical Considerations: Bias, transparency, accountability"
                    ],
                    "interactiveElements": [
                        {
                            "type": "analysis",
                            "title": "Ethics Case Study",
                            "description": "Analyze ethical implications of AI implementations"
                        }
                    ]
                },
                {
                    "id": 6,
                    "title": "Client Communication and Education",
                    "description": "Develop skills for explaining AI concepts to non-technical stakeholders",
                    "duration": "2 weeks",
                    "topics": [
                        "Simplifying AI: Translating technical concepts for business audiences",
                        "Addressing Concerns: Common fears and misconceptions about AI"
                    ],
                    "interactiveElements": [
                        {
                            "type": "presentation",
                            "title": "Client Education Session",
                            "description": "Deliver an AI education presentation to simulated client audience"
                        }
                    ]
                }
            ]
        },
        {
            "id": 2,
            "title": "Technical Competency",
            "description": "Develop technical skills for AI solution assessment and implementation planning.",
            "duration": "Months 4-6",
            "color": "from-green-500 to-emerald-500",
            "certification": "AI Technical Specialist",
            "modules": [
                {
                    "id": 1,
                    "title": "Data Fundamentals for AI",
                    "description": "Understanding data requirements, quality, and preparation for AI projects",
                    "duration": "3 weeks",
                    "topics": [
                        "Data Quality Assessment: Completeness, accuracy, consistency",
                        "Data Preparation: Cleaning, transformation, feature engineering"
                    ],
                    "interactiveElements": [
                        {
                            "type": "exercise",
                            "title": "Data Quality Audit",
                            "description": "Assess data quality for a sample client dataset"
                        }
                    ]
                },
                {
                    "id": 2,
                    "title": "AI Platform Deep Dive",
                    "description": "Hands-on experience with major AI platforms and services",
                    "duration": "3 weeks",
                    "topics": [
                        "Azure AI Services: Cognitive Services, Machine Learning Studio",
                        "Implementation Patterns: Common architectures and best practices"
                    ],
                    "interactiveElements": [
                        {
                            "type": "workshop",
                            "title": "Platform Hands-on Lab",
                            "description": "Build a simple AI solution using Azure AI services"
                        }
                    ]
                },
                {
                    "id": 3,
                    "title": "Solution Architecture Basics",
                    "description": "Learn to design AI solution architectures for common business scenarios",
                    "duration": "3 weeks",
                    "topics": [
                        "Architecture Patterns: Batch processing, real-time inference, hybrid approaches",
                        "Integration Considerations: APIs, data flows, security"
                    ],
                    "interactiveElements": [
                        {
                            "type": "exercise",
                            "title": "Architecture Design",
                            "description": "Design solution architecture for a client use case"
                        }
                    ]
                },
                {
                    "id": 4,
                    "title": "Implementation Planning",
                    "description": "Develop skills for creating detailed AI implementation plans",
                    "duration": "2 weeks",
                    "topics": [
                        "Project Planning: Phases, milestones, resource requirements",
                        "Risk Management: Common pitfalls and mitigation strategies"
                    ],
                    "interactiveElements": [
                        {
                            "type": "roadmap",
                            "title": "Implementation Plan",
                            "description": "Create comprehensive implementation plan for AI project"
                        }
                    ]
                },
                {
                    "id": 5,
                    "title": "Testing and Validation",
                    "description": "Learn methodologies for testing and validating AI solutions",
                    "duration": "2 weeks",
                    "topics": [
                        "Testing Strategies: Unit testing, integration testing, performance testing",
                        "Validation Methods: Accuracy metrics, business value validation"
                    ],
                    "interactiveElements": [
                        {
                            "type": "exercise",
                            "title": "Test Plan Development",
                            "description": "Develop comprehensive test plan for AI solution"
                        }
                    ]
                }
            ]
        },
        {
            "id": 3,
            "title": "Solution Design Mastery",
            "description": "Master advanced solution design and client engagement skills.",
            "duration": "Months 7-9",
            "color": "from-purple-500 to-pink-500",
            "certification": "AI Solution Designer",
            "modules": [
                {
                    "id": 1,
                    "title": "Advanced Solution Patterns",
                    "description": "Learn complex AI solution patterns and architectures",
                    "duration": "3 weeks",
                    "topics": [
                        "Multi-modal AI: Combining text, image, and voice AI",
                        "Edge AI: On-premises and hybrid deployments"
                    ],
                    "interactiveElements": [
                        {
                            "type": "workshop",
                            "title": "Complex Solution Design",
                            "description": "Design multi-component AI solution for enterprise client"
                        }
                    ]
                },
                {
                    "id": 2,
                    "title": "Client Discovery and Assessment",
                    "description": "Master techniques for understanding client needs and AI readiness",
                    "duration": "3 weeks",
                    "topics": [
                        "Discovery Methodologies: Structured interviews, process mapping",
                        "Readiness Assessment: Technical, organizational, cultural factors"
                    ],
                    "interactiveElements": [
                        {
                            "type": "simulation",
                            "title": "Client Discovery Session",
                            "description": "Conduct full discovery session with simulated client"
                        }
                    ]
                },
                {
                    "id": 3,
                    "title": "Proposal Development",
                    "description": "Create compelling AI solution proposals and presentations",
                    "duration": "3 weeks",
                    "topics": [
                        "Proposal Structure: Executive summary, technical approach, implementation plan",
                        "Value Proposition: ROI modeling, business case development"
                    ],
                    "interactiveElements": [
                        {
                            "type": "presentation",
                            "title": "Proposal Presentation",
                            "description": "Present complete AI solution proposal to panel"
                        }
                    ]
                },
                {
                    "id": 4,
                    "title": "Change Management",
                    "description": "Learn to guide clients through AI adoption and organizational change",
                    "duration": "2 weeks",
                    "topics": [
                        "Change Strategy: Communication, training, adoption planning",
                        "Resistance Management: Addressing concerns and building buy-in"
                    ],
                    "interactiveElements": [
                        {
                            "type": "workshop",
                            "title": "Change Management Plan",
                            "description": "Develop change management strategy for AI implementation"
                        }
                    ]
                },
                {
                    "id": 5,
                    "title": "Success Measurement",
                    "description": "Establish metrics and monitoring for AI solution success",
                    "duration": "2 weeks",
                    "topics": [
                        "KPI Framework: Technical and business metrics",
                        "Continuous Improvement: Monitoring, optimization, scaling"
                    ],
                    "interactiveElements": [
                        {
                            "type": "analysis",
                            "title": "Success Metrics Dashboard",
                            "description": "Design comprehensive success measurement framework"
                        }
                    ]
                }
            ]
        },
        {
            "id": 4,
            "title": "Expert Practitioner",
            "description": "Achieve mastery in AI solution design and become a thought leader.",
            "duration": "Months 10-12",
            "color": "from-orange-500 to-red-500",
            "certification": "AI Solution Design Expert",
            "modules": [
                {
                    "id": 1,
                    "title": "Industry Specialization",
                    "description": "Develop deep expertise in specific industry AI applications",
                    "duration": "4 weeks",
                    "topics": [
                        "Vertical Solutions: Healthcare, finance, manufacturing, retail AI",
                        "Regulatory Considerations: Compliance, governance, risk management"
                    ],
                    "interactiveElements": [
                        {
                            "type": "workshop",
                            "title": "Industry Solution Design",
                            "description": "Design specialized AI solution for chosen industry vertical"
                        }
                    ]
                },
                {
                    "id": 2,
                    "title": "Thought Leadership",
                    "description": "Develop skills for AI thought leadership and market positioning",
                    "duration": "4 weeks",
                    "topics": [
                        "Content Creation: Whitepapers, case studies, presentations",
                        "Market Positioning: Competitive differentiation, value messaging"
                    ],
                    "interactiveElements": [
                        {
                            "type": "presentation",
                            "title": "Thought Leadership Content",
                            "description": "Create and present original AI thought leadership content"
                        }
                    ]
                },
                {
                    "id": 3,
                    "title": "Capstone Project",
                    "description": "Complete comprehensive AI solution design project",
                    "duration": "4 weeks",
                    "topics": [
                        "Project Execution: End-to-end solution design and presentation",
                        "Peer Review: Collaborative evaluation and feedback"
                    ],
                    "interactiveElements": [
                        {
                            "type": "presentation",
                            "title": "Capstone Presentation",
                            "description": "Present complete AI solution design to expert panel"
                        }
                    ]
                }
            ]
        }
    ],
    "certificationTests": {
        1: {
            "title": "AI Foundation Certification",
            "description": "Comprehensive test covering AI fundamentals, business applications, and ethical considerations",
            "totalQuestions": 25,
            "totalTime": 45,
            "passingScore": 80,
            "sections": [
                {"title": "AI Concepts and Terminology", "questions": 8, "timeLimit": 15, "type": "Multiple Choice"},
                {"title": "Business Applications", "questions": 7, "timeLimit": 12, "type": "Multiple Choice"},
                {"title": "Ethics and Governance", "questions": 5, "timeLimit": 8, "type": "Multiple Choice"},
                {"title": "IT Channel Applications", "questions": 5, "timeLimit": 10, "type": "Multiple Choice"}
            ]
        },
        2: {
            "title": "AI Technical Specialist Certification",
            "description": "Technical assessment covering data fundamentals, platform knowledge, and solution architecture",
            "totalQuestions": 30,
            "totalTime": 60,
            "passingScore": 75,
            "sections": [
                {"title": "Data Fundamentals", "questions": 10, "timeLimit": 20, "type": "Multiple Choice"},
                {"title": "Platform Knowledge", "questions": 10, "timeLimit": 20, "type": "Multiple Choice"},
                {"title": "Solution Architecture", "questions": 10, "timeLimit": 20, "type": "Multiple Choice"}
            ]
        },
        3: {
            "title": "AI Solution Designer Certification",
            "description": "Advanced assessment covering solution design, client engagement, and project management",
            "totalQuestions": 35,
            "totalTime": 75,
            "passingScore": 85,
            "sections": [
                {"title": "Solution Design", "questions": 15, "timeLimit": 30, "type": "Multiple Choice"},
                {"title": "Client Engagement", "questions": 10, "timeLimit": 20, "type": "Multiple Choice"},
                {"title": "Project Management", "questions": 10, "timeLimit": 25, "type": "Multiple Choice"}
            ]
        },
        4: {
            "title": "AI Solution Design Expert Certification",
            "description": "Expert-level assessment including industry specialization and thought leadership",
            "totalQuestions": 40,
            "totalTime": 90,
            "passingScore": 90,
            "sections": [
                {"title": "Industry Specialization", "questions": 20, "timeLimit": 45, "type": "Multiple Choice"},
                {"title": "Thought Leadership", "questions": 10, "timeLimit": 20, "type": "Multiple Choice"},
                {"title": "Capstone Evaluation", "questions": 10, "timeLimit": 25, "type": "Case Study"}
            ]
        }
    }
}

@training_bp.route('/training-data', methods=['GET'])
def get_training_data():
    """Get complete training data structure"""
    return jsonify(TRAINING_DATA)

@training_bp.route('/user/<int:user_id>/progress', methods=['GET'])
def get_user_progress(user_id):
    """Get user's current progress"""
    user = User.query.get_or_404(user_id)
    
    progress = {
        'currentTrack': user.current_track,
        'currentModule': user.current_module,
        'completedModules': user.get_completed_modules(),
        'certifications': user.get_certifications()
    }
    
    return jsonify(progress)

@training_bp.route('/user/<int:user_id>/progress', methods=['PUT'])
def update_user_progress(user_id):
    """Update user's progress"""
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if 'currentTrack' in data:
        user.current_track = data['currentTrack']
    if 'currentModule' in data:
        user.current_module = data['currentModule']
    if 'completedModules' in data:
        user.set_completed_modules(data['completedModules'])
    if 'certifications' in data:
        user.set_certifications(data['certifications'])
    
    db.session.commit()
    
    # Log activity
    if 'completedModules' in data:
        activity = LearningActivity(
            user_id=user_id,
            activity_type='module',
            description=f'Completed module {data.get("currentModule", user.current_module)}',
            track_id=user.current_track,
            module_id=data.get('currentModule', user.current_module)
        )
        db.session.add(activity)
        db.session.commit()
    
    return jsonify({'success': True})

@training_bp.route('/user/<int:user_id>/module-progress/<int:track_id>/<int:module_id>', methods=['GET'])
def get_module_progress(user_id, track_id, module_id):
    """Get detailed progress for a specific module"""
    progress = ModuleProgress.query.filter_by(
        user_id=user_id, 
        track_id=track_id, 
        module_id=module_id
    ).first()
    
    if not progress:
        return jsonify({
            'completedSections': [],
            'notes': '',
            'exerciseResponses': {}
        })
    
    return jsonify({
        'completedSections': progress.get_completed_sections(),
        'notes': progress.notes,
        'exerciseResponses': progress.get_exercise_responses()
    })

@training_bp.route('/user/<int:user_id>/module-progress/<int:track_id>/<int:module_id>', methods=['PUT'])
def update_module_progress(user_id, track_id, module_id):
    """Update detailed progress for a specific module"""
    data = request.get_json()
    
    progress = ModuleProgress.query.filter_by(
        user_id=user_id, 
        track_id=track_id, 
        module_id=module_id
    ).first()
    
    if not progress:
        progress = ModuleProgress(
            user_id=user_id,
            track_id=track_id,
            module_id=module_id
        )
        db.session.add(progress)
    
    if 'completedSections' in data:
        progress.set_completed_sections(data['completedSections'])
    if 'notes' in data:
        progress.notes = data['notes']
    if 'exerciseResponses' in data:
        progress.set_exercise_responses(data['exerciseResponses'])
    
    progress.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'success': True})

@training_bp.route('/user/<int:user_id>/certification/<int:track_id>', methods=['POST'])
def submit_certification(user_id, track_id):
    """Submit certification test answers"""
    data = request.get_json()
    answers = data.get('answers', {})
    time_taken = data.get('timeTaken', 0)
    
    # Calculate score (simplified - in real implementation, use actual questions)
    total_questions = len(answers)
    correct_answers = sum(1 for answer in answers.values() if answer == 1)  # Simplified scoring
    score = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    # Get passing score from training data
    test_data = TRAINING_DATA['certificationTests'].get(track_id, {})
    passing_score = test_data.get('passingScore', 80)
    passed = score >= passing_score
    
    # Get attempt number
    previous_attempts = CertificationAttempt.query.filter_by(
        user_id=user_id, 
        track_id=track_id
    ).count()
    
    # Save attempt
    attempt = CertificationAttempt(
        user_id=user_id,
        track_id=track_id,
        score=score,
        passed=passed,
        time_taken=time_taken,
        attempt_number=previous_attempts + 1
    )
    attempt.set_answers(answers)
    db.session.add(attempt)
    
    # If passed, update user certifications
    if passed:
        user = User.query.get(user_id)
        certifications = user.get_certifications()
        if track_id not in certifications:
            certifications.append(track_id)
            user.set_certifications(certifications)
            
            # Log certification activity
            activity = LearningActivity(
                user_id=user_id,
                activity_type='certification',
                description=f'Earned {test_data.get("title", "certification")}',
                track_id=track_id
            )
            db.session.add(activity)
    
    db.session.commit()
    
    return jsonify({
        'score': score,
        'passed': passed,
        'attemptNumber': attempt.attempt_number
    })

@training_bp.route('/user/<int:user_id>/activities', methods=['GET'])
def get_user_activities(user_id):
    """Get user's recent learning activities"""
    activities = LearningActivity.query.filter_by(user_id=user_id)\
        .order_by(LearningActivity.created_at.desc())\
        .limit(10).all()
    
    return jsonify([{
        'id': activity.id,
        'type': activity.activity_type,
        'description': activity.description,
        'date': activity.created_at.isoformat(),
        'trackId': activity.track_id,
        'moduleId': activity.module_id
    } for activity in activities])

@training_bp.route('/user', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.get_json()
    
    user = User(
        name=data.get('name', 'Marketing Strategist'),
        email=data.get('email', 'user@presh.ai'),
        role=data.get('role', 'Marketing Strategist')
    )
    
    db.session.add(user)
    db.session.commit()
    
    # Log enrollment activity
    activity = LearningActivity(
        user_id=user.id,
        activity_type='enrollment',
        description='Joined AI Solution Designer Program'
    )
    db.session.add(activity)
    db.session.commit()
    
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role
    })

@training_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user information"""
    user = User.query.get_or_404(user_id)
    
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role,
        'progress': {
            'currentTrack': user.current_track,
            'currentModule': user.current_module,
            'completedModules': user.get_completed_modules(),
            'certifications': user.get_certifications()
        }
    })

