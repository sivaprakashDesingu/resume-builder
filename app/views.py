from django.shortcuts import render


def home(request):
    """Render the home page template."""
    return render(request, 'app/pages/home.html')


def about(request):
    """Render the about page template."""
    return render(request, 'app/pages/about.html')


def resume_explorer(request):
    """Render the resume explorer listing page."""
    return render(request, 'app/pages/resume_explorer.html')


def resume1(request):
    """Render the resume 1 template."""
    return render(request, 'app/resumes/resume1.html')


def resume_detail(request, pk: int):
    """Dynamically serve resume templates (e.g., resume1.html, resume2.html, resume3.html)."""
    template_name = f'app/resumes/resume{pk}.html'
    return render(request, template_name)


def resume_editor(request, pk: int):
    """Render the resume editor with two-column layout for editing."""
    
    # Template-specific data
    if pk == 1:
        # Template 1 - Software Engineer (Emerald theme)
        template_data = {
            'template_id': pk,
            'fullName': 'Liam O\'Connell',
            'professionalTitle': 'Senior Software Engineer',
            'email': 'liam.oconnell@techprodev.com',
            'phone': '+1 (555) 123-4567',
            'location': 'San Francisco, CA',
            'summary': 'Highly accomplished and results-driven Senior Software Engineer with 8+ years of experience in designing, developing, and deploying high-scale, cloud-native applications. Proficient in the MERN stack and microservices architecture with proven ability to lead development teams and drive complex projects from conception through successful launch. Passionate about writing clean, maintainable code and fostering collaborative team environments.',
            'skills': [
                {'name': 'JavaScript', 'level': 95},
                {'name': 'React', 'level': 92},
                {'name': 'Node.js', 'level': 90},
                {'name': 'Python', 'level': 88},
                {'name': 'Docker', 'level': 85},
                {'name': 'Kubernetes', 'level': 82},
                {'name': 'AWS', 'level': 88},
                {'name': 'PostgreSQL', 'level': 87},
                {'name': 'MongoDB', 'level': 85},
            ],
            'experiences': [
                {
                    'title': 'Senior Software Engineer',
                    'company': 'Tech Innovators Inc.',
                    'duration': 'May 2019 – Present',
                    'description': '• Led a team of 5 engineers in migrating to microservices (Docker/K8s), resulting in a 40% reduction in average API latency\n• Implemented a real-time data streaming pipeline using Kafka and Node.js, processing 1M+ events daily\n• Designed and deployed a scalable authentication system using OAuth 2.0, securing 100K+ user accounts\n• Mentored 3 junior developers, improving code quality and accelerating their professional growth'
                },
                {
                    'title': 'Full-Stack Engineer',
                    'company': 'Cloud Solutions Corp',
                    'duration': 'Jan 2017 – Apr 2019',
                    'description': '• Built RESTful APIs serving 50K+ concurrent users using Node.js and Express.js\n• Developed responsive web applications with React, improving user engagement by 35%\n• Optimized database queries reducing query time by 60%, improving overall application performance'
                },
                {
                    'title': 'Junior Software Developer',
                    'company': 'StartupXYZ',
                    'duration': 'Jun 2015 – Dec 2016',
                    'description': '• Developed full-stack features for SaaS platform using JavaScript and Python\n• Contributed to code reviews and implemented best practices for development workflow'
                }
            ],
            'educations': [
                {
                    'degree': 'Master of Science in Computer Science',
                    'school': 'Massachusetts Institute of Technology (MIT)',
                    'year': 'Graduated: May 2015'
                },
                {
                    'degree': 'Bachelor of Science in Computer Engineering',
                    'school': 'University of California, Berkeley',
                    'year': 'Graduated: May 2013'
                }
            ],
            'customSections': [
                {
                    'title': 'Certifications',
                    'content': '• AWS Certified Solutions Architect - Professional\n• Kubernetes Application Developer (CKAD)\n• Docker Certified Associate'
                }
            ]
        }
    elif pk == 2:
        # Template 2 - Product Manager (Blue theme, two-column layout)
        template_data = {
            'template_id': pk,
            'fullName': 'Sarah Chen',
            'professionalTitle': 'Senior Product Manager',
            'email': 'sarah.chen@innovate.io',
            'phone': '+1 (415) 555-8901',
            'location': 'San Francisco, CA',
            'summary': 'Results-driven Product Manager with 6+ years of experience leading cross-functional teams to deliver innovative digital solutions. Proven track record of increasing user engagement by 45% and driving revenue growth through data-driven product decisions. Expertise in SaaS, mobile, and enterprise platforms with a passion for user-centric design.',
            'skills': [
                {'name': 'Product Strategy', 'level': 95},
                {'name': 'User Research', 'level': 90},
                {'name': 'Data Analytics', 'level': 88},
                {'name': 'Cross-functional Leadership', 'level': 92},
                {'name': 'Market Analysis', 'level': 85},
                {'name': 'Agile & Scrum', 'level': 87},
                {'name': 'SQL & Analytics Tools', 'level': 80},
                {'name': 'Go-to-Market Strategy', 'level': 86},
                {'name': 'Stakeholder Management', 'level': 91},
            ],
            'experiences': [
                {
                    'title': 'Senior Product Manager',
                    'company': 'Innovate Tech Solutions',
                    'duration': 'Mar 2021 – Present',
                    'description': '• Led product roadmap for SaaS platform serving 500K+ users, achieving 40% YoY growth\n• Managed cross-functional team of 8 engineers, designers, and analysts\n• Launched 12+ major features resulting in 35% improvement in customer retention\n• Conducted 100+ user interviews to inform product decisions'
                },
                {
                    'title': 'Product Manager',
                    'company': 'Digital Ventures Inc.',
                    'duration': 'Jun 2019 – Feb 2021',
                    'description': '• Owned product strategy for mobile app with 2M+ monthly active users\n• Increased user engagement by 45% through A/B testing and UX optimization\n• Collaborated with marketing to drive user acquisition campaigns'
                },
                {
                    'title': 'Associate Product Manager',
                    'company': 'StartUp Accelerators',
                    'duration': 'Jan 2018 – May 2019',
                    'description': '• Supported product development for early-stage SaaS platform\n• Conducted market research and competitive analysis'
                }
            ],
            'educations': [
                {
                    'degree': 'Master of Business Administration (MBA)',
                    'school': 'Stanford Graduate School of Business',
                    'year': 'Graduated: May 2017'
                },
                {
                    'degree': 'Bachelor of Science in Computer Science',
                    'school': 'University of Washington',
                    'year': 'Graduated: May 2015'
                }
            ],
            'customSections': [
                {
                    'title': 'Certifications',
                    'content': '• Pragmatic Marketing Certified (PMC)\n• Certified Scrum Product Owner (CSPO)\n• Google Analytics Certification'
                }
            ]
        }
    elif pk == 3:
        # Template 3 - Designer (Golden/Creative theme)
        template_data = {
            'template_id': pk,
            'fullName': 'Alex Rivera',
            'professionalTitle': 'Senior UX/UI Designer',
            'email': 'alex.rivera@creative.studio',
            'phone': '+1 (323) 555-6789',
            'location': 'Los Angeles, CA',
            'summary': 'Innovative UX/UI Designer with 7+ years of experience creating intuitive and visually compelling digital experiences. Proven expertise in user-centered design, design systems, and cross-platform applications. Passionate about solving complex design challenges and mentoring design teams.',
            'skills': [
                {'name': 'UI/UX Design', 'level': 95},
                {'name': 'Figma', 'level': 93},
                {'name': 'Design Systems', 'level': 90},
                {'name': 'User Research', 'level': 88},
                {'name': 'Prototyping', 'level': 92},
                {'name': 'Adobe Creative Suite', 'level': 89},
                {'name': 'Wireframing', 'level': 91},
                {'name': 'Interaction Design', 'level': 90},
                {'name': 'HTML/CSS Basics', 'level': 75},
            ],
            'experiences': [
                {
                    'title': 'Senior UX/UI Designer',
                    'company': 'Creative Tech Studios',
                    'duration': 'Aug 2020 – Present',
                    'description': '• Led design system creation for enterprise platform used by 100K+ users\n• Conducted user research and usability testing for 15+ product releases\n• Mentored team of 4 designers, improving design consistency and quality\n• Reduced design-to-development handoff time by 50% through better documentation'
                },
                {
                    'title': 'UX/UI Designer',
                    'company': 'Digital Design Agency',
                    'duration': 'Jan 2018 – Jul 2020',
                    'description': '• Designed user interfaces for 20+ web and mobile applications\n• Collaborated with product and engineering teams to deliver user-centered solutions\n• Conducted 100+ user interviews and usability tests\n• Improved user satisfaction scores by 40% across portfolio of projects'
                },
                {
                    'title': 'Junior Designer',
                    'company': 'StartUp Designs',
                    'duration': 'Jun 2016 – Dec 2017',
                    'description': '• Created wireframes, mockups, and prototypes for web applications\n• Assisted in user research and competitive analysis'
                }
            ],
            'educations': [
                {
                    'degree': 'Master of Fine Arts in Interaction Design',
                    'school': 'School of Visual Arts, New York',
                    'year': 'Graduated: May 2016'
                },
                {
                    'degree': 'Bachelor of Fine Arts in Graphic Design',
                    'school': 'California Institute of the Arts',
                    'year': 'Graduated: May 2014'
                }
            ],
            'customSections': [
                {
                    'title': 'Design Awards & Recognition',
                    'content': '• Best UX Design - Tech Design Awards 2023\n• Featured Designer - Design Community Monthly\n• Speaker - UX Design Conference 2022'
                }
            ]
        }
    elif pk == 4:
        # Template 4 - Executive (Classic Dark theme)
        template_data = {
            'template_id': pk,
            'fullName': 'Margaret Johnson',
            'professionalTitle': 'Chief Technology Officer',
            'email': 'margaret.johnson@executive.com',
            'phone': '+1 (212) 555-9999',
            'location': 'New York, NY',
            'summary': 'Strategic technology executive with 15+ years of experience leading digital transformation initiatives and building world-class engineering organizations. Proven track record of driving innovation, managing multi-million dollar technology budgets, and delivering transformational business results. Expertise in cloud infrastructure, team building, and enterprise architecture.',
            'skills': [
                {'name': 'Strategic Leadership', 'level': 95},
                {'name': 'Technology Strategy', 'level': 93},
                {'name': 'Cloud Architecture', 'level': 90},
                {'name': 'Team Management', 'level': 92},
                {'name': 'Budget Management', 'level': 88},
                {'name': 'Digital Transformation', 'level': 91},
                {'name': 'Enterprise Architecture', 'level': 89},
                {'name': 'Stakeholder Management', 'level': 94},
            ],
            'experiences': [
                {
                    'title': 'Chief Technology Officer',
                    'company': 'Global Tech Corporation',
                    'duration': 'Jan 2020 – Present',
                    'description': '• Oversee $100M technology budget and team of 150+ engineers\n• Led cloud migration saving $30M annually\n• Reduced infrastructure costs by 40% through optimization\n• Established technical excellence standards across organization'
                },
                {
                    'title': 'VP of Engineering',
                    'company': 'Enterprise Solutions Ltd.',
                    'duration': 'Mar 2016 – Dec 2019',
                    'description': '• Built and scaled engineering team from 30 to 120 people\n• Implemented agile practices improving delivery speed by 60%\n• Led successful acquisition integration of 3 tech companies'
                },
                {
                    'title': 'Director of Software Engineering',
                    'company': 'Tech Ventures',
                    'duration': 'Jul 2012 – Feb 2016',
                    'description': '• Managed 50+ engineers across multiple product lines\n• Improved system reliability from 95% to 99.9% uptime'
                }
            ],
            'educations': [
                {
                    'degree': 'Master of Business Administration (MBA)',
                    'school': 'Harvard Business School',
                    'year': 'Graduated: May 2009'
                },
                {
                    'degree': 'Bachelor of Science in Computer Science',
                    'school': 'Stanford University',
                    'year': 'Graduated: May 2007'
                }
            ],
            'customSections': [
                {
                    'title': 'Industry Recognition',
                    'content': '• Listed in Forbes 30 Under 40 in Technology\n• Board Member - Tech Education Foundation\n• Speaker - International Tech Summit'
                }
            ]
        }
    elif pk >= 11:
        # Empty templates - used for creating new resumes from scratch
        template_id_map = {
            11: {'title': 'Minimalist', 'color': '#1f2937'},  # Dark Gray
            12: {'title': 'Modern', 'color': '#3b82f6'},      # Blue
            13: {'title': 'Creative', 'color': '#ec4899'},    # Pink
            14: {'title': 'Professional', 'color': '#7c3aed'}, # Violet
        }
        
        template_info = template_id_map.get(pk, {'title': 'Blank', 'color': '#6b7280'})
        
        template_data = {
            'template_id': pk,
            'template_name': template_info['title'],
            'template_color': template_info['color'],
            'is_empty': True,
            'fullName': '',
            'professionalTitle': '',
            'email': '',
            'phone': '',
            'location': '',
            'summary': '',
            'skills': [],
            'experiences': [],
            'educations': [],
            'customSections': []
        }
    else:
        # Default fallback
        template_data = {
            'template_id': pk,
            'fullName': 'Your Name',
            'professionalTitle': 'Your Title',
            'email': 'your.email@example.com',
            'phone': '+1 (555) 123-4567',
            'location': 'City, State',
            'summary': 'Your professional summary here.',
            'skills': [],
            'experiences': [],
            'educations': [],
            'customSections': []
        }
    
    return render(request, 'app/pages/resume_editor.html', template_data)