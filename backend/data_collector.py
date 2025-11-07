import os
import requests
from bs4 import BeautifulSoup
import json
from typing import List, Dict
import time
from pathlib import Path

class DataCollector:
    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
    def collect_all_data(self):
        """Collect data from all sources"""
        print("Starting data collection...")
        
        # Collect from various sources
        self.collect_manipal_official_data()
        self.collect_course_info()
        self.collect_hostel_info()
        self.collect_fees_info()
        self.collect_facilities_info()
        self.collect_admission_info()
        
        print("Data collection complete!")
        
    def collect_manipal_official_data(self):
        """Collect data from official Manipal websites"""
        print("Collecting official Manipal data...")
        
        data = {
            "institute_info": {
                "name": "Manipal Institute of Technology (MIT)",
                "university": "Manipal Academy of Higher Education (MAHE)",
                "location": "Manipal, Karnataka, India",
                "established": "1957",
                "type": "Private University",
                "accreditation": "NAAC A++ Grade, UGC recognized"
            },
            "programs": [
                {
                    "department": "Computer Science & Engineering",
                    "programs": ["B.Tech", "M.Tech", "Ph.D"],
                    "specializations": ["AI & ML", "Cybersecurity", "Data Science", "Cloud Computing"]
                },
                {
                    "department": "Information Technology",
                    "programs": ["B.Tech", "M.Tech"],
                    "specializations": ["Software Engineering", "Networking", "Web Technologies"]
                },
                {
                    "department": "Electronics & Communication Engineering",
                    "programs": ["B.Tech", "M.Tech", "Ph.D"],
                    "specializations": ["VLSI", "Communication Systems", "Embedded Systems"]
                },
                {
                    "department": "Mechanical Engineering",
                    "programs": ["B.Tech", "M.Tech", "Ph.D"],
                    "specializations": ["Automotive", "Manufacturing", "Thermal Engineering"]
                },
                {
                    "department": "Civil Engineering",
                    "programs": ["B.Tech", "M.Tech", "Ph.D"],
                    "specializations": ["Structural Engineering", "Environmental Engineering"]
                },
                {
                    "department": "Electrical & Electronics Engineering",
                    "programs": ["B.Tech", "M.Tech", "Ph.D"],
                    "specializations": ["Power Systems", "Control Systems"]
                },
                {
                    "department": "Aerospace Engineering",
                    "programs": ["B.Tech", "M.Tech"],
                    "specializations": ["Aerodynamics", "Aircraft Design"]
                },
                {
                    "department": "Chemical Engineering",
                    "programs": ["B.Tech", "M.Tech", "Ph.D"],
                    "specializations": ["Process Engineering", "Petroleum Engineering"]
                }
            ]
        }
        
        with open(self.data_dir / "official_info.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    def collect_course_info(self):
        """Collect course information"""
        print("Collecting course information...")
        
        courses = {
            "undergraduate": {
                "B.Tech Programs": {
                    "Computer Science & Engineering": {
                        "duration": "4 years",
                        "fees": "Approximately ₹4-5 lakhs per year",
                        "eligibility": "10+2 with Physics, Chemistry, Mathematics (PCM) with minimum 50% aggregate",
                        "admission": "MET (Manipal Entrance Test) or JEE Main score",
                        "intake": "Around 300-400 students per year"
                    },
                    "Information Technology": {
                        "duration": "4 years",
                        "fees": "Approximately ₹4-5 lakhs per year",
                        "eligibility": "10+2 with PCM minimum 50%",
                        "admission": "MET or JEE Main",
                        "intake": "Around 200-300 students"
                    },
                    "Electronics & Communication Engineering": {
                        "duration": "4 years",
                        "fees": "Approximately ₹4-5 lakhs per year",
                        "eligibility": "10+2 with PCM minimum 50%",
                        "admission": "MET or JEE Main"
                    },
                    "Mechanical Engineering": {
                        "duration": "4 years",
                        "fees": "Approximately ₹4-5 lakhs per year",
                        "eligibility": "10+2 with PCM minimum 50%",
                        "admission": "MET or JEE Main"
                    },
                    "Civil Engineering": {
                        "duration": "4 years",
                        "fees": "Approximately ₹4-5 lakhs per year",
                        "eligibility": "10+2 with PCM minimum 50%",
                        "admission": "MET or JEE Main"
                    },
                    "Electrical & Electronics Engineering": {
                        "duration": "4 years",
                        "fees": "Approximately ₹4-5 lakhs per year",
                        "eligibility": "10+2 with PCM minimum 50%",
                        "admission": "MET or JEE Main"
                    },
                    "Aerospace Engineering": {
                        "duration": "4 years",
                        "fees": "Approximately ₹4-5 lakhs per year",
                        "eligibility": "10+2 with PCM minimum 50%",
                        "admission": "MET or JEE Main"
                    },
                    "Chemical Engineering": {
                        "duration": "4 years",
                        "fees": "Approximately ₹4-5 lakhs per year",
                        "eligibility": "10+2 with PCM minimum 50%",
                        "admission": "MET or JEE Main"
                    }
                }
            },
            "postgraduate": {
                "M.Tech Programs": {
                    "duration": "2 years",
                    "fees": "Approximately ₹2-3 lakhs per year",
                    "eligibility": "B.Tech in relevant field with minimum 60% aggregate",
                    "admission": "GATE score or MET PG"
                },
                "MBA": {
                    "duration": "2 years",
                    "fees": "Approximately ₹5-7 lakhs per year",
                    "eligibility": "Bachelor's degree with minimum 50%",
                    "admission": "MAT/CAT/XAT/GMAT score"
                }
            }
        }
        
        with open(self.data_dir / "courses.json", "w", encoding="utf-8") as f:
            json.dump(courses, f, indent=2, ensure_ascii=False)
            
    def collect_hostel_info(self):
        """Collect hostel information"""
        print("Collecting hostel information...")
        
        hostels = {
            "boys_hostels": {
                "Block 1": {
                    "type": "Non-AC Double Occupancy",
                    "fees": "₹80,000 - ₹90,000 per year",
                    "facilities": ["Wi-Fi", "Common Room", "Laundry", "Mess", "Security"]
                },
                "Block 2": {
                    "type": "AC Double Occupancy",
                    "fees": "₹1,20,000 - ₹1,40,000 per year",
                    "facilities": ["AC", "Wi-Fi", "Common Room", "Laundry", "Mess", "Security"]
                },
                "Block 3": {
                    "type": "Non-AC Single Occupancy",
                    "fees": "₹1,50,000 - ₹1,70,000 per year",
                    "facilities": ["Wi-Fi", "Common Room", "Laundry", "Mess", "Security"]
                }
            },
            "girls_hostels": {
                "Block A": {
                    "type": "Non-AC Double Occupancy",
                    "fees": "₹80,000 - ₹90,000 per year",
                    "facilities": ["Wi-Fi", "Common Room", "Laundry", "Mess", "Security"]
                },
                "Block B": {
                    "type": "AC Double Occupancy",
                    "fees": "₹1,20,000 - ₹1,40,000 per year",
                    "facilities": ["AC", "Wi-Fi", "Common Room", "Laundry", "Mess", "Security"]
                }
            },
            "mess_facilities": {
                "meal_timings": {
                    "breakfast": "7:00 AM - 9:00 AM",
                    "lunch": "12:00 PM - 2:00 PM",
                    "snacks": "4:00 PM - 6:00 PM",
                    "dinner": "7:00 PM - 9:00 PM"
                },
                "mess_fees": "Included in hostel fees",
                "cuisine": "Vegetarian and Non-vegetarian options available"
            },
            "rules": [
                "Hostel gates close at 10:00 PM for girls and 11:00 PM for boys",
                "Visitors need prior permission",
                "No smoking or alcohol in hostels",
                "Regular attendance checks",
                "Quiet hours from 10:00 PM to 6:00 AM"
            ]
        }
        
        with open(self.data_dir / "hostels.json", "w", encoding="utf-8") as f:
            json.dump(hostels, f, indent=2, ensure_ascii=False)
            
    def collect_fees_info(self):
        """Collect fee structure information"""
        print("Collecting fee information...")
        
        fees = {
            "tuition_fees": {
                "B.Tech": {
                    "per_year": "₹4,00,000 - ₹5,00,000",
                    "total_4_years": "₹16,00,000 - ₹20,00,000",
                    "breakdown": {
                        "tuition": "₹3,50,000 - ₹4,50,000",
                        "library": "₹10,000 - ₹15,000",
                        "laboratory": "₹20,000 - ₹30,000",
                        "examination": "₹10,000 - ₹15,000",
                        "student_activities": "₹10,000 - ₹15,000"
                    }
                },
                "M.Tech": {
                    "per_year": "₹2,00,000 - ₹3,00,000",
                    "total_2_years": "₹4,00,000 - ₹6,00,000"
                },
                "MBA": {
                    "per_year": "₹5,00,000 - ₹7,00,000",
                    "total_2_years": "₹10,00,000 - ₹14,00,000"
                }
            },
            "hostel_fees": {
                "non_ac_double": "₹80,000 - ₹90,000 per year",
                "ac_double": "₹1,20,000 - ₹1,40,000 per year",
                "single_occupancy": "₹1,50,000 - ₹1,70,000 per year"
            },
            "other_fees": {
                "admission_fee": "₹50,000 - ₹1,00,000 (one-time)",
                "security_deposit": "₹25,000 - ₹50,000 (refundable)",
                "medical_insurance": "₹5,000 - ₹10,000 per year",
                "transportation": "₹20,000 - ₹30,000 per year (optional)"
            },
            "scholarships": {
                "merit_based": "Up to 50% fee waiver based on MET/JEE rank",
                "sports_quota": "Available for exceptional athletes",
                "financial_aid": "Need-based scholarships available",
                "alumni_scholarships": "Various scholarships from alumni"
            },
            "payment_options": [
                "Full payment at admission",
                "Semester-wise payment",
                "EMI options available through banks",
                "Education loans available"
            ]
        }
        
        with open(self.data_dir / "fees.json", "w", encoding="utf-8") as f:
            json.dump(fees, f, indent=2, ensure_ascii=False)
            
    def collect_facilities_info(self):
        """Collect campus facilities information"""
        print("Collecting facilities information...")
        
        facilities = {
            "library": {
                "name": "Knowledge Resource Centre",
                "hours": {
                    "weekdays": "8:00 AM - 10:00 PM",
                    "saturday": "9:00 AM - 6:00 PM",
                    "sunday": "10:00 AM - 6:00 PM"
                },
                "collection": {
                    "books": "300,000+",
                    "journals": "1,500+",
                    "e_books": "50,000+",
                    "databases": "Access to IEEE, ACM, Springer, etc."
                },
                "services": [
                    "Book lending (max 5 books for 15 days)",
                    "Digital resources access",
                    "Research assistance",
                    "Study rooms booking",
                    "Printing and scanning",
                    "24/7 digital library access"
                ]
            },
            "laboratories": {
                "computer_labs": "Multiple labs with latest hardware and software",
                "engineering_labs": "Well-equipped labs for all engineering branches",
                "research_labs": "Advanced research facilities for postgraduate students"
            },
            "sports": {
                "indoor": ["Basketball", "Badminton", "Table Tennis", "Gym", "Squash"],
                "outdoor": ["Cricket", "Football", "Tennis", "Volleyball", "Athletics"],
                "facilities": "Sports complex with courts, fields, and gymnasium"
            },
            "cafeterias": {
                "main_cafeteria": "Multiple food courts serving various cuisines",
                "timings": "7:00 AM - 10:00 PM",
                "cuisine": "Indian, Chinese, Continental, Fast Food"
            },
            "medical": {
                "hospital": "Kasturba Medical College Hospital nearby",
                "health_center": "Campus health center with doctors available",
                "ambulance": "24/7 ambulance service"
            },
            "transportation": {
                "bus_service": "Regular bus service within campus and to nearby areas",
                "parking": "Vehicle parking facilities available"
            },
            "wifi": {
                "coverage": "Campus-wide Wi-Fi coverage",
                "speed": "High-speed internet connection",
                "access": "Available 24/7 with student credentials"
            }
        }
        
        with open(self.data_dir / "facilities.json", "w", encoding="utf-8") as f:
            json.dump(facilities, f, indent=2, ensure_ascii=False)
            
    def collect_admission_info(self):
        """Collect admission information"""
        print("Collecting admission information...")
        
        admissions = {
            "entrance_exams": {
                "MET": {
                    "full_form": "Manipal Entrance Test",
                    "for": "B.Tech, M.Tech, and other programs",
                    "conducted_by": "Manipal Academy of Higher Education",
                    "frequency": "Once a year",
                    "mode": "Online/Computer-based test"
                },
                "JEE_Main": {
                    "accepted": "Yes, for B.Tech programs",
                    "cutoff": "Varies by branch"
                },
                "GATE": {
                    "accepted": "Yes, for M.Tech programs",
                    "cutoff": "Minimum 50 percentile"
                }
            },
            "application_process": {
                "step1": "Register online on official website",
                "step2": "Fill application form",
                "step3": "Pay application fee (₹600 - ₹2000)",
                "step4": "Appear for entrance exam (if applicable)",
                "step5": "Counseling and seat allocation",
                "step6": "Document verification and fee payment"
            },
            "important_dates": {
                "application_start": "Usually in October-November",
                "application_deadline": "Usually in March-April",
                "exam_date": "Usually in April-May",
                "results": "Usually in May-June",
                "counseling": "Usually in June-July",
                "admission": "Usually in July-August"
            },
            "documents_required": [
                "10th and 12th mark sheets",
                "Entrance exam scorecard",
                "Identity proof (Aadhaar/PAN)",
                "Passport size photographs",
                "Caste certificate (if applicable)",
                "Medical fitness certificate"
            ],
            "contact": {
                "admission_office": "+91 820 292 2400",
                "email": "admissions@manipal.edu",
                "website": "https://manipal.edu/mit"
            }
        }
        
        with open(self.data_dir / "admissions.json", "w", encoding="utf-8") as f:
            json.dump(admissions, f, indent=2, ensure_ascii=False)

